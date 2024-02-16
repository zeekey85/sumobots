# *************************************************
# Sumo Bot Firmware
# *************************************************
import digitalio
import simpleio
import time
import board
import busio
import neopixel
import pwmio
from adafruit_vl53l0x import VL53L0X
from adafruit_motor.motor import DCMotor
from melodies import note_frequencies
import keypad

# Pin connected to piezo buzzer
PIEZO_PIN = board.GP22

# Pins connected to DC motors (swap variable names if your motors are connected differently)
RIGHT_MOTOR_PIN_A = board.GP8
RIGHT_MOTOR_PIN_B = board.GP9
LEFT_MOTOR_PIN_A = board.GP10
LEFT_MOTOR_PIN_B = board.GP11

# Pin connected to NeoPixels
NEO_PIXEL_PIN = board.GP18

# Pins connected to buttons
BUTTON_1_PIN = board.GP20
BUTTON_2_PIN = board.GP21

# Pins connected to TOF sensors
LEFT_EDGE_SENSOR_PIN = board.GP5
RIGHT_EDGE_SENSOR_PIN = board.GP26
TOF_LEFT_I2C_PINS = (board.GP17, board.GP16)
TOF_RIGHT_I2C_PINS = (board.GP3, board.GP2)
I2C_LEFT_TOGGLE_PIN = board.GP4
I2C_RIGHT_TOGGLE_PIN = board.GP6

# Robot states
STARTUP = 0  # Startup sequence
DISARMED = 1  # Waiting for button press
ARMED = 2  # Waiting for button release
COUNTDOWN = 3  # Counting down to fight
FIGHTING = 4  # Fight mode
LOST = 5  # Bot has lost the match
WON = 6  # Bot has won the match

# Maximum enemy targeting range
MAX_DISTANCE = 770


class SumoBot:
    """
    A sumo wrestling robot.
    """

    def fight(self):
        """
        Robot fighting routine. Modify to use your personal strategy!
        """
        # Back away from the edge
        if self.left_edge_detected() or self.right_edge_detected():
            while self.left_edge_detected() or self.right_edge_detected():
                self.drive(left_speed=-1, right_speed=-1)
            self.stop()

        # Scan for enemy and charge it!

        # Check for enemy straight ahead
        if self.enemy_in_range_right() and self.enemy_in_range_left():
            # Charge!
            while (
                self.enemy_in_range_right()
                and self.enemy_in_range_left()
                and not (self.right_edge_detected() or self.left_edge_detected())
            ):
                self.drive(right_speed=1, left_speed=1)

        # Check for enemy to right
        elif self.enemy_in_range_right():
            # Turn to the right for 0.5 seconds
            self.drive(left_speed=-0.5, right_speed=0.5, duration=0.5)

        # Check for enemy to left
        elif self.enemy_in_range_left():
            # Turn to the left for 0.5 seconds
            self.drive(left_speed=0.5, right_speed=-0.5, duration=0.5)

        # Spin and look for enemy
        else:
            # Turn to the left for 0.5 seconds
            self.drive(left_speed=0.5, right_speed=-0.5, duration=0.25)

    #
    # Utility methods below
    #

    def __init__(self):
        """
        Sets up the sumo bot's hardware and internal state.
        """

        # Initialize Neopixel RGB LEDs
        self.pixels = neopixel.NeoPixel(NEO_PIXEL_PIN, 2, brightness=0.1)
        self.pixels.fill(0)

        # Initialize buttons
        self.keypad = keypad.Keys(
            (BUTTON_1_PIN, BUTTON_2_PIN), value_when_pressed=False, pull=True
        )

        # Initialize DC motors
        self.motor_right = DCMotor(
            pwmio.PWMOut(RIGHT_MOTOR_PIN_A, frequency=50),
            pwmio.PWMOut(RIGHT_MOTOR_PIN_B, frequency=50),
        )
        self.motor_left = DCMotor(
            pwmio.PWMOut(LEFT_MOTOR_PIN_A, frequency=50),
            pwmio.PWMOut(LEFT_MOTOR_PIN_B, frequency=50),
        )
        # Stop motors
        self.stop()

        # Initialize piezo
        self.piezo = PIEZO_PIN

        # Set up input pins for edge detection sensors
        self.edge_left = digitalio.DigitalInOut(LEFT_EDGE_SENSOR_PIN)
        self.edge_left.direction = digitalio.Direction.INPUT
        self.edge_right = digitalio.DigitalInOut(RIGHT_EDGE_SENSOR_PIN)
        self.edge_right.direction = digitalio.Direction.INPUT

        # Set up TOF sensors

        # Set up I2C devices for TOF sensors
        self.i2c_left = busio.I2C(*TOF_LEFT_I2C_PINS)
        self.i2c_right = busio.I2C(*TOF_RIGHT_I2C_PINS)
        # Set up toggles for I2C connections
        i2c_left_toggle = digitalio.DigitalInOut(I2C_LEFT_TOGGLE_PIN)
        i2c_left_toggle.direction = digitalio.Direction.OUTPUT
        i2c_right_toggle = digitalio.DigitalInOut(I2C_RIGHT_TOGGLE_PIN)
        i2c_right_toggle.direction = digitalio.Direction.OUTPUT
        # Shut off both I2C connections
        i2c_left_toggle.value = False
        i2c_right_toggle.value = False
        # Turn on the I2C connection to be used with the right side TOF sensor
        i2c_right_toggle.value = True
        # Create right side ToF sensor using default address of 41 (29 hex)
        self.tof_right = VL53L0X(self.i2c_right, address=0x29)
        # Change address to 62 (3E hex)
        self.tof_right.set_address(0x3E)
        # Turn on the I2C connection to be used with the left side TOF sensor
        i2c_left_toggle.value = True
        # Create left side TOF sensor using default address
        self.tof_left = VL53L0X(self.i2c_left, address=0x29)

        # Set initial state
        self.state = STARTUP

    def run(self):
        """
        Sumo bot main execution loop.
        """
        while True:
            if self.state == STARTUP:
                self.state = DISARMED
            elif self.state == DISARMED:
                self.pixels.fill(0xFF0000)
                key_event = self.keypad.events.get()
                if key_event and key_event.key_number == 0 and key_event.pressed:
                    self.state = ARMED
            elif self.state == ARMED:
                self.pixels.fill(0xFFFF00)
                key_event = self.keypad.events.get()
                if key_event and key_event.key_number == 0 and not key_event.pressed:
                    self.state = COUNTDOWN
            elif self.state == COUNTDOWN:
                self.pixels.fill(0x00FF00)
                simpleio.tone(
                    pin=self.piezo,
                    frequency=note_frequencies.get("C5"),
                    duration=0.3,
                )
                self.state = FIGHTING
            elif self.state == FIGHTING:
                self.pixels.fill(0)
                self.fight()
            elif self.state == LOST:
                # TODO: How does the robot know if it has lost?
                self.shut_down()
            elif self.state == WON:
                # TODO: How does the robot know if it has won?
                self.shut_down()

    def stop(self):
        """
        Stops both motors.
        """
        self.drive(left_speed=0, right_speed=0)

    def drive(self, left_speed: int, right_speed: int, duration: float = 0):
        """
        Drive the robot wheels at the given speeds for the given duration in seconds,
        or indefinitely if no duration given.
        Speeds are capped at 1 (full speed ahead) and -1 (full speed reverse)
        """
        self.set_motor_speed(self.motor_left, left_speed)
        self.set_motor_speed(self.motor_right, right_speed)
        if duration:
            end_time = time.time() + duration
            while time.time() < end_time:
                pass
            self.stop()

    def set_motor_speed(self, motor: DCMotor, speed: int):
        """
        Sets the given motor to the given speed,
        respecting limits of -1 and 1.
        """
        if speed == 0:
            motor.throttle = speed
        elif speed < 0:
            motor.throttle = max(-1, speed)
        else:
            motor.throttle = min(1, speed)

    def left_edge_detected(self):
        """
        Returns True if the edge has been crossed by the left sensor, False otherwise.
        """
        return self.edge_left.value

    def right_edge_detected(self):
        """
        Returns True if the edge has been crossed by the right sensor, False otherwise.
        """
        return self.edge_right.value

    def right_distance(self):
        """
        Returns the distance measurement taken by the right side TOF sensor.
        """
        return max(self.tof_right.range, self.tof_right.range)

    def left_distance(self):
        """
        Returns the distance measurement taken by the left side TOF sensor.
        """
        return max(self.tof_left.range, self.tof_left.range)

    def enemy_in_range_right(self):
        """
        Returns True if the right side TOF sensor detects an obstacle within
        the maximum detection range, False otherwise.
        """
        return self.right_distance() < MAX_DISTANCE

    def enemy_in_range_left(self):
        """
        Returns True if the left side TOF sensor detects an obstacle within
        the maximum detection range, False otherwise.
        """
        return self.left_distance() < MAX_DISTANCE

    def shut_down(self):
        """
        Stops the motors and de-initializes the I2C connections to shut down the robot.
        """
        self.stop()
        self.pixels.fill(0x000000)
        self.i2c_left.unlock()
        self.i2c_left.deinit()
        self.i2c_right.unlock()
        self.i2c_right.deinit()


if __name__ == "__main__":
    SumoBot().run()

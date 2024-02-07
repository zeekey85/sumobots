# *************************************************
# Sumo Bot Firmware
# *************************************************
import simpleio
import time
import board
import busio
import neopixel
import pwmio
import adafruit_vl53l0x
from adafruit_motor import motor
from melodies import note_frequencies
import keypad


# Pin connected to piezo buzzer
PIEZO_PIN = board.GP22

# Pins connected to DC motors (swap values if your motors are connected differently
RIGHT_MOTOR_PIN = board.GP8
LEFT_MOTOR_PIN = board.GP9

# Pin connected to NeoPixels
NEO_PIXEL_PIN = board.GP18

# Pins connected to buttons
BUTTON_1_PIN = board.GP20
BUTTON_2_PIN = board.GP21

# Robot states
STARTUP = 0  # Startup sequence
DISARMED = 1  # Waiting for button press
ARMED = 2  # Waiting for button release
COUNTDOWN = 3  # Counting down to fight
FIGHTING = 4  # Fight mode
LOST = 5  # Bot has lost the match
WON = 6  # Bot has won the match

class SumoBot:

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
        m1a = pwmio.PWMOut(RIGHT_MOTOR_PIN, frequency=50)
        m1b = pwmio.PWMOut(LEFT_MOTOR_PIN, frequency=50)
        self.motor1 = motor.DCMotor(m1a, m1b)
        m2a = pwmio.PWMOut(board.GP10, frequency=50)
        m2b = pwmio.PWMOut(board.GP11, frequency=50)
        self.motor2 = motor.DCMotor(m2a, m2b)

        # Initialize piezo
        self.piezo = PIEZO_PIN

        # Initialize TOF sensors
        self.tof_right = adafruit_vl53l0x.VL53L0X(busio.I2C(board.GP5, board.GP4))

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
                print(f"Range: {self.tof_right.range}mm")
            elif self.state == LOST:
                pass
            elif self.state == WON:
                pass


    def drive(self):
        pass
        # Move motors at 50% speed
        # motor1.throttle = 0.5  # motor1.throttle = 1 or -1 for full speed
        # motor2.throttle = -0.5

        # Brake motors
        # motor1.throttle = 0  # motor1.throttle = None to spin freely
        # motor2.throttle = 0



if __name__ == "__main__":
    SumoBot().run()



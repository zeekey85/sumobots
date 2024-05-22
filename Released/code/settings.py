import board

# Robot hardware settings

# Pin connected to piezo buzzer
PIEZO_PIN = board.GP22

# Pins connected to DC motors (swap variable names if your motors are connected differently)
RIGHT_MOTOR_PIN_B = board.GP11
RIGHT_MOTOR_PIN_A = board.GP10
LEFT_MOTOR_PIN_A = board.GP8
LEFT_MOTOR_PIN_B = board.GP9

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

# Pin for battery voltage reference path
BATTERY_VOLTAGE_PIN = board.A3
# Low battery threshold voltage
BATTERY_VOLTAGE_THRESHOLD = 52500

# Maximum enemy targeting range
MAX_DISTANCE = 600

# Time to charge forward before checking sensors
CHARGE_INTERVAL = 0.05
MAX_CHARGE = 1
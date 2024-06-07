# Sumo Bot

## Initial setup
Open `settings.py` and review the pin assignments there. Change any pin values on your hardware if they dont match the default settings in settings.py.

## Installation instructions
Make a backup copy of the code.py file that cam on your MakerPi board.
Copy the files `base-bot.py`, `code.py`, `adafruit_vl53l0x.mpy`, and `settings.py` to your MakerPi to get a working sumo bot.

## How to use
Turn on your MakerPi. To start a bout hold down the GP20 button until the light turns yellow. Your bot is now armed. Release the button to start at bout after a 5 second delay.
See the rules document for more detail on how Sumo bot matches operate.

## How to customize
Change the `MAX_DISTANCE` in settings.py to change the maximum distance at which your bot will detect enemies.
Other basic configuration settings will be added to this file

## Advanced customization
Modify the `fight()` method in code.py to change your robot's fighting strategy.

## File descriptions 
* 'settings.py' hardware pin assignments and basic behavior settings
* `code.py` defines the `fight()` method which determines the robot's logic while in fight mode.
* `base_bot.py` contains the main class which defines the fundamental methods for robot control such as moving and detecting enemies.
* `adafruit_Vl530x.mpy` is the driver for the time of flight sensors. The robot code won't work without it installed on the MakerPi.
* `original_code.py` is the default demo program that shipped with the MakerPI RP2040. It's not needed for the robot to work.

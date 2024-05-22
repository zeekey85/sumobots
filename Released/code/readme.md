# Sumo Bot

## Initial setup
Open `settings.py` and review the pin assignments there. Change any pin values if your hardware is connected than the default settings.

## Installation instructions
Copy the files `base-bot.py`, `code.py`, `adafruit_vl53l0x.mpy`, and `settings.py` to your MakerPi to get a working sumo bot.

## How to use
Turn on your Maker Pi and press buttons until you find the one that turns the lights from red to yellow. Your bot is now armed. Release the button to enter FIGHT MODE!

## How to customize
Change the `MAX_DISTANCE` setting to change the maximum distance at which your bot will detect enemies.

#### *Coming Soon*
Change the `TIMING_*` settings to change the duration of various robot actions.

## Advanced customization
Modify the `fight()` method in code.py to change your robot's fighting strategy.

## File descriptions 
* `code.py` defines the `fight()` method which determines the robot's logic while in fight mode.
* `base_bot.py` contains the main class which defines the fundamental methods for robot control such as moving and detecting enemies.
* `adafruit_Vl530x.mpy` is the driver for the time of flight sensors. The robot code won't work without it installed on the MakerPi.
* `original_code.py` is the default demo program that shipped with the MakerPI RP2040. It's not needed for the robot to work.

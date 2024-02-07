To see TOF sensor readings:
1. Connect a TOF sensor to your MakerPi via Grove 3 connector. GP4 = SDA, GP5 = SCL. 
2. Copy the folder "adafruit bus device" and the file "adafruit_vl53l0x.mpy" from the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) to the "lib" folder on your MakerPi
3. Copy code.py to your MakerPi
4. MakerPi NeoPixels will light up red. Hold the GP20 button and release it (NeoPixels will turn yellow when button is held and green when button is released).
5. Connect to the MakerPi serial port (e.g., using Putty or other serial IO application) to see range readings.
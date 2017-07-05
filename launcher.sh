#!/bin/sh
#Make sure gpsd has been started.
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket

#Point gpsd to the USB Serial connection.
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

#Run the application
export DISPLAY=":0.0"
su chip -c "python /home/chip/PocketStrava/PocketStrava.py"

#Make sure your clock is synced up
sudo ntpdate -buv pool.ntp.org

#Make sure your system is updated
sudo apt-get update

#Install Python stuff
sudo apt-get install git build-essential python-dev python-pip -y
sudo apt-get install python-imaging-tk

#Install Strava API library
sudo pip install stravalib

#git clone git://github.com/xtacocorex/CHIP_IO.git
#cd CHIP_IO
#sudo python setup.py install
#cd ..
#sudo rm -rf CHIP_IO
#sudo pip install pyserial

#Install gpsd
sudo apt-get install gpsd gpsd-clients python-gps

### Other stuff, have to experiment with this a little.
# #Stop and disable systemd service gpsd installs.
# #Read: https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/setting-everything-up#raspbian-jessie-systemd-service-fix
# sudo systemctl stop gpsd.socket
# sudo systemctl disable gpsd.socket
#
# #Point gpsd to the USB Serial connection
# sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

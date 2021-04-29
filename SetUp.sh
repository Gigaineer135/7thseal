#!/usr/bin/bash
apt install gpsd
apt install gpsd-clients
apt install python3-pip
pip3 install tk
rm -rf /etc/7thseal
gpsd -D 5 -N -n /dev/ttyUSB0

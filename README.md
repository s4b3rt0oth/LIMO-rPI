# LIMO-rPI
Motion activating LIFX lights with a PI Zero W and PIR sensor.

The only requirement is the lifxlan module from pip.

```
pip install lifxlan
```
or

```
sudo pip install -r requirements.txt
```

This was built with python2.7 but it has ran on python3. There are some minor changes to syntax needed to run on 3. I kept it at 2.7 because that's what my version of Raspbian shipped with and I didn't feel like changing it.

This git assumes a couple things:

1. Script will be installed as a system service and started at boot. Restart after fail.
2. There is a PIR motion sensor on pin 16 (Physical), 23(BCM).
3. lifxlan module is installed. It can be found here: https://github.com/mclarkk/lifxlan


To install as a service:

#Move lifx_motion.service file to proper folder

```
sudo mv ./etc/systemd.system/lifx_motion.service /etc/systemd/system/
```

#Move the script into a system accesible folder for better configuration

```
sudo mkdir -p /usr/local/lib/lifx_motion/ && sudo mv ./lifx_motion.py /usr/local/lib/lifx_motion/
```

#Update systemd

```
sudo systemctl daemon-reload
```

#Check that the service loaded

```
sudo systemctl list-unit-files | grep lifx
```



Huge thanks to torfsen for the tutorial: https://github.com/torfsen/python-systemd-tutorial

This couldn't have been done without mclarkk: https://github.com/mclarkk/lifxlan

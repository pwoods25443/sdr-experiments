# GQRX

## OSX

Installed the dmg for OSX from here:  http://gqrx.dk/download

Works great on Mojave 10.14.6


### Tried this - didn't work

Installing gqrx for the raspberry pi

http://gqrx.dk/download/gqrx-sdr-for-the-raspberry-pi

```
wget -O gqrx-sdr-2.11.5-linux-rpi3.tar.xz https://github.com/csete/gqrx/releases/download/v2.11.5/gqrx-sdr-2.11.5-linux-rpi3.tar.xz
tar -x --xz -f gqrx-sdr-2.11.5-linux-rpi3.tar.xz
cd gqrx-sdr-2.11.5-linux-rpi3/
cat readme.txt
sudo apt update
sudo apt install gnuradio libvolk1-bin libusb-1.0-0 gr-iqbal
sudo apt install qt5-default libqt5svg5 libportaudio2
```
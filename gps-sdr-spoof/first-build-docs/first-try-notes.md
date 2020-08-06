# GPS SDR Spoof experimentation

- Goal: Get this working https://github.com/B44D3R/SDR-GPS-SPOOF

### Ubuntu 14.04

First problem - how to get Ubuntu 14.04 on the RPI

Looks like I can't find an image, so first I will try 18.04 LTS and see if that works

### First try

#### Hardware
- Raspberry Pi 4B
- [Hacker RF One](https://greatscottgadgets.com/hackrf_)
- [Ant500](https://greatscottgadgets.com/ant500)
- [GPS Clock](http://www.leobodnar.com/shop/index.php?main_page=product_info&cPath=107&products_id=234)

#### Setup
- Installing 64-bit 18.04 for RPI 4 from here: https://ubuntu.com/download/raspberry-pi
- Flash the image to SD Card: https://ubuntu.com/tutorials/create-an-ubuntu-image-for-a-raspberry-pi-on-macos#1-overview
- Configure wifi https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#3-wifi-or-ethernet
- Install the SD card and boot the RPI
- SSH in to the RPI user: `ubuntu`  pwd:`ubuntu`
- wait for the auto updates to finish running
- install [latest cmake](https://stackoverflow.com/questions/49859457/how-to-reinstall-the-latest-cmake-version) (needed for gr-osmosdr -  CMake 3.13 or higher is required) 


### Test the HackrRF hardware
Connect the HackerRF One and do this
```
$ hackrf_info
hackrf_info version: git-e93d70e
libhackrf version: git-e93d70e (0.5)
Found HackRF
Index: 0
Serial number: 000000000000000075b068dc32432307
Board ID Number: 2 (HackRF One)
Firmware Version: 2018.01.1 (API:1.02)
Part ID Number: 0xa000cb3c 0x0061435b
```

### Test the GPS Clock
```
$ sudo hackrf_debug --si5351c -n 0 -r
```
Working
```
[  0] -> 0x01
```

Not working
```
[  0] -> 0x51
```

### AIS transmitter
Let's try to install an AIS transmitter so we have something to receive with aisdeco2
```
git clone https://github.com/trendmicro/ais.git
cd ais/gr-aistx
mkdir build
cd build
cmake ../
make
sudo make install
```

This works 
```
$ ./AIVDM_Encoder.py --type=1 --mmsi=970010000 --lat=45.6910 --long=9.7235
000001001110011101000100101101100100001111100000000000000001000000101100100000101011101000011010001001010000010010000011010000101111111111001100000000000000000000000000
```

But this doesn't
```
$ ./AiS_TX.py 
linux; GNU C++ version 7.3.0; Boost_106501; UHD_003.010.003.000-0-unknown

Traceback (most recent call last):
  File "./AiS_TX.py", line 32, in <module>
    from gnuradio.gr import firdes
ImportError: cannot import name firdes
```
Edit `AiS_TX.py ` and replace `from gnuradio.gr import firdes` with `from gnuradio.filter import firdes`

Next problem 
```
$ ./AiS_TX.py 
...
ImportError: No module named _AISTX_swig
```

Fixed with
```
export LD_LIBRARY_PATH=/usr/local/lib
```

Now try this
```
./AIVDM_Encoder.py --type=1 --mmsi=970010000 --lat=45.6910 --long=9.7235 | xargs -IX ./AiS_TX.py --payload=X --channel=A
```
Seems to want to connect to the X11 display
```
linux; GNU C++ version 7.3.0; Boost_106501; UHD_003.010.003.000-0-unknown

Unable to access the X Display, is $DISPLAY set properly?
```
OK - looks like this requires `grc_gnuradio.wxgui` so we are not going to be able to run this headlesss

### AIS Receiver
- Download [aisdeco2](http://xdeco.org/?page_id=30#ad2)
Trying the version for `Raspberry Pi 2 / 3 Debian 9`
```
scp ~/Downloads/aisdeco2_rpi2-3_deb9_20180430.tgz ubuntu@192.168.0.23:~/
ssh ubuntu@192.168.0.23
mkdir aisdeco2
mv aisdeco2_rpi2-3_deb9_20180430.tgz aisdeco2
cd aisdeco2
tar xzf aisdeco2_rpi2-3_deb9_20180430.tgz
./aisdeco2 --device-list
```
No good - won't run in ubuntu :-(


-  Copy of install.sh on the ubunbtu RPI image
### install.sh
```
## Need a more recent version of cmake for gr-osmosdr
##

## THIS DOES NOT WORK FOR ARM64 :-(
#sudo apt-get -y install apt-transport-https ca-certificates gnupg \
#                         software-properties-common wget
# wget -qO - https://apt.kitware.com/keys/kitware-archive-latest.asc \
#    | sudo apt-key add -
#sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
#sudo apt-get update

## Trying this...
#sudo snap install cmake --classic


#sudo apt-get -y install \
#                       git \
#                       build-essential \
#                       libusb-1.0-0-dev \
#                       liblog4cpp5-dev \
#                       libboost-dev \
#                       libboost-system-dev \
#                       libboost-thread-dev \
#                       libboost-program-options-dev \
#                       swig \
#                       libfftw3-dev \
#                       libusb-dev \
#                       libusb-1.0-0-dev \
#                       pkg-config \


#mkdir ~/sdr

#cd ~/sdr
#git clone https://github.com/mossmann/hackrf.git

#cd hackrf/host
#mkdir build && cd build

cd ~/sdr/hackrf/host/build
#cmake ../ -DINSTALL_UDEV_RULES=ON
#make
#sudo make install
#sudo ldconfig

#sudo apt-get install gnuradio \
#                       gnuradio-dev \
#                       gr-iqbal

#cd ~/sdr

# Giving up on master becuase it requires gnuradio to be compiled with cmake >= 3.8 and the version that installs with apt is 3.7
#git clone git://git.osmocom.org/gr-osmosdr

# Try to install release v0.1.5 
git clone https://github.com/osmocom/gr-osmosdr.git --branch v0.1.5
cd ~/sdr/gr-osmosdr
mkdir build && cd build

cd ~/sdr/gr-osmosdr/build
cmake ../
make
sudo make install
sudo ldconfig

sudo apt-get install gqrx-sdr
sudo apt-get install libvolk1-bin
volk_profile

cd ~/sdr
git clone https://github.com/osqzss/gps-sdr-sim
cd gps-sdr-sim
gcc gpssim.c -lm -O3 -o gps-sdr-sim

# add to .bashrc
export PATH="/home/ubuntu/sdr/gps-sdr-sim:$PATH"

```

To get the daily ephemeris file (Note must authenticate))
```
https://cddis.nasa.gov/archive/gnss/data/daily/2020/214/20n/brdc2140.20n.Z
# example for Aug 1 2020 (day 214) 
https://cddis.nasa.gov/archive/gnss/data/daily/2020/214/20n/brdc2140.20n.Z
```

NMEA
https://www.gpsinformation.org/dale/nmea.htm

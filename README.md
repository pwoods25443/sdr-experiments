# sdr-experiments
Experiments with software defined radio

Inspired by the [Open Source Ground Station Network](https://satnogs.org/)

### Planned Projects

* SatNOGS ground station
* AIS terrestrial receiver
* AIS transmitter
* GPS sim testbed 

[AIS Receiver](AIS-receiver.md)

Trying https://github.com/opustecnica/public/wiki/Raspberry-PI-Bluetooth-PAN-Network


Had to do this on the raspberry pi
```buildoutcfg
cd /etc/ssl/certs
sudo wget http://curl.haxx.se/ca/cacert.pem
```

### Python environment setup
To run the python tools, do this setup first


```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

*NOTE FOR OSX and libais*
If libais install fails with something like this
```
    In file included from src/libais/ais_py.cpp:6:
    src/libais/ais.h:8:10: fatal error: 'array' file not found
    #include <array>
             ^~~~~~~
    1 warning and 1 error generated.
```

You may have [this issue](https://github.com/schwehr/libais/issues/184). 
In that case, you need to use the gcc compilier instead of the osx clang compiler.   I found that this worked

```buildoutcfg
brew install gcc
CC=gcc-9 CXX=g++-9 pip install libais
```


### Install python 3 and pip on raspberry pi
**NOTE probably don't need this after all**
```buildoutcfg
sudo apt install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev \
  zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential libncursesw5-dev libc6-dev openssl git
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tar.xz
tar xf Python-3.6.9.tar.xz
cd Python-3.6.9/
./configure --enable-optimizations
make -j -l 4
sudo make altinstall
sudo python3.6 get-pip.py
curl -O https://bootstrap.pypa.io/get-pip.py
```

### AIS streaming with tagblock

```buildoutcfg
aisdeco2
```
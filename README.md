# sdr-experiments
Experiments with software defined radio

Inspired by the [Open Source Ground Station Network](https://satnogs.org/)

### Planned Projects

* SatNOGS ground station
* AIS terrestrial receiver 

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

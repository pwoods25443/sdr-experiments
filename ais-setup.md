Working in the AISHub Pi image version 1.1
https://www.aishub.net/rpiais

```buildoutcfg
sudo apt-get update
sudo apt-get install rtl-sdr
scp ~/Downloads/aisdeco2_rpi2-3_deb9_20180430.tgz pi@raspberrypi.local:~
ssh pi@raspberrypi.local
mkdir aisdeco2
mv aisdeco2_rpi2-3_deb9_20180430.tgz aisdeco2
cd aisdeco2
tar xzf aisdeco2_rpi2-3_deb9_20180430.tgz 
./aisdeco2 --device-list
```

Seems that RPIAIS does not show anything listening on port 8080
Maybe does not work on RPI4?  

Trying this instead

https://pysselilivet.blogspot.com/2019/10/ais-receiver-with-openseamap.html

```buildoutcfg
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
sudo npm install -g --unsafe-perm signalk-server
sudo signalk-server-setup
```
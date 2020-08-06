# Pi Setup

## Enable wifi and ssh on first boot
After flashing the raspberry pi image, mount the boot partition.  On OSX do this with the Disk Utility.

To enable SSH, create an empty file called `SSH` on the boot partition.  This file will disappear after the next boot and the appropriate settings will be enabled in `/etc/ on the pi
```buildoutcfg
touch /Volumes/boot/SSH 
```

To enable wifi, create a file called `wpa_supplicant.conf` in the boot partition
```buildoutcfg
nano /Volumes/boot/wpa_supplicant.conf
```

The content of the file should be 

```buildoutcfg
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
  ssid="SSID"
  psk="PASSWORD"
}
```
Where you replace SSID and PASSWORD with the appropriate values

This file will also disappear from the boot partition after boot and the content will be copied into /etc



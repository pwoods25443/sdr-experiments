#AIS Receiver

## Laptop-based Setup Dec 2019
* Macbook pro
* VirtualBox
* Ubuntu 18.04 running in VirtualBox
    * VM networking set to “bridged”

### Installed In Ubuntu    
    * [Aisdeco2](http://xdeco.org/?page_id=30#ai2)
    * [Open CPN](https://opencpn.org/index.html)

### Hardware     
    * RTL-SDR hardware (RTL2832U)
    * Antenna included with RTL-SDR kit

### Configuration
    * Connect the RTL2832U to the laptop
    * Connect the RTL2832U to the VM via the VirtualBox USB menu
    * Set the VirtualBox netoworking mode to Bridged
    * In OpenCPN, create a new input connection: UDP, localhost, port 4159
    * Optional - install high resolution chars in OpenCPPN
    
### Execution
* Startup OpenCPN
* in a terminal run 
```
./aisdeco2 --agc --freq-correction -1 --udp 192.168.43.250:4159
```
Where `192.168.43.25` is the local IP address.  Note that this does not work with `localhost` or `127.0.0.1`

`-freq-correction -1` is the correction factor for the individual SDR hardware.  This needs to be determined experimentally.

If there are AIS messages to be received, they will be logged to the console and also sent to the UDP port.  If everything is set up right then vessels will appear in OpenCPN





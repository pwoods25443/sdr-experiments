# GPS SDR Spoof experimentation

### Background

At Global Fishing Watch and SkyTruth, we have been observing some interesting [AIS broadcasts](https://globalfishingwatch.org/data-blog/circling-above-point-reyes/) collected by satellite receivers that seem to indicate that the GPS inputs to the AIS transmitters are being interfered with so as to cause the AIS to report a false location.

This is different from other [false location broadcasts](https://globalfishingwatch.org/data/when-vessels-report-false-locations/) that we have observed because we suspect that the false location is not intentional on the part of the vessel operator and is the result of external manipulation of the GPS signal.

The goal of this project is to see if we can emulate that effect by using cheap off the shelf SDR hardware to interfere with location reporting in a class B AIS device

### First Project: Get a simple GPS spoofer working
- [First build](first-build-docs/README.md) - Raspberry Pi and HackerRF with Ubuntu 18.04 LTS


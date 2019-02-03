# Raspberry Pi slave library for Arduino with VL6180X sensor attached to I2C bus

Version: 2.1.0 (forked)<br>
Release date: 2019 Feb 3<br>
[www.pololu.com](https://www.pololu.com/)

Summary
-------

This is a port of the Pololu 32U4 Balboa code to add VL6180X support for the Raspberry Pi via the Pi's GPIO header, with the Arduino acting as the I<sup>2</sup>C slave.  It should
work with most Arduino-compatible boards, but we designed it for use
with these Pololu products:

* [A-Star 32U4 Robot Controller LV](https://www.pololu.com/product/3117) or [SV](https://www.pololu.com/product/3119)
* [Romi 32U4 Control Board](https://www.pololu.com/product/3544)
* [VL6180X Python3 port](https://github.com/HeMe2/RPI_ST-VL6180X-Python3)

These boards are designed to connect conveniently to the Pi's GPIO header.  The
idea is that the Raspberry Pi can take care of high-level tasks like video
processing or network communication, while the AVR microcontroller takes care of
actuator control, sensor inputs, and other low-level tasks that the Pi is
incapable of.

There are a few reasons we made a library for this instead of
just recommending the standard Arduino I<sup>2</sup>C library, Wire.h:

* Wire.h just gives you access to raw I<sup>2</sup>C packets; you have to decide
  how they should relate to your data, and that's not trivial. This
  library implements a specific protocol allowing bidirectional access
  to a buffer, with atomic reads and writes.
* The processor on the Raspberry Pi has
  [a major bug](http://www.advamation.com/knowhow/raspberrypi/rpi-i2c-bug.html)
  that corrupts data except at very low speeds.  The standard Arduino
  I<sup>2</sup>C library, Wire.h, is not flexible enough to allow us to follow
  the suggested workarounds (delays inserted at key points).

Getting started
---------------

See [this blog post](https://www.pololu.com/blog/577/building-a-raspberry-pi-robot-with-the-a-star-32u4-robot-controller)
for a complete tutorial including step-by-step build instructions for
an example robot.

Benchmarking
------------

The included script `benchmark.py` times reads and writes of 8 bytes,
to give you an idea of how quickly data can be transferred between the
devices.  Because of a limitation in the AVR's I<sup>2</sup>C module,
we have slowed down reads significantly.

| Bus speed | Reads     | Writes     |
| --------- | --------- | ---------- |
| 100 kHz   | 21 kbit/s | 53 kbit/s  |
| 400 kHz   | 43 kbit/s | 140 kbit/s |

Version history
---------------

* 2.1.0 (2019 Feb 3) Forked code from Pololu "balboa" tree found [here](https://github.com/pololu/pololu-rpi-slave-arduino-library/tree/balboa).
* 2.0.0 (2017 Mar 31): Added support for encoder counts and slave sketch for the Romi 32U4 robot. Updated Raspberry Pi scripts to use Python 3 instead of Python 2.
* 1.0.1 (2017 Jan 23): Added and adjusted delays necessary for reliable operation on the Pi 3.
* 1.0.0 (2016 Feb 16): Original release.

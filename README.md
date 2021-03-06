# QCK Prism
Working out the protocol for the SteelSeries QCK Prism Mousemat.

**Please use [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB) instead of any code here.** This repo exists to document the protocol so it can be PR'd to OpenRGB.

My dev branch for this in OpenRGB is
[here.](https://gitlab.com/bahorn/OpenRGB/-/tree/feature/qck-prism)

Protocol seems to be pretty similar with existing steelseries products, but with a different set of commands.

Everything was figured out from Wireshark captures.

## Communication

Working with the "SteelSeries QcK Prism - Cloth Gaming Mousemat - XL", different revisions might have a different protocol or vendor ID. Controller is probably pretty static between sizes though, just a little USB device connected to a diffusion tube.

* Vendor ID: 1038
* Product ID: 150d
* Device Name: SteelSeries ApS SteelSeries QCK Prism Cloth

```
SET_REPORT
wValue 0x0300
wIndex: 0
bmRequest: 9
bmRequestType 0x21
```

## Known Commands

* 0x0b - Effects.  64 or 524 bytes
* 0x0c - Brightness. 64 Bytes
* 0x0d - Reset? 64 byte packets but empty beyond null bytes.
* 0x0e - Setting Color. 524 bytes
* 0x10 - No idea, got sent when openning the app. Doesn't seem to repsond with anything but the usual status.

### 0x0b - Effects

All the commands sending effects seem to us this.

Timing control seems to be represented as a 16 bit int.

When turning an effect off, the app sent a 524 byte packet with just null bytes.

### 0x0c - Brightness

```
0c 00 BRIGHTNESS
```

Brightness is sent as a byte. In the GUI there are 4 options for brightness `00, 55, aa, ff`.

### 0x0d - Reset

Sent after and before most commands, believe its the reset command.

### 0x0e - Setting Color

Packet looks roughly like this:

```
CMD   00 COUNT 00
COLOR FF 32 c8 00 00 00 CYCLE 00 ZONE
COLOR FF 32 c8 00 00 01 CYCLE 00 ZONE
```

So each led is set with 12 bytes in the packet.

* Color is 3 bytes, representing RGB values.
* Count is the number of leds being set in this message in this message.
* Unsure of the rest, probably flags of some sort?
* Cycle is the needs to be set to 01 if this byte is to change to the specified
  color and not just cycle through them.
* Zone is the LED to control
* Think the FF right after a color is just padding.

It seems you can use the flags to control what colors get merged?

### 0x10 - Unknown

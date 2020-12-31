# Setup

Reviewing `./captures/connecting-device.pcapng`

Initially, it sends normal USB things which can mostly be ignored.

All response just seem to be URB success.


## Interesting Packets

### Packet 51

It sends a request with an `0d` command, with the rest filled with null bytes.

### Packet 53

It just sends a `10` command, rest of it filled with null bytes.

### Packet 55

Sends an `0b`, with byte 3 set to `01`.

This is normally the effect command? Is it setting it to static?

### Packet 57

Sent an `0b` but will the whole packet being null bytes.

### Packet 59

Sends an `0e`, in this case setting both LEDs to `ff5200`

### Packet 61

Sends the brightness packet, setting it to full brightness.

Probably dependent on settings.

### Packet 63

Send an `0d` again.

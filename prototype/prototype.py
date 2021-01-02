import hid
import struct
import time
from enum import Enum

VENDOR_ID = 0x1038
PRODUCT_ID = 0x150d

def pad(msg, length, byte=b'\x00'):
    """
    Padding for our USB messages.
    """
    c = length - len(msg)

    return msg + byte*c


class QCKPrismCMDs(Enum):
    EFFECTS = 0x0b
    BRIGHTNESS = 0x0c
    SAVE = 0x0d
    COLOR = 0x0e
    UNKNOWN = 0x10

class QCKPrism:

    def __init__(self):
        h = hid.device()
        h.open(VENDOR_ID, PRODUCT_ID)
        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        h.set_nonblocking(1)
        self.dev = h

    def brightness(self, value):
        """
        Sets the brightness.
        Reads a value between 0.0 1.0 to set it.
        """
        cmd = QCKPrismCMDs.BRIGHTNESS.value
        msg = struct.pack('hB', cmd, int(255*value))
        self._send(msg)

    def unknown(self):
        cmd = QCKPrismCMDs.UNKNOWN.value
        msg = struct.pack('h', cmd)
        self._send(msg)

    def reset(self):
        cmd = QCKPrismCMDs.SAVE.value
        msg = struct.pack('h', cmd)
        self._send(msg)


    def mode(self):
        cmd = QCKPrismCMDs.EFFECTS.value
        msg = struct.pack('hh', cmd, 0x01)
        self._report(msg)
        msg = struct.pack('hh', cmd, 0x00)
        self._report(msg)

    def color(self, zone1, zone2):
        cmd = QCKPrismCMDs.COLOR.value
        header = struct.pack('hh', cmd, 2)
        c1 = struct.pack('BBB', zone1[0], zone1[1], zone1[2])
        c1 += b'\xff\x32\xc8\x00\x00\x00\x01\x00\x00'
        c2 = struct.pack('BBB', zone2[0], zone2[1], zone2[2])
        c2 += b'\xff\x32\xc8\x00\x00\x00\x01\x00\x01'
        msg = pad(header + c1 + c2, 524)
        print(msg)
        self._report(msg)

    def _send(self, msg):
        self.dev.write(pad(msg, 64))
        time.sleep(0.1)

    def _report(self, msg):
        self.dev.send_feature_report(pad(msg, 524))
        time.sleep(0.1)

try:
    prism = QCKPrism()
    prism.color((0x00, 0x00, 0xff), (0xff, 0x00, 0x00))
    prism.brightness(1.0)
    prism.reset()

except IOError as ex:
    print(ex)

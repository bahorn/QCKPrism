import hid
import struct
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
        msg = struct.pack('hB', int(QCKPrismCMDs.BRIGHTNESS.value),
                          int(255*value))
        self._send(msg)

    def _send(self, msg):
        self.dev.write(msg)

try:
    prism = QCKPrism()
    prism.brightness(0.75)
    
except IOError as ex:
    print(ex)

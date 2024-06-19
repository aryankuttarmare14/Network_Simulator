import random
import time

import urllib3


class EndDevice:
    def __init__(self, num):
        self.num = num

    def generate_mac_address(self):
        mac_addresses = [str(random.randint(0x00, 0xFF)) for _ in range(self.num + 1)]
        return "00:" + ":".join(mac_addresses)
    
    """GENERATES RANDOM MAC ADDRESS AND ASSIGNS TO END-DEVICES"""
    
e1 = EndDevice(2)
print(e1.generate_mac_address())
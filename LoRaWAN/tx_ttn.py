#!/usr/bin/env python3
import sys
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import LoRaWAN
from LoRaWAN.MHDR import MHDR

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

class LoRaWANsend(LoRa):
    def __init__(self, devaddr = [], nwkey = [], appkey = [], verbose = False):
        super(LoRaWANsend, self).__init__(verbose)
        self.devaddr = devaddr
        self.nwkey = nwkey
        self.appkey = appkey

    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        print("TxDone")
        sys.exit(0)

    def start(self):
        lorawan = LoRaWAN.new(nwskey, appskey)
        lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr, 'fcnt': 1, 'data': list(map(ord, 'Python rules!')) })

        self.write_payload(lorawan.to_raw())
        self.set_mode(MODE.TX)
        while True:
            sleep(1)


# Init
devaddr = [0x26, 0x01, 0x19, 0xAC]
nwskey = [0x93, 0xA0, 0x56, 0xC8, 0xE8, 0x94, 0xF8, 0x32, 0xE7, 0x9C, 0x79, 0xF4, 0xCC, 0xA8, 0x3F, 0x94]
appskey = [0x70, 0xEB, 0x0D, 0xD3, 0x7F, 0x2E, 0x31, 0xA4, 0x35, 0x81, 0x8D, 0xAA, 0xDB, 0x50, 0x48, 0xD5]
lora = LoRaWANsend(False)

# Setup
lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([1,0,0,0,0,0])
lora.set_freq(868.1)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(7)
lora.set_pa_config(max_power=0x0F, output_power=0x0E)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

print(lora)
assert(lora.get_agc_auto_on() == 1)

try:
    print("Sending LoRaWAN message\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()

#!/usr/bin/env python3
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import LoRaWAN

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN receiver")

class LoRaWANrcv(LoRa):
    def __init__(self, verbose = False):
        super(LoRaWANrcv, self).__init__(verbose)

    def on_rx_done(self):
        print("RxDone")

        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print("".join(format(x, '02x') for x in bytes(payload)))

        lorawan = LoRaWAN.new(nwskey, appskey)
        lorawan.read(payload)
        print(lorawan.get_mhdr().get_mversion())
        print(lorawan.get_mhdr().get_mtype())
        print(lorawan.get_mic())
        print(lorawan.compute_mic())
        print(lorawan.valid_mic())
        print("".join(list(map(chr, lorawan.get_payload()))))
        print("\n")

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)


# Init
nwskey = [0x93, 0xA0, 0x56, 0xC8, 0xE8, 0x94, 0xF8, 0x32, 0xE7, 0x9C, 0x79, 0xF4, 0xCC, 0xA8, 0x3F, 0x94]
appskey = [0x70, 0xEB, 0x0D, 0xD3, 0x7F, 0x2E, 0x31, 0xA4, 0x35, 0x81, 0x8D, 0xAA, 0xDB, 0x50, 0x48, 0xD5]
lora = LoRaWANrcv(False)

# Setup
lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([0] * 6)
lora.set_freq(868.1)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(7)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

print(lora)
assert(lora.get_agc_auto_on() == 1)

try:
    print("Waiting for incoming LoRaWAN messages\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()

from pirc522 import RFID
import RPi.GPIO as GPIO

def detect(rst=31,irq=29):
  rdr = RFID(pin_rst=rst,pin_irq=irq)
  while True:
    rdr.wait_for_tag()
    (error, tag_type) = rdr.request()
    if not error:
      print("Tag detected")
      (error, uid) = rdr.anticoll()
      if not error:
        uid = str(uid)
        print(uid)
        if not rdr.select_tag(uid):
          if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
            block = str(rdr.read(10))
            print(block)
            rdr.stop_crypto()
            rdr.cleanup()
            return uid,block
          else:
            print("Failed to get block")
            continue


def dectectKey(uid,block,rst=31,irq=29):
  _uid,_block = dectect(rst,irq)
  return _uid == uid and _block == block

def tempGet(rst=None,irq=None):
  return 1, 1

def tempDetect(uid,block):
  return True

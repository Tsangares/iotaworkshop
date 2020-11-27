import time
import RPi.GPIO as pi
import argparse

#Make single beep for a duration
def beepDuration(pin=12,duration=1):
    pi.setwarnings(False)
    pi.setmode(pi.BCM)
    pi.setup(pin,pi.OUT)
    pi.output(pin,pi.HIGH)
    time.sleep(duration)
    pi.output(pin,pi.LOW)
    pi.cleanup()

#Make a series of beepss at a specified frequency
def pulseBeep(pin=12,freq=4,duration=1):
    pi.setwarnings(False)
    pi.setmode(pi.BCM)
    pi.setup(pin,pi.OUT)
    for i in range(int(freq*duration/2)):
        pi.output(pin,pi.HIGH)
        time.sleep(1/freq)
        pi.output(pin,pi.LOW)
        time.sleep(1/freq)
    pi.output(pin,pi.LOW)
    pi.cleanup()

def warning(pin):
    pulseBeep(pin,freq=8,duration=1.5)

def confirmed(pin):
    pulseBeep(pin,freq=16,duration=.5)

def brr(pin):
    pulseBeep(pin,freq=50,duration=.5)

def shortBeep(pin):
    beepDuration(pin,.05)

def mediumBeep(pin):
    beepDuration(pin,.25)

def longBeep(pin):
    beepDuration(pin,.5)

    
def main():
    parser = argparse.ArgumentParser(description='Variety of beeps')
    subparsers = parser.add_subparsers(help='Choose a prompt.')
    
    short = subparsers.add_parser('short', help='Make a short beep.')
    short.add_argument('--pin',type=int, help='The GPIO pin number the beeper is on.',default=12)
    short.set_defaults(func=shortBeep)

    medium = subparsers.add_parser('medium', help='Make a medium beep.')
    medium.add_argument('--pin',type=int, help='The GPIO pin number the beeper is on.',default=12)
    medium.set_defaults(func=mediumBeep)

    longParser = subparsers.add_parser('long', help='Make a long beep.')
    longParser.add_argument('--pin',type=int, help='The GPIO pin number the beeper is on.',default=12)
    longParser.set_defaults(func=longBeep)

    warningParser = subparsers.add_parser('warning', help='Make a warning sound.')
    warningParser.add_argument('--pin',type=int, help='The GPIO pin number the beeper is on.',default=12)
    warningParser.set_defaults(func=warning)

    confirmedParser = subparsers.add_parser('confirmed', help='Make a confirmed sound.')
    confirmedParser.add_argument('--pin',type=int, help='The GPIO pin number the beeper is on.',default=12)
    confirmedParser.set_defaults(func=confirmed)
    
    brrParser = subparsers.add_parser('brr', help='Make a brr sound.')
    brrParser.add_argument('--pin',type=int, help='The GPIO pin number the beeper is on.',default=12)
    brrParser.set_defaults(func=brr)
    
    args = parser.parse_args()
    try:
        args.func(args.pin)
    except AttributeError as e:
        parser.print_help()
        
    

import time,logging
import RPi.GPIO as pi

#Basic servo class using PWM
#Angle is in degrees not radians
class Servo:
    def __init__(self,pin,freq):
        pi.setwarnings(False)
        Servo.clean()
        self.percent = 0
        self.pin = pin
        self.freq = freq
        self.deg = 360
        pi.setmode(pi.BCM)
        pi.setup(pin,pi.OUT)
        self.pwm = pi.PWM(pin,freq)
    def start(self):
        logging.debug("Servo started")
        self.pwm.start(0)
    def stop(self):
        self.pwm.stop()
        Servo.clean()
    def clean():
        pi.cleanup()
    def duty(self):
        return self.percent
    def setDuty(self,percent):
        self.pwm.ChangeDutyCycle(percent)
        self.duty = percent
    def frequency(self):
        return self.freq
    def setFreq(self,freq):
        self.pwm.ChangeFrequency(freq)
        self.freq = freq
    def position(self):
        return self.duty,self.deg
    def setPosition(self,deg,delay=0):
        distance = abs(self.deg - deg)
        sleep = distance/60*.5+delay
        self.setDuty(deg/18 + 2)
        logging.debug(f'Moving to {deg} degrees, duty {self.duty:.0f}%, sleeping for {sleep:.1f} sec.')
        self.deg = deg
        time.sleep(sleep+delay)
    def go(self,deg,delay=0):
        return self.setPosition(deg,delay)

#Set servo on pin to lock position
def lock(pin,angle=90):
    p=Servo(pin,50)
    p.start()
    p.go(angle)
    p.stop()

#Set servo on pin to unlock position
def unlock(pin,angle=0):
    p=Servo(pin,50)
    p.start()
    p.go(angle)
    p.stop()

#Move servo to specific location
def move(pin,angle):
    p=Servo(pin,50)
    p.start()
    p.go(angle)
    p.stop()
    
def main():
    import argparse
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Control display for escrow.')
    
    subparsers = parser.add_subparsers(help='Choose a prompt.')

    lockParse = subparsers.add_parser('lock', help='Move servo to lock position')
    lockParse.add_argument('--pin',type=int, help='The data GPIO pin for the servo',default=19)
    lockParse.add_argument('--angle',type=int, help='angle in degrees to move the servo.',default=90)
    
    lockParse.set_defaults(func=lock)
    
    unlockParse = subparsers.add_parser('unlock', help='Move servo to unlock position')
    unlockParse.add_argument('--pin',type=int, help='The data GPIO pin for the servo',default=19)
    unlockParse.add_argument('--angle',type=int, help='angle in degrees to move the servo.',default=0)
    unlockParse.set_defaults(func=unlock)
    
    move = subparsers.add_parser('move', help='Move servo to a specific position')
    move.add_argument('angle',type=int, help='angle in degrees to move the servo.')
    move.add_argument('--pin',type=int, help='The data GPIO pin for the servo',default=19)
    move.set_defaults(func=move)

    args = parser.parse_args()
    args.func(args.pin,args.angle)

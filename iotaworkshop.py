from iotaescrow import Escrow
import piepd as display
import pibeep as beep
import servo_lock as servo
import rc522 as rfid
import time,logging
import .gatewate

logging.basicConfig(level=logging.INFO)
def testServo():
    pin=19
    servo.lock(pin)
    time.sleep(3)
    servo.unlock(pin)

class IotaWorkshop:
    def __init__(self,collateral,fee,node='https://nodes.thetangle.org:443',tool="A tool",silent=False):
        self.escrow = Escrow(node=node,keepyNode=None)
        self.servoPin=19
        self.beepPin=12
        self.collateral=collateral
        self.fee=fee
        self.tool=tool
        self.silent=silent
        self.escrowAddress = None
        self.available = True
        self.keepyNode=keepyNode
        self.deposit = None
        
    def start(self):
        while True:
            self.unoccupied()
            
    def submitState(self):
        if keepyNode is None: return
        gateway.submitEscrowState(
            self.keepyNode,
            self.collateral,
            self.fee,
            self.tool,
            "rfid",
            self.holdingAddress,
            self.deposit,
            self.available,
        )
        
    def unoccupied(self):
        #Get RFID Tag id
        self.rfid = (1,1)

        #Make sure box is locked
        logging.info("Locking servo.")
        servo.lock(self.servoPin)

        #Get an address to be the escrow
        logging.info("Getting escrow address.")
        address = self.escrow.createEscrow()
        self.holdingAddress = address
        
        logging.info("Interfacing user.")
        logging.info(f"Holding Address: {address}")

        #Set Display to prompt user to give address
        display.unoccupied(address=str(address),fee=11)
        logging.info("Waiting for user to send refund address.")

        #Submit state to ledger
        self.submitState()
        
        #Wait for a user to interface with device
        refundAddress = self.escrow.getRefundAddress()
        if not self.silent: beep.brr(self.beepPin)
        while refundAddress is None:
            time.sleep(3)
            refundAddress = self.escrow.getRefundAddress()
            
        #User has given box an address
        self.deposit = refundAddress

        #Submit new state to ledger
        self.submitState()
        
        #Prompt user to deposit funds
        self.promptDeposit()

    #Prompts the user to deposit collateral funds
    def promptDeposit(self,refundAddress=None):
        if refundAddress is None: refundAddress = self.deposit
        if not self.silent: beep.confirmed(self.beepPin)
        logging.info(f"Address recieved: {refundAddress}")
        address = self.escrow.holdingAddress

        #Display costs to user
        display.depositPage(address=address,fee=self.fee,deposit=self.collateral,duration=120)
        logging.info(f"Waiting for deposit.")

        #Wait for funds to arrive in escrow
        if self.escrow.requestDeposit(self.collateral,refundAddress,duration=120):
            #Escrow recieved unlock box for user
            if not self.silent: beep.confirmed(self.beepPin)
            display.takeItem()
            servo.unlock(self.servoPin)
            time.sleep(5)

            #Prompt occupied display
            display.occupied()
            self.waitForReturn(refundAddress)            
        else:
            #User gave an invalid input, reset
            if not self.silent: beep.warning(self.beepPin)
            logging.warning("User failed to deposit collateral")
            self.unoccupied()

    #Wait for user to return device to box
    def waitForReturn(self,refundAddress):
        #Submit state
        self.available = False
        self.submitState()
        
        #Give user 10 secconds to remove item from box
        time.sleep(10)
        logging.info("Waiting for user to deposit item.")
        
        #Wait for user to deposit item back in box.
        while not tempDetect():
            time.sleep(5)

        #Item returned
        logging.info("User deposited item. Refunding deposit.")
        self.escrow.finalizeEscrow(fee=self.fee)

def tempDetect():
    return True

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Iota workshop utiltiy")
    parser.add_argument('--node',type=str,help="Iota node", default='https://nodes.thetangle.org:443')
    parser.add_argument('--keepy',type=str,help="Iota node", default='https://keepy.gradstudent.me/messages')
    args = parser.parse_args()

    workshop = IotaWorkshop(collateral=26000,fee=1000,node=args.node,keepyNode=args.keepy)
    workshop.start()

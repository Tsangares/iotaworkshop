
from iotaescrow import Escrow
import piepd as display
import pibeep as beep
import servo_lock as servo
import rc522 as rfid
import time,logging
import gateway

logging.basicConfig(level=logging.INFO)
def testServo():
    pin=19
    servo.lock(pin)
    time.sleep(3)
    servo.unlock(pin)

class IotaWorkshop:
    def __init__(self,collateral,fee,tool="A tool",node='https://nodes.thetangle.org:443',keepyNode=None,silent=False):
        self.escrow = Escrow(node=node)
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
        self.holdingAddress = None
        
    def start(self):
        while True:
            self.unoccupied()
            self.deposit=None
            self.holdingAddress=None
            
    def submitState(self,state=None):
        if self.keepyNode is None: return
        gateway.submitEscrowState(
            self.keepyNode,
            self.collateral,
            self.fee,
            self.tool,
            "rfid",
            str(self.holdingAddress),
            str(self.deposit),
            self.available,
            state,
        )
        
    def unoccupied(self):
        #Get RFID Tag id
        self.rfid = (1,1)
        self.submitState('Initializing')
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
        display.unoccupied(address=str(address),fee=self.fee)
        logging.info("Waiting for user to send refund address.")

        #Submit state to ledger
        self.submitState('Waiting for user to send refund address')
        
        #Wait for a user to interface with device
        refundAddress = self.escrow.getRefundAddress()
        if not self.silent: beep.brr(self.beepPin)
        while refundAddress is None:
            time.sleep(3)
            refundAddress = self.escrow.getRefundAddress()
            
        #User has given box an address
        self.deposit = refundAddress

        #Submit new state to ledger
        self.submitState('Refund address recieved. Waiting for deposit.')
        
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
            self.submitState('Deposit recieved openind chassis.')
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
        self.submitState('Tool in use.')
        
        #Give user 10 secconds to remove item from box
        time.sleep(10)
        logging.info("Waiting for user to deposit item.")
        
        #Wait for user to deposit item back in box.
        while not tempDetect():
            time.sleep(5)

        #Item returned
        logging.info("User deposited item. Refunding deposit.")
        self.available = True
        self.escrow.finalizeEscrow(fee=self.fee)
                

def tempDetect():
    return True

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Iota workshop utiltiy")
    parser.add_argument('--node',type=str,help="Iota node", default='https://nodes.thetangle.org:443')
    parser.add_argument('--keepy',type=str,help="Keepy node for streams", default='http://192.168.1.6:3002')
    parser.add_argument('--name',type=str,help="Name of the tool.", default='A tool')
    parser.add_argument('--collateral',type=int,help="The amount of collateral", default=87)
    parser.add_argument('--fee',type=int,help="The fee for using the tool.", default=7)
    args = parser.parse_args()
    logging.info(args)
    workshop = IotaWorkshop(collateral=args.collateral,fee=args.fee,node=args.node,keepyNode=args.keepy,tool=args.name)
    workshop.start()

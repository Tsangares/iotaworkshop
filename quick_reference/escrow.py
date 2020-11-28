import time,json,os,subprocess,requests
from iota import Iota, ProposedTransaction, Address, TryteString, Fragment, Transaction,adapter,ProposedBundle
from iota.crypto.addresses import AddressGenerator
import pathlib,logging,argparse,random
LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZ9"
class Escrow:
    def __init__(self,node='https://nodes.thetangle.org:443'):
        #Get Seet
        self.seed = self.getSeed()

        #Setup API
        self.api = Iota(node,self.seed)

    #Generates a seed for escrow account
    def getSeed(self):
        #If no seed, create one
        if not os.path.isfile('seed.txt'):
            path = pathlib.Path(__file__).parent.absolute()
            seed = ''.join([random.choice(LETTERS) for i in range(81)])
            open('seed.txt','w+').write(seed)
            logging.info("Placed new seed in seed.txt")
        return open('seed.txt').read().strip().encode('utf-8')
    
    #Creates an escrow holding address
    def createEscrow(self):
        self.holdingAddress = self.api.get_new_addresses(count=None,checksum=True)['addresses'][0]
        return self.holdingAddress

    #Waits for a transactions with a refund address
    def getRefundAddress(self):
        #This is the escrow address
        address = self.holdingAddress
        try:
            #Get Hashes from ledger
            txHashes = self.api.find_transactions(addresses=[address,])['hashes']
            #If no hashes, user has not submitted an address yet.
            if len(txHashes)==0:
                return None
            else:
                #Check messages for a valid address
                txs = self.api.get_transaction_objects(txHashes)['transactions']  
                for tx in txs:
                    msg = tx.signature_message_fragment.decode()
                    try:
                        self.deposit = Address(msg.strip())
                        return self.deposit
                    except: pass
                logging.warning("Invalid address recieved")
        except requests.exceptions.ConnectionError as e:
            #Sometimes the public nodes will reject a request
            print("Error contacting server; retrying")
            return self.getRefundAddress()

    #Cli version of escrow
    def startCli(self,collateral,fee=0,delay=120,deposit=None):
        #Create holding address
        self.createEscrow()
        #Wait for a deposit address to be entered
        if self.requestDeposit(collateral,deposit,delay):
            while not self.checkCondition():
                sleep(3)
        self.finalizeEscrow()
                
    #Wait for escrow address to recieve collateral
    def requestDeposit(self,collateral,deposit=None,duration=120):
        #For CLI prompt a deposit address
        if deposit is None:
            self.deposit = input("What is the deposit address: ")
        print(f"You have {duration/60:.1f} min to deposit {collateral} MIOTA to {self.holdingAddress}")

        #Wait for escrow to recive collateral funds.
        count = 0
        while count < duration:
            time.sleep(1)
            balance = self.getBalance(self.holdingAddress)
            if balance >= collateral:
                print("Successfully deposited into escrow",balance)
                return True
        return False

    #Condition to release escrow
    def checkCondition(self):
        #Setup a check condition
        #For example RFID or some ledger condition
        return True

    #Refund user their collateral, remoing the fee
    def finalizeEscrow(self,fee=None,deposit=None):
        if fee is None: fee=self.fee
        if deposit is None: deposit = self.deposit
        #Return money to deposit address
        returnAmount=self.getBalance(self.holdingAddress)
        
        #Calcualte return amount
        if returnAmount > 0:
            returnAmount -= fee

        #Setup transaction
        message="Repayment of collateral"
        feeLocation = self.api.get_new_addresses(count=1,checksum=True)['addresses'][0]
        txs = [
            ProposedTransaction(
                address = Address(deposit),
                value = returnAmount,
                message = TryteString.from_unicode(message)
            ),
        ]
        
        #Send transaction
        bundle = self.api.send_transfer(transfers=txs)['bundle']
        logging.info(bundle.transactions[0].hash)
        logging.info("Sent money back to recipient")
        self.addRevenue(fee)

    def getBalance(self,address):
        try:
            response = self.api.get_balances(addresses=[address])['balances']
            return response[0]
        except requests.exceptions.ConnectionError as e:
            logging.info("Error contacting server; retrying")
            return getBalance(self,address)

    #Record the amount of revenue recieved
    def addRevenue(self,money,filename='revenue.txt'):
        if not os.path.isfile(filename):
            open(filename,'w+').write('0')
        current = int(open(filename).read().strip())
        current+=money
        open(filename).write(current)

    #Get the current amount of revenue
    def getRevenue(self,filename="revenue.txt"):
        if not os.path.isfile(filename): return 0
        return int(open(filename).read().strip())

    #Send revenue to an address
    def sendRevenue(self,outputAddress):
        revenue = self.getRevenue()
        logger.info(f"Currently have {revenue} revenue.")
        message="Output fees from escrow."
        txs = [
            ProposedTransaction(
                address = Address(outputAddress),
                value = revenue,
                message = TryteString.from_unicode(message)
            ),
        ]
        try:
            logger.info("Sending transfer to node.")        
            bundle = self.api.send_transfer(transfers=txs)['bundle']
        except iota.adapter.BadApiResponse as e:
            print("Bad api resonse retrying")
            return self.sendRevenue(outputAddress)
        print(bundle.transactions[0].hash)

def createEscrow(args):
    escrow = Escrow(node=args.node)
    escrow.startCli(50,7)
    
def main():
    parser = argparse.ArgumentParser(description='Basic escrow using IOTA.')
    parser.add_argument('collateral', type=int, help='The collateral costs.')
    parser.add_argument('fee', type=int, help='Non-refundable costs.')
    parser.add_argument('--seed', type=str, help='The seed to use, does not save.')
    parser.add_argument('--node', type=str, help='The iota node to use.',default='https://nodes.thetangle.org:443')
    parser.set_defaults(func=createEscrow)
    args = parser.parse_args()
    args.func(args)

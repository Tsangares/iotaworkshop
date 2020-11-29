import requests,time,logging

#Formats data to the iot2Tangle standard
#Given a device ID and a list of data
def formatData(data,device):
    return {
        'iot2tangle': data,
        'device': device,
        'timestamp': int(time.time())
    }

#Given a series of variables for an escrow state, format the json for a POST
def getEscrowState(collateral,fee,tool,condition,escrow,deposit,available,status):
    datum =     {
        'sensor': 'escrow',
        'data': [
            {
                'status': status,
                'collateral': collateral,
                'tool': tool,
                'verification': condition,
                'fee': fee,
                'start_time': time.time(),
                'esrow_address':  escrow,
                'deposit_address':  deposit,
                'available': available
            }
        ]
    }
    return [datum,]

#Given the state of escrow format and submit to keepy to send to the channel of the device
#keepyNode is the url to the keepy node like: http://localhost:3002
def submitEscrowState(keepyNode,collateral,fee,tool,condition,escrow,deposit,available,status):
    data = getEscrowState(collateral,fee,tool,condition,escrow,deposit,available,status)
    formatted = formatData(data,'ESCROW_PI')
    endpoint = f'{keepyNode}/messages'
    r = requests.post(endpoint,json=formatted)
    logging.info(f"Submitted data to keepy {r.status_code}: {status}")
    if r.status_code != 201:
        logging.warning(r.text)
    
if __name__=="__main__":
    #Test an escrow submit
    submitEscrowState('http://192.168.1.6:3002',107,7,'lockpick','rfid','A'*81,'B'*81,False,'test')

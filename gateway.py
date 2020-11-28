import requests,time,logging

def formatData(data,device):
    return {
        'iot2tangle': data,
        'device': device,
        'timestamp': int(time.time())
    }
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

def submitEscrowState(keepyNode,collateral,fee,tool,condition,escrow,deposit,available,status):
    data = getEscrowState(collateral,fee,tool,condition,escrow,deposit,available,status)
    formatted = formatData(data,'ESCROW_PI')
    endpoint = f'{keepyNode}/messages'
    r = requests.post(endpoint,json=formatted)
    logging.info(f"Submitted data to keepy {r.status_code}: {status}")
    
if __name__=="__main__":
    #Test an escrow submit
    submitEscrowState('http://192.168.1.6:3002',107,7,'arm','rfid','A'*81,'B'*81,False,'test')

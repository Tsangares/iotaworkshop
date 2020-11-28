import requests,time,logging

def formatData(data,device):
    return {
        'iot2tangle': data,
        'device': device,
        'timestamp': int(time.time())
    }
def getEstrowState(collateral,fee,tool,condition,escrow,deposit,available):
    datum =     {
        'sensor': 'escrow',
        'data': [
            {
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

def submitEscrowState(keepyNode,collateral,fee,tool,condition,escrow,deposit,available):
    data = getEscrowState(collateral,fee,tool,condition,escrow,deposit,available)
    formatted = getData(data,'ESCROW_PI')
    r = requests.post(keepyNode,json=data)
    logging.info(f"Submitted data to keepy {r.status_code}")
    

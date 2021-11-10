from web3 import Web3
from hexbytes import HexBytes
import json
import requests

wss1 ="ws://prod-forge-us-west-2-sentry-000-public.prod.findora.org:8546"
wss2 ="ws://prod-forge-us-west-2-sentry-001-public.prod.findora.org:8546"
rpc_url="https://prod-forge.prod.findora.org:8545"
mainnet_url="https://prod-mainnet.prod.findora.org:26657/"



class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def getTransactionsAtBlockHeight(block):
    res=requests.get(mainnet_url+"block", headers={"height": block})
    return res.json()


def getGenesis():
    res=requests.get(mainnet_url+"genesis")
    return res.json()

def getProtocolStatus():
    res=requests.get(mainnet_url+"status")
    return res.json()

def getLatestBlock():
    res=requests.get(mainnet_url+"status")
    block = res.json()["result"]["sync_info"]["latest_block_height"]
    return block

def getTransactionsBetweenBlocks(block1,block2):
    res=requests.get(mainnet_url+"blockchain", headers={"minHeight": block1, "maxHeight" : block2})
    return res.json()

#print(getTransactionsAtBlockHeight("177336"))
#print(json.dumps(getProtocolStatus(),indent =4))
print(getLatestBlock())
w3 = Web3(Web3.WebsocketProvider(wss1))

latest =w3.eth.get_block('latest')
block =w3.eth.block_number

latest_dict = dict(latest)
#print(json.dumps(latest_dict,cls= HexJsonEncoder))
#print(json.dumps(w3.toJSON(latest), indent =4))

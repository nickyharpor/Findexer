from web3 import Web3
from pprint import pprint

from conf import Config
from es import Elastic
from indexer import Indexer
from findora import Findora


def print_recent_blocks(num):
    w3 = Web3(Web3.WebsocketProvider(Config.forge_wss1))
    last = w3.eth.block_number
    first = last - num
    num_iterator = first
    while num_iterator <= last:
        block_info = w3.eth.get_block(num_iterator, full_transactions=True)
        pprint(w3.toJSON(block_info))
        num_iterator += 1


def print_blocks(first, last):
    w3 = Web3(Web3.HTTPProvider(Config.forge_web3))
    num_iterator = first
    while num_iterator <= last:
        block_info = w3.eth.get_block(num_iterator, full_transactions=True)
        print(w3.toJSON(block_info))
        num_iterator += 1


test = ['x', 2, None, 'good']
print(' '.join(str(i) for i in test))

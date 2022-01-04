from findora import Findora
from conf import Config
from es import Elastic


class Indexer:

    def __init__(self, index_base, network='mainnet'):
        self.es_utxo = Elastic(index_base + '_utxo')
        self.es_web3 = Elastic(index_base + '_web3')
        self.es_flat = Elastic(index_base + '_flat')
        self.es_tx = Elastic(index_base + '_tx')
        self.network = network
        if network == 'mainnet':
            self.findora = Findora(Config.mainnet_utxo, Config.mainnet_web3, network=network)
        elif network == 'testnet':
            self.findora = Findora(Config.testnet_utxo, Config.testnet_web3, network=network)
        else:
            self.findora = Findora(Config.forge_utxo, Config.forge_web3, network=network)

    def index_utxo_block(self, block):
        self.es_utxo.index(block, block['result']['block']['header']['height'])

    def index_utxo_num(self, num):
        self.es_utxo.index(self.findora.get_utxo_block(num), num)

    def index_utxo_from(self, num):
        current_height = self.findora.get_height()
        for i in range(num, current_height):
            self.index_utxo_num(i)

    def index_web3_block(self, block):
        self.es_web3.index(block, block['number'])

    def index_web3_num(self, num):
        self.es_web3.index(self.findora.get_web3_block(num), num)

    def index_web3_from(self, num):
        current_height = self.findora.get_height()
        for i in range(num, current_height):
            self.index_web3_num(i)

    def index_flat_block(self, block):
        self.es_flat.index(block, block['utxo_block_height'])

    def index_flat_num(self, num):
        utxo = self.findora.get_utxo_block(num)
        web3 = self.findora.get_web3_block(num)
        self.es_flat.index(self.findora.get_flat(utxo, web3), num)

    def index_flat_from(self, num):
        current_height = self.findora.get_height()
        for i in range(num, current_height):
            self.index_flat_num(i)

    def index_tx_block(self, web3_block):
        transactions = Findora.get_transactions(web3_block)
        for tx in transactions:
            self.es_tx.index(tx, tx['hash'])

    def index_tx_num(self, num):
        transactions = Findora.get_transactions(self.findora.get_web3_block(num))
        for tx in transactions:
            self.es_tx.index(tx, tx['hash'])

    def index_tx_from(self, num):
        current_height = self.findora.get_height()
        for i in range(num, current_height):
            self.index_tx_num(i)

    def index_all_num(self, num):
        utxo = self.findora.get_utxo_block(num)
        web3 = self.findora.get_web3_block(num)
        flat = self.findora.get_flat(utxo, web3)
        self.index_utxo_block(utxo)
        if self.network != 'mainnet':
            self.index_web3_block(web3)
            self.index_tx_block(web3)
        self.index_flat_block(flat)

    def index_all_from(self, num):
        current_height = self.findora.get_height()
        for i in list(range(num, current_height)):
            self.index_all_num(i)
            print('indexed block #' + str(i))

    def get_last_indexed_block_height(self):
        utxo = self.es_utxo.get_utxo_last_indexed()
        flat = self.es_flat.get_flat_last_indexed()
        web3 = self.es_web3.get_web3_last_indexed()
        return min(utxo, web3, flat)

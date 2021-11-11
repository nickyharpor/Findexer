from findora import Findora
from conf import Config
from es import Elastic


class Indexer:

    def __init__(self, index_name, network='mainnet'):
        self.es = Elastic(index_name)
        if network == 'mainnet':
            self.findora = Findora(Config.mainnet_rest)
        elif network == 'testnet':
            self.findora = Findora(Config.testnet_rest)
        else:
            self.findora = Findora(Config.forge_rest)

    # returns a json representation of block #num
    def __get_a_block(self, num):
        return self.findora.get_rest_block(num)

    # indexes a single block #num
    def index_a_block(self, num):
        self.es.index(self.__get_a_block(num), num)

    # indexes all blocks from block #num to current block
    def index_from(self, num):
        current_height = self.findora.get_height()
        for i in range(num, current_height):
            self.index_a_block(i)
            print(i)


from findora import Findora
from conf import Config
import pprint

findora = Findora(Config.forge_utxo, Config.forge_web3)
pprint.pprint(findora.get_web3_block(8238))

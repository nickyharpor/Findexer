import requests
from web3 import Web3
from hexbytes import HexBytes
from datetime import datetime


class Findora:

    def __init__(self, utxo_url, web3_url, network):
        self.utxo_url = utxo_url
        self.web3_url = web3_url
        self.network = network
        self.w3 = Web3(Web3.HTTPProvider(self.web3_url))

    def get_utxo_block(self, num):
        print('getting UTXO block #' + str(num) + ' for ' + self.network)
        block = requests.get(self.utxo_url + '/block?height=' + str(num)).json()
        block['result']['block']['header']['height'] = int(block['result']['block']['header']['height'])
        return dict(block)

    def get_web3_block(self, num):
        print('getting EVM block #' + str(num) + ' for ' + self.network)
        block_info = self.w3.eth.get_block(num, full_transactions=True)
        block = dict(block_info)
        for key, value in block.items():
            if isinstance(value, HexBytes):
                block[key] = value.hex()
        timestamp = datetime.fromtimestamp(block.get('timestamp')).strftime('%Y-%m-%dT%H:%M:%S%z')
        block['timestamp'] = timestamp
        if block['transactions']:
            transactions = []
            for transaction in block.get('transactions'):
                tx = dict(transaction)
                for key, value in tx.items():
                    if isinstance(value, HexBytes):
                        tx[key] = value.hex()
                tx['timestamp'] = timestamp
                tx['valueStr'] = str(tx['value'])
                tx['value'] = float(tx['value'])
                transactions.append(tx)
            block['transactions'] = transactions
        return block

    def get_status(self):
        res = requests.get(self.utxo_url + '/status')
        return res.json()

    def get_height(self):
        res = requests.get(self.utxo_url + '/status')
        block = res.json()['result']['sync_info']['latest_block_height']
        return int(block)

    @staticmethod
    def flatten_utxo_block(block):
        utxo_aio = ''
        txs = block['result']['block']['data']['txs']
        if txs is not None:
            for tx in txs:
                utxo_aio += str(tx) + ' '
        sig_aio = ''
        signatures = block['result']['block']['last_commit']['signatures']
        if signatures is not None:
            for sig in signatures:
                sig_aio += str(sig['block_id_flag']) + ' ' + \
                           str(sig['validator_address']) + ' ' + \
                           str(sig['timestamp']) + ' ' + \
                           str(sig['signature']) + ' '
        flat_doc = {
            'utxo_jsonrpc': block['jsonrpc'],
            'utxo_id': block['id'],
            'utxo_block_hash': block['result']['block_id']['hash'],
            'utxo_block_parts_total': block['result']['block_id']['parts']['total'],
            'utxo_block_parts_hash': block['result']['block_id']['parts']['hash'],
            'utxo_block_version_block': block['result']['block']['header']['version']['block'],
            'utxo_block_version_app': block['result']['block']['header']['version']['app'],
            'utxo_block_chain_id': block['result']['block']['header']['chain_id'],
            'utxo_block_height': block['result']['block']['header']['height'],
            'utxo_block_time': block['result']['block']['header']['time'],
            'utxo_last_block_hash': block['result']['block']['header']['last_block_id']['hash'],
            'utxo_last_block_parts_total': block['result']['block']['header']['last_block_id']['parts']['total'],
            'utxo_last_block_parts_hash': block['result']['block']['header']['last_block_id']['parts']['hash'],
            'utxo_last_commit_hash': block['result']['block']['header']['last_commit_hash'],
            'utxo_data_hash': block['result']['block']['header']['data_hash'],
            'utxo_validators_hash': block['result']['block']['header']['validators_hash'],
            'utxo_next_validators_hash': block['result']['block']['header']['next_validators_hash'],
            'utxo_consensus_hash': block['result']['block']['header']['consensus_hash'],
            'utxo_app_hash': block['result']['block']['header']['app_hash'],
            'utxo_last_results_hash': block['result']['block']['header']['last_results_hash'],
            'utxo_evidence_hash': block['result']['block']['header']['evidence_hash'],
            'utxo_proposer_address': block['result']['block']['header']['proposer_address'],
            'utxo_data': utxo_aio.strip(),
            'utxo_evidence': block['result']['block']['evidence']['evidence'],
            'utxo_last_commit_height': block['result']['block']['last_commit']['height'],
            'utxo_last_commit_round': block['result']['block']['last_commit']['round'],
            'utxo_last_commit_block_hash': block['result']['block']['last_commit']['block_id']['hash'],  # dup
            'utxo_last_commit_block_parts_total': block['result']['block']['last_commit']['block_id']['parts']['total'],  # dup
            'utxo_last_commit_block_parts_hash': block['result']['block']['last_commit']['block_id']['parts']['hash'],  # dup
            'utxo_last_commit_signatures': sig_aio.strip()
        }
        return flat_doc

    @staticmethod
    def flatten_web3_block(block):
        if block is None:
            return dict({})
        seal_aio = ''
        for seal in block['sealFields']:
            seal_aio += seal + ' '
        tx_aio = ''
        for tx in block['transactions']:
            tx_copy = tx.copy()
            tx_copy.pop('timestamp')
            tx_aio += ' '.join(str(i) for i in list(tx_copy.values())) + ' '
        flat_doc = {
            'web3_author': block['author'],
            'web3_difficulty': block['difficulty'],
            'web3_extra_data': block['extraData'],
            'web3_gas_limit': block['gasLimit'],
            'web3_gas_used': block['gasUsed'],
            'web3_hash': block['hash'],
            'web3_logs_bloom': block['logsBloom'],
            'web3_miner': block['miner'],
            'web3_number': block['number'],
            'web3_parent_hash': block['parentHash'],
            'web3_receipts_root': block['receiptsRoot'],
            'web3_seal_fields': seal_aio.strip(),
            'web3_sha3_uncles': block['sha3Uncles'],
            'web3_size': block['size'],
            'web3_state_root': block['stateRoot'],
            'web3_timestamp': block['timestamp'],
            'web3_total_difficulty': block['totalDifficulty'],
            'web3_transactions': tx_aio.strip(),
            'web3_transactions_root': block['transactionsRoot'],
            'web3_uncles': block['uncles']
        }
        return flat_doc

    @staticmethod
    def get_flat(utxo_block, web3_block):
        flat_utxo = Findora.flatten_utxo_block(dict(utxo_block))
        if web3_block:
            flat_web3 = Findora.flatten_web3_block(dict(web3_block))
            flat = {**flat_utxo, **flat_web3}
        else:
            flat = flat_utxo
        flat_aio = ''
        flat_aio += ' '.join(str(i) for i in list(flat.values())) + ' '
        flat['aio'] = flat_aio.strip()
        return flat

    @staticmethod
    def get_transactions(web3_block):
        return web3_block['transactions']

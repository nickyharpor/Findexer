from web3 import Web3

wss1 ="ws://prod-forge-us-west-2-sentry-000-public.prod.findora.org:8546"
wss2 ="ws://prod-forge-us-west-2-sentry-001-public.prod.findora.org:8546"
rpc_url="https://prod-forge.prod.findora.org:8545"

w3 = Web3(Web3.WebsocketProvider(wss1))

latest =w3.eth.get_block('latest')
block =w3.eth.block_number
print(block)
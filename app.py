import traceback
from flask import Flask, request
from flask_apscheduler import APScheduler
from indexer import Indexer
from conf import Config
from searcher import Searcher

mainnet_indexer = Indexer(Config.mainnet_name)
forge_indexer = Indexer(Config.forge_name, network='forge')
testnet_indexer = Indexer(Config.testnet_name, network='testnet')

s = {
    'mainnet': Searcher(Config.mainnet_name),
    'forge': Searcher(Config.forge_name),
    'testnet': Searcher(Config.testnet_name)
}

app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


def get_param(param, default=None):
    if request.method == 'POST':
        return request.form.get(param, default=default)
    elif request.method == 'GET':
        return request.args.get(param, default=default)
    else:
        return default


@scheduler.task('cron', id='do_sync_mainnet', minute='*')
def sync_mainnet():
    try:
        indexed_height = mainnet_indexer.get_last_indexed_block_height()
        mainnet_indexer.index_all_from(indexed_height + 1)
    except:
        traceback.print_exc()


@scheduler.task('cron', id='do_sync_forge', minute='*')
def sync_forge():
    try:
        indexed_height = forge_indexer.get_last_indexed_block_height()
        forge_indexer.index_all_from(indexed_height + 1)
    except:
        traceback.print_exc()


@scheduler.task('cron', id='do_sync_testnet', minute='*')
def sync_testnet():
    try:
        indexed_height = testnet_indexer.get_last_indexed_block_height()
        testnet_indexer.index_all_from(indexed_height + 1)
    except:
        traceback.print_exc()


@app.route('/')
def index():
    return {
        'version': Config.version
    }


@app.route('/status')
def status():
    return {
        'version': Config.version,
        'mainnet_last_indexed_block': mainnet_indexer.get_last_indexed_block_height(),
        'forge_last_indexed_block': forge_indexer.get_last_indexed_block_height(),
        'testnet_last_indexed_block': testnet_indexer.get_last_indexed_block_height()
    }


@app.route('/sql', methods=['GET', 'POST'])
def sql():
    network = get_param('network', 'mainnet')
    query = get_param('query')
    if query.endswith(';'):
        query = query[:-1]
    res = s[network].sql(query)
    return {
        'version': Config.version,
        'response': res
    }


@app.route('/aio_search', methods=['GET', 'POST'])
def aio_search():
    network = get_param('network', 'mainnet')
    return {
        'version': Config.version
    }


if __name__ == '__main__':
    app.run()

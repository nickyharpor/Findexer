import traceback
from flask import Flask
from flask_apscheduler import APScheduler
from indexer import Indexer
from conf import Config

forge_indexer = Indexer('forge', network='forge')
app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', id='do_sync_forge', minute='*')
def sync_forge():
    try:
        indexed_height = forge_indexer.get_last_indexed_block_height()
        forge_indexer.index_all_from(indexed_height + 1)
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
        'forge_last_indexed_block': forge_indexer.get_last_indexed_block_height()
    }


@app.route('/aio_search')
def aio_search():
    return {
        'version': Config.version
    }


if __name__ == '__main__':
    app.run()

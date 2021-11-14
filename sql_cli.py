from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient
import argparse
import traceback
import logging

logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)

parser = argparse.ArgumentParser(description='Findora SQL CLI', add_help=False)
parser.add_argument('--host', '-h', required=False, default='localhost', type=str,
                    help='Elasticsearch host name. Default: localhost')
parser.add_argument('--port', '-p', required=False, default=9200, type=int,
                    help='Elasticsearch port. Default: 9200')
parser.add_argument('--help', action='help')
args = parser.parse_args()

es = Elasticsearch(hosts=[{'host': args.host, 'port': args.port}])
ic = IndicesClient(es)
flat = ic.get_alias(index='*_flat').keys()
tx = ic.get_alias(index='*_tx').keys()
print('Connected to ' + args.host + ':' + str(args.port) + '. Type exit() to get out.\n')
print('Available block tables: ' + ''.join(list(flat)))
print('Available transaction tables: ' + ''.join(list(tx)))
print()

while True:
    print('> ', end='')
    s = input().strip().strip(';')
    if s == 'exit' or s == 'exit()':
        break
    else:
        try:
            print(es.sql.query(body={'query': s}, format='txt'))
        except:
            traceback.print_exc()


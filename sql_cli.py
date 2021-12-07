from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient
import argparse
import traceback
import cmd2
from cmd2 import style
from conf import Config


class CLI(cmd2.Cmd):

    def __init__(self, args):
        super().__init__(multiline_commands=['select', 'SELECT', 'Select'])
        self.es = Elasticsearch(hosts=[{'host': args.host, 'port': args.port}])
        ic = IndicesClient(self.es)
        flat = ic.get_alias(index='*_flat').keys()
        tx = ic.get_alias(index='*_tx').keys()
        self.intro = style('Findexer SQL CLI\n\n'
                           'Connected to ' + args.host + ':' + str(args.port) + '. Type quit to exit.\n\n'
                           'Available block tables: ' + ', '.join(list(flat)) + '\n'
                           'Available transaction tables: ' + ', '.join(list(tx)) + '\n', bold=True)
        self.locals_in_py = True

    def do_SELECT(self, arg):
        try:
            self.poutput(self.es.sql.query(body={'query': 'select ' + arg}, format='txt'))
        except:
            traceback.print_exc()

    def do_select(self, arg):
        self.do_SELECT(arg)

    def do_Select(self, arg):
        self.do_SELECT(arg)

    def do_DESC(self, arg):
        try:
            self.poutput(self.es.sql.query(body={'query': 'desc ' + arg}, format='txt'))
        except:
            traceback.print_exc()

    def do_desc(self, arg):
        self.do_DESC(arg)

    def do_Desc(self, arg):
        self.do_DESC(arg)

    def do_DESCRIBE(self, arg):
        self.do_DESC(arg)

    def do_describe(self, arg):
        self.do_DESC(arg)

    def do_Describe(self, arg):
        self.do_DESC(arg)

    def do_SHOW(self, arg):
        try:
            self.poutput(self.es.sql.query(body={'query': 'show ' + arg}, format='txt'))
        except:
            traceback.print_exc()

    def do_show(self, arg):
        self.do_SHOW(arg)

    def do_Show(self, arg):
        self.do_SHOW(arg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Findora SQL CLI', add_help=False)
    parser.add_argument('--host', '-h', required=False, default=Config.es_host, type=str,
                        help='Elasticsearch host name. Default: ' + Config.es_host)
    parser.add_argument('--port', '-p', required=False, default=Config.es_port, type=int,
                        help='Elasticsearch port. Default: ' + str(Config.es_port))
    parser.add_argument('--help', action='help')
    args = parser.parse_args()
    app = CLI(args)
    app.cmdloop()


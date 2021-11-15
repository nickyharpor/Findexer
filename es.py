from elasticsearch import Elasticsearch


class Elastic:

    def __init__(self, index_name):
        self.es = Elasticsearch(timeout=360)
        self.index_name = index_name

    def create(self, index_name, settings):
        self.es.indices.create(index=index_name, body=settings)

    def exists(self, index_name):
        return self.es.indices.exists(index=index_name)

    def list(self, alias):
        return self.es.indices.get_alias(index=alias).keys()

    def index(self, body, id):
        self.es.index(index=self.index_name,
                      document=body,
                      id=id)

    def index_auto(self, body):
        self.es.index(index=self.index_name,
                      document=body)

    def update(self, body, id):
        self.es.update(index=self.index_name,
                       body=body,
                       id=id)

    def update_wait_for(self, body, id):
        self.es.update(index=self.index_name,
                       body=body,
                       id=id,
                       refresh='wait_for')

    def get_by_id(self, id):
        return self.es.get(index=self.index_name, id=id)

    def sql(self, query, format='json'): # supported formats: json, yaml, txt
        return self.es.sql.query(body={'query': query}, format=format)

    def get_utxo_last_indexed(self):
        body = {
            "aggs": {
                "max_id": {"max": {"field": "result.block.height"}}
            },
            "size": 0
        }
        try:
            res = self.es.search(index=self.index_name, body=body)
            return int(res["aggregations"]["max_id"]["value"])
        except:
            return 0

    def get_web3_last_indexed(self):
        body = {
            "aggs": {
                "max_id": {"max": {"field": "number"}}
            },
            "size": 0
        }
        try:
            res = self.es.search(index=self.index_name, body=body)
            return int(res["aggregations"]["max_id"]["value"])
        except:
            return 0

    def get_flat_last_indexed(self):
        body = {
            "aggs": {
                "max_id": {"max": {"field": "web3_number"}}
            },
            "size": 0
        }
        try:
            res = self.es.search(index=self.index_name, body=body)
            return int(res["aggregations"]["max_id"]["value"])
        except:
            return 0

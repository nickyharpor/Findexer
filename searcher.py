from elasticsearch import Elasticsearch


class Searcher:

    def __init__(self, index_prefix):
        self.index_prefix = index_prefix
        self.es = Elasticsearch(timeout=360)

    def sql(self, query):
        query = query.lower().strip()
        if query.startswith('select') or query.startswith('desc') or query.startswith('show'):
            return self.es.sql.query(body={'query': query}, format='json')
        else:
            return {}

    def aio_search(self, query, size, start):
        body = {
            "track_total_hits": 10000,
            "query": {
                "query_string": {
                    "query": query,
                    "default_field": "aio"
                }
            },
            "size": size,
            "from": start
        }
        return self.es.search(index=self.index_prefix + '_flat', body=body)

    def get_by_height(self, height, index):
        if index == 'flat':
            field = 'utxo_block_height'
        elif index == 'utxo':
            field = 'result.block.header.height'
        elif index == 'web3':
            field = 'number'
        else:
            return {}
        body = {
            "query": {
                "bool": {
                    "must": {
                        "match_all": {}
                    },
                    "filter": {
                        "term": {
                            field: {
                                "value": height
                            }
                        }
                    }
                }
            }
        }
        return self.es.search(index=self.index_prefix + '_' + index, body=body)

    def evm_tx_by_hash(self, tx_hash):
        return self.es.get(index=self.index_prefix + '_tx', id=tx_hash)

    def utxo_by_proposer(self, proposer, size, start):
        body = {
            "query": {
                "bool": {
                    "must": {
                        "match_all": {}
                    },
                    "filter": {
                        "term": {
                            "result.block.proposer_address.keyword": {
                                "value": proposer
                            }
                        }
                    }
                }
            },
            "size": size,
            "from": start
        }
        return self.es.search(index=self.index_prefix + '_utxo', body=body)

    def top_proposers(self, num):
        body = {
            "track_total_hits": 10000,
            "query": {
                "match_all": {}
            },
            "size": 0,
            "aggs": {
                "group_by_shabka": {
                    "terms": {
                        "field": "result.block.proposer_address.keyword",
                        "size": num
                    }
                }
            }
        }
        return self.es.search(index=self.index_prefix + '_utxo', body=body)

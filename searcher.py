from es import Elastic


class Searcher:

    def __init__(self, index_name):
        self.index_name = index_name
        self.s = Elastic(index_name)

    def sql(self, query):
        return self.s.sql(query)

from elasticsearch import Elasticsearch
es = Elasticsearch

class Elastic():
    def __init__(self, index, doc=None):
        self.index = index
        self.doc = doc

    def insert(self, **kwargs):
        es.create(
            self.index,
            kwargs.get('id'),
            kwargs.get('body'),
            kwargs.get('doc_type'),
            True
        )

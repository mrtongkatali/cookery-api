import logging
from elasticsearch import Elasticsearch, RequestError, helpers

from common.schema import DishSchema

class Elastic():
    def __init__(self, index, doc=None):
        self.index = index
        self.doc = doc

        self.es = Elasticsearch([
            {"host": "localhost", "port": "9200"}
        ])

    def search_data(self, **kwargs):
        try:
            logging.debug(f"[info] searching indexed data => {kwargs}")
            res = self.es.search(index=self.index, body=kwargs.get('body'))

            return res
        except Exception as e:
            logging.debug(f"[err] searching indexed data => {kwargs}, {e}")
        # logging.debug(f"[info] searching indexed data => {kwargs.get('body')}")
        # res = self.es.search(index=self.index, body=kwargs.get('body'))
        # return res

    def create(self, **kwargs):
        logging.debug(f"[info] Indexed a document => {self.index}, {self.doc}, {kwargs.get('id')}, {kwargs.get('body')}")
        self.es.create(
            index=self.index,
            id=kwargs.get('id'),
            body=kwargs.get('body'),
            doc_type=self.doc,
            refresh=True
        )

        return

    def index_document(self, **kwargs):
        logging.debug(f"[info] re-indexing the document => {self.index}, {self.doc}, {kwargs.get('id')}, {kwargs.get('body')}")
        self.es.index(
            index=self.index,
            body=kwargs.get('body'),
            id=kwargs.get('id'),
            doc_type=self.doc,
            refresh=True
        )

        return

    def bulk_index(self, **kwargs):
        try:
            def generate_data():
                for dish in kwargs.get('body'):
                    logging.debug(f"[info] bulk_indexing => {dish.id}")
                    yield {
                        "_index": 'cookery-dish',
                        "_id": dish.id,
                        "_source": DishSchema().dump(dish)
                    }

            helpers.bulk(self.es, generate_data())

            return
        except Exception as e:
            logging.debug(f"[err] bulk_index :: {e}")

# Sync to es
# body = {'instruction': [], 'prep_minute': 10, 'ingredients': [], 'id': 1593, 'serving_count': 4, 'updated_at': '2021-01-05T14:03:30', 'description': None, 'course': 1, 'cuisine': 1, 'main_dish': 11, 'prep_hour': 0, 'cook_hour': 3, 'dish_name': 'Bulalo Kare-Kare na may halong Dulang sa Garapon', 'status': 1, 'created_at': '2021-01-05T14:02:47', 'cook_minute': 10}
# es = Elastic('cookery-dish')
# es.index_document(id=1593, body=body, refresh=True)

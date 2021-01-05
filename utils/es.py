import logging
from elasticsearch import Elasticsearch, RequestError

class Elastic():
    def __init__(self, index, doc=None):
        logging.debug(f"[err] ################# HEYYYYY DEBUG!!! => {index}")
        self.index = index
        self.doc = doc

        try:
            self.es = Elasticsearch([
                {"host": "localhost", "port": "9200"}
            ])

            self.init_dish_index()
        except RequestError as error:
            logging.debug(f"[err] ################# HEYYYYY Elastic!!! => {error}")

    def init_dish_index(self):
        try:
            self.es.indices.create(index=self.index, ignore=400)

            mapping = {
                "settings": {
                  "number_of_shards": 3,
                  "number_of_replicas": 2
                },
                "mappings": {
                  "properties": {
                    "dish_id": { "type": "integer" },
                    "user_id": { "type": "integer" },
                    "main_dish": { "type": "integer" },
                    "dish_name": { "type": "text" },
                    "course_id": { "type": "integer" },
                    "course": { "type": "keyword" },
                    "cuisine": { "type": "keyword" },
                    "serving_pax": { "type": "integer" },
                    "prep_hour": { "type": "integer" },
                    "prep_minute": { "type": "integer" },
                    "cook_hour": { "type": "integer" },
                    "cook_minute": { "type": "integer" },
                    "dish_kw": { "type": "text" },
                    "nutrition": { "type": "nested" },
                    "ingredients": { "type": "nested" },
                    "instruction": { "type": "nested" },
                    "status": { "type": "integer" }
                  }
                }
            }

            es.indices.put_mapping(index=self.index,body=mapping)
        except RequestError as error:
            logging.debug(f"[err] ################# HEYYYYY REQUEST!!! => {error}")
            sys.exit(1)

    def create(self, **kwargs):
        pass
        # self.es.indices.create(index=self.index, ignore=[400])
        # self.es.create(
        #     self.index,
        #     kwargs.get('id'),
        #     kwargs.get('body'),
        #     doc_type=self.doc,
        #     params=None,
        #     headers=None
        # )

# body = {
#     "dish_id": 1,
#     "user_id": 1,
#     "main_dish": 1,
#     "dish_name": "Every good boy does payb",
#     "course_id": "1",
#     "course": "1",
#     "cuisine": "1",
#     "serving_pax": "1",
#     "prep_hour": "1",
#     "prep_minute": "1",
#     "dish_kw": "Apple Cider Lemon Zest Maple Syrup Sriracha",
#     "nutrition": [],
#     "ingredients": [
#         {"amount":"1","unit":"bunch","ingredient_name":"Apple Cider","additional_note":"Test","dish_id":"1513"},
#         {"amount":"1","unit":"bunch","ingredient_name":"Lemon Zest","additional_note":"Test","dish_id":"1513"},
#         {"amount":"1","unit":"bunch","ingredient_name":"Maple Syrup","additional_note":"Test","dish_id":"1513"},
#         {"amount":"1","unit":"bunch","ingredient_name":"Sriracha","additional_note":"Test","dish_id":"1513"}
#     ],
#     "instruction": [],
#     "status": "1"
# }
#
# # Sync to es
# es = Elastic('cookery-dish')
# es.create(id=1, body=body, refresh=True)

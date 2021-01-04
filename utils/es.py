from elasticsearch import Elasticsearch

class Elastic():
    def __init__(self, index, doc=None):
        self.index = index
        self.doc = doc

        self.es = Elasticsearch([
            {"host": "localhost", "port": "9200"},
        ])

    def create(self, **kwargs):
        self.es.indices.create(index=self.index, ignore=[400])
        self.es.create(
            self.index,
            kwargs.get('id'),
            kwargs.get('body'),
            doc_type=self.doc,
            params=None,
            headers=None
        )

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

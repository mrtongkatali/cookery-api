from utils.es import Elastic

class ReIndexAPI(Resource):
    def post(self):
        es = Elastic("cookery-dish")
        pass

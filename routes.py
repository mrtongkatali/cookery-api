from resources.user_auth import *
from resources.dishes import *
from resources.data_import import *

def initialize_routes(api):
    api.add_resource(UserSignUp, '/v1/user/sign-up',)
    api.add_resource(UserAuth, '/v1/user/auth',)
    api.add_resource(Dishes, '/v1/dishes',)
    api.add_resource(DishImport, '/v1/dish/import',)

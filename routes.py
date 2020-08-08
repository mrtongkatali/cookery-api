from resources.user_auth import *
from resources.dishes import *
from resources.ingredients import *
from resources.data_import import *

def initialize_routes(api):
    api.add_resource(UserSignUpResource, '/v1/user/sign-up',)
    api.add_resource(UserAuthResource, '/v1/user/auth',)
    api.add_resource(DishesResource,'/v1/dishes',)
    api.add_resource(DishResource,
        '/v1/dish/new',
        '/v1/dish/update/<int:dish_id>',
        '/v1/dish/<int:dish_id>',
    )
    api.add_resource(IngredientResource,
        '/v1/ingredient/new',
        '/v1/ingredient/update/<int:ingr_id>',
        '/v1/ingredient/<int:ingr_id>',
    )
    api.add_resource(DishImport, '/v1/dish/import',)

    # api.add_resource(TodoSimple,
    # #     '/todo/<string:todo_id>',
    # #     '/todo'
    # # ) cookery-api.crazyapp.cloud/v2/

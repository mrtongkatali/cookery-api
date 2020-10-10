from resources.user_auth import *
from resources.dishes import *
from resources.ingredients import *
from resources.data_import import *

def initialize_routes(api):
    api.add_resource(HelloWorldResource, '/hello',)
    api.add_resource(UserSignUpResource, '/v1/user/sign-up',)
    api.add_resource(UserAuthResource, '/v1/user/auth',)
    api.add_resource(DishesResource,'/v1/dish/list',)
    api.add_resource(DishResource,
        '/v1/dish/new',
        '/v1/dish/update/<int:dish_id>',
        '/v1/dish/<int:dish_id>',
    )
    api.add_resource(IngredientResource,
        '/v1/ingredients/new',
        '/v1/ingredients/update/<int:ingr_id>',
        '/v1/ingredients/<int:ingr_id>',
    )
    api.add_resource(DishImport, '/v1/dishes/import',)

    # api.add_resource(TodoSimple,
    # #     '/todo/<string:todo_id>',
    # #     '/todo'
    # # ) cookery-api.crazyapp.cloud/v2/

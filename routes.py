from resources.user_auth import *
from resources.dishes import *
from resources.ingredients import *
from resources.data_import import *

def initialize_routes(api):
    api.add_resource(UserSignUpResource, '/v1/user/sign-up',)
    api.add_resource(UserAuthResource, '/v1/user/auth',)
    api.add_resource(DishesResource,'/v1/dishes',)
    api.add_resource(DishResource,
        '/v1/dishes/new',
        '/v1/dishes/update/<int:dish_id>',
        '/v1/dishes/<int:dish_id>',
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

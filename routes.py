from resources.user_auth import *
from resources.dishes import *
from resources.ingredients import *
from resources.prep_instructions import *
from resources.data_import import *
from resources.misc import *

def register_routes(api):
    # Test URL
    api.add_resource(HelloWorldAPI, '/hello',)

    # User Auth
    api.add_resource(UserSignUpAPI, '/v1/user/sign-up',)
    api.add_resource(UserAuthAPI, '/v1/user/auth',)

    # Dish
    api.add_resource(DishesElasticAPI, '/v1/dish/search')
    api.add_resource(DishesAPI,'/v1/dish/list',)
    api.add_resource(DishAPI,
        '/v1/dish/new',
        '/v1/dish/update/<int:dish_id>',
        '/v1/dish/<int:dish_id>',
    )
    api.add_resource(RemoveDishAPI,
        '/v1/dish/remove/<int:dish_id>',
    )

    # Ingredient
    api.add_resource(IngredientAPI,
        '/v1/ingredients/new',
        '/v1/ingredients/update/<int:ingr_id>',
        '/v1/ingredients/<int:ingr_id>'
    )
    api.add_resource(RemoveIngredientAPI,
        '/v1/ingredients/remove/<int:ingr_id>',
    )

    # PreparationInstruction
    api.add_resource(PrepInstructionAPI,
        '/v1/instructions/new',
        '/v1/instructions/update/<int:instr_id>',
        '/v1/instructions/<int:instr_id>',
    )
    api.add_resource(RemoveInstructionAPI,
        '/v1/instructions/remove/<int:instr_id>',
    )

    # Utils
    api.add_resource(DishImport, '/v1/dishes/import',)
    api.add_resource(ReIndexAPI, '/v1/es/_reindex',)
    api.add_resource(SyncESKewordsAPI, '/v1/es/_update_keywords',)

    # api.add_resource(TodoSimple,
    # #     '/todo/<string:todo_id>',
    # #     '/todo'
    # # ) cookery-api.crazyapp.cloud/v2/

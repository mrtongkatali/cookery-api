data = "onions, sugar, cameltoe"

obj = list(map(
    lambda data: {"ingredients.ingredient_name": data}, data.split(", ")
))
# queries = { "match": { "ingredients.ingredient_name" : value for value in data.split(", ") } }
# print(queries)

must = []
for v in data.split(", "):
    must.append({ "match": { "ingredients.ingredient_name": v }})

print(must)
#
# number = {
#     1: 1,
#     2: 2,
#     3: 3,
#     4: 4,
#     5: 5
# }
#
# dict_compre2 = { key: (value if value % 2 == 0 else "odddds") for key, value in number.items() }
# print(f"\n{dict_compre2}")

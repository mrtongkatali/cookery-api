import requests

url = "http://cookery-dev-api.crazyapp.cloud:9090/v1/es/_reindex"
res = requests.post(url)

print(res)

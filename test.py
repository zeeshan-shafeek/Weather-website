# import urllib library
from urllib.request import urlopen

# import json
import json

# store the URL in url as
# parameter for urlopen
url = "https://bulk.openweathermap.org/sample/city.list.json.gz"

# store the response of URL
print(urlopen(url))

# # storing the JSON response
# # from url in data
# data_json = json.loads(response.read())
#
# # print the json response
# print(data_json)
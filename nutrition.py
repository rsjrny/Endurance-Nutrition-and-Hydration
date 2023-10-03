import http.client
import json
import requests
import pprint
from nutritionix_api import NutritionixAPI, NutrientCalculator
import constants
# conn = http.client.HTTPSConnection("trackapi.nutritionix.com")

# Load API keys from .env file
# app_id = os.getenv('NUTRITIONIX_APP_ID')
# app_key = os.getenv('NUTRITIONIX_APP_KEY')

# Initialize the Nutritionix_api client
nutritionix_api = NutritionixAPI(app_id=app_id, app_key=app_key)
nutrient_calculator = NutrientCalculator()



# aggregated_nutrients = nutrient_calculator.aggregate_nutrients(response)
# caloric_content_info = nutrient_calculator.calculate_calorie_content_me(aggregated_nutrients)
# protein_me = caloric_content_info['protein_me']
# fat_me = caloric_content_info['fat_me']
# carbohydrate_me = caloric_content_info['carbohydrate_me']
# print(protein_me, fat_me, caloric_content_info, carbohydrate_me)

# URL = 'https://trackapi.nutritionix.com/v2/'
#
# def query_search_item(nix_id):
#     # works
#     print("query_search_item")
#     url = URL+"natural/nutrients"
#     headers = {
#         'x-app-id': 'e6541bf3',
#         'x-app-key': '2848dfdacf3be363a7835fffd9aaf72a',
#         "Content-Type": "application/json",
#     }
#
#     params = {
#         "query": nix_id,
#         "timezone": "US/Eastern"
#
#     }
#
#     response = requests.post(url, headers=headers, json=params)
#     data = json.loads(response.text)
#
#     return data
#
#
# def query_search_item_by_nix(nix_id):
#     # works
#     print('query_search_item_by_nix')
#     url = URL+"search/item"
#     headers = {
#         'x-app-id': 'e6541bf3',
#         'x-app-key': '2848dfdacf3be363a7835fffd9aaf72a',
#         "Content-Type": "application/json",
#     }
#
#     params = {
#         "nix_item_id": nix_id,
#
#     }
#
#     response = requests.get(url, headers=headers, params=params)
#     print(response.text)
#     jdata = json.loads(response.text)
#     pprint.pprint(jdata)
#     retdata = "calories = " + str(jdata.get("nf_calories")) + "  sodium = " + str(jdata.get("nf_sodium"))
#     print(retdata)
#     return retdata
#
#
#
# def query_search_nutrients(food):
#     # works
#     # application/json
#     print('query_search_nutrients')
#     url = URL+"natural/nutrients"
#     headers = {
#         'x-app-id': 'e6541bf3',
#         'x-app-key': '2848dfdacf3be363a7835fffd9aaf72a',
#         "Content-Type": "application/json",
#     }
#
#     params = {
#         "query": food,
#         "timezone": "US/Eastern"
#
#     }
#
#     response = requests.post(url, headers=headers, json=params)
#     print(response.status_code)
#     if response.status_code == 200:
#         return json.loads(response.text)
#
#     else:
#         return response.text
#
#
# def query_search_instant(food, branded=True, common=True ):
#     # works
#     print('query_search_instant')
#     url = URL+"search/instant"
#     headers = {
#         'x-app-id': 'e6541bf3',
#         'x-app-key': '2848dfdacf3be363a7835fffd9aaf72a',
#     }
#
#     params = {
#         "query": food,
#         "self": True,
#         "branded": branded,
#         "common": common,
#     }
#     response = requests.post(url, headers=headers, json=params)
#     print('return from request: ', type(response))
#     data = json.loads(response.text)
#     print('after json.loads: ', type(data))
#
#     # print(data)
#     return data
#
#
# def print_loop(type, data, dummy):
#     outvals = {}
#     if len(data) > 0:
#         for k, v in type.items():
#             # exec(key + '=val')  # make me a variable
#             print(k, v)
#             # print(item["nf_calories"])
#
#     return outvals
#
#
# def parse_results(data, rtnfield=None):
#     if rtnfield is None:
#         rtnfield = []
#     if 'message' in data or data is None:
#         print('Error: ', data)
#         return
#     outlist = {}
#     for key, value in data.items():
#         # print(key, '=', value)
#         if len(value) > 0 and isinstance(value, list):
#             # print_loop(value[0], value, rtnfield)
#             for k, v in value[0].items():
#                 # print(k, ' = ', v)
#                 if k in rtnfield:
#                     # print('appending k', k)
#                     outlist[k] = str(v)
#
#                     print(outlist)
#             #     # print(item["nf_calories"])
#
#     return outlist
#

response = nutritionix_api.search_instant(query='Nuun Endurance Strawberry Lemonade')
print(response)
exit()


# response = nutritionix_api.get_item(r'604cc405ab57f2c034e7770a')
# print(response)
for food in response.get("branded", []):
    sv_food = food
    print(food.get("food_name", "Unknown"))
    print(food.get("serving_unit", "Unknown"))
    print(food.get("serving_qty", "Unknown"))
    print(food.get("nix_item_id", "Unknown"))
    nixid = food.get("nix_item_id", "Unknown")
    getit = nutritionix_api.get_item(nixid)
    print(type(getit), '  ', getit)
    for dets in getit.get("foods", "Unknown"):
        print(dets.get("nf_protein", 0))
        print(dets.get("nf_total_fat", 0))
        print(dets.get("nf_sodium", 0))
        print(dets.get("nf_total_carbohydrate", 0))
'''
        'nf_calories': 80,
        'nf_cholesterol': 0,
        'nf_dietary_fiber': 1,
        'nf_ingredient_statement': None,
        'nf_metric_qty': 23,
        'nf_metric_uom': 'g',
        'nf_p': None,
        'nf_potassium': 75,
        'nf_protein': 0,
        'nf_saturated_fat': 0,
        'nf_sodium': 115,
        'nf_sugars': 0,
        'nf_total_carbohydrate': 19,
        'nf_total_fat': 0,
        'nix_brand_id': '5caeea3172e78a410b5cb270',
        'nix_brand_name': 'Ucan',
        'nix_item_id': '604cc405ab57f2c034e7770a',
        'nix_item_name': 'Tropical Orange Workout Energy',
        'note': None,
        'photo': {'highres': None,
                  'is_user_uploaded': False,
                  'thumb': 'https://nutritionix-api.s3.amazonaws.com/604cc406cc6a070008c549bb.jpeg'},
        'serving_qty': 1,
        'serving_unit': 'packet',
'''

# data = query_search_instant('nuun endurance', common=True, branded=True)
# print(data)
# for item in data:
#     print(item)
#     print(type(item))
# pprint.pprint(data)
#
# data = query_search_instant('frosted flakes')
# print(data)
#
#
# # parse_results('foods', data)
#
# # all these work - now assign the necessary variables
# data = query_search_instant('Ucan Tropical Orange Workout Energy')
# print(data)
# # outlist will be empty if no values were sent to parse_results
# # newlist = parse_results(data, [])   # ['serving_qty', 'nf_calories', 'nf_sodium'])
# # print(' newlist out vals: ', newlist)
# data = query_search_nutrients('pear')
# print(data)
# # parse_results(data)
exit()
data = query_search_item_by_nix(r'604cc405ab57f2c034e7770a')
data.get("foods")
for item in data:
    print(item)


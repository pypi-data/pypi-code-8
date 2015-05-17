__author__ = 'scarroll'

from pygov.usda.client import UsdaClient
from pygov.usda.enums import *

usdaClient = UsdaClient("DEMO_KEY")
food = usdaClient.list_foods(1)[0]
food_report = usdaClient.get_food_report(food.id)
food_report_full = usdaClient.get_food_report(food.id, UsdaNdbReportType.full)
nutrient = food_report.nutrients[0]
nutr_report = usdaClient.get_nutrient_report(nutrient.id)

print("done")
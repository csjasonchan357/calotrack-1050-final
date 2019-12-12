import pandas as pd
import numpy as np
import requests
import json
import functools
import logging
import ETL_GCP

import importlib
importlib.reload(ETL_GCP)

logging.basicConfig(level=logging.DEBUG)

headers = {
			'x-app-id': "677b211d",
			'x-app-key': "742d50f2d169f8cc88df795d499f9ff9",
			'Content-Type': 'application/json'
			}
exercise = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutrients = "https://trackapi.nutritionix.com/v2/natural/nutrients"
instant = "https://trackapi.nutritionix.com/v2/search/instant"  

def print_hello():
	g = ETL_GCP.GCP()
	g.print_hello()

# Helper function to build_branded_table_from_list_of_jsons
def build_branded_table(result):
	brand_cols = ['food_name', 'brand_name_item_name',
				  'brand_name', 'serving_unit', 'serving_qty', 'nf_calories']
	table = []
	for i in range(len(result['branded'])):
		row = []
		for col in brand_cols:
			row.append(result['branded'][i][col])
		table.append(row)
	branded = pd.DataFrame(table, columns=brand_cols)
	branded.drop_duplicates(subset='food_name', keep=False, inplace=True)
	return branded

#Helper function to build_common_table_from_list_of_jsons
def build_common_table(result):
	common_cols = ['food_name', 'tag_name',
		'serving_unit', 'serving_qty', 'nf_calories']
	common_fields = ['food_name', 'tag_name',
		'serving_unit', 'serving_qty']
	table = []
	food_names = []
	for i in range(len(result)):
		result_keys = result[i].keys()
		row = []
		for col in common_fields:
			if col in result_keys:
				row.append(result[i][col])
			else:
				row.append("?")
		table.append(row)
		food_names.append(result[i]['food_name'])

	table = np.array(table)
	calories = common_api_get_cals(food_names)

	full_table = np.concatenate((table, calories.T), axis=1)
	common = pd.DataFrame(full_table, columns=common_cols)
	return common

# Helper function to build_common_table
def common_api_get_cals(food_names_list):
	food_names_string = ", ".join(food_names_list)
	query = {'query': food_names_string}
	response = requests.post(
		nutrients, headers=headers, json=query)
	response_json = json.loads(response.content.decode("utf-8"))
	calories_dict = dict()
	for item in response_json['foods']:
		calories_dict[item['food_name']] = item['nf_calories']
	calories = np.array(
		[[calories_dict[name] if name in calories_dict else "?" for name in food_names_list]])
	return calories

def add_to_curr_csvs(new_common, new_branded):
	og_common = pd.read_csv("initial_data/common.csv")
	full_common = og_common.append(new_common, ignore_index=True)
	full_common.to_csv("initial_data/common.csv", index=False)
	print("initial_data/common.csv updated")

	og_branded = pd.read_csv("initial_data/branded.csv")
	full_branded = og_branded.append(new_branded, ignore_index=True)
	full_branded.to_csv("initial_data/branded.csv", index=False)
	print("initial_data/branded.csv updated")

"""
Input must be a list of foods, each of which is a string
"""
def search_foods(food_input):
	# to parse the user query, either it's a single string with commas or none.
	foods = [food.strip().lower() for food in food_input.split(',')]
	logging.debug('List of foods:')
	logging.debug(foods)
	search_results = []
	for food_item in foods:
		search_query = {'query': food_item}
		response = requests.post(
			instant, headers=headers, json=search_query)
		response_json = json.loads(response.content.decode("utf-8"))
		search_results.append(response_json)
	return search_results

def user_food_query(food_input):
	search_results = search_foods(food_input)
	add_branded_table = build_branded_table_from_list_of_jsons(search_results)
	add_common_table = build_common_table_from_list_of_jsons(search_results)
	gcp_conn = ETL_GCP.GCP()
	gcp_conn.update_branded_table(add_branded_table)
	gcp_conn.update_common_table(add_common_table)
	
	total = 0
	for i in search_results:
		cl = len(i['common'])
		bl = len(i['branded'])

		total = total + cl + bl

	return total 

def build_branded_table_from_list_of_jsons(jsons_list):
	df_results = []
	for json_result in jsons_list:
		df_results.append(build_branded_table(json_result))
	full_table = functools.reduce(lambda x, y: x.append(y,ignore_index=True), df_results)
	# drop duplicate rows
	full_table.drop_duplicates(
		subset='food_name', keep=False, inplace=True)
	return full_table

def build_common_table_from_list_of_jsons(jsons_list):
	food_results = [
		item for sublist in jsons_list for item in sublist['common']]
	new_list = []
	# below is to eliminate duplicates
	for d in food_results:
		if d not in new_list:
			new_list.append(d)

	table = build_common_table(new_list)
	return table

# Takes in a string query like "running", or several queries together in one string separated by ", "
# like "running, tennis, hiking"
def search_exercises(exercise_input, gender=None, weight_kg=None, height_cm=None, age=None):
	if gender is not None and weight_kg is not None and height_cm is not None and age is not None:
		query = {"query": exercise_input, 'gender': gender, 'weight_kg':weight_kg,'height_cm':height_cm,'age':age}
	else:
		query = {"query": exercise_input}
	response = requests.post(
		exercise, headers=headers, json=query)
	results = json.loads(response.content.decode("utf-8"))
	return results

def user_exercise_query(exercise_input, gender=None, weight_kg=None, height_cm=None, age=None):
	search_results = search_exercises(exercise_input, gender, weight_kg, height_cm, age)
	add_exercise_table = build_exercise_table(search_results)
	gcp_conn = ETL_GCP.GCP()
	gcp_conn.update_exercise_table(add_exercise_table)
	return len(search_results['exercises'])

def build_exercise_table(exercises):
	table = []
	exercise_fields = ['name', 'duration_min', 'met','nf_calories']
	for i in range(len(exercises['exercises'])):
		row = []
		for col in exercise_fields:
			row.append(exercises['exercises'][i][col])
		table.append(row)
	exercise_table = pd.DataFrame(table, columns=exercise_fields)
	return exercise_table




if __name__ == "__main__":
	print('hi')



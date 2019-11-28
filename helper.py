from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
import random
from cuisine import cuisines, CuisineDF
from category import categories, CategoryDF
from dietarytype import dietarytypes, DietaryTypeDF
from user_data import check_dietary_preference
import pandas as pd
import pymssql
pymssql.__version__
'1.0.3'
import pymysql
pymysql.__version__
'0.9.3'

# MsSql Server connection


# Data
Recipe = pd.read_sql_query('''SELECT* FROM dbo.Recipe''', conn)
RecipeCategory= pd.read_sql_query('''SELECT * FROM dbo.RecipeCategory''', conn)
RecipeDietaryType = pd.read_sql_query('''SELECT* FROM dbo.RecipeDietaryType''', conn)
RecipeCuisine  = pd.read_sql_query('''SELECT* FROM dbo.RecipeCuisine''', conn)

# Recipe = pd.read_csv("../Data/Recipe.csv")
# RecipeCategory = pd.read_csv("../Data/RecipeCategory.csv")
# RecipeDietaryType = pd.read_csv("../Data/RecipeDietaryType.csv")
# RecipeCuisine = pd.read_csv("../Data/RecipeCuisine.csv")

greets = ['Hi! I’m good, how are you?', 'I am fine, what about you?', 'All good, thanks!']
greets_short = ["Hi", "Hi there", "Hello there", "Heya"]

entities = list(cuisines) + list(categories) + list(dietarytypes)
tfidf_entities = TfidfVectorizer(analyzer='char', ngram_range=(3, 5))
entities_vectors = tfidf_entities.fit_transform(entities)


def compute_score_entities(text):
	selected_cuisine_vector = tfidf_entities.transform([text])
	cosine_similarities = cosine_similarity(selected_cuisine_vector, entities_vectors)
	index, value = max(enumerate(list(cosine_similarities[0])), key=operator.itemgetter(1))
	return (index, value)

def find_entity(text, chat):

		(index, value) = compute_score_entities(text)
		if value == 0.0:
			message = "Sorry, I didn't understand. could you please answer again \n"
			return message, chat
		message = ""
		final_entity = entities[index]
		print("Final entity-->")
		print(final_entity)
		if final_entity in list(cuisines):
			print("Found cuisine")
			cuisine_id = CuisineDF.loc[CuisineDF['Title']== final_entity].Id.values[0]
			chat['cuisine_id'] = int(cuisine_id)
			message += "Selected Cuisine: "+final_entity+"\n"
			chat['selected_entities']['cuisine']+=1

		if final_entity in list(dietarytypes):
			print("Found dietarytype")
			dietary_type_id = DietaryTypeDF.loc[DietaryTypeDF['Title'] == final_entity].Id.values[0]
			message += "Selected Dietary type: " + final_entity + "\n"
			chat['dietary_type_ids'].append(int(dietary_type_id))
			chat['selected_entities']['dietarytype']+=1

		#Check Dietery preference
		dietary_pref = check_dietary_preference(chat['user_id'])
		if dietary_pref not in ["", "No dietary preference"]:
			print("Found dietary preference")
			print(dietary_pref)
			dietary_type_id = DietaryTypeDF.loc[DietaryTypeDF['Title'] == dietary_pref].Id.values[0]
			message += "Found Dietary preference: " + dietary_pref + "\n"
			chat['dietary_type_ids'].append(int(dietary_type_id))
			chat['selected_entities']['dietarytype']+=1


		chat['entities'].append(final_entity)
		print("===chat===")
		print(chat)
		return message, chat


# recipe_mapping
def find_recipe_ids_ml(chat, user_message=None, message=""):

	entity_type = [k for k in chat["selected_entities"].values() if k>0]

	recipe_categories_ids = RecipeCategory.loc[RecipeCategory['CategoryId'].isin(chat['category_ids'])].RecipeId.values
	recipe_cuisine_type_ids = RecipeCuisine.loc[RecipeCuisine['CuisineId'] == chat['cuisine_id']].RecipeId.values
	# if chat['dietary_type_ids'] != []:
	recipe_dietary_type_ids = RecipeDietaryType.loc[RecipeDietaryType['DietaryTypeId'].isin(chat['dietary_type_ids'])].RecipeId.values

	if len(entity_type)>=2:
		if chat['dietary_type_ids'] == []:
			recipe_ids = list(set(recipe_categories_ids) & set(recipe_cuisine_type_ids))
		elif chat['category_ids'] == []:
			recipe_ids = list(set(recipe_dietary_type_ids) & set(recipe_cuisine_type_ids))
		elif chat['cuisine_id'] == None:
			recipe_ids = list(set(recipe_dietary_type_ids) & set(recipe_categories_ids))
		else:
			recipe_ids = list(set(recipe_dietary_type_ids) & set(recipe_categories_ids) & set(recipe_cuisine_type_ids))
	else:
		recipe_ids = list(set(recipe_categories_ids) | set(recipe_cuisine_type_ids) | set(recipe_dietary_type_ids))
		
	recipeFoundDF = Recipe[Recipe['Id'].isin(recipe_ids)]
	if user_message:
		recipeFoundDF = recipeFoundDF.loc[recipeFoundDF['cooking_time_category'] == user_message]
	print("message")
	print(message)
	# message += "Number of Recipes found: " + str(len(recipeFoundDF)) + "\n"
	message += "Recipes found:\n"
	num = 0
	dict = {}
	if len(recipeFoundDF)>0:
		#shuffle the dataframe
		recipeFoundDF = recipeFoundDF.sample(frac=1).reset_index(drop=True)
	for index, row in recipeFoundDF.iterrows():
		num += 1
		message += str(num) + ": " + row['Title'] + "\n"
		dict[str(num)] = row['Id']
		if num == 10:
			#Get at max 10
			break

	if num > 0:
		message += "Please select the Recipe number to recieve cooking instructions."
		chat['recipe_mapping'] = dict
		chat['number_of_recipes'] = num

	return message, chat


	
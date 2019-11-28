import pandas as pd
import pymssql
pymssql.__version__
'1.0.3'

# Recipe = pd.read_csv("../Data/Recipe.csv")
# RecipeCategory = pd.read_csv("../Data/RecipeCategory.csv")
# RecipeDietaryType = pd.read_csv("../Data/RecipeDietaryType.csv")
# RecipeCuisine = pd.read_csv("../Data/RecipeCuisine.csv")
# MsSql Server connection

# Db_conn
Recipe = pd.read_sql_query('''SELECT* FROM dbo.Recipe''', conn)
RecipeCategory= pd.read_sql_query('''SELECT * FROM dbo.RecipeCategory''', conn)
RecipeDietaryType = pd.read_sql_query('''SELECT* FROM dbo.RecipeDietaryType''', conn)
RecipeCuisine  = pd.read_sql_query('''SELECT* FROM dbo.RecipeCuisine''', conn)


def categorize(row):
    if row['CookingTime'] <= 10:
        return "1"
    if (row['CookingTime'] > 10 and row['CookingTime'] <= 30):
        return "2"
    if (row['CookingTime'] > 30 and row['CookingTime'] <= 60):
        return "3"
    if row['CookingTime'] <= 60:
        return "4"


Recipe['cooking_time_category'] = Recipe.apply(categorize, axis=1)


# Cook_time options
def Cooking_Time():
    message = "What is the cook time we're looking at?\n"
    message += "1: 0-10mins | 2: under 30mins | 3: 30-1hour | 4: over 1hour"
    return message


def find_recipe_ids(user_message, update_id, chat):

    recipe_categories_ids = RecipeCategory.loc[RecipeCategory['CategoryId'].isin(chat['category_ids'])].RecipeId.values
    recipe_cuisine_type_ids = RecipeCuisine.loc[RecipeCuisine['CuisineId'] == chat['cuisine_id']].RecipeId.values

    if chat['dietary_type_ids'] !=[] :
        recipe_dietary_type_ids = RecipeDietaryType.loc[RecipeDietaryType['DietaryTypeId'].isin(chat['dietary_type_ids'])].RecipeId.values
        recipe_ids = list(set(recipe_categories_ids) & set(recipe_dietary_type_ids) & set(recipe_cuisine_type_ids))
        recipeFoundDF = Recipe[Recipe['Id'].isin(recipe_ids)]        
    else:
        recipe_ids = list(set(recipe_categories_ids) & set(recipe_cuisine_type_ids))
        recipeFoundDF = Recipe[Recipe['Id'].isin(recipe_ids)]
    recipeFoundDF = recipeFoundDF.loc[recipeFoundDF['cooking_time_category']== user_message]

    message = "Number of Recipes found: "+ str(len(recipeFoundDF))+"\n"
    bot_response = ["Number of Recipes found:\n", "list(len(recipeFoundDF))"]
    num = 0
    dict= {}
    for index, row in recipeFoundDF.iterrows():
        num+=1
        message+=str(num)+ ": "+row['Title']+"\n"
        dict[str(num)] = row['Id']

        
    if num>0:
        message+="Please select the Recipe number to recieve cooking instructions."
        chat['recipe_mapping'] = dict
        chat['number_of_recipes'] = num
        
    return message,update_id+1, chat

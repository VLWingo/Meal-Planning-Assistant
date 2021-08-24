# -*- coding: utf-8 -*-
"""
Created on Sun May  9 10:52:33 2021

@author: Victoria Wingo
"""

# 2. offer level of weight given to sale items: none, some, only -> requires
# manual input or webscrapping
# 3. min/max costs
# 4. Web-app

# imports 'dinner_Generator.py' to be used
import dinner_Generator
# imports 'ingredients_Generator.py' to be used
import ingredients_Generator
# imports pandas
import pandas as pd
# used for .literal_eval in Recipe objects and User inputs
import ast
import csv

def load_recipes(ingredients_df):
    '''Reads recipes.csv into a dataframe

    Args:
        None

    Returns:
        recipes_df: dataframe, read from recipes.csv'''

    location = r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python with Pandas\recipes.csv"
    recipes_df = pd.read_csv(
                            location,
                            index_col = 0,
                            names = [
                                    'Difficulty',
                                    'Meat',
                                    'Ingredients',
                                    'Type',
                                    'Subtype',
                                    'Frequency'],
                             converters = {'Ingredients':ast.literal_eval}
                             )
    recipes_df['Cost'] = cost_per_dinner(recipes_df, ingredients_df)

    return recipes_df

def load_ingredients():
    '''Reads ingredients.csv into a dataframe

    Args:
        None

    Returns:
        ingredients_df: dataframe, read from ingredients.csv'''

    location = r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python with Pandas\ingredients.csv"
    ingredients_df = pd.read_csv(
                                location,
                                index_col = 0,
                                names = [
                                        'Unit',
                                        'Purchase Weight',
                                        'Average Cost',
                                        'Aisle',
                                        'Alternative Unit',
                                        'Alternative Weight']
                                )

    return ingredients_df

def check_csv(location, length):
    with open(location, newline='') as csvfile:
        #read file
        recipe_reader = csv.reader(csvfile)
        n_row = 1
        while n_row <= length:
            for row in recipe_reader:
                try:
                    ingredients = ast.literal_eval(row[3])
                    n_row += 1
                except ValueError:
                    print(row[0], 'has a value error in ', ingredients)
                    n_row += 1
                except SyntaxError:
                    print(row[0], 'has a syntax error.')
                    n_row += 1
                
                

def load_saved_weeks():
    '''Reads saved_weeks.csv into a dataframe

    Args:
        None

    Returns:
        saved_df: dataframe, read from saved_weeks.csv'''

    location = r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python with Pandas\saved_weeks.csv"
    saved_df = pd.read_csv(
                            location,
                            names = [
                                    'Date',
                                    'Days',
                                    'Recipes'],
                            converters = {'Recipes':ast.literal_eval}
                            )
    if len(saved_df.index) >= 4:
        saved_df = saved_df.tail(4)
    print('Last 4 Entries: ', saved_df)
    return saved_df


def cost_per_dinner(recipes_df, ingredients_df):
    '''Calculates the cost of all recipes in recipes_df

    Args:
        recipes_df: dataframe, read from recipes.csv
        ingredients_df: dataframe, read from ingredients.csv

    Returns:
        cost: list, cost of each recipe's ingredients'''

    cost = []
    recipes = recipes_df.index
    recipes_done = 0
    while recipes_done < len(recipes):
        for recipe in recipes:
            recipe_cost = 0
            # Calculate the cost of each ingredient
            ingredient_dict = recipes_df['Ingredients'].loc[recipe]
            for ingredient in ingredient_dict:
                if ingredient != 'New Ingredients':
                    # Grab information relevant to the ingredient
                    ingredient_unit = ingredient_dict[ingredient][0]
                    ingredient_weight = ingredient_dict[ingredient][1]
                    try:
                        df_unit = ingredients_df.loc[ingredient, 'Unit']
                        df_purchase_weight = ingredients_df.loc[ingredient,
                                                        'Purchase Weight']
                        df_average_cost = float(ingredients_df.loc[ingredient,
                                                        'Average Cost'])
                        # Store info for alternative unit/weight if it exists
                        if (ingredients_df.loc[ingredient, 'Alternative Unit'] 
                                                        != 'nan'):
                            df_alt_unit = ingredients_df.loc[ingredient,
                                                        'Alternative Unit']
                            df_alt_weight = ingredients_df.loc[ingredient,
                                                        'Alternative Weight']
                        if df_unit == 'Each' and df_alt_unit != 'nan':
                            # 'Each' of the ingredient has this value
                            each = round((df_purchase_weight / df_alt_weight), 
                                                                             2)
                        elif df_alt_unit == 'Each':
                            each = round((df_alt_weight / df_purchase_weight), 
                                                                             2)
        
                        ingredient_tuple = (ingredient_unit, ingredient_weight)
        
                        # If different from both db and alt unit, convert
                        if ingredient_unit == df_unit:
                            cost_per_unit = (df_average_cost / 
                                             df_purchase_weight)
                        elif (df_alt_unit != 'nan' and 
                              ingredient_unit == df_alt_unit):
                            cost_per_unit = df_average_cost / df_alt_weight
                        else:
                            if df_unit == 'Each':
                                cost_per_unit = (df_average_cost / 
                                                 df_purchase_weight)
                                ingredient_weight = ingredient_weight * each
                            elif ((df_unit == 'Lb' 
                                   and 
                                  ingredient_unit != 'Dry Oz') 
                                  or 
                                  (df_unit == 'Dry Oz' 
                                   and 
                                   ingredient_unit != 'Lb')):
                                cost_per_unit = (df_average_cost / 
                                                 df_alt_weight)
                                ingredient_weight = (ingredients_Generator
                                                     .convert_unit(
                                                         ingredient_tuple, 
                                                         df_alt_unit)
                                                     )
                            else:
                                cost_per_unit = (df_average_cost / 
                                                 df_purchase_weight)
                                ingredient_weight = (ingredients_Generator
                                                     .convert_unit(
                                                         ingredient_tuple, 
                                                         df_unit)
                                                     )           
                        # Determine how much it costs
                        ingredient_cost = ingredient_weight * cost_per_unit
                        recipe_cost += round(ingredient_cost, 2)
                        # Testing code
                        # if recipe == 'Scalloped Potatoes':
                        #     print(ingredient, ingredient_cost)
                    # Print key errors instead of interrupting program
                    except KeyError:
                        print('KeyError: ', ingredient, 'in ', recipe)                   
            cost.append(recipe_cost)
            recipes_done += 1

    return cost

def program_UI(recipes_df, ingredients_df):
    '''Interactive interface to begin program

    Args:
        recipes_df: dataframe, read from recipes.csv
        ingredients_df: dataframe, read from ingredients.csv

    Returns:
        True, to kill function'''

    ans = input('''Select option:
                    1 - Generate week
                    2 - Build week around list
                    3 - Generate grocery list from list
                    4 - Exit program ''')

    while ans != '4':
        # 1 - Generate week
        if ans == '1':
            week_df = dinner_Generator.make_Dinners(recipes_df, saved_df)
            print(week_df)
            # Builds a dictionary of ingredients needed to make
            # the week's worth of recipes
            grocery_df = ingredients_Generator.merge_Ingredients(
                                                        week_df,
                                                        ingredients_df
                                                        )
            break
        # 2 - Build week around list
        elif ans == '2':
            week_df = pd.DataFrame()
            week_df = dinner_Generator.generate_partial_week(recipes_df)
            if week_df.empty:
                ans = input('''Select option:
                                1 - Generate week
                                2 - Build week around list
                                3 - Generate grocery list from list
                                4 - Exit program ''')
            else:
                print(week_df)
            # Builds a dictionary of ingredients needed to make
            # the week's worth of recipes
            grocery_df = ingredients_Generator.merge_Ingredients(
                                                        week_df,
                                                        ingredients_df
                                                        )
            print(grocery_df)
            grocery_sum = ingredients_Generator.predict_Grocery(
                                                grocery_df,
                                                ingredients_df
                                                )
            break
        # 3 - Generate grocery list from list
        elif ans == '3':
            week_df = ingredients_Generator.build_Grocery_List(recipes_df)
            grocery_df = ingredients_Generator.merge_Ingredients(
                                                        week_df,
                                                        ingredients_df
                                                        )
            print(grocery_df)
            grocery_sum = ingredients_Generator.predict_Grocery(
                                                grocery_df,
                                                ingredients_df
                                                )
            print('Estamted Grocery Cost: ', grocery_sum)
            break
        # Mistake
        else:
            print('Invalid Command. Please try again.')
            ans = input('''Select option:
                            1 - Generate week
                            2 - Build week around list
                            3 - Generate grocery list from list
                            4 - Exit program ''')
    if ans == '4':
        return True

    ans2 = input('''Select option:
                     1 - Replace a recipe
                     2 - Show grocery list
                     3 - Add an ingredient
                     4 - Remove an ingredient
                     5 - Exit options
                     6 - Exit program ''')

    while ans2 != '5' and ans2 != '6':
        # 1 - Replace a recipe
        if ans2 == '1':
            # Allows User to replace individual recipes with ones of equal
            # meat type and difficulty, and checks to make sure that it fits
            # the type/subtype prerequisites
            ans2b = input(('''Do you want to replace it yourself?
                                           y = yes, n = randomly choose '''))
            if ans2b == 'y':
                week_df = dinner_Generator.user_replace_recipe(recipes_df,
                                                               week_df)
                print(week_df)
            elif ans2b == 'n':
                week_df = dinner_Generator.replace_Recipe(recipes_df, week_df)
                print(week_df)
            else:
                print('Invalid Command. Please try again.')
            ans2 = input('''Select option:
                            1 - Replace a recipe
                            2 - Show grocery list
                            3 - Add an ingredient
                            4 - Remove an ingredient
                            5 - Exit options
                            6 - Exit program ''')
        # 2 - Show grocery list
        elif ans2 == '2':            
            print(grocery_df)
            grocery_sum = ingredients_Generator.predict_Grocery(
                                                grocery_df,
                                                ingredients_df
                                                )
            print('Estamted Grocery Cost: ', grocery_sum)
            ans2 = input('''Select option:
                            1 - Replace a recipe
                            2 - Show grocery list
                            3 - Add an ingredient
                            4 - Remove an ingredient
                            5 - Exit options
                            6 - Exit program ''')
        # 3 - Add an ingredient
        elif ans2 == '3':
            print(grocery_df)
            grocery_sum = ingredients_Generator.predict_Grocery(
                                                grocery_df,
                                                ingredients_df
                                                )
            print('Estamted Grocery Cost: ', grocery_sum)
            ans2 = input('''Select option:
                            1 - Replace a recipe
                            2 - Show grocery list
                            3 - Add an ingredient
                            4 - Remove an ingredient
                            5 - Exit options
                            6 - Exit program ''')
        # 4 - Remove an ingredient
        elif ans2 == '4':
            grocery_df = (ingredients_Generator.remove_Ingredient
                                      (grocery_df))
            print(grocery_df)
            grocery_sum = ingredients_Generator.predict_Grocery(
                                                grocery_df,
                                                ingredients_df
                                                )
            print('Estamted Grocery Cost: ', grocery_sum)
            ans2 = input('''Select option:
                            1 - Replace a recipe
                            2 - Show grocery list
                            3 - Add an ingredient
                            4 - Remove an ingredient
                            5 - Exit options
                            6 - Exit program ''')
        # Mistake
        else:
            print('Invalid Command. Please try again.')
            ans2 = input('''Select option:
                            1 - Replace a recipe
                            2 - Show grocery list
                            3 - Add an ingredient
                            4 - Remove an ingredient
                            5 - Exit options
                            6 - Exit program ''')
    if ans2 == '6':
        exit_ans = input('''Do you wish to save the recipes for the week?
                                                         y - yes, n - no ''')
        while exit_ans != 'y' and exit_ans != 'n':
            print('Invalid Command. Please try again.')
            exit_ans = input('''Do you wish to save the recipes for the week?
                                                         y - yes, n - no ''')
        if exit_ans == 'y':
            dinner_Generator.save_Week(week_df)
        return True

    ans3 = input('''Select option:
                    1 - Show Week
                    2 - Show Grocery List
                    3 - Go Back to Beginning
                    4 - Exit Program ''')

    while ans3 != '4':
        # 1 - Show Week
        if ans3 == '1':
            print(week_df)
            ans3 = input('''Select option:
                        1 - Show Week
                        2 - Show Grocery List
                        3 - Go Back to Beginning
                        4 - Exit Program ''')
        # 2 - Show Grocery List
        elif ans3 == '2':
            print(grocery_df)
            ans3 = input('''Select option:
                            1 - Show Week
                            2 - Show Grocery List
                            3 - Go Back to Beginning
                            4 - Exit Program ''')
        # 3 - Go Back to Beginning
        elif ans3 == '3':
            program_UI(recipes_df, ingredients_df)
            ans3 = '4'
        # Mistake
        else:
            print('Invalid Command. Please try again.')
            ans3 = input('''Select option:
                            1 - Show Week
                            2 - Show Grocery List
                            3 - Go Back to Beginning
                            4 - Exit Program ''')
    if ans3 == '4':
        exit_ans = input('''Do you wish to save the recipes for the week?
                                                         y - yes, n - no ''')
        while exit_ans != 'y' or exit_ans != 'n':
            print('Invalid Command. Please try again.')
            exit_ans = input('''Do you wish to save the recipes for the week?
                                                         y - yes, n - no ''')
        if exit_ans == 'y':
            dinner_Generator.save_Week(week_df)
        f = open("saved_weeks.csv", "r")
        print(f.read())
        return True

# Test code for testing the integrity of the dicts
# check_csv('recipes.csv', 24)

ingredients_df = load_ingredients()
recipes_df = load_recipes(ingredients_df)
saved_df = load_saved_weeks()

# Run main function
program_UI(recipes_df, ingredients_df)

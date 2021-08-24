# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:46:24 2021

@author: Victoria Wingo
"""

# import math for ceiling function
import math
import pandas as pd


def merge_dicts(dict1, dict2):
    '''Merges two (2) dictionaries with single string keys and single
        int/real values

    Args:
        dict1: dictionary
        dict2: dictionary

    Returns:
        merged_dict: dictionary, merged from dict1 and dict2'''

    merged_dict = dict1
    for key in dict2.keys():
        if key in merged_dict.keys():
            merged_dict[key] += dict2[key]
        else:
            merged_dict[key] = dict2[key]

    return merged_dict


def merge_Ingredients(week_df, ingredients_df):
    '''Creates a dictionary containing the combined contents of all
        ingredients columns associated with the week

    Args:
        week_df: dataframe, made from choices for the week
        ingredients_df: dataframe, read from ingredients.csv

    Returns:
        grocery_df: dataframe, ingredients necessary for
            the week's recipes'''

    merged_Ingredients = {}

    dicts = week_df['Ingredients']

    # Dinner is the dict
    for dinner in dicts:
        for ingredient in dinner.keys():
            # Ingredient is not already in merged_Ingredients
            if ingredient not in merged_Ingredients.keys():
                merged_Ingredients[ingredient] = dinner[ingredient]
            elif ingredient == 'New Ingredients':
                merged_Ingredients[ingredient][1] += 1
            # Ingredient already in merged_Ingredients
            else:
                # If same unit
                if dinner[ingredient][0] == merged_Ingredients[ingredient][0]:
                    merged_Ingredients[ingredient][1] += dinner[ingredient][1]
                # If not same unit
                else:
                    df_unit = ingredients_df['Unit'].loc[ingredient]
                    df_purchase_weight = (
                            ingredients_df['Purchase Weight'].loc[ingredient]
                                            )
                    df_alt_unit = (
                        ingredients_df['Alternative Unit'].loc[ingredient]
                                    )
                    df_alt_weight = (
                        ingredients_df['Alternative Weight'].loc[ingredient]
                                        )

                    if df_unit == 'Each' and df_alt_unit != 'nan':
                        # 'Each' of the ingredient has this value percentage
                        each = round((df_purchase_weight / df_alt_weight), 2)
                    elif df_alt_unit == 'Each':
                        each = round((df_alt_weight / df_purchase_weight), 2)

                    ingredient_unit = merged_Ingredients[ingredient][0]
                    ingredient_weight = merged_Ingredients[ingredient][1]
                    ingredient2_unit = dinner[ingredient][0]
                    ingredient2_weight = dinner[ingredient][1]
                    ingredient2_tuple = (ingredient2_unit, ingredient2_weight)

                    if ingredient_unit == 'Each':
                        # Convert ingredient2_unit to 'Each'
                        final_unit = ingredient_unit
                        ingredient2_weight = each * ingredient2_weight
                    elif ingredient2_unit == 'Each':
                        # Convert ingredient_unit to 'Each'
                        final_unit = ingredient2_unit
                        ingredient_weight = each * ingredient_weight
                    else:
                        final_unit = ingredient_unit
                        ingredient2_weight = convert_unit((ingredient2_tuple),
                                                          ingredient_unit)
                    final_weight = ingredient_weight + ingredient2_weight
                    merged_Ingredients[ingredient] = [final_unit, final_weight]

    grocery_df = pd.DataFrame.from_dict(
                                        merged_Ingredients,
                                        orient = 'index',
                                        columns = ['Unit', 'Weight']
                                        )
    indices = grocery_df.index
    aisles = []
    for value in indices:
        if value != 'New Ingredients':
            aisles.append(ingredients_df['Aisle'].loc[value])
        else:
            aisles.append('NaN')
    grocery_df['Aisle'] = aisles
    grocery_df = grocery_df.sort_values(by=['Aisle'])
    return grocery_df


def add_Ingredient(grocery_df, ingredients_df):
    '''Allows User to add more Ingredients to the grocery list for the week

    Args:
        grocery_df: dataframe, ingredients necessary for
            the week's recipes
        ingredients_df: dataframe, read from ingredients.csv

    Returns:
        grocery_df: dataframe, modified from a previous version'''

    ans = 'y'
    while ans != 'e':
        if ans == 'y':
            try:
                # User Input
                name = input('''Please submit name of ingredient: ''')
                unit = input('''Please submit unit of ingredient: ''')
                weight = float(
                    input('''Please submit weight of ingredient: ''')
                    )
                # Adds User Input if the ingredient is not already in the df
                if name not in grocery_df.index:
                    aisle = ingredients_df['Aisle'].loc[name]
                    new_row = pd.DataFrame(
                                            [[unit,weight,aisle]], 
                                            columns = [
                                                        'Unit',
                                                        'Weight',
                                                        'Aisle'],
                                            index = [name])
                    grocery_df = grocery_df.append(
                                                    new_row,
                                                    verify_integrity = True
                                                    )
                # Adds Value to already existing ingredient in df
                else:
                    df_unit = grocery_df['Unit'].loc[name]
                    df_weight = grocery_df['Weight'].loc[name]
                    # If units are equivalent
                    if unit == df_unit:
                        grocery_df['Weight'].loc[name] = df_weight + weight
                    # Ingredient is in df but different unit
                    else:
                        # If either unit is 'Each'
                        if unit == 'Each' or df_unit == 'Each':
                            # Convert original unit to new unit and add
                            alt_weight = (
                                ingredients_df['Alternative Weight'].loc[name]
                                )
                            org_weight = (
                                ingredients_df['Purchase Weight'].loc[name]
                                )
                            if unit == 'Each':
                                each = round((alt_weight / org_weight), 2)
                                grocery_df['Unit'].loc[name] = 'Each'
                                grocery_df['Weight'].loc[name] = (
                                                                (df_weight
                                                                 * each)
                                                                + weight
                                                                    )
                            # Convert new unit to Each and add
                            elif df_unit == 'Each':
                                each = round((org_weight / alt_weight), 2)
                                grocery_df['Weight'].loc[name] = (
                                                                (weight * each) 
                                                                + df_weight
                                                                    )
                        else:
                            # New unit matches ingredients_df unit
                            if unit == ingredients_df['Unit'].loc[name]:
                                # Convert grocery_df unit to new unit and add
                                df_weight = convert_unit(
                                                        (df_unit, df_weight), 
                                                        unit
                                                            )
                                grocery_df['Unit'].loc[name] = unit
                                grocery_df['Weight'].loc[name] = (
                                                                df_weight 
                                                                + weight
                                                                    )
                            # Just convert the input unit to df unit and add
                            else:
                                weight = convert_unit((unit, weight), df_unit)
                                grocery_df['Weight'].loc[name] = (
                                                                    df_weight 
                                                                    + weight
                                                                    )
                print(grocery_df)
                ans = input('''Enter 'y' to add an ingredient
                                            or 'e' to move on. ''')

            # An exception for if User inputs the data incorrectly
            except ValueError:
                print('Invalid submission. Please try again.')
                ans = input('''Enter 'y' to add an ingredient
                                            or 'e' to move on. ''')
            
            except KeyError:
                print('Invalid submission. Try again.')
                ans = input('''Enter 'y' to remove an ingredient
                                                or 'e' to move on. ''')
        else:
            # Notify User that their input is invalid
            print('Invalid command. Please try again.')
            ans = input('''Enter 'y' to add an ingredient
                                        or 'e' to move on. ''')
    grocery_df = grocery_df.sort_values(by = ['Aisle'])
    return grocery_df


def remove_Ingredient(grocery_df):
    '''Allows User to remove Ingredients from the grocery list for the week

    Args:
        grocery_df: dataframe, ingredients necessary for
            the week's recipes

    Returns:
        grocery_df: dataframe, modified from a previous version'''

    ans = 'y'
    # Loop so long as the User does not specify to stop
    while ans != 'e':
        # Checks that User specifies they desire to remove an item
        if ans == 'y':
            try:
                # User Input
                name = input('''Please submit name of ingredient: ''')
                weight = input('''Please submit weight of ingredient or type 
                               'x' to remove the ingredient completely: ''')

                # Checks if the counter has gone to 0 and removes key if yes
                if weight == 'x':
                    grocery_df.drop(labels = name, axis = 0, inplace = True)
                else: 
                    # Removes amount from dataframe
                    weight = float(weight)
                    old_weight = grocery_df['Weight'].loc[name]
                    grocery_df['Weight'].loc[name] = (old_weight - weight)
                    if grocery_df['Weight'].loc[name] <= 0:
                        grocery_df.drop(labels = name, 
                                        axis = 0, 
                                        inplace = True)
                print(grocery_df)
                ans = input('''Enter 'y' to remove an ingredient
                                                or 'e' to move on. ''')

            # An exception for if User inputs the data incorrectly
            except ValueError:
                print('Invalid submission. Try again.')
                ans = input('''Enter 'y' to remove an ingredient
                                                or 'e' to move on. ''')
            
            # An exception for if User inputs something that isn't in the list
            except KeyError:
                print('Invalid submission. Try again.')
                ans = input('''Enter 'y' to remove an ingredient
                                                or 'e' to move on. ''')

        else:
            # Notify User that their input is invalid
            print('Invalid command. Please try again.')
            ans = input('''Enter 'y' to remove an ingredient
                                            or 'e' to move on. ''')
    grocery_df = grocery_df.sort_values(by = ['Aisle'])
    return grocery_df


def build_Grocery_List(recipes_df):
    ''' Makes a grocery list from a User-input list of recipes

    Args:
        recipes_df: dataframe, read from recipes.csv

    Returns:
        week_df: dataframe, made from choices for the week'''

    ans = 'y'
    while ans == 'y':
        try:
            num_recipe = input('''How many recipes are you entering?: ''')
            entries = 0
            ans2 = 'n'
            while ans2 == 'n':
                recipe_input = []
                while entries < num_recipe:
                    recipe = input('''Please enter the name of the recipe: ''')
                    recipe_input.append(recipe)
                print(recipe_input)
                ans2 = input('''Is this list correct? y - yes, n - no ''')
            
            # Insert input values into week dataframe
            week_df = recipes_df.loc[recipe_input]
            return week_df
    
        except ValueError:
            ans = input('Invalid submission. Try again? y - yes, n - no')


def predict_Grocery(grocery_df, ingredients_df):
    '''Predicts the cost of week_df by way of merged_ingredients

    Args:
        ingredients_df: dataframe, read from ingredients.csv
        grocery_df: dataframe, ingredients necessary for
            the week's recipes

    Returns:
        grocery_sum: real, cost of grocery list '''

    grocery_sum = 0
    ingredients_list = grocery_df.index
    for ingredient in ingredients_list:
        # Ignore 'New Ingredient'
        if ingredient != 'New Ingredients':
            # Grab information relevant to the ingredient
            ingredient_unit = grocery_df['Unit'].loc[ingredient]
            ingredient_weight = grocery_df['Weight'].loc[ingredient]
            df_unit = ingredients_df.loc[ingredient, 'Unit']
            df_purchase_weight = ingredients_df.loc[ingredient,
                                                    'Purchase Weight']
            df_average_cost = float(ingredients_df.loc[ingredient,
                                                       'Average Cost'])
            # Store info for alternative unit/weight if it exists
            if ingredients_df.loc[ingredient, 'Alternative Unit'] != 'nan':
                df_alt_unit = ingredients_df.loc[ingredient,
                                                 'Alternative Unit']
                df_alt_weight = ingredients_df.loc[ingredient,
                                                   'Alternative Weight']
            ingredient_tuple = (ingredient_unit, ingredient_weight)    

            # If different from both database and alternative unit, convert
            if ingredient_unit == df_unit:
                pass
            elif df_alt_unit and ingredient_unit == df_alt_unit:
                df_unit = df_alt_unit
                df_purchase_weight = df_alt_weight
            else:
                if ((df_unit == 'Lb' and ingredient_unit != 'Dry Oz') 
                    or 
                    (df_unit == 'Dry Oz' and ingredient_unit != 'Lb')):
                        ingredient_weight = convert_unit(ingredient_tuple, 
                                                         df_alt_unit)
                        ingredient_tuple = (df_alt_unit, ingredient_weight)
                else:
                    ingredient_tuple = (df_unit, convert_unit(ingredient_tuple,
                                                          df_unit))
            # Determine how many whole items need to be purchased to
            # fulfill the ingredient
            purchase_items = round((ingredient_tuple[1] / df_purchase_weight),
                                   2)
            whole_items = int(math.ceil(purchase_items))

            purchase_cost = round((whole_items * df_average_cost), 2)

            grocery_sum += round(purchase_cost, 2)
            
            grocery_sum = round(grocery_sum, 2)

    return grocery_sum

def convert_unit(input1, input2):
    '''Converts a unit to another unit

    Args:
        input1: tuple, (unit, value) to be converted
        input2: string, unit to be converted to

    Returns:
        input2_value: real'''

    tsp_convert = {'Tsp': 1, 'Tbsp': 0.33, 'Oz': 1/6, 'Cup': 1/48,
                   'Pint': 1/96,'Quart': 1/192, 'Gal': 1/768}
    tbsp_convert = {'Tsp': 3, 'Tbsp': 1, 'Oz': 0.5, 'Cup': 1/16, 'Pint': 1/32,
                    'Quart': 1/64, 'Gal': 1/256}
    oz_convert = {'Tsp': 6, 'Tbsp': 2, 'Oz': 1, 'Cup': 1/8, 'Pint': 1/8,
                  'Quart': 1/32, 'Gal': 1/128}
    cup_convert = {'Tsp': 48, 'Tbsp': 16, 'Oz': 8, 'Cup': 1, 'Pint': 1/2,
                   'Quart': 1/4, 'Gal': 1/16}
    pint_convert = {'Tsp': 96, 'Tbsp': 32, 'Oz': 16, 'Cup': 2, 'Pint': 1,
                    'Quart': 1/2, 'Gal': 1/8}
    quart_convert = {'Tsp': 192, 'Tbsp': 64, 'Oz': 32, 'Cup': 4,
                     'Pint': 2, 'Quart': 1, 'Gal': 1/4}
    gallon_convert = {'Tsp': 768, 'Tbsp': 256, 'Oz': 128, 'Cup': 16,
                      'Pint': 8, 'Quart': 4, 'Gal': 1}
    dry_oz = {'Dry Oz': 1, 'Lb': 1/16}
    lb_convert = {'Dry Oz': 16, 'Lb': 1}
    conversion_dict = {'Tsp': tsp_convert, 'Tbsp': tbsp_convert,
                       'Oz': oz_convert, 'Cup': cup_convert,
                       'Pint': pint_convert, 'Quart': quart_convert,
                       'Gal': gallon_convert, 'Lb': lb_convert,
                       'Dry Oz': dry_oz}
    convert_dict = conversion_dict[input1[0]]
    input2_value = convert_dict[input2] * input1[1]
    return input2_value

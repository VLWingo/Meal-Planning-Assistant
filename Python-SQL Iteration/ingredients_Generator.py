# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:46:24 2021

@author: Tori
"""

# used for .literal_eval
import ast
import CSVtoSQL


def merge_dicts(dict1, dict2):
    '''Merged two (2) dictionaries with single string keys and single
        int/real values

    Args:
        dict1: a dictionary
        dict2: a dictionary

    Returns:
        merged_dict: a merged dictionary'''

    merged_dict = dict1
    for key in dict2.keys():
        if key in merged_dict.keys():
            merged_dict[key] += dict2[key]
        else:
            merged_dict[key] = dict2[key]

    return merged_dict


def merge_Ingredients():
    '''Creates a dictionary containing the combined contents of all
        ingredients columns associated with the week

    Args:

    Returns:
        merged_Ingredients: a dictionary of ingredients necessary for
            the week's recipes'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    merged_Ingredients = {}

    ingredient_rows = cur.execute('''SELECT ingredients
                                      FROM recipes
                                      WHERE name
                                      IN week''');
    # literal evaluation of table objects
    dicts = [ast.literal_eval(row[0]) for row in ingredient_rows]
    conn.close()
    for dinner in dicts:
        # dinner is a dict of ingredients from each dinner
        for ingredient in dinner.keys():
            # ingredient is not already in grocery list
            if ingredient not in merged_Ingredients.keys():
                merged_Ingredients[ingredient] = dinner[ingredient]
            else:
                # ingredient in list and unit the same
                if dinner[ingredient][0] == merged_Ingredients[ingredient][0]:
                    merged_Ingredients[ingredient][1] += dinner[ingredient][1]
                # ingredient in list but unit different
                else:
                    merged_Ingredients[ingredient].append(dinner[ingredient][0])
                    merged_Ingredients[ingredient].append(dinner[ingredient][1])

    return merged_Ingredients


def add_Ingredient(merged_Ingredients):
    '''Allows User to add more Ingredients to the grocery list for the week

    Args:
        merged_Ingredients: a dictionary of ingredients necessary for
            the week's recipes

    Returns:
        merged_Ingredients: a dictionary modified from a previous version'''

    ans = 'y'
    while ans != 'e':
        if ans == 'y':
            try:
                # User Input
                data = ast.literal_eval(input('''Please write the item as
                                             ("Item Name", Unit, Amount) '''))
                # Adds User Input if the Ingredient is not already in the List
                if data[0] not in merged_Ingredients.keys():
                    merged_Ingredients.update(data)
                # Adds Value to already existing Ingredient in List
                elif data[0] in merged_Ingredients.keys():
                    #if units are equivalent
                    if data[1] == merged_Ingredients[data[0]][0]:
                        merged_Ingredients[data[0]][1] += data[2]
                    # ingredient in list but unit different
                    else:
                        merged_Ingredients[data[0]].append(data[1])
                        merged_Ingredients[data[0]].append(data[2])
                print(merged_Ingredients)
                ans = input('''Enter 'y' to add an ingredient
                            or 'e' to move on.''')

            # An exception for if User inputs the data incorrectly
            except ValueError:
                print('Invalid submission. Try again.')
                ans = input('''Enter 'y' to add an ingredient
                            or 'e' to move on.''')
        else:
            # Notify User that their input is invalid
            print('Invalid command. Please try again.')
            # Ask for input again
            ans = input('''Enter 'y' to add an ingredient
                        or 'e' to move on.''')

    return merged_Ingredients


def remove_Ingredient(merged_Ingredients):
    '''Allows User to remove Ingredients from the grocery list for the week

    Args:
        merged_Ingredients: a dictionary of ingredients necessary for
            the week's recipes

    Returns:
        a modified merged_Ingredients'''

    ans = 'y'
    # Loop so long as the User does not specify to stop
    while ans != 'e':
        # Checks that User specifies they desire to add an item
        if ans == 'y':
            try:
                # User Input
                data = ast.literal_eval(input('''Please write the item as
                                             ("Item Name", Unit, Amount) '''))
                # Removes amount from dict
                merged_Ingredients[data[0]][1] -= data[2]
                # Checks if the counter has gone to 0 and removes key if yes
                if merged_Ingredients[data[0]][1] <= 0:
                    merged_Ingredients.pop(data[0])
                print(merged_Ingredients)
                ans = input('''Enter 'y' to remove an ingredient
                            or 'e' to move on.''')

            # An exception for if User inputs the data incorrectly
            except ValueError:
                print('Invalid submission. Try again.')
                ans = input('''Enter 'y' to remove an ingredient
                            or 'e' to move on.''')

        # Response for an answer that is neither 'y' or 'n'
        else:
            # Notify User that their input is invalid
            print('Invalid command. Please try again.')
            # Ask for input again
            ans = input('''Enter 'y' to remove an ingredient
                        or 'e' to move on.''')

    return merged_Ingredients


def build_Grocery_List():
    ''' Makes a grocery list from a User-input list of recipes

    Args:

    Returns:
        '''

    try:
        # list version of input
        recipe_input = ast.literal_eval(input(''' Provide list of recipes
                                              as ['Recipe 1', 'Recipe 2',
                                                  etc.]: '''))
        # Insert input values into week table
        for dinner in recipe_input:
            CSVtoSQL.create_week(dinner)

    except ValueError:
        print('Invalid submission. Try again.')
        # list version of input
        recipe_input = ast.literal_eval(input(''' Provide list of recipes as
                                              ['Recipe 1', 'Recipe 2',
                                                  etc.]: '''))


def predict_Grocery(merged_ingredients):
    '''# 1a. Predict costs: 
    # consolidate units if needed
        * 1. check if there are more than 2 entries in the value of each key
            example:
                if merged_ingredients[ingredient][0] == purchase_unit:
                    convert merged_ingredients[ingredient][2] to [0]
                    add together
                    remove [2] and [3]
                elif merged_ingredients[ingredient][2] == purchase_unit:
                    convert [0] to [2]
                    add together
                    remove [2] and [3]
                else:
                    convert [2] to [0]
                    add together
                    remove [2] and [3]
        2. convert amount according to unit conversion
            a. compare merged_ingredients[ingredient][0] v. database unit
            b. if don't match, look for alternative_unit
            c. if no alternative unit, convert according to conversion below
    # calculate how many purchase units are needed
        # compare units needed to purchase unit amount
    # sum purchase units
    # present result
    
    average_cost
    purchase_weight
    unit
    name
    
    for ingredient in merged_ingredients:
        merged_ingredients[ingredient] == name
        merged_ingredients[ingredient][0] == unit
        merged_ingredients[ingredient][1] == (fraction of) purchase_weight
        
    1 tbsp == 3 tsp
    1 oz == 2 tbsp
    1 cup == 8 oz or 16 Tbsp
    1 pint == 16 oz
    1 quart == 32 oz
    1 gallon == 128 oz
    1 pound == 16 oz
    
    wtf to do with 'eaches' that are bought in weights?
        solution: alternative_unit, alternative_weight
    
    Returns:
        grocery_sum: real, cost of grocery list'''

    grocery_sum = 0

    for ingredient in merged_ingredients.keys():
        #grab database unit for ingredient
        conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
        cur = conn.cursor()
        #ingredient_facts[0] = unit, [1] = purchase_weight, [2] = average_cost
        ingredient_facts = cur.execute('''SELECT unit,purchase_weight,average_cost FROM ingredients WHERE name=?''', (ingredient,))
        ingredient_facts = ingredient_facts.rvs(1).reshape(-1)
        #check if ingredient has 2 units
        if len(merged_ingredients[ingredient]) > 2:
            #check if [0] == database unit
            
            #check if [2] == database unit
            
            #else convert [2] to [0]
            pass
        #convert ingredient with single unit
        else:
            #convert [2]  to [0]
            pass
    
    return grocery_sum
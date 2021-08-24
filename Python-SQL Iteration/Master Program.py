# -*- coding: utf-8 -*-
"""
Created on Sun May  9 10:52:33 2021

@author: Tori
"""

# 1. Grocery List: organize by section/type, predict cost
# 1a. Predict costs: 
    # consolidate units if needed
    # calculate how many purchase units are needed
        # compare unit to purchase unit
        # compare units needed to purchase unit amount
    # sum purchase units
    # present result
# 2. offer level of weight given to sale items: none, some, only -> requires
# manual input or webscrapping
# 3. Decision-making: some recipes should be less frequent than others ->
# requires some form of memory and another variable or list
# 4. Web-app
# 5. Costs per meal
    # call: ingredient name, unit, amount/unit, price/unit
    # merged_ingredients dict holds {Name: [Unit, Amount]}
    # 
    # calculate

# imports 'dinner_Generator.py' to be used
import dinner_Generator
# imports 'ingredients_Generator.py' to be used
import ingredients_Generator
# imports CSVtoSQL.py to be used
import CSVtoSQL

conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")

# Removes anything in the week table for a fresh run
cur = conn.cursor()
cur.execute('''DELETE FROM week''');
conn.close()


def program_UI():
    '''Interactive interface to begin program

    Args:

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
            dinner_Generator.make_Dinners()
            dinner_Generator.print_Week()
            break

        # 2 - Build week around list
        elif ans == '2':
            dinner_Generator.generate_partial_week()
            break

        # 3 - Generate grocery list from list
        elif ans == '3':
            ingredients_Generator.build_Grocery_List()
            merged_Ingredients = ingredients_Generator.merge_Ingredients()
            print('Grocery List: ', merged_Ingredients)
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
            dinner_Generator.replace_Recipe()
            dinner_Generator.print_Week()
            ans2 = input('''Select option:
                    1 - Replace a recipe
                    2 - Show grocery list
                    3 - Add an ingredient
                    4 - Remove an ingredient
                    5 - Exit options
                    6 - Exit program ''')

        # 2 - Show grocery list
        elif ans2 == '2':
            # builds a dictionary of ingredients needed to make
            # the week's worth of recipes
            merged_Ingredients = ingredients_Generator.merge_Ingredients()
            print('Grocery List: ', merged_Ingredients)
            ans2 = input('''Select option:
                    1 - Replace a recipe
                    2 - Show grocery list
                    3 - Add an ingredient
                    4 - Remove an ingredient
                    5 - Exit options
                    6 - Exit program ''')

        # 3 - Add an ingredient
        elif ans2 == '3':
            if bool(merged_Ingredients):
                # Allows User to add more items to the Grocery List
                merged_Ingredients = (ingredients_Generator.add_Ingredient
                                      (merged_Ingredients))
                print('Updated Grocery List: ', merged_Ingredients)
            else:
                merged_Ingredients = (ingredients_Generator.merge_Ingredients
                                      ())
                merged_Ingredients = (ingredients_Generator.add_Ingredient
                                      (merged_Ingredients))
                print('Updated Grocery List: ', merged_Ingredients)
            ans2 = input('''Select option:
                    1 - Replace a recipe
                    2 - Show grocery list
                    3 - Add an ingredient
                    4 - Remove an ingredient
                    5 - Exit options
                    6 - Exit program ''')

        # 4 - Remove an ingredient
        elif ans2 == '4':
            if bool(merged_Ingredients):
                # Allows User to remove items from the Grocery List
                merged_Ingredients = (ingredients_Generator.remove_Ingredient
                      (merged_Ingredients))
            else:
                merged_Ingredients = (ingredients_Generator.merge_Ingredients
                                      ())
                merged_Ingredients = (ingredients_Generator.remove_Ingredient
                                      (merged_Ingredients))
                print('Updated Grocery List: ', merged_Ingredients)
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
        return True

    ans3 = input('''Select option:
            1 - Show Week
            2 - Show Grocery List
            3 - Go Back to Beginning
            4 - Exit Program ''')

    while ans3 != '4':
        # 1 - Show Week
        if ans3 == '1':
            dinner_Generator.print_Week()
            ans3 = input('''Select option:
                1 - Show Week
                2 - Show Grocery List
                3 - Go Back to Beginning
                4 - Exit Program ''')

        # 2 - Show Grocery List
        elif ans3 == '2':
            print('Updated Grocery List: ', merged_Ingredients)
            ans3 = input('''Select option:
                1 - Show Week
                2 - Show Grocery List
                3 - Go Back to Beginning
                4 - Exit Program ''')
        # 3 - Go Back to Beginning
        elif ans3 == '3':
            program_UI()
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
        return True

# Run main function
program_UI()

# Closes connection to db
conn.close()

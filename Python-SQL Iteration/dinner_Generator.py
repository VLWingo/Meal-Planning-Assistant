# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:12:26 2021

@author: Tori
"""

# for use choosing recipes in the week (draw_Beef, draw_Pork, etc)
import random
# for use in find_Distribution func
import scipy.stats
# used for .literal_eval in Recipe objects and User inputs
import ast
# imports CSVtoSQL.py
import CSVtoSQL
# imports ingredients_Generator.py
import ingredients_Generator

def find_Distribution(total_days):
    '''Randomly finds a distribution (with a multinomial) of days per meat
        type according to a User preference

    Args:
        total_days: int, number of total days the User wishes to plan

    Returns:
        draw_dict: dictionary'''

    # p = pork, chicken, beef, veggie, seafood
    distribution = (scipy.stats.multinomial(total_days,
                                            p=[0.3, 0.3, 0.2, 0.2, 0]))
    # reshapes the distribution to be a vector of 1 dimension
    random_draw = distribution.rvs(1).reshape(-1)
    # recreates random_draw as a dictionary for easy access
    draw_dict = {'pork': random_draw[0], 'chicken': random_draw[1],
                 'beef': random_draw[2], 'veggie': random_draw[3],
                 'seafood': random_draw[4]}

    return draw_dict


def partial_Week_Dict(partial_week):
    '''Creates a dictionary of meat types in a submitted list

    Args:
        partial_week: list, User generated data

    Returns:
        partial_dict: dictionary, meat: days'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    partial_dict = {'pork': 0, 'chicken': 0, 'beef': 0,
                    'veggie': 0, 'seafood': 0}
    cur = conn.cursor()
    sql = ('''SELECT meat FROM recipes WHERE name=?''')
    for recipe in partial_week:
        rows = cur.execute(sql, (recipe,));
        recipe_meat = [row[0] for row in rows][0]
        partial_dict[recipe_meat] += 1
    conn.close()
    return partial_dict

def check_Distro(draw_dict):
    '''Checks the distribution to make sure it satisfies user preferences

    Args:
        draw_dict: a dictionary of the randomly chosen distribution

    Returns:
        Boolean'''

    if draw_dict['pork'] > 3:
        return False

    if draw_dict['chicken'] > 3:
        return False

    if draw_dict['beef'] > 2:
        return False

    if draw_dict['veggie'] > 2:
        return False

    if draw_dict['seafood'] > 1:
        return False

    # returns true if all checks pass
    return True


def draw_Beef(draw_dict):
    '''Chooses Recipe objects with the .meat 'beef' attribute

    Args:
        draw_dict: a dictionary of the randomly chosen distribution

    Returns:
        beef_choices: a list of names from the recipes table'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT DISTINCT name
                           FROM recipes
                           WHERE meat='beef' ''');
    # rows as a list, since rows is a table of tuples
    meat_beef = [row[0] for row in rows]
    beef_choices = []

    # randomly chooses recipes according to days assigned to beef
    while len(beef_choices) < draw_dict['beef']:
        choice = random.choice(meat_beef)
        if choice not in beef_choices:
            beef_choices.append(choice)
    conn.close()
    return beef_choices


def draw_Chicken(draw_dict):
    '''Chooses Recipe objects with the .meat 'chicken' attribute

    Args:
        draw_dict: a dictionary of the randomly chosen distribution

    Returns:
        chicken_choices: a list of names from the recipes table'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT DISTINCT name
                           FROM recipes
                           WHERE meat='chicken' ''');
    # rows as a list, since rows is a table of tuples
    meat_chicken = [row[0] for row in rows]
    chicken_choices = []

    # randomly chooses recipes according to days assigned to chicken
    while len(chicken_choices) < draw_dict['chicken']:
        choice = random.choice(meat_chicken)
        if choice not in chicken_choices:
            chicken_choices.append(choice)
    conn.close()
    return chicken_choices


def draw_Pork(draw_dict):
    '''Chooses Recipe objects with the .meat 'pork' attribute

    Args:
        draw_dict: a dictionary of the randomly chosen distribution

    Returns:
        pork_choices: a list of names from the recipes table'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT DISTINCT name
                           FROM recipes
                           WHERE meat='pork' ''');
    # rows as a list, since rows is a table of tuples
    meat_pork = [row[0] for row in rows]
    pork_choices = []

    # randomly chooses recipes according to days assigned to pork
    while len(pork_choices) < draw_dict['pork']:
        choice = random.choice(meat_pork)
        if choice not in pork_choices:
            pork_choices.append(choice)
    conn.close()
    return pork_choices


def draw_Veggie(draw_dict):
    '''Chooses Recipe objects with the .meat 'veggie' attribute

    Args:
        draw_dict: a dictionary of the randomly chosen distribution

    Returns:
        veggie_choices: a list of names from the recipes table'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT DISTINCT name
                           FROM recipes
                           WHERE meat='veggie' ''');
    # rows as a list, since rows is a table of tuples
    meat_veggie = [row[0] for row in rows]
    veggie_choices = []

    # randomly chooses recipes according to days assigned to veggie
    while len(veggie_choices) < draw_dict['veggie']:
        choice = random.choice(meat_veggie)
        if choice not in veggie_choices:
            veggie_choices.append(choice)
    conn.close()
    return veggie_choices


def draw_Seafood(draw_dict):
    '''Chooses Recipe objects with the .meat 'seafood' attribute

    Args:
        draw_dict: a dictionary of the randomly chosen distribution

    Returns:
        seafood_choices: a list of names from the recipes table'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT DISTINCT name
                           FROM recipes
                           WHERE meat='seafood' ''');
    # rows as a list, since rows is a table of tuples
    meat_seafood = [row[0] for row in rows]
    seafood_choices = []

    # randomly chooses recipes according to days assigned to seafood
    while len(seafood_choices) < draw_dict['seafood']:
        choice = random.choice(meat_seafood)
        if choice not in seafood_choices:
            seafood_choices.append(choice)
    conn.close()
    return seafood_choices


def build_Week(draw_dict):
    '''Builds a week of recipes according to the User's needs

    Args:
        draw_dict: dictionary, distribution of meal meat types

    Returns:
        Puts week into week table'''

    beef_choices = draw_Beef(draw_dict)
    pork_choices = draw_Pork(draw_dict)
    chicken_choices = draw_Chicken(draw_dict)
    veggie_choices = draw_Veggie(draw_dict)
    seafood_choices = draw_Seafood(draw_dict)

    week_list = (beef_choices + pork_choices + chicken_choices +
                 veggie_choices + seafood_choices)

    for week_recipe in week_list:
        CSVtoSQL.create_week(week_recipe)


def check_Difficulty(diff_days):
    '''Checks that the number of difficult recipes in 'week' matches the
        predetermined variable diff_days

    Args:
        diff_days: randomly drawn integer

    Returns:
        Boolean'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT difficulty
                           FROM recipes
                           WHERE name IN week ''');

    # sums the values from rows as a list, since rows is a table of tuples
    difficult_days = sum([row[0] for row in rows])
    conn.close()
    # runs the check
    if difficult_days > diff_days:
        # run the program again
        return False
    else:
        # keep the list
        return True


def check_Types():
    '''Checks that the number of recipe types in 'week' does not exceed the
        universal constraints
        'soup', 'sandwich' <= 2
        'fried rice', 'pasta', 'burgers', 'hot dog',
            'tacos'. 'curry', 'new' <= 1

    Args:

    Returns:
        Boolean'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute('''SELECT type FROM recipes WHERE name IN week''');

    # rows as a list, since rows is a table of tuples
    types = [row[0] for row in rows]
    conn.close()
    # runs the check
    if ((types.count('soup') > 2) or types.count('sandwich') > 2 or
            (types.count('stir fry') > 1) or (types.count('pasta') > 1) or
            (types.count('burgers') > 1) or (types.count('hot dog') > 1) or
            (types.count('tacos') > 1) or (types.count('curry') > 1) or
            (types.count('new') > 1)):
        return False

    return True


def check_Subtypes():
    '''Checks that the number of recipe subtypes in 'week' does not exceed the
        universal constraints
        'potato soup', 'beef stew' <= 1

    Args:

    Returns:
        Boolean'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute('''SELECT subtype FROM recipes WHERE name IN week''');
    # rows as a list, since rows is a table of tuples
    subtypes = [row[0] for row in rows]
    conn.close()
    # runs the check
    if (subtypes.count('beef stew') or subtypes.count('potato soup')) > 1:
        return False

    return True


def check_All(diff_days):
    '''Runs check_Difficulty, check_Types, and check_Subtypes

    Args:
        diff_days: randomly drawn integer

    Returns:
        a tuple of 3 Booleans'''

    diff = check_Difficulty(diff_days)
    Type = check_Types()
    Subtype = check_Subtypes()
    return (diff, Type, Subtype)


def make_Dinners():
    '''Implements functions to build a list of recipe keys that adhere to
        universal constraints

    Args:

     Returns:
         passes a week table that fulfills prerequisites'''

    # User input for total number of days to be planned
    total_days = int(input('How many days are being planned: '))
    # User input for number of days that are weekends
    ends = int(input('How many days are weekends: '))
    # Randomly generates the number of days that a recipe will require effort,
    # between 0 and number of weekend days
    diff_days = random.randint(0, ends)
    # find distribution of meat-types for the number of days requested
    draw_dict = find_Distribution(total_days)

    # while the distribution fails parameters, find a new distribution
    while not check_Distro(draw_dict):
        draw_dict = find_Distribution(total_days)
        check_Distro(draw_dict)

    # generate a week of results and place them in the week table
    build_Week(draw_dict)

    # runs 3 checks and reruns build_Week if any 1 fails
    while not all(check_All(diff_days)):
        CSVtoSQL.delete_week()
        build_Week(draw_dict)
        check_All(diff_days)


def print_Week():
    '''Prints results from make_Dinners, by providing a list object

    Args:

    Returns:
        week_list: list, representing the name column in week table'''

    conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    rows = cur.execute(''' SELECT DISTINCT name FROM week ''');
    week_list = [row[0] for row in rows]
    conn.close()
    print(week_list)


def generate_partial_week():
    ''' Generates a list of recipes that fulfill preset parameters and include
        a non-zero number of pre-chosen recipes

    Args:

    Returns:
         passes a week table that fulfills prerequisites '''


    try:
        # list version of input
        partial_week = ast.literal_eval(input(''' Provide list of recipes
                                              as ['Recipe 1', 'Recipe 2',
                                                  etc.]: '''))

        # Insert input values into week table
        for dinner in partial_week:
            CSVtoSQL.create_week(dinner)

        # in place of total_days
        remaining_days = int(input('''How many more days are
                                   you planning? '''))
        # find distribution of meat-types for the number of days requested
        draw_dict = find_Distribution(remaining_days)
        partial_dict = partial_Week_Dict(partial_week)
        total_dict = ingredients_Generator.merge_dicts(draw_dict,
                                                       partial_dict)

        conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
        cur = conn.cursor()
        diff_result = cur.execute(''' SELECT difficulty FROM recipes
                                   WHERE name IN week ''');
        partial_diff = sum([row[0] for row in diff_result])
        conn.close()

        distro_input = input(''' Do you want to ignore meat
                              distribution checks? ''')
        # while the distribution fails parameters, find a new distribution
        # if User wants
        if distro_input != 'y':
            while not check_Distro(total_dict):
                draw_dict = find_Distribution(remaining_days)
                total_dict = ingredients_Generator.merge_dicts(draw_dict,
                                                               partial_dict)
                check_Distro(total_dict)

        diff_input = int(input(''' How many more days can
                               be difficult? '''))
        diff_days = diff_input + partial_diff
        # generate the remaining week and place them in the week table
        build_Week(draw_dict)
        conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
        cur = conn.cursor()
        rows = cur.execute(''' SELECT DISTINCT name FROM week ''');
        # rows as a list, since rows is a table of tuples,
        # and without predetermined entries
        dinners = [row[0] for row in rows]
        conn.close()
        new_dinners = dinners.copy()
        for dinner in dinners:
            if dinner in partial_week:
                new_dinners.remove(dinner)

        # runs 3 checks and reruns build_Week if any 1 fails
        while not all(check_All(diff_days)):
            for dinner in new_dinners:
                print(dinner)
                CSVtoSQL.delete_week_by_name(dinner)
            build_Week(draw_dict)

            conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
            cur = conn.cursor()
            rows = cur.execute('''SELECT DISTINCT name FROM week ''');
            # rows as a list, since rows is a table of tuples,
            # and without predetermined entries
            dinners = [row[0] for row in rows]
            conn.close()
            new_dinners = dinners.copy()
            for dinner in dinners:
                if dinner in partial_week:
                    new_dinners.remove(dinner)
            check_All(diff_days)

        print_Week()

    except ValueError:
        print('Invalid submission. Try again.')
        # list version of input
        partial_week = ast.literal_eval(input(''' Provide list of recipes as
                                              ['Recipe 1', 'Recipe 2',
                                                  etc.]: '''))


def replace_Recipe():
    '''Allows User to replace a recipe in the generated list with one of
    similar difficulty and meat-type that adheres to original restrictions

    Args:

    Returns:
        Modifies the week table'''

    ans = 'y'
    while ans != 'n':
        if ans == 'y':
            try:
                # User Input
                conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
                cur = conn.cursor()
                replace_name = input('''Please write the
                                         recipe as "Recipe Name": ''')
                replace_name = ast.literal_eval(replace_name)
                replace_meat = cur.execute(''' SELECT meat FROM recipes
                                               WHERE name = ? ''',
                                            (replace_name,));
                # makes a list from a table object
                replace_meat = [row[0] for row in replace_meat]
                conn.close()
                conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
                cur = conn.cursor()
                replace_difficulty = cur.execute(''' SELECT difficulty
                                                     FROM recipes
                                                     WHERE name = ? ''',
                                                 (replace_name,));
                # makes a list from a table object
                replace_difficulty = [row[0] for row in replace_difficulty]
                conn.close()
                # Delete row in week
                CSVtoSQL.delete_week_by_name(replace_name)

                conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
                cur = conn.cursor()
                # SELECT possible recipes according to meat
                rows_meat = cur.execute('''SELECT DISTINCT name
                                           FROM recipes
                                           WHERE
                                               meat = ?''',
                                        (replace_meat));
                # create a list from table object
                possible_replace_meat = [row[0] for row in rows_meat]
                conn.close()

                conn = CSVtoSQL.create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
                cur = conn.cursor()
                # SELECT possible recipes according to difficulty
                rows_difficulty = cur.execute('''SELECT DISTINCT name
                                                  FROM recipes
                                                  WHERE
                                                      difficulty = ?''',
                                              (replace_difficulty));
                # create a list from a table object
                possible_replace_diff = [row[0] for row in rows_difficulty]
                conn.close()
                # intersects list of possible replacements
                intersection = list(set(possible_replace_meat)
                                    & set(possible_replace_diff))
                possible_replacements = intersection
                # removes the item being replaced
                possible_replacements.remove(replace_name)

                replaced = (False, False)

                # checks that replacement does not violate parameters
                while not all(replaced):
                    replacement = random.choice(possible_replacements)
                    CSVtoSQL.create_week(replacement)
                    replaced = (check_Types(),
                                check_Subtypes())

                print_Week()
                ans = input('''Do you want to replace another
                                recipe? y = yes, n = no ''')

            except ValueError:
                print('Invalid submission. Try again.')
                print_Week()
                ans = input('''Do you want to replace
                                a recipe? y = yes, n = no ''')

        else:
            print('Invalid Command. Please try again.')
            print_Week()
            ans = input('''Do you want to replace another recipe?
                        y = yes, n = no ''')

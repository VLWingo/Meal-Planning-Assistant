# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:12:26 2021

@author: Victoria Wingo
"""

# for use choosing recipes in the week (draw_Beef, draw_Pork, etc)
import random
# for use in find_Distribution func
import scipy.stats
import ingredients_Generator
from datetime import date
import csv
import pandas as pd

def find_Distribution(total_days):
    '''Randomly finds a distribution (with a multinomial) of days per meat
        type according to a User preference

    Args:
        total_days: int, number of total days the User wishes to plan

    Returns:
        draw_dict: dictionary, a randomly chosen distribution of meat types'''

    # p = pork, chicken, beef, veggie, seafood
    distribution = (scipy.stats.multinomial(total_days,
                                            p=[0.3, 0.2, 0.2, 0.2, 0.1]))
    # reshapes the distribution to be a vector of 1 dimension
    random_draw = distribution.rvs(1).reshape(-1)
    # recreates random_draw as a dictionary for easy access
    draw_dict = {'pork': random_draw[0], 'chicken': random_draw[1],
                 'beef': random_draw[2], 'veggie': random_draw[3],
                 'seafood': random_draw[4]}

    return draw_dict


def partial_Week_Dict(partial_week, recipes_df):
    '''Creates a dictionary of meat types in a submitted list

    Args:
        partial_week: list, User-generated data
        recipes_df: dataframe, read from recipes.csv

    Returns:
        partial_dict: dictionary, meat: days'''

    partial_dict = {'pork': 0, 'chicken': 0, 'beef': 0,
                    'veggie': 0, 'seafood': 0}

    for recipe in partial_week:
        recipe_meat = recipes_df['Meat'].loc[recipe]
        partial_dict[recipe_meat] += 1
    return partial_dict

def check_Distro(draw_dict):
    '''Checks the distribution to make sure it satisfies user preferences

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types

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

    # Returns true if all checks pass
    return True


def draw_Beef(draw_dict, recipes_df):
    '''Chooses Recipe objects with the .meat 'beef' attribute

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types
        recipes_df: dataframe, read from recipes.csv

    Returns:
        beef_choices: list, all names from recipes_df where Meat == beef'''

    # List of indices from recipes_df where "meat" value == "beef"
    meat_beef = list(recipes_df[recipes_df["Meat"] == "beef"].index)
    beef_choices = []

    # Randomly chooses recipes according to days assigned to beef
    while len(beef_choices) < draw_dict['beef']:
        choice = random.choice(meat_beef)
        if choice not in beef_choices:
            beef_choices.append(choice)
    return beef_choices


def draw_Chicken(draw_dict, recipes_df):
    '''Chooses Recipe objects with the .meat 'chicken' attribute

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types
        recipes_df: dataframe, read from recipes.csv

    Returns:
        chicken_choices: list, all names from recipes_df
            where Meat == Chicken'''

    # List of indices from recipes_df where "meat" value == "chicken"
    meat_chicken = list(recipes_df[recipes_df["Meat"] == "chicken"].index)
    chicken_choices = []

    # Randomly chooses recipes according to days assigned to chicken
    while len(chicken_choices) < draw_dict['chicken']:
        choice = random.choice(meat_chicken)
        if choice not in chicken_choices:
            chicken_choices.append(choice)
    return chicken_choices


def draw_Pork(draw_dict, recipes_df):
    '''Chooses Recipe objects with the .meat 'pork' attribute

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types
        recipes_df: dataframe, read from recipes.csv

    Returns:
        pork_choices: list, all names from recipes_df where Meat == Pork'''

    # List of indices from recipes_df where "meat" value == "pork"
    meat_pork = list(recipes_df[recipes_df["Meat"] == "pork"].index)
    pork_choices = []

    # Randomly chooses recipes according to days assigned to pork
    while len(pork_choices) < draw_dict['pork']:
        choice = random.choice(meat_pork)
        if choice not in pork_choices:
            pork_choices.append(choice)
    return pork_choices


def draw_Veggie(draw_dict, recipes_df):
    '''Chooses Recipe objects with the .meat 'veggie' attribute

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types
        recipes_df: dataframe, read from recipes.csv

    Returns:
        veggie_choices: list, all names from recipes_df
            where Meat == Veggie'''

    # List of indices from recipes_df where "meat" value == "veggie"
    meat_veggie = list(recipes_df[recipes_df["Meat"] == "veggie"].index)
    veggie_choices = []

    # Randomly chooses recipes according to days assigned to veggie
    while len(veggie_choices) < draw_dict['veggie']:
        choice = random.choice(meat_veggie)
        if choice not in veggie_choices:
            veggie_choices.append(choice)
    return veggie_choices


def draw_Seafood(draw_dict, recipes_df):
    '''Chooses Recipe objects with the .meat 'seafood' attribute

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types
        recipes_df: dataframe, read from recipes.csv

    Returns:
        seafood_choices: list, all names from recipes_df
            where Meat == Seafood'''

    # List of indices from recipes_df where "meat" value == "seafood"
    meat_seafood = list(recipes_df[recipes_df["Meat"] == "seafood"].index)
    seafood_choices = []

    # Randomly chooses recipes according to days assigned to seafood
    while len(seafood_choices) < draw_dict['seafood']:
        choice = random.choice(meat_seafood)
        if choice not in seafood_choices:
            seafood_choices.append(choice)
    return seafood_choices


def build_Week(draw_dict, recipes_df):
    '''Builds a week of recipes according to the User's needs

    Args:
        draw_dict: dictionary, a randomly chosen distribution of meat types
        recipes_df: dataframe, read from recipes.csv

    Returns:
        week_df: dataframe, made from choices for the week'''

    beef_choices = draw_Beef(draw_dict, recipes_df)
    pork_choices = draw_Pork(draw_dict, recipes_df)
    chicken_choices = draw_Chicken(draw_dict, recipes_df)
    veggie_choices = draw_Veggie(draw_dict, recipes_df)
    seafood_choices = draw_Seafood(draw_dict, recipes_df)

    week_list = (beef_choices + pork_choices + chicken_choices +
                 veggie_choices + seafood_choices)

    week_df = recipes_df.loc[week_list]

    return week_df


def check_Difficulty(diff_days, week_df):
    '''Checks that the number of difficult recipes in 'week' matches the
        predetermined variable diff_days

    Args:
        diff_days: int, randomly chosen with parameters
        week_df: dataframe, made from choices for the week

    Returns:
        Boolean'''

    # Sums the values of Difficulty
    difficult_days = week_df['Difficulty'].sum()

    # Runs the check
    if difficult_days > diff_days:
        # Run build_Week() again
        return False
    else:
        # Keep the list
        return True


def check_Types(week_df):
    '''Checks that the number of recipe types in 'week' does not exceed the
        universal constraints
        'soup', 'sandwich' <= 2
        everything else <= 1

    Args:
        week_df: dataframe, made from choices for the week

    Returns:
        Boolean'''


    # Histogram of Types in Week
    types = dict(week_df['Type'].value_counts())

    # Runs the check
    for key in types.keys():
        if key != 'None':
            if key != 'soup' or key != 'sandwich':
                if types[key] > 1:
                    return False
            else:
                if types[key] > 2:
                    return False
    return True


def check_Subtypes(week_df):
    '''Checks that the number of recipe subtypes in 'week' does not exceed the
        universal constraints

    Args:
        week_df: dataframe, made from choices for the week

    Returns:
        Boolean'''

    # Histogram of subtypes in Week
    subtypes = dict(week_df['Subtype'].value_counts())

    # Runs the check
    for key in subtypes.keys():
        if key != 'None':
            if subtypes[key] > 1:
                return False

    return True


def check_Frequency(week_df, saved_df):
    '''Checks that the recipes have not been chosen too recently
    according to their constraints

    Args:
        week_df: dataframe, made from choices for the week
        saved_df: dataframe, most recent 4 lines of saved entries

    Returns:
        Boolean'''

    # Histogram of past entries, up to 4 entries (approx 1 month)
    past_frequencies = dict(to_1D(saved_df['Recipes']).value_counts())

    # Run comparison check
    for recipe in week_df.index:
        if recipe in past_frequencies.keys():
            frequency = week_df['Frequency'].loc[recipe]
            if frequency <= past_frequencies[recipe]:
                return False

    return True


def to_1D(series):
    return pd.Series([x for _list in series for x in _list])


def check_All(diff_days, week_df, saved_df):
    '''Runs check_Difficulty, check_Types, check_Subtypes, and check_Frequency

    Args:
        diff_days: int, randomly chosen with parameters
        week_df: dataframe, made from choices for the week
        saved_df: dataframe, most recent 4 lines of saved entries

    Returns:
        a tuple of 4 Booleans'''

    diff = check_Difficulty(diff_days, week_df)
    Type = check_Types(week_df)
    Subtype = check_Subtypes(week_df)
    Frequency = check_Frequency(week_df, saved_df)
    return (diff, Type, Subtype, Frequency)


def make_Dinners(recipes_df, saved_df):
    '''Implements functions to build a list of recipe keys that adhere to
        universal constraints

    Args:
        recipes_df: dataframe, read from recipes.csv
        saved_df: dataframe, most recent 4 lines of saved entries

     Returns:
        week_df: dataframe, made from choices for the week'''

    total_days = int(input('How many days are being planned: '))
    ends = int(input('How many days are weekends: '))
    # Randomly generates the number of days that a recipe will require effort,
    # between 0 and number of weekend days
    diff_days = random.randint(0, ends)
    # Find distribution of meat-types for the number of days requested
    draw_dict = find_Distribution(total_days)

    # While the distribution fails parameters, find a new distribution
    while not check_Distro(draw_dict):
        draw_dict = find_Distribution(total_days)
        check_Distro(draw_dict)

    # Generate a week of results and place them in the week table
    week_df = build_Week(draw_dict, recipes_df)
    
    # Test code
    trial = 1
    print(trial, week_df.index)

    # Runs 4 checks and reruns build_Week if any 1 fails
    while not all(check_All(diff_days, week_df, saved_df)):
        week_df = build_Week(draw_dict, recipes_df)
        check_All(diff_days, week_df, saved_df)
        # Test Code
        trial += 1
        print(trial, week_df.index)

    return week_df


def generate_partial_week(recipes_df, saved_df):
    '''Generates a list of recipes that fulfill preset parameters and include
        a non-zero number of pre-chosen recipes

    Args:
        recipes_df: dataframe, read from recipes.csv
        saved_df: dataframe, most recent 4 lines of saved entries

    Returns:
        week_df: dataframe, made from choices for the week'''

    ans = 'y'
    while ans != 'n':
        try:
            ans_num = input('''How many recipes do you have? ''')
            partial_week = []
            while len(partial_week) < ans_num:
                recipe = input('''Please submit recipe: ''')
                partial_week.append(recipe)
            ans_acc = input('''Is this list correct? y - yes, n - no''',
                            partial_week)
            while ans_acc != 'y':
                if ans_acc == 'n':
                    ans_acc2 = input('''Do you want to remove or add?
                                         r - remove, a -add''')
                    while ans_acc2 != 'r' and ans_acc2 != 'a':
                        print('''Invalid submission. Please try again.''')
                        ans_acc2 = input('''Do you want to remove or add?
                                             r - remove, a -add''')
                    if ans_acc2 == 'a':
                        recipe = input('''Please submit recipe to add: ''')
                        partial_week.append(recipe)
                    else:
                        recipe = input('''Please submit recipe to remove: ''')
                        partial_week.remove(recipe)
                else:
                    print('''Invalid submission. Please try again.''')
                    ans_acc = input('''Is this list correct?
                                        y - yes, n - no''',
                                        partial_week)
                ans_acc = input('''Is this list correct? y - yes, n - no''',
                                    partial_week)

            # Build dataframe from partial_week
            partial_df = recipes_df.loc[partial_week]
            # Build dataframe as a subset of recipes_df that
            # excludes partial_df
            recipes_index = recipes_df.index
            exclusion_list = [recipe for recipe in recipes_index
                              if recipe not in partial_week]
            exclusion_df = recipes_df.loc[exclusion_list]

            # In place of total_days
            remaining_days = int(input('''How many more days are
                                           you planning? '''))
            # Find distribution of meat-types for the number of days requested
            draw_dict = find_Distribution(remaining_days)
            distro_input = input('''Do you want to ignore meat
                                      distribution checks? y = yes, n = no ''')
            # While the distribution fails parameters, find a new distribution
            # if User wants
            while distro_input != 'y':
                if distro_input == 'n':
                    partial_dict = partial_Week_Dict(partial_week, recipes_df)
                    total_dict = ingredients_Generator.merge_dicts(
                                                                draw_dict,
                                                                partial_dict
                                                                )
                    while not check_Distro(total_dict):
                        draw_dict = find_Distribution(remaining_days)
                        total_dict = ingredients_Generator.merge_dicts(
                                                                draw_dict,
                                                                partial_dict
                                                                )
                        check_Distro(total_dict)
                    break
                else:
                    print('Invalid command. Please try again.')
                    distro_input = input('''Do you want to ignore meat
                                             distribution checks?
                                             y = yes, n = no ''')

            # Handle difficulty condition
            diff_input = int(input('''How many more days can
                                       be difficult? '''))
            partial_diff = partial_df['Difficulty'].sum()
            diff_days = diff_input + partial_diff

            # Generate the remaining week and place them in the week table
            remaining_week = build_Week(draw_dict, exclusion_df)
            print(remaining_week)
            remaining_week = list(remaining_week.index)

            # Create dataframe for the week
            week = remaining_week + partial_week
            week_df = recipes_df.loc[week]

            freq_input = input('''Do you want to ignore frequency checks?
                                   y = yes, n = no ''')
            while freq_input != 'y':
                if freq_input == 'n':
                    # Runs 3 checks and reruns build_Week if any 1 fails
                    while not all(check_All(diff_days, week_df, saved_df)):
                        # Chooses another set of dinners
                        remaining_week = build_Week(draw_dict, exclusion_df)
                        # Re-form dataframe
                        remaining_week = list(remaining_week.index)
                        week = remaining_week + partial_week
                        week_df = recipes_df.loc[week]
                        check_All(diff_days, week_df, saved_df)
                    return week_df
                else:
                    print('Invalid command. Please try again.')
                    freq_input = input('''Do you want to ignore
                                           frequency checks?
                                           y = yes, n = no ''')

            if freq_input == 'y':
                diff = check_Difficulty(diff_days, week_df)
                Type = check_Types(week_df)
                Subtype = check_Subtypes(week_df)
                checks = (diff, Type, Subtype)
                while not all(checks):
                    # Chooses another set of dinners
                    remaining_week = build_Week(draw_dict, exclusion_df)
                    # Re-form dataframe
                    week = remaining_week + partial_week
                    week_df = recipes_df.loc[week]
                    checks
                return week_df

        except ValueError:
            print('Invalid submission. Please try again.')
            ans = input('''y = Try again, n = Exit to options''')


def replace_Recipe(recipes_df, week_df):
    '''Allows User to replace a recipe in the generated list with one of
    similar difficulty and meat-type that adheres to original restrictions

    Args:
        recipes_df: dataframe, read from recipes.csv
        week_df: dataframe, made from choices for the week

    Returns:
        week_df: dataframe, made from choices for the week'''

    ans = 'y'
    while ans != 'n':
        if ans == 'y':
            try:
                # Entry to be replaced
                replace_name = input('''Please submit recipe: ''')
                replace_meat = week_df['Meat'].loc[replace_name]
                replace_diff = week_df['Difficulty'].loc[replace_name]

                week_df.drop(labels=replace_name,axis=0,inplace=True)

                # Dataframe of possible replacements
                meat_replacements = recipes_df[recipes_df['Meat'] == 
                                               replace_meat]
                diff_replacements = recipes_df[recipes_df['Difficulty'] == 
                                               replace_diff]
                possible_replacements_index = list(meat_replacements.index
                                                   .intersection(
                                                       diff_replacements
                                                       .index))

                # Removes the item being replaced and any in the week
                possible_replacements_index.remove(replace_name)
                week_list = list(week_df.index)
                for dinner in week_list:
                    if dinner in possible_replacements_index:
                        possible_replacements_index.remove(dinner)

                replaced = (False, False)

                # Checks that replacement does not violate parameters
                while not all(replaced):
                    replacement = random.choice(possible_replacements_index)
                    week_list.append(replacement)
                    week_df = recipes_df.loc[week_list]
                    replaced = (check_Types(week_df),
                                check_Subtypes(week_df))
                    if not all(replaced):
                        possible_replacements_index.remove(replacement)
                        week_list.remove(replacement)

                print(week_df)
                ans = input('''Do you want to replace another
                                recipe? y = yes, n = no ''')

            except ValueError:
                print('Invalid submission. Please try again.')
                print(week_df)
                ans = input('''Do you want to replace
                                a recipe? y = yes, n = no ''')

        else:
            print('Invalid Command. Please try again.')
            print(week_df)
            ans = input('''Do you want to replace another recipe?
                            y = yes, n = no ''')

    return week_df

def user_replace_recipe(recipes_df, week_df):
    '''Allows User to replace a recipe in the generated list
        with their own choice

    Args:
        recipes_df: dataframe, read from recipes.csv
        week_df: dataframe, made from choices for the week

    Returns:
        week_df: dataframe, made from choices for the week'''

    ans = 'y'
    while ans != 'n':
        if ans == 'y':
            try:
                # Entry to be replaced
                replace_name = input('''Please submit recipe: ''')

                week_df.drop(labels=replace_name,axis=0,inplace=True)

                # Replacement
                new_name = input('''Please submit replacement recipe: ''')
                week_list = list(week_df.index)
                week_list.append(new_name)
                week_df = recipes_df.loc[week_list]
                print(week_df)
                ans = input('''Do you want to replace another recipe?
                                y = yes, n = exit to options ''')

            except ValueError:
                    print('Invalid submission. Please try again.')
                    print(week_df)
                    ans = input('''Do you want to replace a recipe?
                                    y = yes, n = exit to options ''')
        else:
            print('Invalid Command. Please try again.')
            print(week_df)
            ans = input('''Do you want to replace a recipe?
                            y = yes, n = exit to options ''')

    return week_df

def save_Week(week_df):
    '''Stores the generated week in saved_weeks.csv

    Args:
        week_df: dataframe, made from choices for the week

    Returns:
        None'''

    recipe_list = list(week_df.index)
    row = [date.today(), len(recipe_list), recipe_list]
    with open("saved_weeks.csv", "a", newline="") as f:
        # Create csv writer
        writer = csv.writer(f)

        # Write new entry to csv
        writer.writerow(row)
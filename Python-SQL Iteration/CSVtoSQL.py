# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 20:41:43 2021

@author: Tori
"""

# imports SQLite module
import sqlite3
from sqlite3 import Error
# imports csv
import csv


def create_connection(db_file):
    '''Creates a database connection to a SQLite database specified by db_file

    Args:
        db_file: database file

    Returns:
        Connection object or None'''

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(create_table_sql):
    '''Create a table from the create_table_sql statement

    Args:
        create_table_sql: a CREATE TABLE statement'''

    try:
        conn = create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
        cur = conn.cursor()
        cur.execute(create_table_sql);
    except Error as e:
        print(e)
    conn.close()


def create_recipe(recipe):
    '''Create a new recipe into the recipes table

    Args:
        recipe: table object

    Returns:
        recipe id'''

    sql = ''' INSERT INTO recipes(name,difficulty,meat,
                ingredients,type,subtype) VALUES(?,?,?,?,?,?) '''

    conn = create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    cur.execute(sql, recipe);
    conn.commit()
    conn.close()
    return cur.lastrowid


def create_ingredient(ingredient):
    '''Create a new ingredient into the ingredients table

    Args:
        ingredient: table object

    Returns:
        ingredient id'''

    sql = ''' INSERT INTO ingredients(name,unit,purchase_weight,
                average_cost,aisle,alternative_unit,alternative_weight)
                VALUES(?,?,?,?,?,?,?) '''

    conn = create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    cur.execute(sql, ingredient);
    conn.commit()
    conn.close()
    return cur.lastrowid


def create_week(week_recipe):
    '''Create a new week into the week table

    Args:
        conn: connection object
        week_recipe: object in week

    Returns:
        week id'''

    conn = create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    sql = ''' INSERT INTO week(name) VALUES(?) '''
    cur.execute(sql, (week_recipe,));
    conn.commit()
    conn.close()
    return cur.lastrowid


def delete_week():
    '''Updates the week  by deleting all rows and rerunning build_Week

    Args:

    Returns:
        passes an updated week table'''

    conn = create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    cur.execute('''DELETE FROM week''');
    conn.commit()
    conn.close()

def delete_week_by_name(entry):
    ''' Delete a task by task id

    Args:
        entry: name to identify row

    Returns:
        passes an updated week table'''

    conn = create_connection(r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db")
    cur = conn.cursor()
    cur.execute(''' DELETE FROM week WHERE name = ? ''', (entry,));
    conn.commit()
    conn.close()

def main():
    # Opens database
    database = r"C:\Users\Tori\Documents\Python Scripts\Grocery List\Python-SQL Iteration\recipe.db"

    # SQL code to create a recipes table
    sql_create_recipes_table = ''' CREATE TABLE IF NOT EXISTS recipes (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    difficulty INTEGER,
                                    meat TEXT,
                                    ingredients TEXT,
                                    type TEXT,
                                    subtype TEXT
                                );'''
    # SQL code to create an ingredients table
    sql_create_ingredients_table = '''CREATE TABLE IF NOT EXISTS ingredients (
                                    ingredient_id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    unit TEXT,
                                    purchase_weight REAL DEFAULT 0,
                                    average_cost REAL DEFAULT 0,
                                    aisle TEXT,
                                    alternative_unit TEXT,
                                    alternative_weight REAL
                                );'''
    # SQL code to create a week table
    sql_create_week_table = '''CREATE TABLE IF NOT EXISTS week (
                                name TEXT NOT NULL
                            );'''

    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(sql_create_recipes_table);

        create_table(sql_create_ingredients_table);

        create_table(sql_create_week_table);
    else:
        print("Error! Connot create the database connection.")

    with conn:
        # Reads recipes.csv into recipes table
        with open('recipes.csv', newline='') as csvfile:
            # read file
            recipe_reader = csv.reader(csvfile)

            for row in recipe_reader:
                recipe = (row)
                create_recipe(recipe)

        # Reads ingredients.csv into ingredients table
        with open('ingredients.csv', newline='') as csvfile:
            ingredient_reader = csv.reader(csvfile)
            for row in ingredient_reader:
                ingredient = (row)
                create_ingredient(ingredient)

    conn.close()


if __name__ == '__main__':
    main()

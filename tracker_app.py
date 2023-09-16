# TRACKER APP
""" This application allows a user to manage his or her budget
by tracking and managing income and expense categories and values."""

##############################################################################################################
# IMPORT LIBRARIES

import sqlite3
import os
from tabulate import tabulate

##############################################################################################################
# DATABASE FUNCTIONS

db_file = "data/tracker_db"

def create_connection(db_file):
    """Attempt connecting to budget database and return error if unable"""
    db = None
    
    try:
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        using_app = True
        
    except Exception as e:
        print(e)
        print("Could not connect to database. Exiting app. ")
        exit()
        
    # Database is closed upon exit of main menu
    return db, cursor, using_app

db, cursor, menu_status = create_connection(db_file)

def create_expense_table(db, cursor):
    """ Creates a table called 'expense_table" in the database."""
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY, category TEXT, amount REAL)''')
    initial_data = [[1,"Mortgages", 13000],
                    [2,"Electricity", 5000],
                    [3, "Food", 5200.01]]
    
    cursor.executemany('''INSERT OR REPLACE INTO expenses(id, category, amount) VALUES(?,?,?)''',initial_data)
    db.commit()

def create_income_table(db, cursor):
    """ Creates a table called 'income_table" in the database."""
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS incomes(id INTEGER PRIMARY KEY, category TEXT, amount REAL)''')
    initial_data = [[1,"Rent", 13000],
                    [2,"Art sales", 5000],
                    [3, "Salary", 20000]]
    
    cursor.executemany('''INSERT OR REPLACE INTO incomes(id, category, amount) VALUES(?,?,?)''',initial_data)
    db.commit()

create_expense_table(db, cursor)
create_income_table(db,cursor)
  
def add_category(table_name, db, cursor):
     
    """ Adds an expense category to the expenses table"""
    # REMEMBER TO ADD FAIL SAFE TRY-EXCEPT BLOCKS
    max_query = f"SELECT max(id) FROM {table_name}"
    insert_query = f"INSERT OR REPLACE INTO {table_name}(id, category, amount) VALUES(?,?,?)"
    
    new_expense = input("Please enter the expense category you would like to add:")
    cursor.execute(max_query)
    last_id = cursor.fetchone()[0]

    if last_id == None:
        last_id = 1
    else:
        last_id +=1

    new_category = [last_id, new_expense, 0]
    cursor.execute(insert_query, new_category)
    db.commit()

def remove_category(table_name, db, cursor):
    category = input("What category would you like to remove?")
    delete_query = f"DELETE FROM {table_name} WHERE category = ?"
    
    cursor.execute(delete_query, (category,))
    
    # INSERT CODE THAT CHECKS IF USER IS SURE !!!!!!!!!
    db.commit()

def update_amount(table_name, db, cursor):
    
    category = input("Specify the category where you want to update amount: ")
    
    query = f"SELECT * FROM {table_name} WHERE category = ?"
    cursor.execute(query, (category,))
    edit_item = cursor.fetchone()
    print(f"You are making changes to {edit_item[1]} and amount of R{edit_item[2]}")
    
    new_amount = float(input("Specify the new amount: "))
    
    ##### Not quire rounding correctly to database !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    new_amount = round(new_amount, 2)
    print(new_amount)
    
    update_query = f"UPDATE {table_name} SET amount = ? WHERE category = ?"
    
    print(update_query)
    print(category, new_amount)
    cursor.execute(update_query, (new_amount, category))

    db.commit()

    
def view_tables(table_name, cursor):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    table = cursor.fetchall()
    print(f"Showing entries in {table_name}:")
    
    # https://stackoverflow.com/questions/37079957/pythons-tabulate-number-of-decimal
    # Accessed 16 Sep 2023, Wanted to know how to format numbers using tabulate module
    print(tabulate(table, headers=["ID","CATEGORY","AMOUNT (RANDS)"], floatfmt=".2f"))
    print("\n")  

##############################################################################################################
# SUB MENU FUNCTIONS

def expense_menu():
    """Display the expense management sub-menu.""" 
    # INSERT FUNCTION DOCSTRING INFORMATION HERE
    
    expense_management = True
    
    while expense_management:
        
        user_choice = input('''\nWould you like to:
a - Add expense categories
u - Update expense amount
r - Remove expense category
c - View expense categories
v - View expense history
q - Exit expense management\n''').lower()
        
        if user_choice == "a":
            print("You have selected to add an expense category.") 
            add_category("expenses", db, cursor)
            view_tables("expenses", cursor)
        
            
        elif user_choice == "u":
            print("You have selected to update an expense amount.")
            update_amount("expenses", db, cursor)
            view_tables("expenses", cursor)
        
        elif user_choice == "r":
            print("You have selected to remove an expense category.")
        
            
        elif user_choice == "c":
            print("You have selected to view expense categories.")
            view_tables("expenses", cursor)
        
        elif user_choice == "v":
            print("You have selected to view your expense history.")
            
        
        elif user_choice == "q":
            print("Exiting expense management.")
            expense_management = False 

        else:
            print("Please select a valid menu option.")
    
    return user_choice

def income_menu():
    """Display the income management sub-menu.""" 
    # INSERT FUNCTION DOCSTRING INFORMATION HERE
    
    user_choice = input('''\nWould you like to:
a - Add expense categories
u - Update expense amount
r - Remove expense category
c - View income categories
v - View expense history
q - Exit expense management\n''').lower()
    
    income_management = True
    
    while income_management:
        if user_choice == "a":
            print("You have selected to add an income category.")

       
        elif user_choice == "u":
            print("You have selected to update an income amount.")

        
        elif user_choice == "r":
            print("You have selected to remove an income category.")

            
        elif user_choice == "c":
            print("You have selected to view income categories.")

        
        elif user_choice == "v":
            print("You have selected to view your income history.")

        
        elif user_choice == "q":
            print("Exiting income management.")
            income_management = False 

        else:
            print("Please select a valid menu option.")
    
    return user_choice 

##############################################################################################################
# MAIN MENU

menu_status = True

user_choice = ""

while menu_status:
    user_choice = input('''\nMain Menu Options:
e - View expense management menu
i - View income management menu
b - View budget summary
q - Exit 

Enter selection:\n''').lower()
    
    if user_choice == "e":
       print("You have selected the expense menu.") 
       user_choice = expense_menu()
       
    elif user_choice == "i":
        print("You have selected the income menu.") 
        user_choice = income_menu()
        
    elif user_choice == "b":
        print("You have selected to view your budget summary.") 
        
    elif user_choice == "q":
        menu_status = False
        print("Good bye!")
        db.close()
    
    else:
        print("Please select a valid menu option.")
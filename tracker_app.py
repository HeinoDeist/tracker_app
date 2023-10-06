# TRACKER APP
""" This application allows a user to manage his or her budget
by tracking and managing income and expense categories and values.
This app has been version controlled and can be accessed at:
https://github.com/HeinoDeist/tracker_app
"""

# To do
# 1 - try-except blocks for SQL code
# 2 - Menu options to be verified
# 3 - Write Sphinx documentation
# 4 - Testing

##############################################################################################################
# IMPORT LIBRARIES

""" Import sqlite3 and tabulate libraries. Sqlite3 performs database manipulation
and tabulate is used to represent output in neat and readable format.
"""
import sqlite3
from tabulate import tabulate

##############################################################################################################
# DATABASE FUNCTIONS

# Reference the path to the database file.
db_file = "data/tracker_db"


def create_connection(db_file):
    """Attempt connecting to budget database and return error if unable.
    :param db: Database object
    :param cursor: Cursor object
    :param bool using_app: Indicates whether app is in use
    :raises Exception: Raises error when unable to connect
    :returns: Active database connection, cursor and app_status is True
    """
    
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

# Assign variable and objects by calling create_connection function.
db, cursor, menu_status = create_connection(db_file)

def create_expense_table(db, cursor):
    """ Creates a table called 'expense_table' in the database if nothing currently exists
    or ignores if table does exist.
    :param list initial_data: Dummy-data to initialise table
    :returns: Expense table created in database 'db'
    """
    
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY, category TEXT, amount REAL)''')
        initial_data = [[1,"None", 0]]
    
        # https://stackoverflow.com/questions/29721656/most-efficient-way-to-do-a-sql-insert-if-not-exists
        # Accessed 29 Sep 2023, How to ignore if data already exists. 
        cursor.executemany('''INSERT OR IGNORE INTO expenses(id, category, amount) VALUES(?,?,?)''',initial_data)
        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unexpected error. Table might already exist")

def create_income_table(db, cursor):
    """ Creates a table called 'income_table" in the database if nothing currently exists
    or ignores if table does exist
    param list initial_data: Dummy-data to initialise table.
    :returns: Income table created in database 'db'
    """
    
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS incomes(id INTEGER PRIMARY KEY, category TEXT, amount REAL)''')
        initial_data = [[1,"None", 0]]
    
        cursor.executemany('''INSERT OR IGNORE INTO incomes(id, category, amount) VALUES(?,?,?)''',initial_data)
        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unexpected error. Table might already exist")

create_expense_table(db, cursor)
create_income_table(db,cursor)

def add_category(table_name, db, cursor):
    """ Adds a category to either an income or expense table
    :param str table_name: Name of the table where category is added
    :param str new_addition: Name of new income or expense category 
    :param str max_query: Query string to find last row
    :param str status_query: Query string used to find category name that matches id
    :param str insert_query: Query string that runs to insert new row
    :param int last_id: Value assigned to last entry primary key in the database table
    :returns: A new income or expense category added to either the income or expense table
    """
    
    max_query = f"SELECT max(id) FROM {table_name}"
    status_query = f"SELECT * FROM {table_name} WHERE id = ?"
    insert_query = f"INSERT OR REPLACE INTO {table_name}(id, category, amount) VALUES(?,?,?)"
    
    new_addition = None
    
    try: 
        new_addition = input("Please enter the expense category you would like to add:")
        cursor.execute(max_query)
        last_id = cursor.fetchone()[0]
        last_id = int(last_id)
        cursor.execute(status_query,(last_id,))
        table_status = cursor.fetchone()[1]
        
        # Check if last primary key (id) corresponds to the initial default value
        # If it's 'None' then replace, otherwise add a new row.
        if last_id == 1 and table_status == "None":
            new_category = [last_id, new_addition, 0]
            cursor.execute(insert_query, new_category)
            
        else:
            last_id +=1
            new_category = [last_id, new_addition, 0]
            cursor.execute(insert_query, new_category)

        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to create category.")

def remove_category(table_name, db, cursor):
    """ Removes an income or expense category from either the income or expense table
    
    """
    category = None
    
    try:
        category = input("What category would you like to remove?")
        delete_query = f"DELETE FROM {table_name} WHERE category = ?"
        
        cursor.execute(delete_query, (category,))
        
        # INSERT CODE THAT CHECKS IF USER IS SURE !!!!!!!!!
        print(f"You have removed category: {category} from {table_name}. ")
        
        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to remove category.")

def update_amount(table_name, db, cursor):
    print("Displaying category items:")
    view_tables(table_name, cursor)
    
    category = None
    
    try:
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
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to update.")

def view_tables(table_name, cursor):
    """ Views both expense or income tables in net format."""
    
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    table = cursor.fetchall()
    print(f"Showing entries in {table_name}:")
    
    # https://stackoverflow.com/questions/37079957/pythons-tabulate-number-of-decimal
    # Accessed 16 Sep 2023, Wanted to know how to format numbers using tabulate module
    print(tabulate(table, headers=["ID","CATEGORY","AMOUNT (RANDS)"], floatfmt=".2f"))
    print("\n")  

def budget_summary(income_table, expense_table, db, cursor):
    """ Function calculates difference between income and spend and outputs result."""
    
    query_total_income = f"SELECT Total(amount) FROM {income_table}"
    query_total_expenses = f"SELECT Total(amount) FROM {expense_table}"
    
    try: 
        cursor.execute(query_total_income)
        total_income = cursor.fetchone()[0]
        total_income = format(float(total_income), ".2f")
        
        cursor.execute(query_total_expenses)
        total_expenses = cursor.fetchone()[0]
        total_expenses = format(float(total_expenses),".2f")

        budget = format(float(total_income) - float(total_expenses), ".2f")
        budget = f"R{budget}"
        total_income = f"R{total_income}"
        total_expenses = f"R{total_expenses}"
        
        table = [["Income:", total_income],
                ["Expenses:", total_expenses],
                ["Budget", budget]]
        
        print(tabulate(table, headers = ["CATEGORY", "AMOUNT (Rands)"]))
    
    except Exception as error_msg:
        print("Unable to extract budget summary.")


##############################################################################################################
# SUB MENU FUNCTIONS

def expense_menu():
    """ Display the expense management sub-menu.""" 
    # INSERT FUNCTION DOCSTRING INFORMATION HERE
    
    expense_management = True
    
    while expense_management:
        
        user_choice = input('''\nWould you like to:
a - Add expense categories
u - Update expense amount
r - Remove expense category
c - View expense categories and amounts
v - View expense summary and total
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
            remove_category("expenses", db, cursor)
            view_tables("expenses", cursor)
            
        elif user_choice == "c":
            print("You have selected to view expense categories.")
            view_tables("expenses", cursor)
        
        elif user_choice == "v":
            print("You have selected to view your expense history.")
            view_tables("expenses", cursor)           
        
        elif user_choice == "q":
            print("Exiting expense management.")
            expense_management = False 

        else:
            print("Please select a valid menu option.")
    
    return user_choice

def income_menu():
    """ Display the income management sub-menu.""" 
    # INSERT FUNCTION DOCSTRING INFORMATION HERE
    
    income_management = True
    
    while income_management:
        user_choice = input('''\nWould you like to:
a - Add income categories
u - Update income amount
r - Remove income category
c - View income categories and amounts
v - View income summary and total
q - Exit expense management\n''').lower()
        if user_choice == "a":
            print("You have selected to add an income category.")
            add_category("incomes", db, cursor)
            view_tables("incomes", cursor)
       
        elif user_choice == "u":
            print("You have selected to update an income amount.")
            update_amount("incomes", db, cursor)
            view_tables("incomes", cursor)
        
        elif user_choice == "r":
            print("You have selected to remove an income category.")
            remove_category("incomes", db, cursor)
            view_tables("incomes", cursor)
            
        elif user_choice == "c":
            print("You have selected to view income categories.")
            view_tables("incomes", cursor)
        
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

menu_status = True      # User changes status to False when selecting 'Exit' option. 

user_choice = ""

# Loops over menu options and enters sub-menu items based on selection. 
while menu_status:
    user_choice = input('''\nMain Menu Options:
e - View expense management menu
i - View income management menu
b - View budget summary
q - Exit 

Enter selection:\n''').lower()
    
    if user_choice == "e":
       print("You have selected the expense menu.") 
       user_choice = expense_menu()         # Calls the expense sub-menu function. 
       
    elif user_choice == "i":
        print("You have selected the income menu.") 
        user_choice = income_menu()         # Calls the income sub-menu function. 
        
    elif user_choice == "b":
        print("You have selected to view your budget summary.") 
        budget_summary("incomes","expenses", db, cursor)        # Calls the budget summary function
        
    elif user_choice == "q": 
        # Set menu_status to false on exit to exit menu while-loop and programme.    
        menu_status = False
        print("Exiting programme. Good bye!")
        db.close()
    
    else:
        print("Please select a valid menu option.")
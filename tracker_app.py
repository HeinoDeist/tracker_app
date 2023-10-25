# TRACKER APP
""" This application, developed using only the finest key-strokes,
allows a user to manage his or her budget by tracking and managing 
income and expense categories and values. It also allows the user to
specify goals (or targets) per category and track progress towards 
overall financial goals.
This app has been version controlled and can be accessed at:
https://github.com/HeinoDeist/tracker_app

"""

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
    :raises Exception: Raises error when unable to create table and does db rollback.
    :returns: Expense table created in database 'db' and commits db
    """
    
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY, category TEXT, actual REAL, budget REAL)''')
        initial_data = [[1,"None", 0, 0]]
    
        # https://stackoverflow.com/questions/29721656/most-efficient-way-to-do-a-sql-insert-if-not-exists
        # Accessed 29 Sep 2023, How to ignore if data already exists. 
        cursor.executemany('''INSERT OR IGNORE INTO expenses(id, category, actual, budget) VALUES(?,?,?,?)''',initial_data)
        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unexpected error. Table might already exist")


def create_income_table(db, cursor):
    """ Creates a table called 'income_table" in the database if nothing currently exists
    or ignores if table does exist
    param list initial_data: Dummy-data to initialise table.
    :returns: Income table created in database 'db' and commits db
    """
    
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS incomes(id INTEGER PRIMARY KEY, category TEXT, actual REAL, budget REAL )''')
        initial_data = [[1,"None", 0, 0]]
    
        cursor.executemany('''INSERT OR IGNORE INTO incomes(id, category, actual, budget) VALUES(?,?,?,?)''',initial_data)
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
    insert_query = f"INSERT OR REPLACE INTO {table_name}(id, category, actual, budget) VALUES(?,?,?,?)"
    
    new_addition = None
    
    try: 
        
        check_query = f"SELECT category FROM {table_name}"
        cursor.execute(check_query)
        category_list = cursor.fetchall()
        clean_category_list = [item[0] for item in category_list]
        
        while True:
            # Implementing loop to ensure user enters category that does not already exist
            new_addition = input("Please enter the category you would like to add:")
            if new_addition in clean_category_list:
                # The user might want to change fonts to assign different meaning to the category
                print(f"That category already exists in {table_name}. Change the category or font.")
            else:
                break
        
        cursor.execute(max_query)
        last_id = cursor.fetchone()[0]
        last_id = int(last_id)
        cursor.execute(status_query,(last_id,))
        table_status = cursor.fetchone()[1]
        
        # Check if last primary key (id) corresponds to the initial default value
        # If it's 'None' then replace, otherwise add a new row.
        if last_id == 1 and table_status == "None":
            new_category = [last_id, new_addition, 0, 0]
            cursor.execute(insert_query, new_category)
            
        else:
            last_id +=1
            new_category = [last_id, new_addition, 0, 0]
            cursor.execute(insert_query, new_category)

        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to create category.")


def remove_category(table_name, db, cursor):
    """ Removes an income or expense category from either the income or expense table
    :param str category: Name of category to be removed from table
    :param str delete_query: String query to delete category from given table name
    :param str table_name: Name of relevant table to be modified in the database
    :raises Exception: Error raised when unable to execute query or find category and does db rollback
    :returns: Income or expense table where relevant category has been removed and commits database
    """
    category = None
    
    try:
        category = input("What category would you like to remove?")
        delete_query = f"DELETE FROM {table_name} WHERE category = ?"
        
        user_confirm = input(f"Are you sure you want to remove: {category}?. Type 'Y' to confirm, or anything else to abort.").lower()
        
        if user_confirm == "y":  
            cursor.execute(delete_query, (category,))
            print(f"You have removed category: {category} from {table_name}. ")
            db.commit()
        else:
            print("No changes made.")
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to remove category.")


def update_actual(table_name, db, cursor):
    """ Changes the amount currently allocated to an income or expense item
    :param str table_name: Name of relevant income or expense table to be modified
    :param str category: Name of category where amount is to be updated
    :param str query: String query to select data from table specified
    :param float new_actual: The updated amount to be allocated to the expense or income item
    :param str update_query: Query string to set new values for specified category and table
    :raises Exception: Error message when unable to update amount and does db rollback
    :returns: Updated income or expense amount in relevant table and commits db
    """ 

    print("Displaying category items:")
    view_tables(table_name, cursor)
    
    category = None
    
    try:
        category = input("Specify the category where you want to update amount: ")
        query = f"SELECT * FROM {table_name} WHERE category = ?"
        cursor.execute(query, (category,))
        edit_item = cursor.fetchone()
        print(f"You are making changes to {edit_item[1]} and amount of R{edit_item[2]}")
        
        while True:
            try:
                new_actual = float(input("Specify the new amount: "))
                break
            except Exception:
                print("Please enter a valid number.")
        
        new_actual = round(new_actual, 2)
        update_query = f"UPDATE {table_name} SET actual = ? WHERE category = ?"
        cursor.execute(update_query, (new_actual, category))
        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to update. Please enter a valid category (case sensitive).")


def update_goal(table_name, db, cursor):
    """ This function allows a user to enter goals, i.e.: budgets for expenses
    and targets for income categories
    :param str table_name: Name of relevant income or expense table to be modified
    :param str category: Name of category where amount is to be updated
    :param str query: String query to select data from table specified
    :param float new_target: The updated budget / target value to be allocated to the category
    :param str update_query: Query string to set new target for specified category and table
    :raises Exception: Error message when unable to update amount and does db rollback
    :returns: Updated income or expense target in relevant table and commits db
    """
    
    print("Displaying category items:")
    view_tables(table_name, cursor)
    
    category = None
    
    try:
        category = input("Specify the category where you want to update goals: ")
        query = f"SELECT * FROM {table_name} WHERE category = ?"
        cursor.execute(query, (category,))
        edit_item = cursor.fetchone()
        print(f"You are making changes to {edit_item[1]} and current target of R{edit_item[3]}")
        
        while True:
            try:
                new_target = float(input("Specify the new target value: "))
                break
            except Exception:
                print("Please enter a valid number.")
        
        new_target = round(new_target, 2)
        update_query = f"UPDATE {table_name} SET budget = ? WHERE category = ?"
        cursor.execute(update_query, (new_target, category))
        db.commit()
        
    except Exception as error_msg:
        db.rollback()
        print("Unable to update. Please enter a valid category (case sensitive).")


def view_tables(table_name, cursor):
    """ Views both expense or income tables in net format.
    :param str table_name: Name of table to be displayed
    :param str query: String query to retrieve all data from specified table
    :param str get_total: String query to get total of amounts
    :returns: Tabulate table categories and amounts in readable format
    """
    
    query = f"SELECT * FROM {table_name}"
    get_total_actual = f"SELECT Total(actual) from {table_name}"
    get_total_budget = f"SELECT Total(budget) from {table_name}"
    
    cursor.execute(query)
    table = cursor.fetchall()
    
    cursor.execute(get_total_actual)
    actual_total = cursor.fetchone()[0]
    actual_total = format(float(actual_total), ".2f")
    
    cursor.execute(get_total_budget)
    budget_total = cursor.fetchone()[0]
    budget_total = format(float(budget_total), ".2f")
    
    table.append(["","TOTAL",actual_total, budget_total])
        
    print(f"Showing entries in {table_name}:")
    
    # https://stackoverflow.com/questions/37079957/pythons-tabulate-number-of-decimal
    # Accessed 16 Sep 2023, Wanted to know how to format numbers using tabulate module
    print(tabulate(table, headers=["ID","CATEGORY","ACTUAL (RANDS)","BUDGET (RANDS)"], floatfmt = ".2f"))
    print("\n")  


def budget_summary(income_table, expense_table, db, cursor):
    """ Function calculates difference between income and spend and outputs result.
    :param str query_total_income: Query to calculate total from income table
    :param str query_total_expenses: Query to calculate total from expenses table
    :param float total_income: Sum of all income categories formatted to two decimals
    :param float total_expenses: Sum of all expense categories formatted to two decimals
    :param float budget: Difference between income and expense categories
    :param list table: Prepares budget item summary for tabulate function
    :raises Exception: Raises error message when unable to perform queries
    :returns: Visual output of budget summary table
    """
    
    query_total_income = f"SELECT Total(actual) FROM {income_table}"
    query_budget_income = f"SELECT Total(budget) FROM {income_table}"
    
    query_total_expenses = f"SELECT Total(actual) FROM {expense_table}"
    query_budget_expenses = f"SELECT Total(budget) FROM {expense_table}"
    
    try: 
        cursor.execute(query_total_income)
        total_income = cursor.fetchone()[0]
        total_income = format(float(total_income), ".2f")
        
        cursor.execute(query_budget_income)
        budget_income = cursor.fetchone()[0]
        budget_income = format(float(budget_income), ".2f")
        
        cursor.execute(query_total_expenses)
        total_expenses = cursor.fetchone()[0]
        total_expenses = format(float(total_expenses),".2f")
            
        cursor.execute(query_budget_expenses)
        budget_expenses = cursor.fetchone()[0]
        budget_expenses = format(float(budget_expenses),".2f")


        income_variance = format(float(total_income) - float(budget_income), ".2f")
        expense_variance = format(float(budget_expenses) - float(total_expenses), ".2f")
        actual_difference = format(float(total_income) - float(total_expenses), ".2f")
        budget_difference = format(float(budget_income) - float(budget_expenses), ".2f")
        savings_variance = format(float(actual_difference) - float(budget_difference),".2f")
            
        table = [["Income:", total_income, budget_income, income_variance],
                ["Expenses:", total_expenses, budget_expenses, expense_variance],
                ["Savings", actual_difference, budget_difference, savings_variance]]
            
        print(tabulate(table, headers = ["Category", "Actual (Rands)", "Budget (Rands)", "Variance (Rands)"], floatfmt = ".2f"))
    
        if income_variance < 0:
            print(f"You have earned R{-income_variance} less than planned.")
        elif income_variance > 0:
            print(f"You have earned R{-income_variance} more than planned. Great!!")
        elif income_variance == 0:
            print("Your income is exactly as planned. Spot on!")
            
        if expense_variance > 0:
            print(f"You have managed to save R{expense_variance} on your expenses! You're on track!")
        elif expense_variance < 0:
            print(f"Careful! You have spent R{-expense_variance} more than budgeted!")
        elif expense_variance == 0:
            print("Your spending matches your budget.")
            
        if savings_variance < 0:
            print(f"Between income and expenses, you are R{-savings_variance} behind your goal!")
        elif savings_variance > 0:
            print(f"Between income and expenses, you are R{savings_variance} ahead of your goal! Keep going!")
        elif savings_variance == 0:
            print("You are breaking even in terms of your goals. ")
    
    except Exception as error_msg:
        print("Unable to extract budget summary.")


##############################################################################################################
# SUB MENU FUNCTIONS


def expense_menu():
    """ Display the expense management sub-menu.
    :param bool expense_management: Indicates true when menu is active
    :param str user_choice: Selected menu option
    :returns: The menu option selected by the user
    """ 
    
    expense_management = True
    
    # Loop stays in expense management sub-menu until exited.
    while expense_management:
        
        user_choice = input('''\nWould you like to:
a - Add expense categories
u - Update expense amount (actual)
g - Update expense budget
r - Remove expense category
v - View expense categories, amounts and total
q - Exit expense management\n''').lower()
        
        if user_choice == "a":
            print("You have selected to add an expense category.") 
            add_category("expenses", db, cursor)
            view_tables("expenses", cursor)
        
        elif user_choice == "u":
            print("You have selected to update an expense amount.")
            update_actual("expenses", db, cursor)
            view_tables("expenses", cursor)
            
        elif user_choice == "g":
            print("You have selected to enter a new budget for an item.")
            update_goal("expenses", db, cursor)
            view_tables("expenses",cursor)
        
        elif user_choice == "r":
            print("You have selected to remove an expense category.")
            remove_category("expenses", db, cursor)
            view_tables("expenses", cursor)
        
        elif user_choice == "v":
            print("You have selected to view your expense summary.")
            view_tables("expenses", cursor)           
        
        elif user_choice == "q":
            print("Exiting expense management.")
            expense_management = False 

        else:
            # Activates when no valid menu option is selected
            print("Please select a valid menu option.")
    
    return user_choice


def income_menu():
    """ Display the income management sub-menu.
    :param bool income_management: Indicates true when menu is active
    :param str user_choice: Selected menu option
    :returns: The menu option selected by the user
    """ 
    # INSERT FUNCTION DOCSTRING INFORMATION HERE
    
    income_management = True
    
    # Loop stays in income management menu until exited.
    while income_management:
        user_choice = input('''\nWould you like to:
a - Add income categories
u - Update income amount
g - Update income targets
r - Remove income category
v - View income categories, amounts and total
q - Exit income management\n''').lower()
        
        if user_choice == "a":
            print("You have selected to add an income category.")
            add_category("incomes", db, cursor)
            view_tables("incomes", cursor)
       
        elif user_choice == "u":
            print("You have selected to update an income amount.")
            update_actual("incomes", db, cursor)
            view_tables("incomes", cursor)
            
        elif user_choice == "g":
            print("You have selected to enter a new target for an income category.")
            update_goal("incomes", db, cursor)
            view_tables("incomes",cursor)
        
        elif user_choice == "r":
            print("You have selected to remove an income category.")
            remove_category("incomes", db, cursor)
            view_tables("incomes", cursor)
        
        elif user_choice == "v":
            print("You have selected to view your income summary.")
            view_tables("incomes", cursor)
        
        elif user_choice == "q":
            print("Exiting income management.")
            income_management = False 

        else:
            # Activates when no valid menu option is selected
            print("Please select a valid menu option.")
    
    return user_choice 


##############################################################################################################
# MAIN MENU


''' Main Menu provides user with options to enter expense or income menus, 
view budget summary or quit programme.'''

menu_status = True      # User changes status to False when selecting 'Exit' option. 

user_choice = ""

# Loops over menu options and enters sub-menu items based on selection. 
while menu_status:
    user_choice = input('''\nMain Menu Options:
e - View expense management menu
i - View income management menu
b - View progress against goals
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
        # Activates when no valid menu options are selected
        print("Please select a valid menu option.")


##############################################################################################################
# END OF CODE     

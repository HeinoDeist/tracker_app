#---Tracker App---#
""" This application allows a user to manage his or her budget
by tracking and managing income and expense categories and values."""

def expense_menu():
    """Display the expense management sub-menu.""" 
    # INSERT FUNCTION DOCSTRING INFORMATION HERE
    
    user_choice = input('''\nWould you like to:
a - Add expense categories
u - Update expense amount
r - Remove expense category
c - View expense categories
v - View expense history
q - Exit expense management''').lower()
    
    expense_management = True
    
    while expense_management:
        if user_choice == "a":
            print("You have selected to add an expense category.") 
       
        elif user_choice == "u":
            print("You have selected to update an expense amount.") 
        
        elif user_choice == "r":
            print("You have selected to remove an expense category.")
            
        elif user_choice == "c":
            print("You have selected to view expense categories.") 
        
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
q - Exit expense management''').lower()
    
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
            expense_management = False 

        else:
            print("Please select a valid menu option.")
    
    return user_choice 

menu_status = True

while menu_status:
    user_choice = input('''\nWould you like to:
e - View expense management menu
i - View income management menu
b - View budget summary
q - Exit 

Enter selection:''').lower()
    
    if user_choice == "e":
       print("You have selected the expense menu.") 
       
    elif user_choice == "i":
        print("You have selected the income menu.") 
        
    elif user_choice == "b":
        print("You have selected to view your budget summary.") 
        
    elif user_choice == "q":
        menu_status = False
        print("Good bye!")
    
    else:
        print("Please select a valid menu option.")
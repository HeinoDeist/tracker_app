#---Tracker App---#
""" This application allows a user to manage his or her budget
by tracking and managing income and expense categories and values"""

menu_status = True

while menu_status:
    user_choice = input('''\nWould you like to:
a - Add expense categories
u - Update expense amount
d - Remove expense category
s - View expense history
i - Add income categories
r - Remove an income category
v - View income history
w - View income and expense categories
b - Calculate budget
q - Quit the budget app

Enter selection:''')
    
    if user_choice == "a":
       print("You have selected to add an expense category.") 
       
    elif user_choice == "u":
        print("You have selected to update an expense amount.") 
        
    elif user_choice == "d":
        print("You have selected to remove an expense category.") 
        
    elif user_choice == "s":
        print("You have selected to view your expense history.") 
        
    elif user_choice == "i":
        print("You have selected to add income categories.") 
        
    elif user_choice == "r":
        print("You have selected to remove an income category.") 
        
    elif user_choice == "v":
        print("You have selected to view income history.") 
        
    elif user_choice == "w":
        print("You have selected to view income and expense categories.") 
        
    elif user_choice == "b":
        print("You have selected to calculate your budget.") 
        
    elif user_choice == "q":
        menu_status = False
        print("Good bye!")
    
    else:
        print("Please select a valid menu option.")
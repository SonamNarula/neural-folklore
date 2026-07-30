"""
Topic: If Statements
Section: Control Flow
Description:
Demonstrates conditional logic using if, elif, and else statements
to handle user input, validate conditions, and control program flow.
"""

# ----- Asking User For thier age -----

age = int(input("Enter Your age: "))

if age >= 100:
    print("You are too old to signed up!")
elif age < 0:
    print("You haven't been born yet!")
elif age >= 18:
    print("You are now signed up!")
else:
    print("You must be 18+ to sign up")   
    
# ----- Asking User For like food -----
response = input("Would you like food? (Y/N): ")
if response == "Y":
    print("Have some food")
elif response == "N":
    print("No food for you!")
else:
    print("Print valid Value")
    
# ----- Asking User For name -----
name = input("Enter your name: ")

if name == "":
    print("You didn't type in your name!")
else:
    print(f"Hello {name}")
    
# ----- Check for sale -----
for_sale = True
if for_sale:
    print("This item is for sale")
else:
    print("This item is not for sale")
    
# ----- Check for Online -----
online = False
if online:
    print("The user is Online")
else:
    print("The user is Offline")
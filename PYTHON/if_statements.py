"""
Topic: If Statements
Section: Control Flow
Description:
Demonstrates conditional logic using if, elif, and else statements
to handle user input, validate conditions, and control program flow.
"""

# ----- Asking user for their age -----

age = int(input("Enter Your age: "))

if age >= 100:
    print("You are too old to sign up!")
elif age < 0:
    print("You haven't been born yet!")
elif age >= 18:
    print("You are now signed up!")
else:
    print("You must be 18+ to sign up")
    
# ----- Asking user if they would like food -----
response = input("Would you like food? (Y/N): ").upper()
if response == "Y":
    print("Have some food")
elif response == "N":
    print("No food for you!")
else:
    print("Please enter a valid value")
    
# ----- Asking user for their name -----
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
    
# ----- Check for online status -----
online = False
if online:
    print("The user is online")
else:
    print("The user is offline")

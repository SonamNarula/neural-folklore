"""
Topic: String Methods
Section: Fundamentals
Description:
Demonstrates common string methods including:
len(), find(), rfind(), capitalize(), upper(), lower(),
isdigit(), isalpha(), count(), and replace()
to manipulate and validate user input.
"""

name = input("Enter your full name: ")

# ----- len() function (gives length of string) -----
result = len(name)
print(f"Length: {result}")

# ----- string.find() function (gives position of first occurrence of given character else -1) -----
result = name.find(" ")
print(f"First occurrence position of ' ': {result}")

# ----- string.rfind() function (gives position of last occurrence of given character else -1) -----
result = name.rfind("a")
print(f"Last occurrence position of 'a': {result}")

# ----- capitalize function (capitalize first letter of word) -----
result = name.capitalize()
print(f"Before: {name} After: {result}")

# ----- upper function (Uppercase all the alphabets) -----
result = name.upper()
print(f"Before: {name} After: {result}")

# ----- lower function (lowercase all the alphabets) -----
result = name.lower()
print(f"Before: {name} After: {result}")

# ----- isdigit() function (returns true or false if there are only digits) -----
result = name.isdigit()
print(f"Contains only digits: {result}")

# ----- isalpha() function (returns true or false if there are only alphabetical characters) -----
result = name.isalpha()
print(f"Contains only alphabets: {result}")

phone_number = input("Enter phone number: ")

# ----- count() function (returns count of given character) -----
result = phone_number.count("-")
print(f"Number of '-': {result}")

# ----- replace(from, to) function (returns string replacing the given value) -----
result = phone_number.replace("-", "#")
print(f"Before: {phone_number} After: {result}")

# ----- help(str) function (returns comprehensive list of all of the string methods available) -----
# print(help(str))

# --------------------------------------------------------------

# ----- Exercise 1: Validate User Input -----
# 1. username is no more than 12 characters  
# 2. username must not contain spaces  
# 3. username must not contain digits

user_name = input("Enter the name of user: ")

if user_name == "":
    print("You haven't entered a username.")
elif len(user_name) > 12:
    print(f"{user_name} must be no more than 12 characters")
elif user_name.find(" ") != -1:
    print(f"{user_name} must not contain spaces.")
elif not user_name.isalpha():
    print(f"{user_name} must not contain digits.")
else:
    print(f"Welcome {user_name}")

"""
Topic: Conditional Expressions
Section: Control Flow
Description:
- A one-line shortcut for the if-else statement (ternary operator)
- Print or assign one of two values based on a condition
- X if condition else Y
"""

# ----- Check positive or negative -----
num = 5
print("Positive" if num > 0 else "Negative")

# ----- Check even or odd -----
num = 5
print("Even" if num % 2 == 0 else "Odd")

# ----- Check maximum and minimum -----
a = 7
b = 3
print(f"Maximum: {a if a > b else b}")
print(f"Minimum: {a if a < b else b}")

# ----- Check adult status -----
age = 9
status = "Adult" if age >= 21 else "Not Adult"
print(f"Age: {age} Status: {status}")

# ----- Check hot or cold -----
temperature = 30
weather = "Hot" if temperature > 20 else "Cold"
print(f"Temperature: {temperature} Weather: {weather}")

# ----- Check access -----
user_mode = "guest"
access_level = "Full Access" if user_mode == "admin" else "Limited Access"
print(f"User Mode: {user_mode} Access Level: {access_level}")

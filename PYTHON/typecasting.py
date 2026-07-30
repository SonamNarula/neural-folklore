"""
Topic: Type casting
Section: Fundamentals
Description:
Typecasting = the process of converting a variable from one data type to another.
Common conversion functions include str(), int(), float(), and bool().
"""

name = ""
age = 21
gpa = 3.8
is_student = True


# to get the data type of variable `type(variable name)`

print(type(name))  # string
print(type(age))  # integer
print(type(gpa))  # float
print(type(is_student))  # boolean

# ---- Float to Integer ----
gpa = int(gpa)
print(f"Value: {gpa} Data-type: {type(gpa)}")

# ---- Integer to Float ----
age = float(age)
print(f"Value: {age} Data-type: {type(age)}")

# ---- Integer to String ----
age = str(age)
print(f"Value: {age} Data-type: {type(age)}")

# string concatenation
age += "1"
print(f"Age becomes {age}")

# ---- String to Boolean ----
name = bool(name)
print(f"Is there a name: {name}")

# ---- Integer to Boolean ----
num = 0
num = bool(num)
print(f"Value: {num} Data-type: {type(num)}")

# ---- Boolean to String ----
num = str(num)
print(f"Value: {num} Data-type: {type(num)}")

# ---- Boolean to Integer ----
num2 = True
num2 = int(num2)
print(f"Value: {num2} Data-type: {type(num2)}")

# ---- Boolean to Float ----
num2 = float(num2)
print(f"Value: {num2} Data-type: {type(num2)}")

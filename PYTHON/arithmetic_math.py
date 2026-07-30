"""
Topic: Arithmetic Operators & Math Module
Section: Fundamentals
Description:
Covers basic arithmetic operations, augmented assignment operators,
built-in math functions, and practical exercises using the math module
such as calculating circle measurements and triangle hypotenuse.
"""

import math

# arithmetic operators
# math functions
# exercise

# 1: Basic Arithmetic Operations
# ------Addition------
friend = 0
friend = friend + 1
friend += 1  # augmented assignment operator

# ------Subtraction------
friend = friend - 2
friend -= 2  # augmented assignment operator

# ------Multiplication------
friend = friend * 3
friend *= 3

# ------Division------
friend = friend / 2
friend /= 2  # augmented assignment operator

# ------Exponentiation------
friend = friend**2  # friend ^ 2
friend **= 2  # augmented assignment operator

# ------Modulus------
remainder = int(friend % 3)
print(remainder)

print(friend)

# --------------------------------

# 2: Math Related Function

x = 3.14
y = -4
z = 5

# ------Round function------
result = round(x)
result = round(x, 2)  # round(value, digit number to rounded at)

# ------absolute function (distance away from zero)------
result = abs(y)

# ------Power function------
result = pow(5, 3)  # pow(base, exponent)

# ------Maximum & Minimum function------
result = max(x, y, z)
result = min(x, y, z)
print(result)

# --------------------------------

# 3: Constants and Functions From Math Module
print(math.pi)  # pi value
print(math.e)  # exponent constant
print(math.sqrt(x))  # square root function
print(math.ceil(x))  # rounds to the nearest integer greater than or equal to it
print(math.floor(x))  # rounds to the nearest integer less than or equal to that number

# --------------------------------

# ------Exercise 1: Circumference of Circle------
print("Calculating Circumference of a circle")
radius = float(input("Enter a radius of a circle: "))
circumference = 2 * math.pi * radius
print(f"Circumference: {round(circumference, 2)} cm")

# ------Exercise 2: Area of Circle------
print("Calculating Area of a circle")
radius = float(input("Enter a radius of a circle: "))
area = math.pi * pow(radius, 2)
print(f"Area: {round(area, 2)} cm^2")

# ------Exercise 3: Hypotenuse of Right Angle Triangle------
print("Calculating Hypotenuse of Right Angle Triangle")
perpendicular = float(input("Enter the perpendicular of Right Angle Triangle (cm): "))
base = float(input("Enter the base of Right Angle Triangle (cm): "))

hypotenuse = math.sqrt(pow(perpendicular, 2) + pow(base, 2))
print(f"Hypotenuse: {round(hypotenuse, 2)} cm")

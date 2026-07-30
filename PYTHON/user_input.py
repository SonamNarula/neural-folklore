"""
Topic: User Input
Section: Fundamentals
Description:
input() = A function that prompts the user to enter data. It returns the entered data as a string
"""

name = input("What is your name janab: ")
age = input("How old are you buddy: ")
# OR age = int(input("How old are you buddy: "))

age = int(age) #string to integer (wah python wah)
age = age + 1

print(f"Hello {name}!")
print("Happy Birthday!")
print(f"You are {age} years old.")

#------------EXERCISE 01: Calculate Rectangle Area------------
print("---- Area Calculator ----")
lenght = float(input("Enter the length: "))
breadth = float(input("Enter the breadth: "))
area = lenght * breadth

print(f"Length = {lenght}, Breadth = {breadth} -> Area = {area} cm^2")

#------------EXERCISE 02: Shopping Cart Program------------
print("---- Shopping Cart Program ----")
item = input("What item would you like to buy?: ") #stirng
price = float(input("What is the price?: ")) #string to float
quantity = int(input("How many would you like?: ")) #stirng to integer

total = float(price * quantity)
print(f"Purchased item: {quantity} x {item}\s")
print(f"Total Bill: ${total}")


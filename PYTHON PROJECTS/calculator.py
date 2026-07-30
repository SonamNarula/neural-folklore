# Calculator

operator = input("Enter an operator (+ - * /): ")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

if operator == "+":
    print(f"Sum: {round(num1 + num2, 3)}")
elif operator == "-":
    print(f"Subtraction: {round(num1 - num2, 3)}")
elif operator == "*":
    print(f"Multiplication: {round(num1 * num2, 3)}")
elif operator == "/":
    print(f"Division: {round(num1 / num2, 3)}")
else:
    print(f"{operator} is not a valid operator")
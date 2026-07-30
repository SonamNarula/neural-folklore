"""
Topic: Format Specifiers
Section: Fundamentals
Description:
format specifiers = {:flags} format a value based on which flags are inserted
- :.(number)f = round to that many decimal places (fixed point)
- :(number)  = allocate that many spaces
- :03        = allocate and zero-pad that many spaces
- :<         = left justify
- :>         = right justify
- :^         = center align
- :+         = use a plus sign to indicate positive value
- :=         = place sign to leftmost position
- :          = insert a space before positive numbers
- :,         = comma separator
"""

price1 = 3.14159
price2 = -90087.65
price3 = 1952.34

# ----- Add Precision -> value:.(number)f -----
print(f"Price 1 is ${price1:.2f}")
print(f"Price 2 is ${price2:.1f}")
print(f"Price 3 is ${price3:.3f}")

# ----- Allocate that many spaces -> value:(number) -----
print(f"Price 1 is ${price1:10}")
print(f"Price 2 is ${price2:11}")
print(f"Price 3 is ${price3:15}")

# ----- Allocate and zero-pad that many spaces -> value:0(number) -----
print(f"Price 1 is ${price1:010}")
print(f"Price 2 is ${price2:011}")
print(f"Price 3 is ${price3:015}")

# ----- Left justify -> value:<(number) -----
print(f"Price 1 is ${price1:<10}")
print(f"Price 2 is ${price2:<11}")
print(f"Price 3 is ${price3:<15}")

# ----- Right justify -> value:>(number) -----
print(f"Price 1 is ${price1:>10}")
print(f"Price 2 is ${price2:>11}")
print(f"Price 3 is ${price3:>15}")

# ----- Center align -> value:^(number) -----
print(f"Price 1 is ${price1:^10}")
print(f"Price 2 is ${price2:^11}")
print(f"Price 3 is ${price3:^15}")

# ----- Use a plus sign to indicate positive value -> value:+ -----
print(f"Price 1 is ${price1:+}")
print(f"Price 2 is ${price2:+}")
print(f"Price 3 is ${price3:+}")

# ----- Place sign to leftmost position -> value:= -----
print(f"Price 1 is ${price1:=}")
print(f"Price 2 is ${price2:=}")
print(f"Price 3 is ${price3:=}")

# ----- Insert a space before positive numbers -> value:  -----
print(f"Price 1 is ${price1: }")
print(f"Price 2 is ${price2: }")
print(f"Price 3 is ${price3: }")

# ----- Comma separator -> value:, -----
print(f"Price 1 is ${price1:,}")
print(f"Price 2 is ${price2:,}")
print(f"Price 3 is ${price3:,}")

# ----- Mix format specifiers -----
print(f"Price 1 is ${price1:+,.2f}")
print(f"Price 2 is ${price2:+,.2f}")
print(f"Price 3 is ${price3:+,.2f}")

"""
Topic: String Indexing
Section: Fundamentals
Description:
Demonstrates how to access and slice strings using indexing
and slicing syntax [start:end:step], including negative indexing
and reversing a string.
"""

credit_card_number = "1234-5678-2423-1238"

print(credit_card_number[0])  # any position, 0-indexed
print(credit_card_number[:4])  # range from start to given index (excluding that index)
print(credit_card_number[5:9])  # range [from : to] excluding the last index
print(credit_card_number[5:])  # range from index to end
print(credit_card_number[-1])  # access from the end using negative indexing

# ---- Dealing with Step ----
print(credit_card_number[::4])  # [start:end:step]

# ---------------------------------------------------------

# ------ Exercise 1: Program to get last 4 digits of credit card number ------
last_digits = credit_card_number[-4:]
print(f"XXXX-XXXX-XXXX-{last_digits}")

# ------ Exercise 2: Program to reverse credit card number ------
print(f"Before: {credit_card_number[::1]} After: {credit_card_number[::-1]}")

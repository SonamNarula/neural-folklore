# Weight converter

weight = float(input("Enter Your weight: "))
unit = input("Kilograms or Pounds (KG or LBS): ").upper()

if unit == "KG":
    weight *= 2.205
    unit = "Lbs."
    print(f"Your weight is: {round(weight, 3)} {unit}")
elif unit == "LBS":
    weight /= 2.205
    unit = "Kgs."
    print(f"Your weight is: {round(weight, 3)} {unit}")
else:
    print(f"{unit} is not a valid unit")

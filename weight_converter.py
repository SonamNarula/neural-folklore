# weight converter

weight = float(input("Enter Your weight: "))
unit = input("Kilogram or Pounds (KG or LBS): ")

if unit == "KG":
    weight *= 2.205
    unit = "Lbs."
    print(f"Your weight is: {round(weight, 3)} {unit}")
elif unit == "LBS":
    weight /= 2.205
    unit = "Kgs."
    print(f"Your weight is: {round(weight, 3)} {unit}")
else:
    print(f"{unit} wasn't valid unit")
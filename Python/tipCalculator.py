print("Welcome to the Tip Calculator.\n")

totalBill = float(input("What was the total bill? $"))
tipPercentage = int(input("What percentage tip would you like to give? 10, 12, or 15? "))
billSplitNum = int(input("How many people are splitting this bill? "))

indivPay = ((totalBill * tipPercentage/100) + totalBill) / billSplitNum

print(f"Each person should pay: ${round(indivPay,2)}")
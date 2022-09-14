################################################################################
# Author: Saad Abdullah
# Date Completed: Sepetember, 12, 2022
# Purpose: Post-Interview Coding task for a FEDNOR Junior Contract position
################################################################################

import re

filteredFile = []

# Open text file to parse
with open('C:/Users/SaadAbdullah/OneDrive/Programming/Learning-Projects/Python/FEDNOR_Coding_Task/sample.txt') as file:
    lines = file.read().splitlines()

# Check line for integer value
def isInteger(lines):
    try:
        int(lines)
        return True
    except ValueError:
        return False

# Check if line is also a float (not an int)
def isfloat(lines):
    try:
        float(lines)
        return True
    except ValueError:
        return False

# Strip all integer values from string line
def extractNum(i):
    nums = re.compile(r"[-+]?\d*\.?\d+|\d+")
    return nums.findall(i)

# Check for prime number
def isPrime(n):
    for i in range (2, n):
        if (n%i) == 0:
            return False
    return True

# Parse through file and isolate integers
for i in lines:
    if extractNum(i):
        # print(extractNum(i)[0])
        if isfloat(extractNum(i)[0]) and isInteger(extractNum(i)[0]):
            # print(i + " Is an integer")
            # all integer specific strings are stored in this array now
            filteredFile.append(extractNum(i)[0])

# Convert string list to int
primalFile = [eval(i) for i in filteredFile]

for i in primalFile:
    if isPrime(i):
        print("Prime")
    elif i%3 == 0:
        print("Fizz")
    elif i%5 == 0:
        print("Buzz")
    else:
        print(i)

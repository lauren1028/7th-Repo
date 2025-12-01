# ask the user to import a series of numbers
numbers = []

# Enter the first value
value = float(input('Enter a value:'))

#display the value for 0 to end
while value!= 0:
    numbers.append(value)
    value=float(input('Enter a value (or 0 to end):'))

# display the range
if numbers:
    print(numbers)
    range_value = max(numbers) - min(numbers)
    print(f'Range= {range_value}')


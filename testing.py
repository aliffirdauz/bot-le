import datetime

# Get the current date
current_date = datetime.datetime.now()

# Extract the year
current_year = current_date.year

# Get the last two digits of the current year as a string
last_two_digits = str(current_year)[-2:]


print("Current Year:", current_year)
print("Last Two Digits:", last_two_digits)

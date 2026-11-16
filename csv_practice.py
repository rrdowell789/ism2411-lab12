# ISM2411 Lab 12 - Read a Sales CSV, Write a Cleaned Report
# Author: Ruby Dowell
# Run with: python3 csv_practice.py   (from the ism2411-lab12 folder)

#Reflection questions:

#1.)Python is better when you need to do the same job again and again, or when the file is really big. You write the steps once, and the computer repeats them in seconds.
#Excel is better when you just want to look at numbers, click around, make a quick chart, or change a number by hand.

#2.)Example: a store writes one new line every night with the date and how much money it made.
#“Append” mode means add to the end of the file without erasing what’s already there.
#That’s the right tool because you keep the whole history. If you used the normal write mode, each night would erase the old lines and you’d only have the latest one.

import csv
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
SALES_PATH = BASE / "data" / "sales.csv"
CLEANED_PATH = BASE / "data" / "cleaned.csv"
LOG_PATH = BASE / "data" / "run_log.txt"


# Exercise 1:
print("=== Exercise 1: Check file ===")
if not SALES_PATH.exists():
    raise SystemExit(f"Missing {SALES_PATH}. Put sales.csv in the data folder.")
with open(SALES_PATH, newline="") as f:
    pass  # opens with no error
print(f"Found {SALES_PATH.relative_to(BASE)}")


# Exercise 2:
print("\n=== Exercise 2: Raw rows ===")
with open(SALES_PATH, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)


# Exercise 3: 
print("\n=== Exercise 3: Skip header ===")
with open(SALES_PATH, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)


# Exercise 4: 
print("\n=== Exercise 4: Totals ===")
total_revenue = 0.0
with open(SALES_PATH, newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for product, price, quantity in reader:
        price = float(price)
        quantity = int(quantity)
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:,.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")


# Exercise 5:
print("\n=== Exercise 5: Filter and write ===")
rows_read = 0
rows_written = 0
with open(SALES_PATH, newline="") as infile, \
        open(CLEANED_PATH, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for product, price, quantity in reader:
        rows_read += 1
        price = float(price)
        quantity = int(quantity)
        total = price * quantity
        if total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{total:.2f}"])
            rows_written += 1
print(f"Wrote {rows_written} rows out of {rows_read} in the original")


# Exercise 6: 
# csv.reader uses positions (row[0]) - short and fast, good for simple files with few columns.
# DictReader uses column names (row["price"]) - easier to read and safer if columns get reordered.
print("\n=== Exercise 6: DictReader ===")
dict_total = 0.0
with open(SALES_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:,.2f}")
print(f"Total revenue (DictReader): ${dict_total:,.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))


# Exercise 7: 
print("\n=== Exercise 7: Summary by product ===")
summary = {}
with open(SALES_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["product"]
        summary[name] = summary.get(name, 0.0) + float(row["price"]) * int(row["quantity"])
for name in sorted(summary):
    print(f"{name}: ${summary[name]:,.2f}")

# Exercise 8:
print("\n=== Exercise 8: Run log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_PATH, "a") as log:
    log.write(f"{timestamp} - total revenue: ${total_revenue:,.2f}\n")
print(f"Appended a line to {LOG_PATH.relative_to(BASE)}")

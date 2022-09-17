import pdfplumber
import tabula
import pandas as pd

# Print a PDF line-by-line using pdfplumber
def print_by_line(filepath):
    with open(filepath, 'rb') as fp:
        pdf_obj = pdfplumber.open(fp)
        for page in pdf_obj.pages:
            lines = page.extract_text().split('\n')
            for line in lines:
                print(line)

# Return if a string can be converted to a float
def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


# Extract date, price and vendor from a Chase transaction string
def parse_chase_transaction(transaction):
    arr = transaction.split(" ")

    date = arr[0]
    price = arr[-1]
    vendor = " ".join(arr[1:-1])

    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None



pdf_path = "BofAStatement.pdf"
pdf_obj = pdfplumber.open(pdf_path)

print_by_line(pdf_path)

is_transactions = False

for page in pdf_obj.pages:
    lines = page.extract_text().split('\n')
    for index, line in lines:
        if not is_transactions:
            is_transactions = (line == "PURCHASE") and 
            continue

        if "Totals Year-to-Date" in line:
            is_transactions = False
            break

        info = parse_chase_transaction(line)
        if info:
            date, price, vendor = info
            print("Date: " + date + ", Price: " + price + ", Vendor: " + vendor.strip())


'''
with open(pdf_path, 'rb') as fp:
    pdf_obj = PdfFileReader(fp, strict=False)
    page = pdf_obj.getPage(3)
    print(page.extract_text())


text = ""
for page in pdf_obj.pages:
    text += page.extract_text() + "\n"

print(text)
'''



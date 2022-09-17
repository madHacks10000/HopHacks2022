import pdfplumber
import tabula
import pandas as pd
import re

# Return if a string can be converted to a float
def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def get_bank(pages):
    bank_urls = ["www.chase.com", "www.bankofamerica.com"]
    bank_frequency = {key: 0 for key in bank_urls}

    for page in pages:
        lines = page.extract_text().split('\n')

        for line in lines:
            for bank_url in bank_urls:
                if bank_url.lower() in line.lower():
                    bank_frequency[bank_url] += 1

    return max(bank_frequency, key=bank_frequency.get)


def get_end_digits(page):
    account_num_exps = {"Account Number", "Account #"}

    lines = page.extract_text().split('\n')

    for line in lines:
        for exp in account_num_exps:
            if exp.lower() in line.lower():
                cc_num = re.findall("\d{4}\s\d{4}\s\d{4}\s\d{4}", line)[0]
                my_end_digits = cc_num.split(" ")[-1]
                return my_end_digits


def is_table_header(line, bank):
    if bank == "www.chase.com":
        return line.lower() == "PURCHASE".lower()

    if bank == "www.bankofamerica.com":
        return line.lower() == "PURCHASES AND ADJUSTMENTS".lower()


def is_table_footer(line, bank):
    if bank == "www.chase.com":
        return "totals year-to-date" in line.lower()

    if bank == "www.bankofamerica.com":
        print(line.lower())
        print("total purchases and adjustments for this period")
        print("\n")

        return "total purchases and adjustments for this period" in line.lower()


def parse_transaction(line, bank):
    if bank == "www.chase.com":
        return parse_chase_transaction(line)

    if bank == "www.bankofamerica.com":
        return parse_bofa_transaction(line)


def parse_chase_transaction(transaction):
    #print(transaction)
    arr = transaction.split(" ")

    date = arr[0]
    price = arr[-1]
    vendor = " ".join(arr[1:-1])

    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None
    
def parse_bofa_transaction(transaction):
    #print(transaction)
    return None




                
pdf_path = "BofAStatement.pdf"
pdf_obj = pdfplumber.open(pdf_path)

bank = get_bank(pdf_obj.pages)
end_digits = get_end_digits(pdf_obj.pages[0])

is_table = False

for page in pdf_obj.pages:
    lines = page.extract_text().split('\n')

    for line in lines:
        #print(line)
        if not is_table:
            is_table = is_table_header(line, bank)
            continue

        if is_table_footer(line, bank):
            break # Only breaks out of first page

        info = parse_transaction(line, bank)

        if info:
            date, price, vendor = info
            #print("Date: " + date + ", Price: " + price + ", Vendor: " + vendor.strip())



























#print(bank)
#print(end_digits)

#bank, end_digits = get_metadata(pdf_obj.pages[0])
#print(bank)
#print(end_digits)

'''
is_table = False

for page in pdf_obj.pages:
    lines = page.extract_text().split('\n')

    for line in lines:
        if not is_table:
            is_table = is_table_header(line, bank)
            continue

        if is_table_footer(line, bank):
            break

        info = parse_transaction(line, bank)

        if info:
            date, price, vendor = info
            print("Date: " + date + ", Price: " + price + ", Vendor: " + vendor.strip())






for page in pdf_obj.pages:
    lines = page.extract_text().split('\n')































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

def is_transactions_header(line, bank):
    if bank == "chase":
        return line == "PURCHASE"


# Extract date, price and vendor from a Chase transaction string
def parse_chase_transaction(transaction):
    arr = transaction.split(" ")

    date = arr[0]
    price = arr[-1]
    vendor = " ".join(arr[1:-1])

    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None


# Extract list of lines that fall in the table boundary
def get_transactions_info():





pdf_path = "BofAStatement.pdf"
pdf_obj = pdfplumber.open(pdf_path)

print_by_line(pdf_path)

inside_transactions = False

for page in pdf_obj.pages:
    lines = page.extract_text().split('\n')

    bank = ?
    table_data = get_transactions_table(lines, bank)

    for transaction in table_data:
        info = parse_transaction(line, bank)

        if info:
            date, price, vendor = info
            print("Date: " + date + ", Price: " + price + ", Vendor: " + vendor.strip())

    for line in lines:
        if not 



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


with open(pdf_path, 'rb') as fp:
    pdf_obj = PdfFileReader(fp, strict=False)
    page = pdf_obj.getPage(3)
    print(page.extract_text())


text = ""
for page in pdf_obj.pages:
    text += page.extract_text() + "\n"

print(text)
'''



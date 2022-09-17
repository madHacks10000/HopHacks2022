import sys
import re
import pdfplumber

# Helper Functions

def is_float(str):
    '''Return if a string can be converted to a float'''

    try:
        float(str)
        return True
    except ValueError:
        return False



def get_bank(pages):
    '''Identify the bank referenced in the statement'''

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
    '''Identify the last four digits of the credit card in the statement'''

    account_num_exps = {"Account Number", "Account #"}

    lines = page.extract_text().split('\n')

    for line in lines:
        for exp in account_num_exps:
            if exp.lower() in line.lower():
                cc_num = re.findall("\d{4}\s\d{4}\s\d{4}\s\d{4}", line)[0]
                my_end_digits = cc_num.split(" ")[-1]
                return my_end_digits


def is_table_header(line, bank):
    '''Return if the current line is the starting point of the transaction table'''

    if bank == "www.chase.com":
        return line.lower() == "PURCHASE".lower()

    if bank == "www.bankofamerica.com":
        return line.lower() == "PURCHASES AND ADJUSTMENTS".lower()


def is_table_footer(line, bank):
    '''Return if the current line is the ending point of the transaction table'''

    if bank == "www.chase.com":
        return "totals year-to-date" in line.lower()

    if bank == "www.bankofamerica.com":
        return ("total purchases and adjustments for this period" in line.lower())


def parse_transaction(line, bank):
    '''Extract the transaction information from a given string'''

    if bank == "www.chase.com":
        return parse_chase_transaction(line)

    if bank == "www.bankofamerica.com":
        return parse_bofa_transaction(line)


def parse_chase_transaction(transaction):
    '''Extract the transaction information from a given Chase string'''

    arr = transaction.split(" ")

    date = arr[0]
    price = arr[-1]
    vendor = " ".join(arr[1:-1])

    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None
    

def parse_bofa_transaction(transaction):
    '''Extract the transaction information from a given BofA string'''

    arr = transaction.split(" ")

    date = arr[1]
    price = arr[-1]
    vendor = " ".join(arr[2:-3])

    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None


# Beginning of main program
                
pdf_path = sys.argv[1]
pdf_obj = pdfplumber.open(pdf_path)

bank = get_bank(pdf_obj.pages)
end_digits = get_end_digits(pdf_obj.pages[0])
start_date, end_date = ()


print("Bank: " + bank)
print("Credit Card: " + end_digits)

is_table = False

for page in pdf_obj.pages:
    lines = page.extract_text().split('\n')

    for line in lines:
        if not is_table:
            is_table = is_table_header(line, bank)
            continue

        if is_table_footer(line, bank):
            exit()

        info = parse_transaction(line, bank)

        if info:
            date, price, vendor = info
            print("Date: " + date + ", Price: " + price + ", Vendor: " + vendor.strip())

import pdfplumber
import sys
import re
import json

# Helper Functions

def is_float(str):
    '''Return if a string can be converted to a float'''

    try:
        float(str)
        return True
    except ValueError:
        return False



def get_bank(pages):
    '''Identify the bank referenced in the statement by associating it with the most common URL'''

    bank_frequency = {}

    for page in pages:
        lines = page.extract_text().split('\n')

        for line in lines:
            result = re.search("www\.([a-zA-Z]+)\.com", line.lower())

            if result is not None:
                bank = result.group(1)

                if bank in bank_frequency.keys():
                    bank_frequency[bank] += 1
                else:
                    bank_frequency[bank] = 1

    if (len(bank_frequency) > 0):
        return max(bank_frequency, key=bank_frequency.get)

    print("No banks found!")
    exit()



def get_end_digits(page):
    '''Identify the last four digits of the credit card in the statement'''

    account_num_exps = {"Account Number", "Account #", "Account Ending In "}

    lines = page.extract_text().split('\n')

    for line in lines:
        for exp in account_num_exps:
            if exp.lower() in line.lower():
                cc_num = re.search("\d{4}\s\d{4}\s\d{4}\s\d{4}", line)

                if cc_num is None:
                    return re.search("\d{4}", line).group(0)
                
                return cc_num.group(0).split(" ")[-1]


def is_table_header(line, bank):
    '''Return if the current line is the starting point of the transaction table'''

    if bank == "chase":
        return line.lower() == "PURCHASE".lower()

    if bank == "bankofamerica":
        return line.lower() == "PURCHASES AND ADJUSTMENTS".lower()

    return ("transactions" == line.lower().strip())


def is_table_footer(line, bank):
    '''Return if the current line is the ending point of the transaction table'''

    if bank == "chase":
        return "totals year-to-date" in line.lower()

    if bank == "bankofamerica":
        return ("total purchases and adjustments for this period" in line.lower())

    return ("total" in line.lower())


def parse_transaction(line, bank):
    '''Extract the transaction information from a given string'''

    if bank == "chase":
        return parse_chase_transaction(line)

    if bank == "bankofamerica":
        return parse_bofa_transaction(line)

    return parse_generic_transaction(line)


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
    vendor = " ".join(arr[2:-3]).split("  ")[0]

    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None


def parse_generic_transaction(transaction):
    '''Extract the transaction information from a given string from an arbitrary bank'''

    date, price, vendor = None, None, None
    arr = transaction.lower().split(" ")
    
    # Return false if the entry is too short or is a payment
    if len(arr) == 1 or arr[-2] == "-":
        return None


    # Find the date
    first_date = re.search("\d+/\d+", arr[0])
    second_date = re.search("\d+/\d+", arr[1])

    word_months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    # Case 0: No date found 
    if first_date is None and second_date is None and arr[0] not in word_months:
        return None

    # Case 1: Two numeric dates
    elif first_date is not None and second_date is not None:
        date = min(first_date.group(0), second_date.group(0))

    # Case 2: One numeric date
    elif first_date is None and second_date is not None:
        date = second_date.group(0)

    elif first_date is None and second_date is not None:
        date = first_date.group(0)

    # Case 3: String date
    if arr[0] in word_months:
        date = str(word_months.index(arr[0]) + 1) + "/" + arr[1]


    # Find the price
    price = re.search("\d+\.\d+", arr[-1]).group(0)



    # Find the vendor
    vendor = " ".join(arr[2:-2])


    # Return results
    if "/" in date and is_float(price):
        return (date, price, vendor)

    return None


def parse_pdf(filename):
    # Create array of dictionaries to track all transactions in PDF
    transactions_info = []

    pdf_path = sys.argv[1]
    pdf_obj = pdfplumber.open(pdf_path)

    bank = get_bank(pdf_obj.pages)
    end_digits = get_end_digits(pdf_obj.pages[0])

    is_table = False

    for page in pdf_obj.pages:
        lines = page.extract_text().split('\n')

        for line in lines:
            if not is_table:
                is_table = is_table_header(line, bank)
                continue

            if is_table_footer(line, bank):
                return transactions_info

            info = parse_transaction(line, bank)

            if info:
                date, price, vendor = info

                new_transaction = {
                    "bank": bank,
                    "end_digits": end_digits,
                    "date": date,
                    "price": price,
                    "vendor": vendor.strip()
                }

                transactions_info.append(new_transaction)

    return transactions_info
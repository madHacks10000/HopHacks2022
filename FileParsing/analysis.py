# Categories
# 1. Income
# 2. Entertainment
# 3. Food
# 4. Rent&Bills
# 5. Travel
# 6. Transport
# 7. Sport
# 8. Transfer
# 9. Materialistic Desire
# 10. Cash Withdrawal
# 11. Gifts
# 12. Groceries
# 13. Personal care
# 14. Other


def count_word_overlap(a, b):
    ''' Count the number of distinct shared words across two sentences'''

    arr1 = a.lower().split(" ")
    arr2 = b.lower().split(" ")

    set1 = {word for word in arr1}
    set2 = {word for word in arr2}

    return (len(set1.intersection(set2)))


def is_match(receipt, transaction):
    ''' Match a receipt and transaction on their dates, amounts, and having two or more keywords in common'''

    return (receipt[0] == transaction[0] and receipt[1] == transaction[1] and count_word_overlap(receipt[2], transaction[2]) > 0)

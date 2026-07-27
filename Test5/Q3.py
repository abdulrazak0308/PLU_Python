import sqlite3

class Transaction:
    def __init__(self, transaction_id, account_number, amount, date, tx_type):
        self.transaction_id = transaction_id
        self.account_number = account_number
        self.amount = amount
        self.date = date
        self.tx_type = tx_type

    def __repr__(self):
        return f"ID: {self.transaction_id} | Account: {self.account_number} | Amount: ${self.amount:.2f} | Date: {self.date} | Type: {self.tx_type}"


def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE transactions (
            transaction_id INTEGER PRIMARY KEY,
            account_number TEXT,
            amount REAL,
            date TEXT,
            tx_type TEXT
        )
    ''')

    cursor.execute("INSERT INTO transactions VALUES (501, 'ACC1001', 1200.50, '2026-03-01', 'Credit')")
    cursor.execute("INSERT INTO transactions VALUES (502, 'ACC1002', 450.00, '2026-03-02', 'Debit')")
    cursor.execute("INSERT INTO transactions VALUES (503, 'ACC1001', 89.99, '2026-03-03', 'Debit')")
    cursor.execute("INSERT INTO transactions VALUES (504, 'ACC1003', 3500.00, '2026-03-04', 'Credit')")
    cursor.execute("INSERT INTO transactions VALUES (505, 'ACC1002', 12.50, '2026-03-05', 'Debit')")
    cursor.execute("INSERT INTO transactions VALUES (506, 'ACC1004', 2100.00, '2026-03-06', 'Credit')")
    cursor.execute("INSERT INTO transactions VALUES (507, 'ACC1001', 650.25, '2026-03-07', 'Debit')")

    conn.commit()
    return conn


def quick_sort_by_amount(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left = []  
    right = []  

    for item in arr[:-1]:
        if item.amount <= pivot.amount:
            left.append(item)
        else:
            right.append(item)

    return quick_sort_by_amount(left) + [pivot] + quick_sort_by_amount(right)


def binary_search_by_id(transactions, target_id):
    low = 0
    high = len(transactions) - 1

    while low <= high:
        mid = (low + high) // 2
        if transactions[mid].transaction_id == target_id:
            return transactions[mid]
        elif transactions[mid].transaction_id < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None

def main():
    conn = setup_database()
    cursor = conn.cursor()

    cursor.execute("SELECT transaction_id, account_number, amount, date, tx_type FROM transactions")
    rows = cursor.fetchall()

    transaction_list = []
    for row in rows:
        t = Transaction(row[0], row[1], row[2], row[3], row[4])
        transaction_list.append(t)

    print("=== All Transactions (From Database) ===")
    for t in transaction_list:
        print(t)
    print("\n" + "-"*50 + "\n")


    sorted_by_amount = quick_sort_by_amount(transaction_list)

    print("=== Transactions Sorted by Amount (Quick Sort) ===")
    for t in sorted_by_amount:
        print(t)
    print("\n" + "-"*50 + "\n")


    sorted_by_id = sorted(transaction_list, key=lambda x: x.transaction_id)
    search_id = 504

    print(f"=== Searching for Transaction ID: {search_id} ===")
    found = binary_search_by_id(sorted_by_id, search_id)
    if found:
        print("Found:", found)
    else:
        print("Transaction not found.")
    print("\n" + "-"*50 + "\n")


    total_credits = 0.0
    total_debits = 0.0

    for t in transaction_list:
        if t.tx_type == "Credit":
            total_credits += t.amount
        elif t.tx_type == "Debit":
            total_debits += t.amount

    print("=== Financial Summary ===")
    print(f"Total Credits: ${total_credits:.2f}")
    print(f"Total Debits:  ${total_debits:.2f}")
    print("\n" + "-"*50 + "\n")

    top_5 = sorted_by_amount[-5:]
    top_5.reverse()

    print("=== Top Highest-Value Transactions ===")
    for t in top_5:
        print(t)

    conn.close()


if __name__ == "__main__":
    main()
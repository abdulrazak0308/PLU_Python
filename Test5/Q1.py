import sqlite3

class Product:
    def __init__(self, product_id, name, category, quantity, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"ID: {self.product_id:<4} | Name: {self.name:<18} | Category: {self.category:<12} | Qty: {self.quantity:<4} | Price: {self.price:.2f}"


def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    
    sample_data = [
        (101, "Wireless Mouse", "Electronics", 45, 25.99),
        (104, "Mechanical Keyboard", "Electronics", 8, 89.99),
        (102, "Coffee Mug", "Home", 120, 12.50),
        (105, "Desk Lamp", "Furniture", 5, 34.00),
        (103, "USB-C Cable", "Electronics", 3, 9.99),
        (106, "Notebook", "Stationery", 60, 4.50),
    ]
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", sample_data)
    conn.commit()
    return conn


def fetch_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, category, quantity, price FROM products")
    rows = cursor.fetchall()
    return [Product(*row) for row in rows]



def merge_sort_by_quantity(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_by_quantity(arr[:mid])
    right = merge_sort_by_quantity(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].quantity <= right[j].quantity:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result



def binary_search_by_id(products, target_id):
    """
    Searches for a product by product_id using Binary Search.
    Note: Requires the list to be sorted by product_id first.
    """
    low = 0
    high = len(products) - 1

    while low <= high:
        mid = (low + high) // 2
        if products[mid].product_id == target_id:
            return products[mid]
        elif products[mid].product_id < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None



def main():
    conn = setup_database()
    products = fetch_products(conn)

    print("=== All Products (Unsorted DB Order) ===")
    for p in products:
        print(p)

    sorted_by_qty = merge_sort_by_quantity(products)
    print("\n=== Products Sorted by Quantity (Merge Sort) ===")
    for p in sorted_by_qty:
        print(p)

    print("\n=== Low Stock Alert (Quantity < 10) ===")
    low_stock_items = [p for p in products if p.quantity < 10]
    for p in low_stock_items:
        print(p)


    products_sorted_by_id = sorted(products, key=lambda x: x.product_id)
    
    search_id = 104
    print(f"\n=== Binary Search for Product ID: {search_id} ===")
    found_product = binary_search_by_id(products_sorted_by_id, search_id)

    if found_product:
        print("Product Found:")
        print(found_product)
    else:
        print("Product not found.")

    conn.close()


if __name__ == "__main__":
    main()
import pymysql
from tabulate import tabulate

# Database configuration
def create_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Deep@$915736"  # Replace with your MySQL password
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_db")
        print("Database created or already exists.")
        connection.close()
    except Exception as e:
        print("Error creating database:", e)

# Connect to the database
def connect_to_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Deep@$915736",  # Replace with your MySQL password
            database="inventory_db"
        )
        return connection
    except Exception as e:
        print("Error connecting to database:", e)
        return None

# Initialize table
def initialize_table():
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS inventory (
                        item_id INT AUTO_INCREMENT PRIMARY KEY,
                        item_name VARCHAR(255) NOT NULL,
                        quantity INT NOT NULL,
                        price DECIMAL(10, 2) NOT NULL
                    )
                    """
                )
                print("Table initialized successfully.")
        except Exception as e:
            print("Error initializing table:", e)
        finally:
            connection.close()

# Add a new inventory item
def add_item():
    connection = connect_to_database()
    if connection:
        try:
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO inventory (item_name, quantity, price) VALUES (%s, %s, %s)",
                    (item_name, quantity, price)
                )
                connection.commit()
                print("Item added successfully.")
        except Exception as e:
            print("Error adding item:", e)
        finally:
            connection.close()

# View all inventory items
def view_inventory():
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM inventory")
                rows = cursor.fetchall()
                if rows:
                    print(tabulate(rows, headers=["Item ID", "Item Name", "Quantity", "Price"], tablefmt="pretty"))
                else:
                    print("No items in inventory.")
        except Exception as e:
            print("Error fetching inventory:", e)
        finally:
            connection.close()

# Update an existing inventory item
def update_item():
    connection = connect_to_database()
    if connection:
        try:
            item_id = int(input("Enter item ID to update: "))
            new_quantity = int(input("Enter new quantity: "))
            new_price = float(input("Enter new price: "))
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE inventory SET quantity = %s, price = %s WHERE item_id = %s",
                    (new_quantity, new_price, item_id)
                )
                connection.commit()
                print("Item updated successfully.")
        except Exception as e:
            print("Error updating item:", e)
        finally:
            connection.close()

# Delete an inventory item
def delete_item():
    connection = connect_to_database()
    if connection:
        try:
            item_id = int(input("Enter item ID to delete: "))
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM inventory WHERE item_id = %s", (item_id,))
                connection.commit()
                print("Item deleted successfully.")
        except Exception as e:
            print("Error deleting item:", e)
        finally:
            connection.close()

# Main menu
def main_menu():
    create_database()
    initialize_table()
    while True:
        print("\n--- Inventory Management System ---")
        print("1. Add Item")
        print("2. View Inventory")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()

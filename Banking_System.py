import pymysql

def connect_to_database(use_database=False):
    """Connect to MySQL server. Optionally use the Banking database."""
    if use_database:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="nslab@60510",
            database="Banking",
        )
    else:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="nslab@60510",
        )

def Create_Database():
    """Create the Banking database and Accounts table if they do not exist."""
    connection = connect_to_database()  # Connect without specifying a database
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS Banking")

    # Connect to the Banking database to create the table
    connection.select_db("Banking")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts(
                       account_number INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(255) NOT NULL,
                       balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
                   )""")
    connection.commit()
    connection.close()

def Create_Account(name, initial_deposit):
    """Create a new account with the specified name and initial deposit."""
    connection = connect_to_database(use_database=True)
    cursor = connection.cursor()

    # Check if the name already exists in the database
    cursor.execute("SELECT account_number FROM Accounts WHERE name = %s", (name,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("\n===========================================================================================")
        print(f"Warning: An account with the name '{name}' already exists. Please choose a different name.")
        print("============================================================================================")
    else:
        # If the name doesn't exist, create the account
        cursor.execute(
            "INSERT INTO Accounts (name, balance) VALUES (%s, %s)", 
            (name, initial_deposit)
        )
        connection.commit()
        print("\n===================================================================")
        print(f"Account Created Successfully! Account number is {cursor.lastrowid}")
        print("====================================================================")

    connection.close()

def View_Balance(account_number):
    """View the balance of a specified account."""
    connection = connect_to_database(use_database=True)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT balance FROM Accounts WHERE account_number = %s", (account_number,)
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        print(f"Account balance: ${result[0]:.2f}")
    else:
        print("Account not found")

def Deposit(account_number, amount):
    """Deposit an amount into a specified account."""
    connection = connect_to_database(use_database=True)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Accounts SET balance = balance + %s WHERE account_number = %s",
        (amount, account_number)
    )
    connection.commit()

    if cursor.rowcount:
        print(f"Deposited ${amount:.2f} Successfully!")
    else:
        print("Account not found")

    cursor.execute(
        "SELECT balance FROM Accounts WHERE account_number = %s", (account_number,)
    )
    result = cursor.fetchone()
    connection.close()

    if result:
        print(f"Account balance: ${result[0]:.2f}")
    else:
        print("Account not found")

def Withdraw(account_number, amount):
    """Withdraw an amount from a specified account if sufficient balance exists."""
    connection = connect_to_database(use_database=True)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT balance FROM Accounts WHERE account_number = %s", (account_number,)
    )
    result = cursor.fetchone()

    if result and result[0] >= amount:
        cursor.execute(
            "UPDATE Accounts SET balance = balance - %s WHERE account_number = %s",
            (amount, account_number)
        )
        connection.commit()
        print(f"Withdrew ${amount:.2f} Successfully!")
    else:
        print("Insufficient funds or Account not found")

    cursor.execute(
        "SELECT balance FROM Accounts WHERE account_number = %s", (account_number,)
    )
    result = cursor.fetchone()

    if result:
        print(f"Account balance: ${result[0]:.2f}")
    else:
        print("Account not found")

    connection.close()

def Main_Menu():
    while True:
        print("\nBanking System Menu:")
        print("1. Create Account")
        print("2. View Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter your name: ").strip()
            initial_deposit = float(input("Enter initial deposit: "))
            Create_Account(name, initial_deposit)

        elif choice == "2":
            account_number = int(input("Enter your account number: "))
            View_Balance(account_number)

        elif choice == "3":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter amount to deposit: "))
            Deposit(account_number, amount)

        elif choice == "4":
            account_number = int(input("Enter your account number: "))
            amount = float(input("Enter amount to withdraw: "))
            Withdraw(account_number, amount)

        elif choice == "5":
            print("\n=============================")
            print("Exiting the system. Goodbye!")
            print("=============================")
            break

if __name__ == "__main__":
    print("Initializing Banking System....")
    Create_Database()  # Ensure the database and table are created
    Main_Menu()

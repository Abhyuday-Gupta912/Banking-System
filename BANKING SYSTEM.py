import random
import csv
import mysql.connector

# Establish MySQL connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="abhyuday"
)
db_cursor = db_connection.cursor()

# Create a table if it doesn't exist
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_number VARCHAR(8),
    name VARCHAR(255),
    gender VARCHAR(10),
    city VARCHAR(255),
    phone_number VARCHAR(15),
    balance FLOAT,
    password VARCHAR(255)
)
""")
users = {}

def generate_account_number():
    """Generates a random 8-digit account number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def create_account():
    """Creates a new account."""
    name = input("Enter your name: ")
    gender = input("Enter your gender: ")
    city = input("Enter your city: ")
    phone_number = input("Enter your phone number: ")
    balance = float(input("Enter your balance: "))
    password = input("Create a password: ")

    account_number = generate_account_number()

    # Insert into MySQL database
    db_cursor.execute("""
    INSERT INTO accounts (account_number, name, gender, city, phone_number, balance, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (account_number, name, gender, city, phone_number, balance, password))

    db_connection.commit()

    print('Your account number is:', account_number)

def view_account_info(account_number):
    """Views the account information of the specified account number."""
    db_cursor.execute("""
    SELECT * FROM accounts WHERE account_number = %s
    """, (account_number,))
    account_info = db_cursor.fetchone()

    if account_info:
        password = input("Enter your password to continue: ")
        if password == account_info[6]:  # Password is at index 6
            print("Your account information:")
            print("Name:", account_info[1])
            print("Gender:", account_info[2])
            print("City:", account_info[3])
            print("Phone Number:", account_info[4])
            print("Account number:", account_info[0])
            print("Balance:", account_info[5])
        else:
            print("Incorrect password")
    else:
        print("Account not found")

def update_account_info(account_number):
    """Updates the account information of the specified account number."""
    db_cursor.execute("""
    SELECT * FROM accounts WHERE account_number = %s
    """, (account_number,))
    account_info = db_cursor.fetchone()

    if account_info:
        password = input("Enter your password to continue: ")
        if password == account_info[6]:  # Password is at index 6
            print("What do you want to update?")
            print("1. Name")
            print("2. Gender")
            print("3. City")
            print("4. Phone Number")
            print("5. Balance")
            option = input("Enter your choice: ")

            if option == "1":
                new_name = input("Enter your new name: ")
                db_cursor.execute("""
                UPDATE accounts SET name = %s WHERE account_number = %s
                """, (new_name, account_number))
            elif option == "2":
                new_gender = input("Enter your new gender: ")
                db_cursor.execute("""
                UPDATE accounts SET gender = %s WHERE account_number = %s
                """, (new_gender, account_number))
            elif option == "3":
                new_city = input("Enter your new city: ")
                db_cursor.execute("""
                UPDATE accounts SET city = %s WHERE account_number = %s
                """, (new_city, account_number))
            elif option == "4":
                new_phone_number = input("Enter your new phone number: ")
                db_cursor.execute("""
                UPDATE accounts SET phone_number = %s WHERE account_number = %s
                """, (new_phone_number, account_number))
            elif option == "5":
                new_balance = float(input("Enter your new balance: "))
                db_cursor.execute("""
                UPDATE accounts SET balance = %s WHERE account_number = %s
                """, (new_balance, account_number))
                print("Balance updated")
            else:
                print("Invalid option")
            
            db_connection.commit()
        else:
            print("Incorrect password")
    else:
        print("Account not found")

def delete_account(account_number):
    """Deletes the account of the specified account number."""
    db_cursor.execute("""
    SELECT * FROM accounts WHERE account_number = %s
    """, (account_number,))
    account_info = db_cursor.fetchone()

    if account_info:
        password = input("Enter your password to continue: ")
        if password == account_info[6]:  # Password is at index 6
            db_cursor.execute("""
            DELETE FROM accounts WHERE account_number = %s
            """, (account_number,))

            db_connection.commit()
            print("Account deleted")
        else:
            print("Incorrect password")
    else:
        print("Account not found")

def transaction(account_number):
    """Performs a transaction/withdrawal."""
    db_cursor.execute("""
    SELECT * FROM accounts WHERE account_number = %s
    """, (account_number,))
    account_info = db_cursor.fetchone()

    if account_info:
        password = input("Enter your password to continue: ")
        if password == account_info[6]:  # Password is at index 6
            amount = float(input("Enter the amount you want to withdraw: "))
            if amount > account_info[5]:  # Balance is at index 5
                print("Insufficient balance")
            else:
                new_balance = account_info[5] - amount
                db_cursor.execute("""
                UPDATE accounts SET balance = %s WHERE account_number = %s
                """, (new_balance, account_number))
                db_connection.commit()
                print("Transaction successful")
        else:
            print("Incorrect password")
    else:
        print("Account not found")

def transfer_money(sender_account_number):
    """Transfers money from one account to another."""
    db_cursor.execute("""
    SELECT * FROM accounts WHERE account_number = %s
    """, (sender_account_number,))
    sender_info = db_cursor.fetchone()

    if sender_info:
        password = input("Enter your password to continue: ")
        if password == sender_info[6]:  # Password is at index 6
            recipient_account_number = input("Enter the recipient's account number: ")
            db_cursor.execute("""
            SELECT * FROM accounts WHERE account_number = %s
            """, (recipient_account_number,))
            recipient_info = db_cursor.fetchone()

            if recipient_info:
                amount = float(input("Enter the amount you want to transfer: "))
                if amount > sender_info[5]:  # Balance is at index 5
                    print("Insufficient balance")
                else:
                    sender_balance = sender_info[5] - amount
                    recipient_balance = recipient_info[5] + amount

                    db_cursor.execute("""
                    UPDATE accounts SET balance = %s WHERE account_number = %s
                    """, (sender_balance, sender_account_number))

                    db_cursor.execute("""
                    UPDATE accounts SET balance = %s WHERE account_number = %s
                    """, (recipient_balance, recipient_account_number))

                    db_connection.commit()
                    print("Transaction successful")
            else:
                print("Recipient account not found")
        else:
            print("Incorrect password")
    else:
        print("Account not found")

def main():
    try:
        # Fetch accounts data from the database
        db_cursor.execute("""
        SELECT * FROM accounts
        """)
        rows = db_cursor.fetchall()

        for row in rows:
            account_number, name, gender, city, phone_number, balance, password = row
            users[account_number] = {'name': name, 'gender': gender, 'city': city, 'phone_number': phone_number, 'balance': float(balance), 'password': password}

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    while True:
        print("  ┌────────────────┐  ╭───────────────────────╮            ") 
        print("  │  ╭┼┼╮          │  │ ▶︎ 1 • Create Account  │            ")
        print("  │  ╰┼┼╮          │  ├───────────────────────┴─────╮      ")
        print("  │  ╰┼┼╯          │  │ ▶︎ 2 • View Account info     │     ")
        print("  │                │  |────────────────────────────┬╯    ")
        print("  │  L V I S       │  │ ▶︎ 3 • Update Account Info  │      ")
        print("  │  B A N K I N G │  ├────────────────────────┬───╯      ")
        print("  │                │  │ ▶︎ 4 • Delete Account   │   ")
        print("  │                │  ├───────────────────────┬╯    ") 
        print("  │                │  │ ▶︎ 5 • Transacation    │   ")
        print("  │                │  ├───────────────────┬───╯      ") 
        print("  │                │  │ ▶︎ 6 • Transfer    │           ")  
        print("  │ ║│┃┃║║│┃║│║┃│  │  |───────────────────┴╮             ")
        print("  │ ║│┃┃║║│┃║│║┃│  │  │ ▶︎ 7 • Exit System  │              ")
        print("  └────────────────┘  ╰────────────────────╯  ")    
        
        action = input("Enter your choice: ")
        
        if action == "1":
            create_account()
        elif action == "2":
            account_number = input("Enter your account number: ")
            view_account_info(account_number)
        elif action == "3":
            account_number = input("Enter your account number: ")
            update_account_info(account_number)
        elif action == "4":
            account_number = input("Enter your account number: ")
            delete_account(account_number)
        elif action == "5":
            account_number = input("Enter your account number: ")
            transaction(account_number)
        elif action == "6":
            account_number = input("Enter your account number: ")
            transfer_money(account_number)
        elif action == "7":
            break
        else:
            print("Invalid choice")

main()

db_connection.close()

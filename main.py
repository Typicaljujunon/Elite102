# Importing necessary libraries
import mysql.connector
import tkinter as tk
from tkinter import ttk

# Establishing connection to the MySQL database
connection = mysql.connector.connect(
    host='localhost',
    database='student',
    user='root',
    password='2017Elclasico!'
)

# Admin code for privileged operations
admin_code = 984797597556439562859

# Function to handle user login
def login():
    # Retrieving username and PIN from entry fields
    username = username_entry.get()
    pin = pin_entry.get()
    # Creating a cursor to execute SQL queries
    cursor = connection.cursor()
    # Retrieving account information based on the username
    cursor.execute("SELECT * FROM bankaccounts WHERE username = %s", (username,))
    account = cursor.fetchone()
    # Validating account existence
    if account:
        # Checking if entered PIN matches the account PIN
        if pin == account[2]: 
            print("Login successful")
            root.withdraw()
            # Redirecting to logged-in state
            logged_in(username, account[5])
        else:
            login_status_label.config(text="Incorrect PIN")
    else:
        login_status_label.config(text="Account doesn't exist with that username")

# Function to create a new account
def create_account():
    def save_account():
        # Retrieving account details from entry fields
        name = name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        pin = pin_entry.get()
        is_admin = int(admin_code_entry.get())
        # Determining account privileges based on admin code
        if is_admin == admin_code:
            perms = "admin"
        else:
            perms = "customer"
        # Inserting account details into the database
        cursor = connection.cursor()
        cursor.execute("INSERT INTO bankaccounts (name, username, pin, balance, perms, email) VALUES (%s, %s, %s, %s, %s, %s)", (name, username, pin, 0, perms, email))
        connection.commit()
        print("Account created")

    # Creating a window for account creation
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")

    # Creating entry fields for account details
    name_label = tk.Label(create_account_window, text="Name:", font=("Calibri", 12))
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(create_account_window, font=("Calibri", 12))
    name_entry.grid(row=0, column=1)

    username_label = tk.Label(create_account_window, text="Username:", font=("Calibri", 12))
    username_label.grid(row=1, column=0)
    username_entry = tk.Entry(create_account_window, font=("Calibri", 12))
    username_entry.grid(row=1, column=1)

    email_label = tk.Label(create_account_window, text="Email:", font=("Calibri", 12))
    email_label.grid(row=2, column=0)
    email_entry = tk.Entry(create_account_window, font=("Calibri", 12))
    email_entry.grid(row=2, column=1)

    pin_label = tk.Label(create_account_window, text="PIN:", font=("Calibri", 12))
    pin_label.grid(row=3, column=0)
    pin_entry = tk.Entry(create_account_window, show="*", font=("Calibri", 12))
    pin_entry.grid(row=3, column=1)

    admin_code_label = tk.Label(create_account_window, text="Admin Code:", font=("Calibri", 12))
    admin_code_label.grid(row=4, column=0)
    admin_code_entry = tk.Entry(create_account_window, show="*", font=("Calibri", 12))
    admin_code_entry.grid(row=4, column=1)

    save_button = tk.Button(create_account_window, text="Create Account", command=save_account, font=("Calibri", 12))
    save_button.grid(row=5, columnspan=2)

# Function to handle password change
def change_password(username):
    def save_new_password():
        # Retrieving new password from entry field
        new_password = new_password_entry.get()
        # Updating password in the database
        cursor = connection.cursor()
        cursor.execute("UPDATE bankaccounts SET password = %s WHERE username = %s", (new_password, username))
        connection.commit()
        print("Password changed successfully.")

    # Creating a window for password change
    change_password_window = tk.Toplevel(logged_in_window)
    change_password_window.title("Change Password")

    # Creating entry field for new password
    new_password_label = tk.Label(change_password_window, text="New Password:", font=("Calibri", 12))
    new_password_label.grid(row=0, column=0)
    new_password_entry = tk.Entry(change_password_window, show="*", font=("Calibri", 12))
    new_password_entry.grid(row=0, column=1)

    save_button = tk.Button(change_password_window, text="Save", command=save_new_password, font=("Calibri", 12))
    save_button.grid(row=1, columnspan=2)

# Function to handle email change
def change_email(username):
    def save_new_email():
        # Retrieving new email from entry field
        new_email = new_email_entry.get()
        # Updating email in the database
        cursor = connection.cursor()
        cursor.execute("UPDATE bankaccounts SET email = %s WHERE username = %s", (new_email, username))
        connection.commit()
        print("Email changed successfully.")

    # Creating a window for email change
    change_email_window = tk.Toplevel(logged_in_window)
    change_email_window.title("Change Email")

    # Creating entry field for new email
    new_email_label = tk.Label(change_email_window, text="New Email:", font=("Calibri", 12))
    new_email_label.grid(row=0, column=0)
    new_email_entry = tk.Entry(change_email_window, font=("Calibri", 12))
    new_email_entry.grid(row=0, column=1)

    save_button = tk.Button(change_email_window, text="Save", command=save_new_email, font=("Calibri", 12))
    save_button.grid(row=1, columnspan=2)

# Function to handle information change
def change_information(username):
    def change_info():
        # Retrieving selected information to change
        info = info_combobox.get()
        if info == "Username":
            change_username(username)
        elif info == "Password":
            change_password(username)
        elif info == "Email":
            change_email(username)

    # Creating a window for information change
    change_info_window = tk.Toplevel(logged_in_window)
    change_info_window.title("Change Information")

    # Creating a dropdown menu to select information
    info_label = tk.Label(change_info_window, text="Select information to change:", font=("Calibri", 12))
    info_label.grid(row=0, column=0)
    info_options = ["Username", "Password", "Email"]
    info_combobox = ttk.Combobox(change_info_window, values=info_options, font=("Calibri", 12))
    info_combobox.grid(row=0, column=1)

    execute_button = tk.Button(change_info_window, text="Change", command=change_info, font=("Calibri", 12))
    execute_button.grid(row=1, columnspan=2)

# Function to handle deposit operation
def deposit(username):
    def deposit_money():
        # Retrieving deposit amount from entry field
        amount = float(amount_entry.get())
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM bankaccounts WHERE username = %s", (username,))
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance + amount
        cursor.execute("UPDATE bankaccounts SET balance = %s WHERE username = %s", (new_balance, username))
        connection.commit()
        print("Deposit successful. New balance:", new_balance)
    
    # Creating a frame for deposit operation
    deposit_frame = tk.Frame(logged_in_window)
    deposit_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    amount_label = tk.Label(deposit_frame, text="Amount to deposit:", font=("Calibri", 12))
    amount_label.grid(row=0, column=0)
    amount_entry = tk.Entry(deposit_frame, font=("Calibri", 12))
    amount_entry.grid(row=0, column=1)
    
    deposit_button = tk.Button(deposit_frame, text="Deposit", command=deposit_money, font=("Calibri", 12))
    deposit_button.grid(row=1, column=0, columnspan=2)

# Function to handle withdrawal operation
def withdrawal(username):
    def withdraw_money():
        # Retrieving withdrawal amount from entry field
        amount = float(amount_entry.get())
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM bankaccounts WHERE username = %s", (username,))
        current_balance = cursor.fetchone()[0]
        if current_balance >= amount:
            new_balance = current_balance - amount
            cursor.execute("UPDATE bankaccounts SET balance = %s WHERE username = %s", (new_balance, username))
            connection.commit()
            print("Withdrawal successful. New balance:", new_balance)
        else:
            print("Insufficient funds for withdrawal.")
    
    # Creating a frame for withdrawal operation
    withdrawal_frame = tk.Frame(logged_in_window)
    withdrawal_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    amount_label = tk.Label(withdrawal_frame, text="Amount to withdraw:", font=("Calibri", 12))
    amount_label.grid(row=0, column=0)
    amount_entry = tk.Entry(withdrawal_frame, font=("Calibri", 12))
    amount_entry.grid(row=0, column=1)
    
    withdrawal_button = tk.Button(withdrawal_frame, text="Withdraw", command=withdraw_money, font=("Calibri", 12))
    withdrawal_button.grid(row=1, column=0, columnspan=2)

# Function to handle transfer operation
def transfer(username):
    def transfer_money():
        # Retrieving transfer amount and recipient from entry fields
        amount = float(amount_entry.get())
        recipient = recipient_entry.get()
        print("Transfer amount:", amount, "to", recipient)
        
    # Creating a frame for transfer operation
    transfer_frame = tk.Frame(logged_in_window)
    transfer_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    amount_label = tk.Label(transfer_frame, text="Amount to transfer:", font=("Calibri", 12))
    amount_label.grid(row=0, column=0)
    amount_entry = tk.Entry(transfer_frame, font=("Calibri", 12))
    amount_entry.grid(row=0, column=1)
    
    recipient_label = tk.Label(transfer_frame, text="Recipient username:", font=("Calibri", 12))
    recipient_label.grid(row=1, column=0)
    recipient_entry = tk.Entry(transfer_frame, font=("Calibri", 12))
    recipient_entry.grid(row=1, column=1)
    
    transfer_button = tk.Button(transfer_frame, text="Transfer", command=transfer_money, font=("Calibri", 12))
    transfer_button.grid(row=2, column=0, columnspan=2)

# Function to handle name change
def change_name(username):
    def update_name():
        # Retrieving new name from entry field
        new_name = new_name_entry.get()
        cursor = connection.cursor()
        cursor.execute("UPDATE bankaccounts SET name = %s WHERE username = %s", (new_name, username))
        connection.commit()
        print("Name updated successfully.")

    # Creating a window for name change
    change_name_window = tk.Toplevel(logged_in_window)
    change_name_window.title("Change Name")

    # Creating entry field for new name
    new_name_label = tk.Label(change_name_window, text="New Name:", font=("Calibri", 12))
    new_name_label.grid(row=0, column=0)
    new_name_entry = tk.Entry(change_name_window, font=("Calibri", 12))
    new_name_entry.grid(row=0, column=1)

    update_button = tk.Button(change_name_window, text="Update Name", command=update_name, font=("Calibri", 12))
    update_button.grid(row=1, columnspan=2)

# Function to handle username change
def change_username(username):
    def update_username():
        # Retrieving new username from entry field
        new_username = new_username_entry.get()
        cursor = connection.cursor()
        cursor.execute("UPDATE bankaccounts SET username = %s WHERE username = %s", (new_username, username))
        connection.commit()
        print("Username updated successfully.")

    # Creating a window for username change
    change_username_window = tk.Toplevel(logged_in_window)
    change_username_window.title("Change Username")

    # Creating entry field for new username
    new_username_label = tk.Label(change_username_window, text="New Username:", font=("Calibri", 12))
    new_username_label.grid(row=0, column=0)
    new_username_entry = tk.Entry(change_username_window, font=("Calibri", 12))
    new_username_entry.grid(row=0, column=1)

    update_button = tk.Button(change_username_window, text="Update Username", command=update_username, font=("Calibri", 12))
    update_button.grid(row=1, columnspan=2)

# Function to close an account
def close_account():
    def delete_account():
        # Retrieving username of the account to close
        delete_username = username_entry.get()
        cursor = connection.cursor()
        # Deleting account from the database
        cursor.execute("DELETE FROM bankaccounts WHERE username = %s", (delete_username,))
        connection.commit()
        print("Account for", delete_username, "has been deleted.")

    # Creating a window for closing an account
    close_account_window = tk.Toplevel(logged_in_window)
    close_account_window.title("Close Account")

    # Creating entry field for username of the account to close
    username_label = tk.Label(close_account_window, text="Username of account to close:", font=("Calibri", 12))
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(close_account_window, font=("Calibri", 12))
    username_entry.grid(row=0, column=1)

    delete_button = tk.Button(close_account_window, text="Close Account", command=delete_account, font=("Calibri", 12))
    delete_button.grid(row=1, columnspan=2)

# Function to reset PIN
def reset_pin():
    def reset_pin_action():
        # Retrieving username and new PIN from entry fields
        reset_username = username_entry.get()
        new_pin = pin_entry.get()
        cursor = connection.cursor()
        # Updating PIN in the database
        cursor.execute("UPDATE bankaccounts SET pin = %s WHERE username = %s", (new_pin, reset_username))
        connection.commit()
        print("PIN for", reset_username, "has been reset.")

    # Creating a window for PIN reset
    reset_pin_window = tk.Toplevel(logged_in_window)
    reset_pin_window.title("Reset PIN")

    # Creating entry fields for username and new PIN
    username_label = tk.Label(reset_pin_window, text="Username of account to reset PIN:", font=("Calibri", 12))
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(reset_pin_window, font=("Calibri", 12))
    username_entry.grid(row=0, column=1)

    pin_label = tk.Label(reset_pin_window, text="New PIN:", font=("Calibri", 12))
    pin_label.grid(row=1, column=0)
    pin_entry = tk.Entry(reset_pin_window, show="*", font=("Calibri", 12))
    pin_entry.grid(row=1, column=1)

    reset_button = tk.Button(reset_pin_window, text="Reset PIN", command=reset_pin_action, font=("Calibri", 12))
    reset_button.grid(row=2, columnspan=2)

# Function to handle operations after login
def logged_in(username, perms):
    global logged_in_window
    logged_in_window = tk.Toplevel(root)
    logged_in_window.title("Logged In")
    
    # Dropdown menu to select operations
    operation_label = tk.Label(logged_in_window, text="Select operation:", font=("Calibri", 12))
    operation_label.grid(row=0, column=0)
    operations = ["Change Information", "Deposit", "Withdrawal", "Transfer", "Change Name"]
    if perms == 'admin':
        operations.append("Admin Privilege")
    operation_combobox = ttk.Combobox(logged_in_window, values=operations, font=("Calibri", 12))
    operation_combobox.grid(row=0, column=1)
    
    def execute_operation():
        # Executing selected operation
        operation = operation_combobox.get()
        if operation == "Change Information":
            change_information(username)
        elif operation == "Deposit":
            deposit(username)
        elif operation == "Withdrawal":
            withdrawal(username)
        elif operation == "Transfer":
            transfer(username)
        elif operation == "Change Name":
            change_name(username)
        elif operation == "Admin Privilege" and perms == 'admin':
            admin_privilege(username)
    
    execute_button = tk.Button(logged_in_window, text="Execute", command=execute_operation, font=("Calibri", 12))
    execute_button.grid(row=1, columnspan=2)

# Function to handle admin privileges
def admin_privilege(username):
    def execute_admin_operation():
        # Executing selected admin operation
        admin_operation = admin_operation_combobox.get()
        if admin_operation == "Create Account":
            create_account()
        elif admin_operation == "Close Account":
            close_account()
        elif admin_operation == "Reset PIN":
            reset_pin()
    
    # Creating a window for admin privileges
    admin_privilege_window = tk.Toplevel(logged_in_window)
    admin_privilege_window.title("Admin Privilege")
    
    # Dropdown menu to select admin operations
    admin_operation_label = tk.Label(admin_privilege_window, text="Select admin operation:", font=("Calibri", 12))
    admin_operation_label.grid(row=0, column=0)
    admin_operations = ["Create Account", "Close Account", "Reset PIN"]
    admin_operation_combobox = ttk.Combobox(admin_privilege_window, values=admin_operations, font=("Calibri", 12))
    admin_operation_combobox.grid(row=0, column=1)
    
    execute_button = tk.Button(admin_privilege_window, text="Execute", command=execute_admin_operation, font=("Calibri", 12))
    execute_button.grid(row=1, columnspan=2)

# Creating the main window for the banking app
root = tk.Tk()
root.title("Banking App")

# Login interface
login_label = tk.Label(root, text="Login", font=("Calibri", 16))
login_label.grid(row=0, columnspan=2)

username_label = tk.Label(root, text="Username:", font=("Calibri", 12))
username_label.grid(row=1, column=0)
username_entry = tk.Entry(root, font=("Calibri", 12))
username_entry.grid(row=1, column=1)

pin_label = tk.Label(root, text="PIN:", font=("Calibri", 12))
pin_label.grid(row=2, column=0)
pin_entry = tk.Entry(root, show="*", font=("Calibri", 12))
pin_entry.grid(row=2, column=1)

login_button = tk.Button(root, text="Login", command=login, font=("Calibri", 12))
login_button.grid(row=3, columnspan=2)

login_status_label = tk.Label(root, text="", font=("Calibri", 12))
login_status_label.grid(row=4, columnspan=2)

# Button to create a new account
create_account_button = tk.Button(root, text="Create Account", command=create_account, font=("Calibri", 12))
create_account_button.grid(row=5, columnspan=2)

# Running the main event loop
root.mainloop()

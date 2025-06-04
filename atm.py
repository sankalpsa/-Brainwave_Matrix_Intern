import tkinter as tk
from tkinter import messagebox, simpledialog, font
import sqlite3
import os
import random
import datetime

DB_PATH = "atm_user_data.db"

class ATMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python ATM Interface")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#1f2937")  # dark blue-gray background

        # Initialize database and load user data
        self.conn = None
        self.cursor = None
        self.setup_database()
        self.load_user_data()

        self.attempts = 0
        self.max_attempts = 3

        self.verification_code = None  # For forgot password

        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=10, slant="italic")

        # Create frames
        self.login_frame = tk.Frame(self.root, bg="#1f2937")
        self.menu_frame = tk.Frame(self.root, bg="#1f2937")
        self.transaction_frame = tk.Frame(self.root, bg="#1f2937")

        self.current_operation = None  # track current operation frame showing

        self.create_login_frame()
        self.create_menu_frame()
        self.create_transaction_frame()

        self.login_frame.pack(fill="both", expand=True)

    def setup_database(self):
        """Create and connect to the SQLite database. Create users and logs tables if not exist."""
        db_exists = os.path.exists(DB_PATH)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                pin TEXT NOT NULL,
                balance REAL NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event TEXT NOT NULL
            );
        """)
        self.conn.commit()

        # Check if user exists; if not, add default user
        self.cursor.execute("SELECT COUNT(*) FROM users;")
        count = self.cursor.fetchone()[0]
        if count == 0:
            # Insert default user with pin=1234 and balance=1000.00
            self.cursor.execute("INSERT INTO users (pin, balance) VALUES (?, ?);", ("1234", 1000.0))
            self.conn.commit()
            self.log_event("New user created with default PIN and balance")

    def load_user_data(self):
        """Load user's PIN and balance from database."""
        self.cursor.execute("SELECT pin, balance FROM users WHERE id = 1;")
        row = self.cursor.fetchone()
        if row:
            self.correct_pin, self.balance = row
            # Ensure pin and balance are correct types
            self.correct_pin = str(self.correct_pin).strip()
            self.balance = float(self.balance)
        else:
            self.correct_pin = "1234"
            self.balance = 1000.0

    def log_event(self, event_description):
        """Insert a new log event with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO logs (timestamp, event) VALUES (?, ?);", (timestamp, event_description))
        self.conn.commit()

    def create_login_frame(self):
        lbl = tk.Label(self.login_frame, text="Enter Your PIN", fg="#f9fafb", bg="#1f2937", font=self.title_font)
        lbl.pack(pady=(60,20))

        self.pin_entry = tk.Entry(self.login_frame, show="*", font=self.custom_font, justify="center", width=10)
        self.pin_entry.pack(pady=10)
        self.pin_entry.focus_set()

        self.login_status_lbl = tk.Label(self.login_frame, text="", fg="#f87171", bg="#1f2937", font=self.status_font)
        self.login_status_lbl.pack()

        btn_login = tk.Button(self.login_frame, text="Login", command=self.authenticate, bg="#3b82f6", fg="white", font=self.custom_font,
                              activebackground="#2563eb", activeforeground="white", width=12)
        btn_login.pack(pady=10)

        btn_forgot = tk.Button(self.login_frame, text="Forgot Password?", command=self.forgot_password_flow, bg="#fbbf24", fg="black", font=self.custom_font,
                              activebackground="#f59e0b", activeforeground="black", width=15)
        btn_forgot.pack(pady=10)

    def create_menu_frame(self):
        lbl = tk.Label(self.menu_frame, text="ATM Main Menu", fg="#f9fafb", bg="#1f2937", font=self.title_font)
        lbl.pack(pady=(30,30))

        balance_btn = tk.Button(self.menu_frame, text="Check Balance", command=self.check_balance,
                                bg="#10b981", fg="white", font=self.custom_font, width=20,
                                activebackground="#059669", activeforeground="white")
        balance_btn.pack(pady=10)

        withdraw_btn = tk.Button(self.menu_frame, text="Withdraw Cash", command=self.withdraw_cash,
                                 bg="#f59e0b", fg="white", font=self.custom_font, width=20,
                                 activebackground="#b45309", activeforeground="white")
        withdraw_btn.pack(pady=10)

        deposit_btn = tk.Button(self.menu_frame, text="Deposit Cash", command=self.deposit_cash,
                                bg="#3b82f6", fg="white", font=self.custom_font, width=20,
                                activebackground="#2563eb", activeforeground="white")
        deposit_btn.pack(pady=10)

        change_pin_btn = tk.Button(self.menu_frame, text="Change PIN", command=self.change_pin,
                                   bg="#f97316", fg="white", font=self.custom_font, width=20,
                                   activebackground="#c2410c", activeforeground="white")
        change_pin_btn.pack(pady=10)

        exit_btn = tk.Button(self.menu_frame, text="Exit", command=self.exit_atm,
                             bg="#ef4444", fg="white", font=self.custom_font, width=20,
                             activebackground="#b91c1c", activeforeground="white")
        exit_btn.pack(pady=10)

        self.balance_display_lbl = tk.Label(self.menu_frame, text="", fg="#d1d5db", bg="#1f2937", font=self.status_font)
        self.balance_display_lbl.pack(pady=20)

    def create_transaction_frame(self):
        # This frame will be reused for withdraw and deposit
        self.transaction_lbl = tk.Label(self.transaction_frame, text="", fg="#f9fafb", bg="#1f2937", font=self.title_font)
        self.transaction_lbl.pack(pady=(40, 20))

        self.amount_entry = tk.Entry(self.transaction_frame, font=self.custom_font, justify="center", width=12)
        self.amount_entry.pack(pady=10)

        self.transaction_status_lbl = tk.Label(self.transaction_frame, text="", fg="#f87171", bg="#1f2937", font=self.status_font)
        self.transaction_status_lbl.pack()

        btn_frame = tk.Frame(self.transaction_frame, bg="#1f2937")
        btn_frame.pack(pady=30)

        confirm_btn = tk.Button(btn_frame, text="Confirm", command=self.perform_transaction,
                                bg="#3b82f6", fg="white", font=self.custom_font, width=10,
                                activebackground="#2563eb", activeforeground="white")
        confirm_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel_transaction,
                               bg="#ef4444", fg="white", font=self.custom_font, width=10,
                               activebackground="#b91c1c", activeforeground="white")
        cancel_btn.pack(side="left", padx=10)

    def authenticate(self):
        entered_pin = self.pin_entry.get().strip()
        correct_pin = str(self.correct_pin).strip()
        if entered_pin == correct_pin:
            self.attempts = 0
            self.login_status_lbl.config(text="")
            self.pin_entry.delete(0, 'end')
            self.login_frame.pack_forget()
            self.menu_frame.pack(fill="both", expand=True)
            self.update_balance_display()
            self.log_event("User logged in successfully")
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            if remaining == 0:
                messagebox.showerror("Account Locked", "Too many incorrect PIN attempts. Account locked temporarily.")
                self.log_event("User account locked due to too many failed login attempts")
                self.root.destroy()
            else:
                self.login_status_lbl.config(text=f"Incorrect PIN. Attempts left: {remaining}")
                self.pin_entry.delete(0, 'end')
                self.log_event(f"Failed login attempt. Attempts left: {remaining}")

    def update_balance_display(self):
        self.balance_display_lbl.config(text=f"Current Balance: ${self.balance:,.2f}")

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is:\n${self.balance:,.2f}")
        self.log_event("Checked account balance")

    def withdraw_cash(self):
        self.current_operation = "withdraw"
        self.menu_frame.pack_forget()
        self.transaction_lbl.config(text="Withdraw Cash")
        self.amount_entry.delete(0, 'end')
        self.transaction_status_lbl.config(text="")
        self.transaction_frame.pack(fill="both", expand=True)
        self.amount_entry.focus_set()

    def deposit_cash(self):
        self.current_operation = "deposit"
        self.menu_frame.pack_forget()
        self.transaction_lbl.config(text="Deposit Cash")
        self.amount_entry.delete(0, 'end')
        self.transaction_status_lbl.config(text="")
        self.transaction_frame.pack(fill="both", expand=True)
        self.amount_entry.focus_set()

    def perform_transaction(self):
        amount_text = self.amount_entry.get()
        try:
            amount = float(amount_text)
            if amount <= 0:
                self.transaction_status_lbl.config(text="Amount must be positive.")
                return
            if self.current_operation == "withdraw":
                if amount > self.balance:
                    self.transaction_status_lbl.config(text="Insufficient funds.")
                    return
                confirm = messagebox.askyesno("Confirm Withdrawal", f"Withdraw ${amount:,.2f}?")
                if confirm:
                    new_balance = self.balance - amount
                    self.update_balance(new_balance)
                    messagebox.showinfo("Success", f"Please take your cash: ${amount:,.2f}")
                    self.log_event(f"Withdrew ${amount:,.2f} successfully")
            elif self.current_operation == "deposit":
                confirm = messagebox.askyesno("Confirm Deposit", f"Deposit ${amount:,.2f}?")
                if confirm:
                    new_balance = self.balance + amount
                    self.update_balance(new_balance)
                    messagebox.showinfo("Success", f"${amount:,.2f} deposited successfully.")
                    self.log_event(f"Deposited ${amount:,.2f} successfully")
            else:
                self.transaction_status_lbl.config(text="Unknown operation.")
                return
            self.transaction_frame.pack_forget()
            self.update_balance_display()
            self.menu_frame.pack(fill="both", expand=True)
        except ValueError:
            self.transaction_status_lbl.config(text="Invalid input. Please enter a numeric amount.")

    def cancel_transaction(self):
        self.transaction_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def change_pin(self):
        current = simpledialog.askstring("Current PIN", "Enter current PIN:", show="*")
        if current != self.correct_pin:
            messagebox.showerror("Error", "Incorrect current PIN.")
            self.log_event("Failed PIN change attempt due to incorrect current PIN")
            return

        new_pin = simpledialog.askstring("New PIN", "Enter new 4-digit PIN:", show="*")
        if new_pin is None:
            return
        if len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror("Error", "PIN must be exactly 4 digits.")
            return

        confirm_pin = simpledialog.askstring("Confirm PIN", "Confirm new PIN:", show="*")
        if confirm_pin != new_pin:
            messagebox.showerror("Error", "PIN confirmation does not match.")
            return

        self.update_pin(new_pin)
        messagebox.showinfo("Success", "PIN changed successfully.")
        self.log_event("PIN changed successfully by user")

    def forgot_password_flow(self):
        # Step 1: Generate verification code
        self.verification_code = "{:06d}".format(random.randint(0, 999999))
        # Simulate sending to user's phone by showing in dialog
        messagebox.showinfo("Verification Code Sent",
                            f"Verification code has been sent to your registered phone number.\n\nCode (for demo): {self.verification_code}")

        # Step 2: Ask user to enter verification code
        entered_code = simpledialog.askstring("Verification", "Enter the 6-digit verification code:")
        if entered_code is None:
            return  # Cancelled
        if entered_code != self.verification_code:
            messagebox.showerror("Error", "Verification code incorrect.")
            self.log_event("Failed password reset due to incorrect verification code")
            return

        # Step 3: Allow user to reset PIN
        new_pin = simpledialog.askstring("Reset PIN", "Enter new 4-digit PIN:", show="*")
        if new_pin is None:
            return
        if len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror("Error", "PIN must be exactly 4 digits.")
            return
        confirm_pin = simpledialog.askstring("Confirm PIN", "Confirm new PIN:", show="*")
        if confirm_pin != new_pin:
            messagebox.showerror("Error", "PIN confirmation does not match.")
            return

        self.update_pin(new_pin)
        messagebox.showinfo("Success", "Your PIN has been reset successfully.")
        self.log_event("PIN reset successfully via forgot password")

    def update_balance(self, new_balance):
        """Update balance in the database and in-memory."""
        self.balance = new_balance
        self.cursor.execute("UPDATE users SET balance = ? WHERE id = 1;", (self.balance,))
        self.conn.commit()

    def update_pin(self, new_pin):
        """Update PIN in the database and in-memory."""
        self.correct_pin = new_pin
        self.cursor.execute("UPDATE users SET pin = ? WHERE id = 1;", (self.correct_pin,))
        self.conn.commit()

    def exit_atm(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.log_event("User exited ATM application")
            self.conn.close()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMGUI(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox, simpledialog, font, ttk, filedialog
import sqlite3
import os
import random
import datetime
import hashlib
import hmac
import csv

# ---------- Configuration and Utilities ----------

DB_PATH = "advanced_atm.db"
DEFAULT_LANGUAGE = 'en'

def get_hashed_pin(pin, salt=None):
    """
    Hash PIN using PBKDF2 HMAC SHA256 with salt.
    Returns (salt_hex, hash_hex).
    """
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt)
    dk = hashlib.pbkdf2_hmac('sha256', pin.encode(), salt, 100000)
    return salt.hex(), dk.hex()

def verify_pin(stored_salt, stored_hash, entered_pin):
    salt = stored_salt
    expected_hash = stored_hash
    _, entered_hash = get_hashed_pin(entered_pin, salt)
    return hmac.compare_digest(expected_hash, entered_hash)


# Localization dictionaries
locales = {
    'en': {
        'title': "ATM Interface",
        'login': "Login",
        'register': "Register",
        'username': "Username",
        'pin': "PIN",
        'enter_pin': "Enter PIN",
        'enter_username': "Enter Username",
        'forgot_password': "Forgot Password?",
        'verification_code_sent': "Verification code sent (demo): {}",
        'enter_verification_code': "Enter the 6-digit verification code",
        'verification_failed': "Verification code incorrect.",
        'reset_pin': "Reset PIN",
        'confirm_pin': "Confirm PIN",
        'pin_must_4_digits': "PIN must be exactly 4 digits.",
        'pin_mismatch': "PIN confirmation does not match.",
        'pin_reset_success': "Your PIN has been reset successfully.",
        'pin_change': "Change PIN",
        'current_pin': "Enter current PIN:",
        'new_pin': "Enter new 4-digit PIN:",
        'confirm_new_pin': "Confirm new PIN:",
        'incorrect_current_pin': "Incorrect current PIN.",
        'balance': "Balance",
        'withdraw': "Withdraw Cash",
        'deposit': "Deposit Cash",
        'change_pin_btn': "Change PIN",
        'logout': "Logout",
        'exit': "Exit",
        'check_balance': "Check Balance",
        'enter_amount': "Enter amount:",
        'amount_positive': "Amount must be positive.",
        'insufficient_funds': "Insufficient funds.",
        'confirm_withdraw': "Withdraw ${:,.2f}?",
        'confirm_deposit': "Deposit ${:,.2f}?",
        'success_withdraw': "Please take your cash: ${:,.2f}",
        'success_deposit': "${:,.2f} deposited successfully.",
        'transaction_history': "Transaction History",
        'export_logs': "Export Logs",
        'no_transactions': "No transactions found.",
        'invalid_amount': "Invalid amount. Please enter a numeric value.",
        'account_locked': "Too many incorrect PIN attempts. Account locked temporarily.",
        'failed_login': "Incorrect username or PIN. Attempts left: {}",
        'locked_out': "Account locked due to too many failed attempts. Try later.",
        'welcome': "Welcome, {}!",
        'inactive_logout': "Logged out due to inactivity.",
        'theme_toggle': "Toggle Theme",
        'language_toggle': "Change Language",
        'register_success': "Registration successful. You can login now.",
        'user_exists': "Username already exists.",
        'registration_failed': "Registration failed. Try again.",
        'log_date': "Date",
        'log_event': "Event",
        'logout_confirm': "Are you sure you want to logout?",
        'exit_confirm': "Are you sure you want to exit?",
        'user_not_found': "User not found.",
        'cancelled': "Operation cancelled.",
    },
    'es': {
        'title': "Interfaz ATM",
        'login': "Iniciar sesión",
        'register': "Registrar",
        'username': "Usuario",
        'pin': "PIN",
        'enter_pin': "Ingrese PIN",
        'enter_username': "Ingrese usuario",
        'forgot_password': "¿Olvidó su PIN?",
        'verification_code_sent': "Código de verificación enviado (demo): {}",
        'enter_verification_code': "Ingrese el código de verificación de 6 dígitos",
        'verification_failed': "Código de verificación incorrecto.",
        'reset_pin': "Restablecer PIN",
        'confirm_pin': "Confirmar PIN",
        'pin_must_4_digits': "El PIN debe tener exactamente 4 dígitos.",
        'pin_mismatch': "La confirmación del PIN no coincide.",
        'pin_reset_success': "Su PIN ha sido restablecido con éxito.",
        'pin_change': "Cambiar PIN",
        'current_pin': "Ingrese el PIN actual:",
        'new_pin': "Ingrese nuevo PIN de 4 dígitos:",
        'confirm_new_pin': "Confirme el nuevo PIN:",
        'incorrect_current_pin': "PIN actual incorrecto.",
        'balance': "Saldo",
        'withdraw': "Retirar efectivo",
        'deposit': "Depositar efectivo",
        'change_pin_btn': "Cambiar PIN",
        'logout': "Cerrar sesión",
        'exit': "Salir",
        'check_balance': "Consultar saldo",
        'enter_amount': "Ingrese monto:",
        'amount_positive': "El monto debe ser positivo.",
        'insufficient_funds': "Fondos insuficientes.",
        'confirm_withdraw': "¿Retirar ${:,.2f}?",
        'confirm_deposit': "¿Depositar ${:,.2f}?",
        'success_withdraw': "Por favor tome su efectivo: ${:,.2f}",
        'success_deposit': "${:,.2f} depositados con éxito.",
        'transaction_history': "Historial de transacciones",
        'export_logs': "Exportar registros",
        'no_transactions': "No se encontraron transacciones.",
        'invalid_amount': "Monto inválido. Por favor ingrese un valor numérico.",
        'account_locked': "Demasiados intentos fallidos. Cuenta bloqueada temporalmente.",
        'failed_login': "Usuario o PIN incorrectos. Intentos restantes: {}",
        'locked_out': "Cuenta bloqueada por demasiados intentos fallidos. Intente más tarde.",
        'welcome': "Bienvenido(a), {}!",
        'inactive_logout': "Sesión cerrada por inactividad.",
        'theme_toggle': "Cambiar tema",
        'language_toggle': "Cambiar idioma",
        'register_success': "Registro exitoso. Ahora puede iniciar sesión.",
        'user_exists': "El usuario ya existe.",
        'registration_failed': "Registro fallido. Intenta de nuevo.",
        'log_date': "Fecha",
        'log_event': "Evento",
        'logout_confirm': "¿Está seguro que desea cerrar sesión?",
        'exit_confirm': "¿Está seguro que desea salir?",
        'user_not_found': "Usuario no encontrado.",
        'cancelled': "Operación cancelada.",
    },
}

def translate(text_id):
    return locales.get(App.language, locales[DEFAULT_LANGUAGE]).get(text_id, text_id)


# ---------- Main Application Class ----------

class App:
    language = DEFAULT_LANGUAGE

    def __init__(self, root):
        self.root = root
        self.root.title(translate('title'))
        self.root.geometry("500x550")
        self.root.minsize(500, 550)
        self.root.configure(bg="#1f2937")  # Default dark theme background
        self.style = ttk.Style()
        self.dark_theme = True
        self.set_theme(self.dark_theme)

        # SQLite connection
        self.conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        self.setup_db()

        self.current_user_id = None
        self.current_username = None

        # Rate limiting data
        self.failed_login_attempts = {}
        self.locked_out_users = {}

        # Inactivity timer
        self.inactivity_seconds = 5 * 60  # 5 minutes auto logout
        self.inactivity_job = None

        # Verification code for forgot password
        self.verification_code = None
        self.verification_user = None

        # Fonts
        self.font_title = font.Font(family="Helvetica", size=22, weight="bold")
        self.font_button = font.Font(family="Helvetica", size=12, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=11)
        self.font_status = font.Font(family="Helvetica", size=10, slant="italic")

        # Setup frames
        self.frames = {}
        self.create_login_frame()
        self.create_register_frame()
        self.create_main_menu_frame()
        self.create_transaction_frame()
        self.create_history_frame()

        self.show_frame('login')

        # Bind events for inactivity
        self.root.bind_all("Any-KeyPress>", self.reset_inactivity_timer)
        self.root.bind_all("Any-ButtonPress>", self.reset_inactivity_timer)

    # ---------------- Database setup ----------------

    def setup_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                pin_salt TEXT NOT NULL,
                pin_hash TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                event TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    # ---------------- Inactivity Logout ----------------

    def reset_inactivity_timer(self, event=None):
        if self.inactivity_job:
            self.root.after_cancel(self.inactivity_job)
        self.inactivity_job = self.root.after(self.inactivity_seconds * 1000, self.handle_inactivity_logout)

    def handle_inactivity_logout(self):
        if self.current_user_id:
            messagebox.showinfo(translate('inactive_logout'), translate('inactive_logout'))
            self.log_event(self.current_user_id, translate('inactive_logout'))
            self.logout()

    # ----------------- Frame management -----------------

    def show_frame(self, frame_name):
        for fr in self.frames.values():
            fr.pack_forget()
        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill='both', expand=True)
        self.reset_inactivity_timer()

    # ----------------- Login/Register --------------------

    def create_login_frame(self):
        frame = tk.Frame(self.root, bg="#1f2937")
        self.frames['login'] = frame

        label = tk.Label(frame, text=translate('login'), font=self.font_title, fg="#f9fafb", bg="#1f2937")
        label.pack(pady=25)

        username_lbl = tk.Label(frame, text=translate('username'), font=self.font_label, fg="#d1d5db", bg="#1f2937")
        username_lbl.pack(pady=(10,0))
        self.login_username = tk.Entry(frame, font=self.font_button)
        self.login_username.pack(pady=(0,15))
        self.login_username.focus_set()

        pin_lbl = tk.Label(frame, text=translate('pin'), font=self.font_label, fg="#d1d5db", bg="#1f2937")
        pin_lbl.pack()
        self.login_pin = tk.Entry(frame, show="*", font=self.font_button)
        self.login_pin.pack(pady=(0,15))

        self.login_status = tk.Label(frame, text="", fg="#f87171", bg="#1f2937", font=self.font_status)
        self.login_status.pack()

        btn_login = tk.Button(frame, text=translate('login'), command=self.handle_login,
                              bg="#3b82f6", fg="white", font=self.font_button,
                              activebackground="#2563eb", activeforeground="white", width=15)
        btn_login.pack(pady=(10, 5))

        btn_register = tk.Button(frame, text=translate('register'), command=lambda: self.show_frame('register'),
                                 bg="#10b981", fg="white", font=self.font_button,
                                 activebackground="#059669", activeforeground="white", width=15)
        btn_register.pack(pady=5)

        btn_forgot = tk.Button(frame, text=translate('forgot_password'), command=self.forgot_password_flow,
                               bg="#fbbf24", fg="black", font=self.font_button,
                               activebackground="#f59e0b", activeforeground="black", width=15)
        btn_forgot.pack(pady=5)

        # Allow pressing Enter to trigger login
        self.root.bind('Return>', lambda event: self.handle_login())

    def create_register_frame(self):
        frame = tk.Frame(self.root, bg="#1f2937")
        self.frames['register'] = frame

        label = tk.Label(frame, text=translate('register'), font=self.font_title, fg="#f9fafb", bg="#1f2937")
        label.pack(pady=25)

        username_lbl = tk.Label(frame, text=translate('username'), font=self.font_label, fg="#d1d5db", bg="#1f2937")
        username_lbl.pack(pady=(10,0))
        self.reg_username = tk.Entry(frame, font=self.font_button)
        self.reg_username.pack(pady=(0,15))

        pin_lbl = tk.Label(frame, text=translate('pin'), font=self.font_label, fg="#d1d5db", bg="#1f2937")
        pin_lbl.pack()
        self.reg_pin = tk.Entry(frame, show="*", font=self.font_button)
        self.reg_pin.pack(pady=(0,15))

        confirm_pin_lbl = tk.Label(frame, text=translate('confirm_pin'), font=self.font_label, fg="#d1d5db", bg="#1f2937")
        confirm_pin_lbl.pack()
        self.reg_confirm_pin = tk.Entry(frame, show="*", font=self.font_button)
        self.reg_confirm_pin.pack(pady=(0,15))

        self.register_status = tk.Label(frame, text="", fg="#f87171", bg="#1f2937", font=self.font_status)
        self.register_status.pack()

        btn_register = tk.Button(frame, text=translate('register'), command=self.handle_register,
                                 bg="#10b981", fg="white", font=self.font_button,
                                 activebackground="#059669", activeforeground="white", width=15)
        btn_register.pack(pady=(10, 5))

        btn_back = tk.Button(frame, text=translate('login'), command=lambda: self.show_frame('login'),
                             bg="#3b82f6", fg="white", font=self.font_button,
                             activebackground="#2563eb", activeforeground="white", width=15)
        btn_back.pack(pady=5)

    # --------------------- Main Menu ---------------------

    def create_main_menu_frame(self):
        frame = tk.Frame(self.root, bg="#1f2937")
        self.frames['menu'] = frame

        self.welcome_lbl = tk.Label(frame, text="", font=self.font_title, fg="#f9fafb", bg="#1f2937")
        self.welcome_lbl.pack(pady=15)

        btn_check_balance = tk.Button(frame, text=translate('check_balance'), command=self.show_balance,
                                      bg="#10b981", fg="white", font=self.font_button,
                                      activebackground="#059669", activeforeground="white", width=20)
        btn_check_balance.pack(pady=8)

        btn_withdraw = tk.Button(frame, text=translate('withdraw'), command=lambda: self.start_transaction('withdraw'),
                                 bg="#f59e0b", fg="white", font=self.font_button,
                                 activebackground="#b45309", activeforeground="white", width=20)
        btn_withdraw.pack(pady=8)

        btn_deposit = tk.Button(frame, text=translate('deposit'), command=lambda: self.start_transaction('deposit'),
                                bg="#3b82f6", fg="white", font=self.font_button,
                                activebackground="#2563eb", activeforeground="white", width=20)
        btn_deposit.pack(pady=8)

        btn_history = tk.Button(frame, text=translate('transaction_history'), command=self.show_history,
                                bg="#8b5cf6", fg="white", font=self.font_button,
                                activebackground="#7c3aed", activeforeground="white", width=20)
        btn_history.pack(pady=8)

        btn_pin_change = tk.Button(frame, text=translate('change_pin_btn'), command=self.change_pin_flow,
                                   bg="#f97316", fg="white", font=self.font_button,
                                   activebackground="#c2410c", activeforeground="white", width=20)
        btn_pin_change.pack(pady=8)

        btn_export = tk.Button(frame, text=translate('export_logs'), command=self.export_logs,
                               bg="#06b6d4", fg="white", font=self.font_button,
                               activebackground="#0891b2", activeforeground="white", width=20)
        btn_export.pack(pady=8)

        btn_logout = tk.Button(frame, text=translate('logout'), command=self.logout_confirm,
                               bg="#ef4444", fg="white", font=self.font_button,
                               activebackground="#b91c1c", activeforeground="white", width=20)
        btn_logout.pack(pady=8)

        # Theme toggle and language toggle buttons
        btn_theme = tk.Button(frame, text=translate('theme_toggle'), command=self.toggle_theme,
                              bg="#6b7280", fg="white", font=self.font_button,
                              activebackground="#4b5563", activeforeground="white", width=20)
        btn_theme.pack(pady=8)

        btn_lang = tk.Button(frame, text=translate('language_toggle'), command=self.toggle_language,
                             bg="#6b7280", fg="white", font=self.font_button,
                             activebackground="#4b5563", activeforeground="white", width=20)
        btn_lang.pack(pady=8)

    # ---------------- Transaction Frame ------------------

    def create_transaction_frame(self):
        frame = tk.Frame(self.root, bg="#1f2937")
        self.frames['transaction'] = frame

        self.trans_label = tk.Label(frame, text="", font=self.font_title, fg="#f9fafb", bg="#1f2937")
        self.trans_label.pack(pady=(40,20))

        amount_lbl = tk.Label(frame, text=translate('enter_amount'), font=self.font_label, fg="#d1d5db", bg="#1f2937")
        amount_lbl.pack()

        self.trans_amount = tk.Entry(frame, font=self.font_button, justify="center")
        self.trans_amount.pack(pady=10)

        self.trans_status = tk.Label(frame, text="", fg="#f87171", bg="#1f2937", font=self.font_status)
        self.trans_status.pack()

        btn_frame = tk.Frame(frame, bg="#1f2937")
        btn_frame.pack(pady=30)

        btn_confirm = tk.Button(btn_frame, text=translate('confirm_pin'), command=self.perform_transaction,
                                bg="#3b82f6", fg="white", font=self.font_button, width=12,
                                activebackground="#2563eb", activeforeground="white")
        btn_confirm.pack(side='left', padx=10)

        btn_cancel = tk.Button(btn_frame, text=translate('cancelled'), command=self.cancel_transaction,
                               bg="#ef4444", fg="white", font=self.font_button, width=12,
                               activebackground="#b91c1c", activeforeground="white")
        btn_cancel.pack(side='left', padx=10)

    # ---------------- Transaction History Frame -----------

    def create_history_frame(self):
        frame = tk.Frame(self.root, bg="#1f2937")
        self.frames['history'] = frame

        lbl_title = tk.Label(frame, text=translate('transaction_history'), font=self.font_title, fg="#f9fafb", bg="#1f2937")
        lbl_title.pack(pady=15)

        # Treeview for history display with scrollbar
        columns = ('date', 'type', 'amount')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        self.tree.heading('date', text=translate('log_date'))
        self.tree.heading('type', text=translate('log_event'))
        self.tree.heading('amount', text='Amount')

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
        vsb.pack(side='left', fill='y', pady=10, padx=(0,10))

        btn_back = tk.Button(frame, text=translate('login'), command=lambda: self.show_frame('menu'),
                             bg="#3b82f6", fg="white", font=self.font_button,
                             activebackground="#2563eb", activeforeground="white", width=15)
        btn_back.pack(pady=10)

    # --------------------- Authentication ---------------------

    def handle_login(self):
        username = self.login_username.get().strip()
        pin = self.login_pin.get().strip()
        if not username or not pin:
            self.login_status.config(text=translate('user_not_found'))
            return

        # Check lockout
        if username in self.locked_out_users:
            self.login_status.config(text=translate('locked_out'))
            return

        self.cursor.execute("SELECT id, pin_salt, pin_hash FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if not row:
            self.login_status.config(text=translate('failed_login').format(3))
            return
        user_id, pin_salt, pin_hash = row

        if verify_pin(pin_salt, pin_hash, pin):
            self.current_user_id = user_id
            self.current_username = username
            self.login_status.config(text="")
            self.login_username.delete(0, 'end')
            self.login_pin.delete(0, 'end')
            self.failed_login_attempts.pop(username, None)
            self.locked_out_users.pop(username, None)
            self.load_user_balance()
            self.update_welcome()
            self.show_frame('menu')
            self.log_event(user_id, "User logged in successfully")
        else:
            self.failed_login_attempts[username] = self.failed_login_attempts.get(username, 0) + 1
            tries_left = 3 - self.failed_login_attempts[username]
            if tries_left = 0:
                self.locked_out_users[username] = True
                self.log_event(user_id, "User account locked due to too many failed login attempts")
                self.login_status.config(text=translate('account_locked'))
            else:
                self.log_event(user_id, f"Failed login attempt, {tries_left} tries left")
                self.login_status.config(text=translate('failed_login').format(tries_left))
            self.login_pin.delete(0, 'end')

    def handle_register(self):
        username = self.reg_username.get().strip()
        pin = self.reg_pin.get().strip()
        confirm_pin = self.reg_confirm_pin.get().strip()
        if not username or not pin or not confirm_pin:
            self.register_status.config(text=translate('registration_failed'))
            return
        if len(pin) != 4 or not pin.isdigit():
            self.register_status.config(text=translate('pin_must_4_digits'))
            return
        if pin != confirm_pin:
            self.register_status.config(text=translate('pin_mismatch'))
            return
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone():
            self.register_status.config(text=translate('user_exists'))
            return

        salt, hash_pin = get_hashed_pin(pin)
        try:
            self.cursor.execute("INSERT INTO users (username, pin_salt, pin_hash, balance) VALUES (?, ?, ?, ?)",
                                (username, salt, hash_pin, 0.0))
            self.conn.commit()
        except Exception:
            self.register_status.config(text=translate('registration_failed'))
            return

        messagebox.showinfo(translate('register'), translate('register_success'))
        self.reg_username.delete(0, 'end')
        self.reg_pin.delete(0, 'end')
        self.reg_confirm_pin.delete(0, 'end')
        self.register_status.config(text="")
        self.show_frame('login')

    # ----------------- Load user data ---------------------

    def load_user_balance(self):
        self.cursor.execute("SELECT balance FROM users WHERE id = ?", (self.current_user_id,))
        row = self.cursor.fetchone()
        self.current_balance = row[0] if row else 0.0

    def update_welcome(self):
        self.welcome_lbl.config(text=translate('welcome').format(self.current_username))

    # ------------------ Banking functions ------------------

    def show_balance(self):
        msg = f"{translate('balance')}: ${self.current_balance:,.2f}"
        messagebox.showinfo(translate('balance'), msg)
        self.log_event(self.current_user_id, "Checked balance")

    def start_transaction(self, trans_type):
        self.trans_type = trans_type
        self.trans_label.config(text=translate(trans_type))
        self.trans_amount.delete(0, 'end')
        self.trans_status.config(text="")
        self.show_frame('transaction')

    def perform_transaction(self):
        amount_str = self.trans_amount.get().strip()
        try:
            amount = float(amount_str)
            if amount = 0:
                self.trans_status.config(text=translate('amount_positive'))
                return
        except ValueError:
            self.trans_status.config(text=translate('invalid_amount'))
            return

        if self.trans_type == 'withdraw':
            if amount > self.current_balance:
                self.trans_status.config(text=translate('insufficient_funds'))
                return
            if not messagebox.askyesno(translate('withdraw'), translate('confirm_withdraw').format(amount)):
                return
            self.current_balance -= amount
            self.update_balance_in_db()
            self.log_transaction('withdraw', amount)
            messagebox.showinfo(translate('withdraw'), translate('success_withdraw').format(amount))
            self.log_event(self.current_user_id, f"Withdrew ${amount:,.2f}")
        elif self.trans_type == 'deposit':
            if not messagebox.askyesno(translate('deposit'), translate('confirm_deposit').format(amount)):
                return
            self.current_balance += amount
            self.update_balance_in_db()
            self.log_transaction('deposit', amount)
            messagebox.showinfo(translate('deposit'), translate('success_deposit').format(amount))
            self.log_event(self.current_user_id, f"Deposited ${amount:,.2f}")
        else:
            self.trans_status.config(text="Unknown transaction type")
            return

        self.show_frame('menu')

    def cancel_transaction(self):
        self.show_frame('menu')

    def update_balance_in_db(self):
        self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (self.current_balance, self.current_user_id))
        self.conn.commit()

    def log_transaction(self, trans_type, amount):
        self.cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)",
                            (self.current_user_id, trans_type, amount))
        self.conn.commit()

    # -------------- Transaction History -------------------

    def show_history(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT timestamp, type, amount FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
                            (self.current_user_id,))
        rows = self.cursor.fetchall()
        if not rows:
            messagebox.showinfo(translate('transaction_history'), translate('no_transactions'))
            return
        for ts, ttype, amt in rows:
            ts_str = ts if isinstance(ts, str) else ts.strftime("%Y-%m-%d %H:%M:%S")
            self.tree.insert('', 'end', values=(ts_str, ttype.capitalize(), f"${amt:,.2f}"))
        self.show_frame('history')

    # -------------- PIN Change -----------------------------

    def change_pin_flow(self):
        current_pin = simpledialog.askstring(translate('pin_change'), translate('current_pin'), show='*')
        if current_pin is None:
            return  # Cancelled
        if not verify_pin_user(self.current_user_id, current_pin, self.cursor):
            messagebox.showerror(translate('pin_change'), translate('incorrect_current_pin'))
            self.log_event(self.current_user_id, "Failed PIN change - incorrect current PIN")
            return

        new_pin = simpledialog.askstring(translate('pin_change'), translate('new_pin'), show='*')
        if new_pin is None:
            return
        if len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror(translate('pin_change'), translate('pin_must_4_digits'))
            return

        confirm_pin = simpledialog.askstring(translate('pin_change'), translate('confirm_new_pin'), show='*')
        if confirm_pin != new_pin:
            messagebox.showerror(translate('pin_change'), translate('pin_mismatch'))
            return

        self.update_user_pin(new_pin)
        messagebox.showinfo(translate('pin_change'), "PIN changed successfully.")
        self.log_event(self.current_user_id, "PIN changed successfully")

    def update_user_pin(self, new_pin):
        salt, hash_pin = get_hashed_pin(new_pin)
        self.cursor.execute("UPDATE users SET pin_salt = ?, pin_hash = ? WHERE id = ?", (salt, hash_pin, self.current_user_id))
        self.conn.commit()

    # ---------------- Forgot Password ---------------------

    def forgot_password_flow(self):
        # Ask username first
        username = simpledialog.askstring(translate('forgot_password'), translate('enter_username'))
        if username is None:
            messagebox.showinfo(translate('forgot_password'), translate('cancelled'))
            return
        username = username.strip()
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user is None:
            messagebox.showerror(translate('forgot_password'), translate('user_not_found'))
            return
        user_id = user[0]
        self.verification_user = user_id
        self.verification_code = "{:06d}".format(random.randint(0, 999999))

        # Show verification code dialog (simulate SMS)
        messagebox.showinfo(translate('forgot_password'), translate('verification_code_sent').format(self.verification_code))

        # Ask user to enter verification code
        entered_code = simpledialog.askstring(translate('forgot_password'), translate('enter_verification_code'))
        if entered_code is None:
            messagebox.showinfo(translate('forgot_password'), translate('cancelled'))
            return
        if entered_code.strip() != self.verification_code:
            messagebox.showerror(translate('forgot_password'), translate('verification_failed'))
            self.log_event(user_id, "Failed password reset - wrong verification code")
            return

        # Ask new PIN
        new_pin = simpledialog.askstring(translate('forgot_password'), translate('reset_pin'), show='*')
        if new_pin is None:
            messagebox.showinfo(translate('forgot_password'), translate('cancelled'))
            return
        if len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror(translate('forgot_password'), translate('pin_must_4_digits'))
            return

        confirm_pin = simpledialog.askstring(translate('forgot_password'), translate('confirm_new_pin'), show='*')
        if confirm_pin != new_pin:
            messagebox.showerror(translate('forgot_password'), translate('pin_mismatch'))
            return

        salt, hash_pin = get_hashed_pin(new_pin)
        self.cursor.execute("UPDATE users SET pin_salt = ?, pin_hash = ? WHERE id = ?", (salt, hash_pin, user_id))
        self.conn.commit()
        messagebox.showinfo(translate('forgot_password'), translate('pin_reset_success'))
        self.log_event(user_id, "PIN reset via forgot password")

    # ---------------- Logging -----------------------------

    def log_event(self, user_id, event):
        self.cursor.execute("INSERT INTO logs (user_id, event) VALUES (?, ?)", (user_id, event))
        self.conn.commit()

    # ---------------- Export Logs -------------------------

    def export_logs(self):
        if not self.current_user_id:
            return
        self.cursor.execute("SELECT timestamp, event FROM logs WHERE user_id = ? ORDER BY timestamp DESC", (self.current_user_id,))
        logs = self.cursor.fetchall()
        csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not csv_path:
            return
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([translate('log_date'), translate('log_event')])
                for row in logs:
                    ts_str = row[0] if isinstance(row[0], str) else row[0].strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([ts_str, row[1]])
            messagebox.showinfo(translate('export_logs'), f"Logs exported to {csv_path}")
        except Exception as e:
            messagebox.showerror(translate('export_logs'), str(e))

    # ---------------- Logout ------------------------------

    def logout_confirm(self):
        if messagebox.askyesno(translate('logout'), translate('logout_confirm')):
            self.logout()

    def logout(self):
        self.current_user_id = None
        self.current_username = None
        self.failed_login_attempts.clear()
        self.locked_out_users.clear()
        self.show_frame('login')
        self.log_event(None, "User logged out")

    # -------------- Theme and Language --------------------

    def set_theme(self, dark_mode:bool):
        if dark_mode:
            self.style.theme_use('clam')
            self.style.configure('.', background='#1f2937', foreground='white', fieldbackground='#374151',
                                 font=('Helvetica', 11))
            self.root.configure(bg='#1f2937')
        else:
            self.style.theme_use('default')
            self.style.configure('.', background='SystemButtonFace', foreground='black',
                                 font=('Helvetica', 11))
            self.root.configure(bg='SystemButtonFace')

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.set_theme(self.dark_theme)

    def toggle_language(self):
        if App.language == 'en':
            App.language = 'es'
        else:
            App.language = 'en'
        self.root.title(translate('title'))
        # Rebuild all UI labels and buttons for new language
        self.rebuild_ui_language()

    def rebuild_ui_language(self):
        # Destroy all frames and recreate using current language
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        self.create_login_frame()
        self.create_register_frame()
        self.create_main_menu_frame()
        self.create_transaction_frame()
        self.create_history_frame()
        if self.current_user_id:
            self.update_welcome()
            self.show_frame('menu')
        else:
            self.show_frame('login')

# Utility function outside class for PIN verification
def verify_pin_user(user_id, entered_pin, cursor):
    cursor.execute("SELECT pin_salt, pin_hash FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        return False
    pin_salt, pin_hash = row
    return verify_pin(pin_salt, pin_hash, entered_pin)


# -------- Unit Tests for core logic -------------------

def run_tests():
    print("Running unit tests...")

    # Test hashing and verification
    pin = "1234"
    salt, hash_pin = get_hashed_pin(pin)
    assert verify_pin(salt, hash_pin, pin), "PIN verification failed for correct PIN"
    assert not verify_pin(salt, hash_pin, "0000"), "PIN verified incorrectly for wrong PIN"

    # Test database insertion and retrieval
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        pin_salt TEXT NOT NULL,
        pin_hash TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0
    )''')
    salt, hash_pin = get_hashed_pin("9999")
    cursor.execute("INSERT INTO users (username, pin_salt, pin_hash, balance) VALUES (?, ?, ?, ?)",
                   ("testuser", salt, hash_pin, 500.0))
    conn.commit()

    cursor.execute("SELECT id FROM users WHERE username = ?", ("testuser",))
    row = cursor.fetchone()
    assert row is not None, "User insertion failed"

    user_id = row[0]
    assert verify_pin_user(user_id, "9999", cursor), "verify_pin_user failed for valid PIN"
    assert not verify_pin_user(user_id, "0000", cursor), "verify_pin_user incorrectly passed for invalid PIN"

    print("All tests passed successfully.")

# ------------------ Run application -------------------

if __name__ == "__main__":
    run_tests()
    root = tk.Tk()
    app = App(root)
    root.mainloop()

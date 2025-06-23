# Brain Wave Matrix Solution - Task 1: Python ATM Interface

## Overview

This project is a **Python ATM Interface** application, designed as Task 1 for the Brain Wave Matrix Solution. It provides a realistic graphical ATM simulation with user authentication, balance inquiry, cash withdrawal, cash deposit, PIN management, and event logging. The application uses Python's `tkinter` for the GUI and `sqlite3` for persistent data storage.

---

## Features

- **User Login & Authentication:**  
  Secure login screen with PIN entry, limited attempts, and account lockout on repeated failures.

- **Forgot PIN/Password Workflow:**  
  Users can reset their PIN using a verification code (demo: code displayed in dialog).

- **Main Menu:**  
  - **Check Balance:** View current account balance.
  - **Withdraw Cash:** Withdraw funds, with balance validation.
  - **Deposit Cash:** Add funds to your account.
  - **Change PIN:** Securely change your account PIN.
  - **Exit:** Safely exit the ATM interface.

- **Transaction Logging:**  
  All actions are logged in an SQLite database for review and audit.

- **Data Persistence:**  
  User data (PIN and balance) and logs are stored in an SQLite database (`atm_user_data.db`).

- **Customizable GUI:**  
  Modern look and feel with custom fonts and color schemes for an enhanced user experience.

---

## Requirements

- Python 3.x  
- Standard Python libraries used: `tkinter`, `sqlite3`, `os`, `random`, `datetime`

No external or third-party dependencies are required.

---

## How to Run

1. **Clone or Download the Repository:**
    ```
    git clone <repo-url>
    cd <repo-directory>
    ```

2. **Run the Application:**
    ```bash
    python atm_gui.py
    ```
    *(Replace `atm_gui.py` with the actual filename if different.)*

3. **Default User Credentials:**
    - **PIN:** `1234`
    - **Initial Balance:** `$1000.00`

4. **Database:**
    - A file named `atm_user_data.db` will be created in the working directory to store user data and activity logs.

---

## File Structure

- `atm_gui.py` - Main application script containing all the code for the ATM interface.
- `atm_user_data.db` - SQLite database file (auto-created on first run).
- `README.md` - This documentation file.

---

## Usage & Demo

1. **Login:**  
   Enter the default PIN (`1234`) or your set PIN to access the main menu.

2. **Forgot PIN:**  
   Click "Forgot Password?" and follow on-screen instructions (use the code shown in dialog for demo).

3. **Perform Transactions:**  
   Select options to check balance, withdraw or deposit cash, or change your PIN.

4. **Exit:**  
   Click "Exit" to close the application safely.

---

## Notes

- This project is for educational/demo purposes. In a real-world scenario, sensitive information and verification codes would not be displayed openly.
- Only a single user is supported for demo simplicity.
- All logs are stored for session and security tracking.

---

## License

This project is part of the Brain Wave Matrix Solution Task 1 and is distributed for academic use.

---

## Author

- Developed by Sankalp B Chandavarkar for Brain Wave Matrix Solution, Task 1.

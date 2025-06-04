task 1
Project Report: ATM Simulation Using Python and Tkinter
I have developed a fully functional ATM simulation system using Python’s Tkinter library for the graphical user interface and SQLite for secure, persistent data storage. This project is designed to emulate the core functionalities of a real-world ATM, offering a seamless user experience within a desktop environment.

Objective
The goal of this project was to build an interactive and user-friendly ATM interface that allows users to securely access and manage their account operations such as checking balance, withdrawing and depositing cash, changing their PIN, and resetting their PIN if forgotten.

Key Features Implemented
1. User Authentication
Upon launching the application, users are greeted with a login screen where they must enter a 4-digit PIN. This login system ensures that only authorized users can access the account dashboard. I have also implemented a secure verification system that limits incorrect login attempts to three, simulating real ATM behavior.

2. PIN Reset Functionality
Understanding that users may forget their PIN, I incorporated a "Forgot Password" feature. When this option is selected, a 6-digit verification code is generated and shown (simulating a message sent to the user’s registered phone). After verifying the code, users are guided through the process of resetting their PIN securely.

3. Transaction Operations
The main menu provides users with the ability to:

Check Balance: Displays the current account balance in a formatted message box.

Withdraw Cash: Allows users to enter a withdrawal amount, confirms the transaction, and updates the balance.

Deposit Cash: Provides a similar interface for depositing cash with real-time balance updates.
Each transaction is confirmed through a dialog box, ensuring that no operation is performed accidentally.

4. PIN Change Option
Users can easily change their current PIN through the main menu. The process includes current PIN verification and confirmation of the new PIN, providing a secure way to update login credentials.

5. Visual Design and Usability
The interface is built using modern design principles with a consistent color scheme, custom fonts, and interactive buttons that respond visually on hover. Each screen transition—from login to menu to transaction—occurs smoothly, ensuring a professional and intuitive experience.

6. Database Integration
The application connects to an SQLite database (atm_user_data.db) where all user information and transaction logs are stored. I created two tables:

users: To store PIN and balance data.

logs: To keep a timestamped record of all user events and transactions.

I ensured that even if the database file is deleted or missing, the program creates it with default data, making the application highly reliable and self-sufficient.

7. Logging and Audit Trail
Every significant event—login attempts, successful logins, balance checks, transactions, and PIN changes—is recorded in the logs table with accurate timestamps. This feature simulates real-world ATM audit trails and supports future data analysis or debugging.

Conclusion
This project demonstrates a well-rounded understanding of GUI development, secure data handling, and user-centered design. Through this ATM simulation, I have successfully recreated essential banking operations in a digital environment that prioritizes security, clarity, and user convenience. This system can easily be extended further to support multiple users or even connect with web-based APIs for real-world integration.

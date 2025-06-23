# Advanced Inventory Management System

## Overview

This project is a feature-rich, modern Inventory Management System (IMS) built in Python using the PyQt5 framework for the GUI. It is designed for both small businesses and larger organizations to efficiently manage products, inventory, sales, analytics, and users. The application offers a professional user experience, robust data management, and advanced reporting tools.

---

## Key Features

- **User Authentication & Role Management**  
  - Secure login for users (admin and staff roles)  
  - Admin can register new users and assign roles

- **Product Inventory Management**  
  - Add, edit, and delete products  
  - Track product quantities and prices  
  - Low stock alerts with color-coded warnings

- **Sales Processing & Tracking**  
  - Sell products with real-time inventory deduction  
  - Prevent sales exceeding available stock  
  - Log every sale with timestamp and details

- **Live Analytics & Dashboard**  
  - Daily sales revenue charts  
  - Top performing products (by quantity/revenue)  
  - Inventory levels and valuation charts  
  - All charts created with Matplotlib, embedded in the GUI

- **Reporting & Data Export**  
  - Export inventory and sales data to CSV, Excel, or PDF  
  - Professionally formatted PDF reports using ReportLab

- **Activity Logging**  
  - Tracks all key actions (logins, sales, product changes, user management)  
  - Admins can view complete activity history

- **Modern UI & UX**  
  - Responsive, well-styled interface with clear layouts  
  - Pagination for handling large datasets  
  - Search and filter products instantly  
  - Toolbars and dialogs for a professional user experience

---

## Screenshots & Visual Guide

Below, you will find each major function or screen described with a recommended spot to insert a screenshot, along with an explanation of its purpose and how it works.

---

### 1. Login Screen

**Insert Screenshot: Login Screen**  
`![Login Screen](screenshots/login.png)`

- **What it shows:**  
  The login window where users (admin or staff) enter their username and password.
- **How it works:**  
  - Credentials are securely checked against the database.
  - Passwords are hashed with SHA-256.
  - Only valid users can log in; admins can access all features, staff have limited access.

---

### 2. Registration Dialog (Admin Only)

**Insert Screenshot: Registration Dialog**  
`![Registration Dialog](screenshots/register.png)`

- **What it shows:**  
  The dialog for registering new users, available only to admins.
- **How it works:**  
  - Admin enters username, password, confirms the password, and selects a role (admin or staff).
  - The user is created in the SQLite database.
  - Duplicate usernames are prevented.

---

### 3. Main Dashboard

**Insert Screenshot: Main Dashboard After Login**  
`![Main Dashboard](screenshots/dashboard.png)`

- **What it shows:**  
  The primary application window post-login, displaying the top bar, search, product table, and main controls.
- **How it works:**  
  - Shows a list of all products with columns for ID, name, quantity, price, and creation date.
  - Product quantities below thresholds are color-coded (yellow for <10, red for <5).
  - Pagination controls allow browsing large inventories.
  - Admins see extra buttons for managing products and users.  
  - Search bar allows real-time filtering of products.

---

### 4. Add Product Dialog

**Insert Screenshot: Add Product Dialog**  
`![Add Product](screenshots/add_product.png)`

- **What it shows:**  
  Dialog for adding a new product with fields for name, quantity, and price.
- **How it works:**  
  - Only admins can add products.
  - Input validation ensures correct data entry.
  - New products appear instantly in the product table.

---

### 5. Sell Product Dialog

**Insert Screenshot: Sell Product Dialog**  
`![Sell Product](screenshots/sell_product.png)`

- **What it shows:**  
  Dialog for processing a product sale: select product, quantity, see unit and total price, and process sale.
- **How it works:**  
  - Only products in stock are available for sale.
  - Quantity cannot exceed available stock.
  - Selling a product updates the inventory and logs the sale.

---

### 6. Sales History

**Insert Screenshot: Sales History**  
`![Sales History](screenshots/sales_history.png)`

- **What it shows:**  
  View listing all historical sales, including date, product, quantity, and total price.
- **How it works:**  
  - Accessible from the Tools menu.
  - Data is fetched from the Sales table in the database.
  - Admins can see all sales, including totals at the bottom.

---

### 7. Inventory Export

**Insert Screenshot: Export Dialog**  
`![Export Dialog](screenshots/export.png)`

- **What it shows:**  
  Dialog for exporting inventory or sales data to CSV, Excel, or PDF.
- **How it works:**  
  - User selects export format and file location.
  - Data is formatted and saved using pandas or reportlab.
  - Export actions are logged in the Activity Log.

---

### 8. Analytics Dashboard

**Insert Screenshot: Analytics Dashboard**  
`![Analytics Dashboard](screenshots/analytics.png)`

- **What it shows:**  
  Multiple tabs with embedded charts for daily sales, top products, and inventory overview.
- **How it works:**  
  - Uses matplotlib to visualize data within the GUI.
  - Tabs include:
    - Daily Sales Revenue (bar chart)
    - Top Selling Products (quantity and revenue)
    - Inventory Levels and Value

---

### 9. Low Stock Alert

**Insert Screenshot: Low Stock Alert**  
`![Low Stock Alert](screenshots/low_stock.png)`

- **What it shows:**  
  Dialog listing products with quantity below 10, color-coded for urgency.
- **How it works:**  
  - Highlights restocking needs for efficient inventory control.
  - Products with quantity <5 are red, <10 are yellow.

---

### 10. Activity Log

**Insert Screenshot: Activity Log**  
`![Activity Log](screenshots/activity_log.png)`

- **What it shows:**  
  Full log of all important actions: logins, product changes, exports, sales, etc.
- **How it works:**  
  - Accessible from the Tools menu.
  - Displays timestamp, user, action, and details.
  - Useful for auditing and tracking user activity.

---

### 11. About Dialog

**Insert Screenshot: About Dialog**  
`![About Dialog](screenshots/about.png)`

- **What it shows:**  
  Dialog showing program version, author, and a summary of features.
- **How it works:**  
  - Accessed via Help > About in the menu.
  - Static information for end users.

---

## Installation

### 1. Prerequisites

- Python 3.7 or higher
- The following libraries:
  - PyQt5
  - pandas
  - matplotlib
  - reportlab

Install with:

```sh
pip install PyQt5 pandas matplotlib reportlab
```

### 2. Clone the Repository

```sh
git clone https://github.com/sankalpsa/-Brainwave_Matrix_Intern.git
cd -Brainwave_Matrix_Intern/Task\ 2
```

---

## Usage

### 1. Run the Application

```sh
python "Inventory Management System"
```

### 2. Default Admin Login

- **Username:** `admin`
- **Password:** `admin123`

> The default admin user is automatically created on first run if the database does not exist.

---

## Application Structure

- `Inventory Management System` (main script): Contains all code (GUI, database logic, reporting, etc.)
- `inventory.db` (auto-generated): SQLite3 database for persistent storage.

---

## Troubleshooting

- If you encounter missing packages, check dependencies and reinstall with pip.
- For GUI display issues, ensure all PyQt5 dependencies are properly installed.
- Database errors may occur if the app is run without write permissions in the directory.

---

## License

This project is provided for educational and demonstration purposes.

---

## Credits

Developed as part of the Brainwave Matrix Internship by [sankalpsa](https://github.com/sankalpsa).

---

## Contact

For questions, suggestions, or contributions, please open an issue or contact via GitHub.


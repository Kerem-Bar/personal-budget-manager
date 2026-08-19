# 💰 Personal Budget Manager

A comprehensive, object-oriented Python system for personal financial management. The application allows users to manage incomes and expenses, persist data using CSV files, perform financial reporting with Pandas, visualize data using Matplotlib, and stay within monthly budget limits.

![](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![](https://img.shields.io/badge/Architecture-OOP_%26_Inheritance-2563EB?style=flat)
![](https://img.shields.io/badge/Tests-21_Passed_%7C_Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![](https://img.shields.io/badge/Pandas-Financial_Analytics-150458?style=flat&logo=pandas&logoColor=white)
![](https://img.shields.io/badge/Matplotlib-Data_Visualization-11557c?style=flat)
![](https://img.shields.io/badge/Project-Completed-44cc11?style=flat)

---

## 📁 Project Structure

```text
budget_project/
│── main.py              # Application entry point and CLI interactive menus
│── models.py            # OOP Hierarchy: Transaction (Base), Income, Expense
│── budget_manager.py    # Transaction operations, CSV persistence, Budget tracking
│── reports.py           # Pandas analytics, financial reports, and Matplotlib charts
│── test_budget.py       # Automated unit tests written with pytest
│── create_data.py       # Helper script to generate initial CSV sample dataset
│── transactions.csv     # Data persistence storage
└── README.md            # System documentation

```

---

## 🛠️ Class Architecture & Responsibilities

1. **`Transaction` (`models.py`)**: Base class representing a financial transaction with attributes (`id`, `date`, `type`, `category`, `description`, `amount`) and input validation.
2. **`Income` (`models.py`)**: Child class inheriting from `Transaction`, adding unique attribute `source`.
3. **`Expense` (`models.py`)**: Child class inheriting from `Transaction`, adding unique attributes `merchant` and `paymentMethod`.
4. **`BudgetManager` (`budget_manager.py`)**: Handles in-memory list operations (add, edit, delete, search), sets budget limits, and manages CSV loading and saving.
5. **`ReportGenerator` (`reports.py`)**: Reads CSV data into Pandas DataFrames to perform financial aggregations, date filtering, CSV report exports, and Matplotlib chart generation.

---

## 📊 Analytical Reports (Pandas) & Charts (Matplotlib)

* **Financial Overview**: Total Income, Total Expense, and Net Balance calculation.
* **Category Aggregations**: Expenses grouped by Category & Income grouped by Category.
* **Monthly Summary**: Grouped total amounts by `YYYY-MM` and transaction type.
* **Transaction Analytics**: Max transaction amount and average expense calculations.
* **Date Filtering**: Filter transactions within a specified date range (`YYYY-MM-DD`).
* **CSV Export**: Export generated report DataFrames to customized CSV files.
* **Visualizations**: Bar charts for Expenses and Incomes per Category (saved automatically as `.png`).

---

## 🏆 Implemented Bonus Features

* 🎨 **Matplotlib Bar Charts**: Visualizing expense/income distributions per category.
* 🎯 **Monthly Budget Limit & Alerts**: Setting spending limits with real-time overspending alerts.
* ✏️ **Edit Existing Transactions**: Updating transaction details by ID with automated persistence.
* 🗓️ **Date Range Filtering**: Filtering transactions between custom start and end dates.
* 💾 **Export Reports to CSV**: Exporting dynamic Pandas reports to external CSV files.
* 📝 **Consistent Type Hints**: Applied across all modules for code safety.
* 🧪 **Automated Pytest Suite**: 21 unit tests covering edge cases and input validation.

## 🚀 How to Run the Project

1. Clone the repository and enter the directory:
```bash
git clone https://github.com/Kerem-Bar/personal-budget-manager.git
cd personal-budget-manager
```

2. Install dependencies:
```bash
pip install pandas matplotlib pytest
```

3. Run the main application:
```bash
python main.py
```

4. Run automated unit tests:
```bash
pytest -v
```
```


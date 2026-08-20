# 💳 Personal Budget Manager

A comprehensive, object-oriented Python system for personal financial management. The application allows users to manage incomes and expenses, persist data using CSV files, perform financial reporting with Pandas, visualize data using Matplotlib, and monitor monthly budget limits.

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
│── main.py                                                 # Application entry point and CLI interactive menus
│── models.py                                               # OOP Hierarchy: Transaction (Base), Income, Expense
│── budget_manager.py                                       # Transaction operations, CSV persistence, Budget tracking
│── reports.py                                              # Pandas analytics, financial reports, and Matplotlib charts
│── test_budget.py                                          # Automated unit tests written with pytest
│── create_data.py                                          # Helper script to generate initial CSV sample dataset
│── transactions.csv                                        # Data persistence storage
│── Personal Budget Manager - Execution Documentation.pdf   # Complete execution walkthrough & output screenshots
└── README.md                                               # System documentation
```

---

## 🛠️ Class Architecture & Responsibilities

1. **`Transaction` (`models.py`)**: Base class representing a financial transaction with core attributes (`id`, `date`, `type`, `category`, `description`, `amount`) and input validation.
2. **`Income` (`models.py`)**: Child class inheriting from `Transaction`, adding the unique attribute `source`.
3. **`Expense` (`models.py`)**: Child class inheriting from `Transaction`, adding unique attributes `merchant` and `paymentMethod`.
4. **`BudgetManager` (`budget_manager.py`)**: Handles in-memory list operations (add, edit, delete, search), sets budget limits, and manages CSV loading and saving.
5. **`ReportGenerator` (`reports.py`)**: Reads CSV data into Pandas DataFrames to perform financial aggregations, date filtering, CSV report exports, and Matplotlib chart generation.

---

## ⚙️ Key Features & System Capabilities

* **OOP Architecture & Data Persistence:** Hierarchical class structure with inheritance and automatic bidirectional synchronization with `transactions.csv`.
* **Full Transaction Lifecycle (CRUD):** Add, view, edit by ID, and delete transactions with dynamic auto-incrementing ID generation.
* **Budget Tracking & Overdraft Alerts:** Configurable monthly spending thresholds with real-time budget status checks and overdraft alerts.
* **Financial Analytics & Aggregations (Pandas):** Calculation of net balance, categorical expense/income breakdowns, monthly summaries (`YYYY-MM`), and custom date range filtering.
* **Custom CSV Report Export:** Export dynamically generated Pandas analytical reports directly to customized CSV files.
* **Data Visualizations (Matplotlib):** Automated generation and high-resolution export of category-level expense and income distribution charts.
* **Code Quality & Automated Testing:** Strict type hinting across all modules and an automated 21-test Pytest suite validating input integrity and edge cases.

---

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

---

## 👤 Author

**Kerem Bar**  
*Master's Student in Information Sciences (Information Technology Specialization)*

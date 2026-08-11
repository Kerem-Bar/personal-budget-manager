# Import pytest framework for writing and running automated unit tests
import pytest

# Import os standard module for file and operating system operations (used for cleaning up test files)
import os

# Import base Transaction and inherited classes (Income, Expense) from models.py
from models import Transaction, Income, Expense

# Import budget management system class from budget_manager.py
from budget_manager import BudgetManager

# Import financial reporting and analysis class from reports.py
from reports import ReportGenerator


# Test 1: Verify that creating a transaction with a negative amount raises a ValueError
def test_invalid_amount_raises_error():
    
    # Instruct pytest to expect a ValueError when running the code block below
    with pytest.raises(ValueError):
        
        # Attempt to create an Expense object with a negative transAmount (-50.0)
        Expense(
            transID=1,
            transDate="2026-06-01",
            transCategory="Food",
            transDescription="Lunch",
            transAmount=-50.0,  # Negative amount (triggers ValueError in models.py)
            merchant="Restaurant",
            paymentMethod="Credit Card"
        )
              
        
# Test 2: Verify that creating a transaction with an invalid date format raises a ValueError
def test_invalid_date_raises_error():
    
    # Use pytest.raises context manager to verify that models.py catches invalid input and throws a ValueError
    with pytest.raises(ValueError):
        
        # Attempt to create an Expense instance with an invalid date string ("1 /6/2026" instead of YYYY-MM-DD)
        Expense(
            transID=2,
            transDate="1 /6/2026",  # Invalid date format (triggers date validation in models.py)
            transCategory="Food",
            transDescription="Lunch",
            transAmount=50.0,
            merchant="Restaurant",
            paymentMethod="Credit Card"
        )
        
        
# Test 3: Verify that creating a transaction with an empty category raises a ValueError
def test_empty_category_raises_error():
    
    # Expect a ValueError when transCategory is an empty string or whitespace
    with pytest.raises(ValueError):
        
        Expense(
            transID=3,
            transDate="2026-06-01",
            transCategory="",  # Empty category (triggers validation in models.py)
            transDescription="Lunch",
            transAmount=50.0,
            merchant="Restaurant",
            paymentMethod="Credit Card"
        )


# Test 4: Verify that creating a transaction with an empty description raises a ValueError
def test_empty_description_raises_error():
    
    # Expect a ValueError when transDescription is an empty string
    with pytest.raises(ValueError):
        
        Expense(
            transID=4,
            transDate="2026-06-01",
            transCategory="Food",
            transDescription="",  # Empty description (triggers validation in models.py)
            transAmount=50.0,
            merchant="Restaurant",
            paymentMethod="Credit Card"
        )
        
        
# Test 5: Verify that creating an Income with an empty source raises a ValueError
def test_empty_source_raises_error():
    
    # Expect a ValueError when source is an empty string
    with pytest.raises(ValueError):
        
        Income(
            transID=5,
            transDate="2026-06-01",
            transCategory="Salary",
            transDescription="Bonus",
            transAmount=1000.0,
            source=""  # Empty source (triggers validation in models.py)
        )


# Test 6: Verify that creating an Expense with an empty merchant raises a ValueError
def test_empty_merchant_raises_error():
    
    # Expect a ValueError when merchant is an empty string
    with pytest.raises(ValueError):
        
        Expense(
            transID=6,
            transDate="2026-06-01",
            transCategory="Food",
            transDescription="Dinner",
            transAmount=120.0,
            merchant="",  # Empty merchant (triggers validation in models.py)
            paymentMethod="Credit Card"
        )


# Test 7: Verify that creating an Expense with an empty payment method raises a ValueError
def test_empty_payment_method_raises_error():
    
    # Expect a ValueError when paymentMethod is an empty string
    with pytest.raises(ValueError):
        
        Expense(
            transID=7,
            transDate="2026-06-01",
            transCategory="Food",
            transDescription="Dinner",
            transAmount=120.0,
            merchant="Restaurant",
            paymentMethod=""  # Empty payment method (triggers validation in models.py)
        )
        

# Test 8: Verify set_budget updates budget correctly and raises ValueError for invalid amounts
def test_set_budget():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Scenario 1: Valid budget update
    bm.set_budget(1000)
    
    # Explicit Assertion: Verify monthly_budget attribute was updated correctly
    assert bm.monthly_budget == 1000

    # Scenario 2: Invalid negative budget raises ValueError
    with pytest.raises(ValueError):
        bm.set_budget(-500.0)
        
        
# Test 9: Verify get_next_id returns 1 for empty lists and auto-increments for existing transactions
def test_get_next_id():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Scenario 1: Empty list should return ID = 1
    
    # Explicit Assertion: Verify get_next_id returns 1 for empty transactions list
    assert bm.get_next_id() == 1

    # Scenario 2: List with existing transactions should return max_id + 1
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    bm.add_transaction(test_expense)

    # Explicit Assertion: Verify get_next_id auto-increments to max_id + 1
    assert bm.get_next_id() == 2
   
        
# Test 10: Verify that adding a new transaction successfully appends it to the manager's list      
def test_add_transaction():
    
    # Create a BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")
    
    # Create a dummy Expense object with test data
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    
    # Add the transaction to the budget manager
    bm.add_transaction(test_expense)
    
    # Assert that the transactions list length increased to 1
    assert len(bm.transactions) == 1
   
    
# Test 11: Verify search_category handles non-existent categories and correctly cleans whitespace and casing for matches
def test_search_category():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Create a dummy Expense transaction with transCategory = "Food"
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    bm.add_transaction(test_expense)

    # Scenario 1: Search for a category that does NOT exist
    result_empty = bm.search_category("rent")
    # Assert that an empty list is returned
    assert result_empty == []

    # Scenario 2: Search for an existing category with leading/trailing spaces and lowercase ("  food  ")
    result_found = bm.search_category("  food  ")
    
    # Assert that exactly 1 transaction was found after input cleaning (.strip().title())
    assert len(result_found) == 1
    # Assert that the returned transaction category matches "Food"
    assert result_found[0].transCategory == "Food"
    
    
# Test 12: Verify search_date handles valid dates, invalid date formats, and non-existent dates correctly
def test_search_date():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Create a dummy Expense transaction with transDate = "2026-06-01"
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    bm.add_transaction(test_expense)

    # Scenario 1: Search for a valid date that exists in the transactions list
    result_found = bm.search_date("2026-06-01")
    # Assert that 1 transaction was returned and its date is correct
    assert len(result_found) == 1
    assert result_found[0].transDate == "2026-06-01"

    # Scenario 2: Search with an invalid date format (triggers try...except in budget_manager.py)
    result_invalid_format = bm.search_date("01/06/2026")
    # Assert that an empty list is returned when format validation fails
    assert result_invalid_format == []

    # Scenario 3: Search with a valid YYYY-MM-DD format, but the date does NOT exist in transactions
    result_not_found = bm.search_date("2026-12-31")
    # Assert that an empty list is returned when no matching transactions are found
    assert result_not_found == []
  
    
# Test 13: Verify delete_transaction removes existing transactions and raises ValueError for non-existent IDs
def test_delete_transaction():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Create a dummy Expense transaction with ID = 1
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    bm.add_transaction(test_expense)

    # Scenario 1: Attempt to delete a non-existent ID (ID = 99) should raise ValueError
    with pytest.raises(ValueError):
        bm.delete_transaction(99)
    
    # Explicit Assertion: Verify list length remains 1 when deletion of non-existent ID fails
    assert len(bm.transactions) == 1

    # Scenario 2: Delete an existing ID (ID = 1)
    bm.delete_transaction(1)
    
    # Explicit Assertion: Verify transaction was removed and list length becomes 0
    assert len(bm.transactions) == 0
    
# Test 14: Verify update_transaction updates existing transactions and handles non-existent IDs gracefully
def test_update_transaction():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")
    
    # Create an initial dummy Expense transaction with ID = 1
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    # Add the initial transaction to the budget manager's list
    bm.add_transaction(test_expense)
    
    # Scenario 1: Update an existing transaction (ID = 1) with new details
    bm.update_transaction(Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="hotel",
        paymentMethod="Voucher"
    ))
    
    # Explicit Assertion: Verify merchant was updated and formatted with title case ("Hotel")
    assert bm.transactions[0].merchant == "Hotel"
    
    # Explicit Assertion: Verify paymentMethod was updated correctly to "Voucher"
    assert bm.transactions[0].paymentMethod == "Voucher"
    
    # Scenario 2: Attempt to update a non-existent transaction ID (ID = 2) should raise ValueError
    with pytest.raises(ValueError):
        bm.update_transaction(Expense(
            transID=2,
            transDate="2026-06-01",
            transCategory="Food",
            transDescription="Lunch",
            transAmount=50.0,
            merchant="Cafe",
            paymentMethod="Cash"
        ))
    
    # Assert that the list length remains 1 (no new transaction was created by mistake)
    assert len(bm.transactions) == 1
    # Assert that the original transaction (ID = 1) was not modified by the failed update
    assert bm.transactions[0].paymentMethod == "Voucher"
    
# Test 15: Verify filter_by_date_range filters transactions correctly by date range and handles invalid inputs
def test_filter_by_date_range():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Create 4 dummy Expense transactions with different dates across June 2026
    expense_1 = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Coffee",
        transAmount=15.0,
        merchant="Cafe",
        paymentMethod="Credit Card"
    )
    expense_2 = Expense(
        transID=2,
        transDate="2026-06-10",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    expense_3 = Expense(
        transID=3,
        transDate="2026-06-20",
        transCategory="Transport",
        transDescription="Bus",
        transAmount=10.0,
        merchant="Egged",
        paymentMethod="Cash"
    )
    expense_4 = Expense(
        transID=4,
        transDate="2026-06-30",
        transCategory="Shopping",
        transDescription="Groceries",
        transAmount=150.0,
        merchant="Supermarket",
        paymentMethod="Credit Card"
    )

    # Add all 4 transactions to the budget manager instance
    bm.add_transaction(expense_1)
    bm.add_transaction(expense_2)
    bm.add_transaction(expense_3)
    bm.add_transaction(expense_4)
    
    # Scenario 1: Filter within a valid range (June 1st to June 20th)
    filter_1 = bm.filter_by_date_range("2026-06-01", "2026-06-20")
    # Assert exactly 3 transactions are returned (expense_4 on June 30th is correctly excluded)
    assert len(filter_1) == 3
    
    # Scenario 2: Filter with valid date range where no transactions exist (July 2026)
    filter_2 = bm.filter_by_date_range("2026-07-01", "2026-07-31")
    # Assert an empty list is returned when no transactions fall in the range
    assert len(filter_2) == 0

    # Scenario 3: Filter with reversed date logic (start_date is after end_date)
    filter_3 = bm.filter_by_date_range("2026-06-20", "2026-06-01")
    # Assert an empty list is returned when date order is invalid
    assert len(filter_3) == 0
    
    # Scenario 4: Filter with invalid date string format in start_date
    filter_4 = bm.filter_by_date_range("2026/06-01", "2026/06/20")
    # Assert an empty list is returned when start_date parsing fails
    assert len(filter_4) == 0
    
    # Scenario 5: Filter with invalid date string format in end_date
    filter_5 = bm.filter_by_date_range("2026/06/01", "2026/06-20")
    # Assert an empty list is returned when end_date parsing fails
    assert len(filter_5) == 0
    

# Test 16: Verify ReportGenerator calculates total income, total expense, and current balance with multiple transactions
def test_report_totals_and_balance():
    
    # Create BudgetManager instance with a dummy filename
    bm = BudgetManager(filename="test_dummy.csv")

    # Create two dummy Income transactions (Total Income = 1500.0)
    income_trans_1 = Income(
        transID=1,
        transDate="2026-06-01",
        transCategory="Salary",
        transDescription="June Salary",
        transAmount=1000.0,
        source="Company"
    )
    income_trans_2 = Income(
        transID=2,
        transDate="2026-06-05",
        transCategory="Freelance",
        transDescription="Web Project",
        transAmount=500.0,
        source="Client"
    )

    # Create two dummy Expense transactions (Total Expense = 700.0)
    expense_trans_1 = Expense(
        transID=3,
        transDate="2026-06-02",
        transCategory="Food",
        transDescription="Groceries",
        transAmount=300.0,
        merchant="Supermarket",
        paymentMethod="Credit Card"
    )
    expense_trans_2 = Expense(
        transID=4,
        transDate="2026-06-10",
        transCategory="Transport",
        transDescription="Fuel",
        transAmount=400.0,
        merchant="Gas Station",
        paymentMethod="Credit Card"
    )

    # Add all 4 transactions to BudgetManager (this automatically updates test_dummy.csv)
    bm.add_transaction(income_trans_1)
    bm.add_transaction(income_trans_2)
    bm.add_transaction(expense_trans_1)
    bm.add_transaction(expense_trans_2)

    # Create ReportGenerator instance reading from the updated dummy CSV file
    rg = ReportGenerator(filename="test_dummy.csv")

    # Assert total_income correctly sums all income transactions (1000 + 500 = 1500.0)
    assert rg.total_income() == 1500.0

    # Assert total_expense correctly sums all expense transactions (300 + 400 = 700.0)
    assert rg.total_expense() == 700.0

    # Assert current_balance returns the exact net balance (1500 - 700 = 800.0)
    assert rg.current_balance() == 800.0
    
    
    
# Test 17: Verify ReportGenerator handles both empty and populated data correctly
def test_report_average_expense_and_max_transaction():
    
    # Explicit filename for isolation
    filename = "test_dummy_2.csv"
    
    # Clean up residual test file if it exists from a previous run.
    # Required because I test both an empty state and a populated state within the same test function.
    if os.path.exists(filename):
        os.remove(filename)

    # senario 1: Test empty state (File does not exist yet)
    
    # Create ReportGenerator instance reading from the updated dummy CSV file
    rg_empty = ReportGenerator(filename=filename)
    
    # Method returns a float -> Valid comparison
    assert rg_empty.average_expense() == 0.0
    
    # .empty returns a single boolean (True/False) -> Valid comparison
    assert rg_empty.max_transaction().empty == True


    # senario 2: Populate data with BudgetManager
    bm = BudgetManager(filename=filename)

    # Create dummy Income transactions
    income_trans_1 = Income(
        transID=1,
        transDate="2026-06-01",
        transCategory="Salary",
        transDescription="June Salary",
        transAmount=1000.0,
        source="Company"
    )
    income_trans_2 = Income(
        transID=2,
        transDate="2026-06-05",
        transCategory="Freelance",
        transDescription="Web Project",
        transAmount=500.0,
        source="Client"
    )

    # Create dummy Expense transactions
    expense_trans_1 = Expense(
        transID=3,
        transDate="2026-06-02",
        transCategory="Food",
        transDescription="Groceries",
        transAmount=300.0,
        merchant="Supermarket",
        paymentMethod="Credit Card"
    )
    expense_trans_2 = Expense(
        transID=4,
        transDate="2026-06-10",
        transCategory="Transport",
        transDescription="Fuel",
        transAmount=400.0,
        merchant="Gas Station",
        paymentMethod="Credit Card"
    )

    # Add transactions to populate test_dummy_2.csv
    bm.add_transaction(income_trans_1)
    bm.add_transaction(income_trans_2)
    bm.add_transaction(expense_trans_1)
    bm.add_transaction(expense_trans_2)


    # Test populated state
    rg_populated = ReportGenerator(filename=filename)
    
    max_trans = rg_populated.max_transaction()
    average_expense = rg_populated.average_expense()
    
    # Extract single value with .iloc[0] -> Valid comparison
    assert max_trans['amount'].iloc[0] == 1000.0
    
    # Float comparison -> Valid comparison
    assert average_expense == 350.0
    
    
# Test 18: Verify ReportGenerator correctly groups expenses, incomes, and monthly summary
def test_report_groupings():
    
    # Explicit filename for test isolation
    filename = "test_dummy_3.csv"

    # Clean up residual test file if it exists from a previous run
    if os.path.exists(filename):
        os.remove(filename)

    # Scenario 1: Test empty state
    # Create ReportGenerator instance reading from the updated dummy CSV file
    rg_empty = ReportGenerator(filename=filename)
    
    # Assert grouping methods on empty dataset return empty DataFrames
    assert rg_empty.expenses_by_category().empty == True
    
    # Explicit Assertion: Verify income_by_category returns empty DataFrame on empty dataset
    assert rg_empty.income_by_category().empty == True
        
    # Explicit Assertion: Verify monthly_summary returns empty DataFrame on empty dataset
    assert rg_empty.monthly_summary().empty == True


    # Scenario 2: Populate data with BudgetManager 
    bm = BudgetManager(filename=filename)

    # Create dummy Expense transactions (2 Food expenses = 200.0, 1 Transport expense = 100.0)
    expense_food_1 = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Coffee",
        transAmount=50.0,
        merchant="Cafe",
        paymentMethod="Cash"
    )
    expense_food_2 = Expense(
        transID=2,
        transDate="2026-06-05",
        transCategory="Food",
        transDescription="Dinner",
        transAmount=150.0,
        merchant="Restaurant",
        paymentMethod="Credit Card"
    )
    expense_transport = Expense(
        transID=3,
        transDate="2026-06-10",
        transCategory="Transport",
        transDescription="Bus Pass",
        transAmount=100.0,
        merchant="Egged",
        paymentMethod="Credit Card"
    )

    # Create dummy Income transactions (2 Salary incomes = 4000.0 total)
    income_salary_1 = Income(
        transID=4,
        transDate="2026-06-01",
        transCategory="Salary",
        transDescription="June Salary",
        transAmount=3000.0,
        source="Company"
    )
    income_salary_2 = Income(
        transID=5,
        transDate="2026-06-15",
        transCategory="Salary",
        transDescription="Bonus",
        transAmount=1000.0,
        source="Company"
    )

    # Add all transactions to BudgetManager
    bm.add_transaction(expense_food_1)
    bm.add_transaction(expense_food_2)
    bm.add_transaction(expense_transport)
    bm.add_transaction(income_salary_1)
    bm.add_transaction(income_salary_2)


    # Test populated state
    rg_populated = ReportGenerator(filename=filename)

    # Verify expenses_by_category sums Food correctly (50.0 + 150.0 = 200.0)
    expenses_cat_df = rg_populated.expenses_by_category()
    food_row = expenses_cat_df[expenses_cat_df["category"] == "Food"]
    assert food_row["amount"].iloc[0] == 200.0

    # Verify income_by_category sums Salary correctly (3000.0 + 1000.0 = 4000.0)
    income_cat_df = rg_populated.income_by_category()
    salary_row = income_cat_df[income_cat_df["category"] == "Salary"]
    assert salary_row["amount"].iloc[0] == 4000.0

    # Verify monthly_summary (Returns 2 rows: 1 for total expenses, 1 for total income in June 2026)
    monthly_df = rg_populated.monthly_summary()
    assert len(monthly_df) == 2
    
# Test 19: Verify ReportGenerator filters transactions by date range and handles invalid inputs
def test_report_filter_by_date_range():
    
    # Explicit filename for test isolation
    filename = "test_dummy_4.csv"

    # Clean up residual test file if it exists from a previous run
    if os.path.exists(filename):
        os.remove(filename)
        
        
    # Scenario 1: Test empty state
    rg_empty = ReportGenerator(filename=filename)
        
    filter_1 = rg_empty.filter_by_date_range("2026-06-01", "2026-06-20")
    
    # Explicit Assertion: Verify empty dataset filter returns 0 rows
    assert len(filter_1) == 0
    
    # Explicit Assertion: Verify returned DataFrame is empty
    assert filter_1.empty == True
    
    
    # Populate test data using BudgetManager
    bm = BudgetManager(filename=filename)
    
    # Create 4 dummy Expense transactions across June 2026
    expense_1 = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Coffee",
        transAmount=15.0,
        merchant="Cafe",
        paymentMethod="Cash"
    )
    expense_2 = Expense(
        transID=2,
        transDate="2026-06-10",
        transCategory="Food",
        transDescription="Groceries",
        transAmount=200.0,
        merchant="Supermarket",
        paymentMethod="Credit Card"
    )
    expense_3 = Expense(
        transID=3,
        transDate="2026-06-20",
        transCategory="Transport",
        transDescription="Bus Pass",
        transAmount=50.0,
        merchant="Egged",
        paymentMethod="Cash"
    )
    expense_4 = Expense(
        transID=4,
        transDate="2026-06-30",
        transCategory="Shopping",
        transDescription="Clothes",
        transAmount=150.0,
        merchant="Gas Station",
        paymentMethod="Credit Card"
    )

    # Add all 4 transactions to BudgetManager to populate test_dummy_4.csv
    bm.add_transaction(expense_1)
    bm.add_transaction(expense_2)
    bm.add_transaction(expense_3)
    bm.add_transaction(expense_4)


    # Scenario 2: Test populated state
    rg_populated = ReportGenerator(filename=filename)
    
    # Filter 2: Valid date range (June 1st to June 20th -> Should include 3 transactions: expense_1, expense_2, expense_3)
    filter_2 = rg_populated.filter_by_date_range("2026-06-01", "2026-06-20")
    
    # Explicit Assertion: Verify valid date range returns exactly 3 matching transactions
    assert len(filter_2) == 3
    
    # Filter 3: Invalid date order (start_date after end_date -> Should return empty DataFrame)
    filter_3 = rg_populated.filter_by_date_range("2026-06-20", "2026-06-01")
    
    
    # Explicit Assertion: Verify returned DataFrame row count is 0 for invalid date order
    assert len(filter_3) == 0
    
    # Explicit Assertion: Verify returned DataFrame is empty
    assert filter_3.empty == True

    # Filter 4: Invalid start date format (end date is valid -> Should return empty DataFrame)
    filter_4 = rg_populated.filter_by_date_range("01/06/2026", "2026-06-20")
    
    # Explicit Assertion: Verify returned DataFrame row count is 0 when start date format is invalid
    assert len(filter_4) == 0
    
    # Explicit Assertion: Verify returned DataFrame is empty
    assert filter_4.empty == True

    # Filter 5: Invalid end date format (start date is valid -> Should return empty DataFrame)
    filter_5 = rg_populated.filter_by_date_range("2026-06-01", "20/06/2026")
    
    # Explicit Assertion: Verify returned DataFrame row count is 0 when end date format is invalid
    assert len(filter_5) == 0
    
    # Explicit Assertion: Verify returned DataFrame is empty
    assert filter_5.empty == True
    
    
# Test 20: Verify BudgetManager load_from_csv correctly populates transactions list from existing CSV
def test_budget_manager_load_from_csv():

    # Step 1: Pre-test cleanup
    # Delete residual CSV file ("test_dummy_load.csv") if it exists from a previous run
    if os.path.exists("test_dummy_load.csv"):
        os.remove("test_dummy_load.csv")

    # Step 2: Setup - Create a CSV file on disk with 1 expense using BudgetManager
    # "test_dummy_load.csv" is the CSV file generated by BudgetManager to store raw transactions
    bm_setup = BudgetManager(filename="test_dummy_load.csv")
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card",
    )
    
    # Calling add_transaction creates "test_dummy_load.csv" on disk and writes this 1 expense into it
    bm_setup.add_transaction(test_expense)

    # Step 3: Simulate a fresh application run (fresh RAM state)
    # Create a brand new BudgetManager instance pointing to the existing CSV file ("test_dummy_load.csv").
    # At this moment, bm_loader.transactions is an empty list [] in RAM.
    bm_loader = BudgetManager(filename="test_dummy_load.csv")

    # Run load_from_csv method to read rows from CSV and convert them into Expense objects in RAM
    bm_loader.load_from_csv()

    # Step 4: Explicit Assertions (Verification)
    # Verify that exactly 1 transaction was loaded from the CSV file into RAM
    assert len(bm_loader.transactions) == 1

    # Verify that the loaded transaction ID matches our original data
    assert bm_loader.transactions[0].transID == 1

    # Step 5: Post-test cleanup (Teardown)
    # Delete the test CSV file from disk after test completion
    if os.path.exists("test_dummy_load.csv"):
        os.remove("test_dummy_load.csv")


# Test 21: Verify ReportGenerator exports DataFrame correctly to a new CSV file
def test_report_export_to_csv():

    # Step 1: Pre-test cleanup
    # Clean up any leftover CSV files from previous test runs:
    # - "test_dummy_5.csv": Source CSV file containing raw transactions created by BudgetManager
    # - "exported_report.csv": Target CSV file generated by ReportGenerator export method
    if os.path.exists("test_dummy_5.csv"):
        os.remove("test_dummy_5.csv")
    if os.path.exists("exported_report.csv"):
        os.remove("exported_report.csv")

    # Step 2: Populate source CSV file with raw transaction data using BudgetManager
    # Creates "test_dummy_5.csv" on disk with 1 expense
    bm = BudgetManager(filename="test_dummy_5.csv")
    test_expense = Expense(
        transID=1,
        transDate="2026-06-01",
        transCategory="Food",
        transDescription="Lunch",
        transAmount=50.0,
        merchant="Restaurant",
        paymentMethod="Credit Card",
    )
    
    # Calling add_transaction creates "test_dummy_5.csv" on disk with 1 raw expense
    bm.add_transaction(test_expense)

    # Step 3: Instantiate ReportGenerator and generate a summary DataFrame
    # ReportGenerator reads "test_dummy_5.csv" into Pandas DataFrame.
    # expenses_by_category() processes it into summary_df (DataFrame grouped by category).
    rg = ReportGenerator(filename="test_dummy_5.csv")
    summary_df = rg.expenses_by_category()

    # Step 4: Export the summary DataFrame to a new CSV file
    # "exported_report" is the target name passed to export_to_csv (method creates "exported_report.csv")
    rg.export_to_csv(summary_df, "exported_report")

    # Step 5: Explicit Assertion (Verification)
    # Verify that the exported CSV file ("exported_report.csv") physically exists on disk
    assert os.path.exists("exported_report.csv") == True

    # Step 6: Post-test cleanup (Teardown)
    # Delete both temporary CSV files from disk after test completion
    if os.path.exists("test_dummy_5.csv"):
        os.remove("test_dummy_5.csv")
    if os.path.exists("exported_report.csv"):
        os.remove("exported_report.csv")
      
# Run pytest automatically when pressing the Run button in Spyder
if __name__ == '__main__':
    pytest.main(['-v'])
        
        

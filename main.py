1# Import os standard module for operating system operations (checking file paths, file existence, etc.)
import os

# Import sys standard module for system-specific functions (used for clean application exit via sys.exit)
import sys

# Import datetime library capabilities for date parsing and validation
from datetime import datetime

# Import base class and inherited financial models from models.py
from models import Transaction, Income, Expense

# Import the core budget manager system from budget_manager.py
from budget_manager import BudgetManager

# Import financial reporting and Pandas analytics from reports.py
from reports import ReportGenerator


# Function to display the Main Menu options to the user
def display_main_menu() -> None:
    print("==================================================")
    print("💰  PERSONAL BUDGET MANAGER - MAIN MENU  📊")
    print("==================================================")
    print("  [1] 📝 Transaction Management")
    print("  [2] 🎯 Monthly Budget & Alerts")
    print("  [3] 📈 Financial Reports & Analysis")
    print("  [4] 🎨 Data Visualization & Charts")
    print("  [5] 💾 Save & Exit")
    print("==================================================")


# Function to display the Transaction Management sub-menu options
def display_transaction_menu() -> None:
    print("--------------------------------------------------")
    print("📝 TRANSACTION MANAGEMENT")
    print("--------------------------------------------------")
    print("  [1] 📄 View All Transactions")
    print("  [2] ➕ Add New Transaction")
    print("  [3] ✏️ Edit Existing Transaction by ID")
    print("  [4] ❌ Delete Transaction by ID")
    print("  [5] 🔍 Search & Filter Transactions")
    print("  [6] 🔙 Back to Main Menu")
    print("--------------------------------------------------")


# Function to display the Monthly Budget & Alerts sub-menu options
def display_budget_menu() -> None:
    print("--------------------------------------------------")
    print("🎯 MONTHLY BUDGET & ALERTS")
    print("--------------------------------------------------")
    print("  [1] ⚙️ Set / Update Monthly Budget")
    print("  [2] 🔔 Check Budget Status & Spending Limit")
    print("  [3] 🔙 Back to Main Menu")
    print("--------------------------------------------------")


# Function to display the Financial Reports & Analysis sub-menu options
def display_reports_menu() -> None:
    print("--------------------------------------------------")
    print("📈 FINANCIAL REPORTS & ANALYSIS")
    print("--------------------------------------------------")
    print("  [1] 💵 Financial Overview (Total Income, Expenses & Balance)")
    print("  [2] 🏷️ Expenses by Category")
    print("  [3] 💼 Income by Category")
    print("  [4] 📅 Monthly Summary")
    print("  [5] 🏆 Highest Transaction (Max Amount)")
    print("  [6] 📐 Average Expense")
    print("  [7] 🗓️ Filter Transactions by Date Range")
    print("  [8] 💾 Export Selected Report to CSV")
    print("  [9] 🔙 Back to Main Menu")
    print("--------------------------------------------------")


# Function to display the Data Visualization & Charts sub-menu options
def display_visualization_menu() -> None:
    print("--------------------------------------------------")
    print("🎨 DATA VISUALIZATION & CHARTS")
    print("--------------------------------------------------")
    print("  [1] 📊 View & Save Expense by Category Chart")
    print("  [2] 📈 View & Save Income by Category Chart")
    print("  [3] 🔙 Back to Main Menu")
    print("--------------------------------------------------")
    
    
# Helper function to safely read a positive integer (used for IDs)
def get_valid_int(prompt: str) -> int:
    
    # Infinite loop to keep asking until a valid positive integer is provided
    while True:
        try:
            # 1. Read input string and attempt to convert it to an integer
            user_number_int = int(input(prompt))
            
            # 2. Logical check: ensure ID is a positive number (greater than 0)
            if user_number_int <= 0:
                print("Error: ID must be a positive whole number.")
                continue  # Skip to next iteration
                
            # 3. Success condition: return valid integer (exits loop and function)
            return user_number_int
            
        except ValueError:
            # 4. Caught if user entered text or decimals (e.g., "abc" or "1.5")
            print("Error: Please enter a valid whole number (integer).")
    

# Helper function to safely read a positive float number from the user
def get_valid_float(prompt: str) -> float:
    
    # Infinite loop to keep asking until valid input is received
    while True:
        try:
            # 1. Read input string and attempt to convert it to float
            user_number_float = float(input(prompt))
            
            # 2. Check logical validation: ensure the number is strictly positive
            if user_number_float <= 0:
                print("Error: Amount must be positive.")
                continue  # Skip to the next iteration of the loop
                
            # 3. Success condition: return valid number (exits loop and function)
            return user_number_float
            
        except ValueError:
            # 4. Caught if user typed letters or symbols that couldn't convert to float
            print("Error: Please enter a valid number.")
            
            
# Helper function to safely read a valid date string in YYYY-MM-DD format
def get_valid_date(prompt: str) -> str:
    
    # Infinite loop to keep asking until valid input is received
    while True:
        # Read input string and clean extra whitespace
        user_date = input(prompt).strip()
        
        try:
            # 1. Validate format and calendar accuracy
            datetime.strptime(user_date, "%Y-%m-%d")
            
            # 2. Return valid date string (exits loop and function)
            return user_date
            
        except ValueError:
            # 3. Print error message and loop automatically continues to ask again
            print("Error: Date must be in YYYY-MM-DD format (e.g., 2026-06-01).")
            
            
# Helper function to safely read a non-empty string from the user
def get_valid_string(prompt: str) -> str:
    
    # Infinite loop to keep asking until non-empty input is received
    while True:
        # 1. Read input string, clean leading/trailing spaces, and convert to Title Case
        user_text = input(prompt).strip().title()
        
        # 2. Check if the string is empty or contains only whitespace
        if not user_text:
            print("Error: Input cannot be empty.")
            continue  # Skip to next iteration to prompt the user again
            
        # 3. Return formatted non-empty string (exits loop and function)
        return user_text
    
# Function to manage all transaction-related sub-menu operations
def handle_transaction_menu(bm: BudgetManager) -> None:

    # Sub-menu loop: keeps user inside transaction menu until they select option '6'
    while True:
        # 1. Display transaction menu design to screen
        display_transaction_menu()

        # 2. Capture choice and remove whitespace
        choice = input("Select an option (1-6): ").strip()

        # --- OPTION 1: View All Transactions ---
        if choice == "1":
            # BudgetManager method automatically prints all transactions or empty message
            bm.show_all_transactions()

        # --- OPTION 2: Add New Transaction ---
        elif choice == "2":
            # Safely capture base fields using helper functions
            trans_date = get_valid_date("Enter date (YYYY-MM-DD): ")
            trans_category = get_valid_string("Enter category: ")
            trans_amount = get_valid_float("Enter amount: ")
            trans_description = get_valid_string("Enter description: ")

            # Get automatically generated ID for new transaction
            trans_id = bm.get_next_id()

            # Loop until valid transaction type is supplied
            while True:
                # Capture type and format to Title Case (e.g. 'Income' or 'Expense')
                trans_type = (
                    input("Is this Income or Expense? ").strip().title()
                )

                # Check if the user entered exactly 'Income' or 'Expense'
                if trans_type in ["Income", "Expense"]:
                    
                    # Exit the validation loop only when a valid type is provided
                    break
                
                # If input is invalid, display error message and repeat loop
                print("❌ Invalid input. Please enter 'Income' or 'Expense'.")

            # Handle Income creation
            if trans_type == "Income":
                # Get unique Income field
                source = get_valid_string(
                    "Enter income source (e.g., Salary, Gift): "
                )

                # Create Income instance matching exact parameters from models.py
                new_trans = Income(
                    transID=trans_id,
                    transDate=trans_date,
                    transCategory=trans_category,
                    transDescription=trans_description,
                    transAmount=trans_amount,
                    source=source,
                )

            # Handle Expense creation
            else:
                # Get unique Expense fields
                merchant = get_valid_string("Enter merchant: ")
                payment_method = get_valid_string("Enter payment method: ")

                # Create Expense instance matching exact parameters from models.py
                new_trans = Expense(
                    transID=trans_id,
                    transDate=trans_date,
                    transCategory=trans_category,
                    transDescription=trans_description,
                    transAmount=trans_amount,
                    merchant=merchant,
                    paymentMethod=payment_method,
                )

            # Pass constructed transaction object to BudgetManager for saving
            bm.add_transaction(new_trans)
            print("✅ Transaction added successfully!")
            
            
        # --- OPTION 3: Edit Existing Transaction by ID ---
        elif choice == "3":
            # Step 1: Prompt user for the target transaction ID using integer validation helper
            trans_id = get_valid_int(
                "Enter the transaction ID you want to edit: "
            )

            # Step 2: Collect updated base field values using custom input validation helper functions
            trans_date = get_valid_date("Enter new date (YYYY-MM-DD): ")
            trans_category = get_valid_string("Enter new category: ")
            trans_amount = get_valid_float("Enter new amount: ")
            trans_description = get_valid_string("Enter new description: ")

            # Step 3: Prompt user for transaction type before/inside loop
            # Infinite validation loop: keeps prompting until user provides a valid type ('Income' or 'Expense')
            while True:
                trans_type = (
                    input("Is this Income or Expense? ").strip().title()
                )

                # Validation condition: if input matches allowed options, break out of loop to proceed
                if trans_type in ["Income", "Expense"]:
                    break

                # If validation fails, display error message and repeat loop
                print("❌ Invalid input. Please enter 'Income' or 'Expense'.")

            # Step 4: Handle subclass specific fields and object instantiation
            if trans_type == "Income":
                # Prompt for unique Income field using helper function
                source = get_valid_string("Enter new income source: ")

                # Instantiate updated Income object with original trans_id
                updated_trans = Income(
                    transID=trans_id,
                    transDate=trans_date,
                    transCategory=trans_category,
                    transDescription=trans_description,
                    transAmount=trans_amount,
                    source=source,
                )

            else:
                # Prompt for unique Expense fields using helper functions
                merchant = get_valid_string("Enter new merchant: ")
                payment_method = get_valid_string("Enter new payment method: ")

                # Instantiate updated Expense object with original trans_id
                updated_trans = Expense(
                    transID=trans_id,
                    transDate=trans_date,
                    transCategory=trans_category,
                    transDescription=trans_description,
                    transAmount=trans_amount,
                    merchant=merchant,
                    paymentMethod=payment_method,
                )

            # Step 5: Execute update operation inside try-except block
            try:
                # BudgetManager checks if ID exists; updates list and CSV or raises ValueError if missing
                bm.update_transaction(updated_trans)
                print(f"✅ Update for Transaction ID {trans_id} succeeded!")

            # Catch ValueError raised by BudgetManager if target trans_id does not exist
            except ValueError as e:
                print(f"❌ Error: {e}")

        # --- OPTION 4: Delete Transaction by ID---
        elif choice == "4":
            # Prompt user for the transaction ID using integer helper function
            trans_id = get_valid_int("Enter the transaction ID to delete: ")

            try:
                # Attempt to delete the transaction via BudgetManager
                bm.delete_transaction(trans_id)

                # Printed only if deletion was successful (valid ID was provided)
                print("✅ Transaction deleted successfully!")

            # Reached except block because the transaction ID does not exist
            except ValueError as e:
                # Display the error message raised by BudgetManager
                print(f"❌ Error: {e}")
            
           
        # --- OPTION 5: Search & Filter Transactions ---
        elif choice == "5":
            print("\n🔍 Search & Filter Options:")
            print("  [1] 🏷️ Search by Category")
            print("  [2] 📅 Search by Specific Date (YYYY-MM-DD)")
            print("  [3] 🗓️ Filter by Date Range")

            # Capture user choice (1-3) and remove whitespace
            search_option = input("Choose an option (1-3): ").strip()

            # Sub-option 1: Search by Category
            if search_option == "1":
                # Prompt for category using helper function get_valid_string
                user_category = get_valid_string("Enter category to search: ")
                # BudgetManager method filters and prints matches directly
                bm.search_category(user_category)

            # Sub-option 2: Search by Specific Date
            elif search_option == "2":
                # Prompt for date using helper function get_valid_date
                user_date = get_valid_date("Enter date to search (YYYY-MM-DD): ")
                # BudgetManager method filters and prints matches directly
                bm.search_date(user_date)

            # Sub-option 3: Filter by Date Range
            elif search_option == "3":
                # Prompt for start and end dates using helper function get_valid_date
                user_start_date = get_valid_date("Enter start date (YYYY-MM-DD): ")
                user_end_date = get_valid_date("Enter end date (YYYY-MM-DD): ")
                # BudgetManager method filters and prints matches directly
                bm.filter_by_date_range(user_start_date, user_end_date)

            # Fallback for invalid sub-menu choices
            else:
                print("❌ Invalid selection. Returning to transaction menu.")

       
        # --- OPTION 6: Return to Main Menu ---
        elif choice == "6":
            print("Returning to Main Menu...")
            break

        # Handle invalid menu selections
        else:
            print("❌ Invalid option. Please enter a number between 1 and 6.")
            
            
# Function to manage all monthly budget & alert sub-menu operations
def handle_budget_menu(bm: BudgetManager) -> None:

    # Sub-menu loop: keeps user inside budget menu until they explicitly select option '3'
    while True:
        # Display monthly budget sub-menu interface to the screen
        display_budget_menu()

        # Capture user input string and clean leading/trailing whitespace
        choice = input("Select an option (1-3): ").strip()

        # --- OPTION 1: Set / Update Monthly Budget ---
        if choice == "1":
            
            # Prompt user for positive budget amount using UI helper function get_valid_float
            budget_amount = get_valid_float("Enter monthly budget amount: ")

            # Pass amount to BudgetManager to update the internal self.monthly_budget variable
            bm.set_budget(budget_amount)

            # Print confirmation message formatted to 2 decimal places
            print(f"✅ Monthly budget updated to: {budget_amount:.2f}")

        # --- OPTION 2: Check Budget Status & Spending Limit ---
        elif choice == "2":
            
            # 1. Calculate total expenses using List Comprehension (always calculated regardless of budget)
            total_expenses = sum(
                [trans.transAmount for trans in bm.transactions if trans.transType == "expense"]
            )

            # 2. Always display general budget status header and baseline summary
            print("\n🎯 --- BUDGET STATUS ---")
            print(f"📌 Monthly Budget Limit: {bm.monthly_budget:.2f}")
            print(f"💸 Total Spent So Far:  {total_expenses:.2f}")

            # 3. Case A: User has not configured a budget limit yet (limit is 0.0 (the default value set in BudgetManager __init__))
            if bm.monthly_budget == 0:
                print("⚠️ Note: No monthly budget limit set yet. Set a budget in Option 1 to enable alerts.")

            # 4. Case B: Spending exceeded the set monthly budget limit
            elif total_expenses > bm.monthly_budget:
                over_amount = total_expenses - bm.monthly_budget
                print(f"🚨 ALERT: You have exceeded your budget by {over_amount:.2f}!")

            # 5. Case C: Spending is within the set monthly budget limit
            else:
                remaining = bm.monthly_budget - total_expenses
                print(f"✅ Good news! You are within budget. Remaining: {remaining:.2f}")
        
        # --- OPTION 3: Return to Main Menu ---
        elif choice == "3":
            # Print feedback message notifying return to main menu
            print("Returning to Main Menu...")

            # Break out of the while loop to exit handle_budget_menu function
            break

        # --- Fallback Branch for Invalid Choices ---
        else:
            # Display error message if user selected a number outside 1-3
            print("❌ Invalid option. Please enter a number between 1 and 3.")


# Function to manage all financial reports & analytics sub-menu operations
def handle_reports_menu() -> None:

    # Reload data into ReportGenerator to ensure latest transactions from CSV are loaded into Pandas DataFrame
    rg = ReportGenerator()

    # Sub-menu loop: keeps user inside reports menu until they explicitly select option '9'
    while True:
        # Display the reports menu options on screen
        display_reports_menu()

        # Capture user menu choice and clean leading/trailing whitespace
        choice = input("Select an option (1-9): ").strip()

        # --- OPTION 1: Financial Overview (Total Income, Expenses & Balance) ---
        if choice == "1":
            print("\n💵 --- FINANCIAL OVERVIEW ---")
            
            # Fetch numeric values (floats) and format to 2 decimal places
            print(f"💰 Total Income:   {rg.total_income():.2f}")
            print(f"💸 Total Expenses: {rg.total_expense():.2f}")
            print(f"⚖️ Current Balance: {rg.current_balance():.2f}")

        # --- OPTION 2: Expenses by Category ---
        elif choice == "2":
            
            print("\n🏷️ --- EXPENSES BY CATEGORY ---")
            
            # Print DataFrame returned by expenses_by_category()
            print(rg.expenses_by_category())

        # --- OPTION 3: Income by Category ---
        elif choice == "3":
            
            print("\n💼 --- INCOME BY CATEGORY ---")
            
            # Print DataFrame returned by income_by_category()
            print(rg.income_by_category())

        # --- OPTION 4: Monthly Summary ---
        elif choice == "4":
            
            print("\n📅 --- MONTHLY SUMMARY ---")
            
            # Print DataFrame returned by monthly_summary()
            print(rg.monthly_summary())

        # --- OPTION 5: Highest Transaction (Max Amount) ---
        elif choice == "5":
            
            print("\n🏆 --- HIGHEST TRANSACTION ---")
            
            # Print DataFrame containing max transaction row(s)
            print(rg.max_transaction())

        # --- OPTION 6: Average Expense ---
        elif choice == "6":
            
            print("\n📐 --- AVERAGE EXPENSE ---")
            
            # Print calculated average expense float value
            print(f"💵 Average Expense: {rg.average_expense():.2f}")

        # --- OPTION 7: Filter Transactions by Date Range ---
        elif choice == "7":
            print("\n🗓️ --- FILTER BY DATE RANGE ---")
            
            # Safely capture start and end dates using UI helper function
            user_start_date = get_valid_date("Enter start date (YYYY-MM-DD): ")
            user_end_date = get_valid_date("Enter end date (YYYY-MM-DD): ")
            
            # Print filtered DataFrame returned by filter_by_date_range()
            print(rg.filter_by_date_range(user_start_date, user_end_date))

        # --- OPTION 8: Export Selected Report to CSV ---
        elif choice == "8":
            print("\n💾 --- EXPORT REPORT TO CSV ---")
            print("Select a report to export:")
            print("  [1] Expenses by Category")
            print("  [2] Income by Category")
            print("  [3] Monthly Summary")
            print("  [4] Filtered Transactions by Date Range")

            # Capture sub-menu choice for export report type (1-4)
            export_choice = input("Choose a report option (1-4): ").strip()

            # Initialize target_df as None (sentinel / placeholder variable).
            # It will hold the selected Pandas DataFrame object if a valid option (1-4) is selected.
            target_df = None

            # Choice 1: Fetch pre-calculated Expenses by Category DataFrame (no extra input required)
            if export_choice == "1":
                target_df = rg.expenses_by_category()

            # Choice 2: Fetch pre-calculated Income by Category DataFrame (no extra input required)
            elif export_choice == "2":
                target_df = rg.income_by_category()

            # Choice 3: Fetch pre-calculated Monthly Summary DataFrame (no extra input required)
            elif export_choice == "3":
                target_df = rg.monthly_summary()

            # Choice 4: Requires dynamic user input (date range) before generating the DataFrame.
            # Asks user for start and end dates first, then generates filtered DataFrame on the fly.
            elif export_choice == "4":
                s_date = get_valid_date("Enter start date (YYYY-MM-DD): ")
                e_date = get_valid_date("Enter end date (YYYY-MM-DD): ")
                target_df = rg.filter_by_date_range(s_date, e_date)

            # Fallback for invalid export menu choices (e.g., '9' or 'abc').
            # Leaves target_df as None so export execution is safely skipped below.
            else:
                print("❌ Invalid export selection.")

            # Check if a valid DataFrame object was assigned to target_df (is not None).
            # If user entered an invalid choice, target_df remains None and file prompt/export are bypassed.
            if target_df is not None:
                
                # Prompt user for export file name using validation helper
                file_name = get_valid_string("Enter name for exported CSV file: ")
                
                # Call export_to_csv method; method internally prints success or empty data warning
                rg.export_to_csv(target_df, file_name)

        # --- OPTION 9: Return to Main Menu ---
        elif choice == "9":
            print("Returning to Main Menu...")
            
            # Exit while loop to return control to main application menu
            break

        # Fallback branch for invalid choices outside range 1-9
        else:
            print("❌ Invalid option. Please enter a number between 1 and 9.")
            

# Function to manage all data visualization & charts sub-menu operations
def handle_visualization_menu() -> None:

    # Reload data into ReportGenerator to ensure latest transactions from CSV are loaded
    rg = ReportGenerator()

    # Sub-menu loop: keeps user inside visualization menu until they select option '3'
    while True:
        # Display the visualization menu options on screen
        display_visualization_menu()

        # Capture choice and clean leading/trailing whitespace
        choice = input("Select an option (1-3): ").strip()

        # --- OPTION 1: View & Save Expense by Category Chart ---
        if choice == "1":
            print("\n📊 --- EXPENSE BY CATEGORY CHART ---")
            # Displays plot window and automatically saves 'expenses_by_category.png'
            rg.figure_expenses_by_category()
            print("✅ Chart saved successfully as 'expenses_by_category.png'")

        # --- OPTION 2: View & Save Income by Category Chart ---
        elif choice == "2":
            print("\n📈 --- INCOME BY CATEGORY CHART ---")
            # Displays plot window and automatically saves 'income_by_category.png'
            rg.figure_income_by_category()
            print("✅ Chart saved successfully as 'income_by_category.png'")

        # --- OPTION 3: Return to Main Menu ---
        elif choice == "3":
            print("Returning to Main Menu...")
            break

        # --- Fallback Branch for Invalid Choices ---
        else:
            print("❌ Invalid option. Please enter a number between 1 and 3.")
            
# Main application entry point that manages top-level menu navigation and system lifecycle
def main() -> None:

    # 1. Instantiate the primary BudgetManager object OUTSIDE the loop (once at startup)
    bm = BudgetManager("transactions.csv")

    # 2. Load existing transaction records from CSV file into memory (RAM)
    bm.load_from_csv()

    # 3. Main application navigation loop
    while True:
        # Display main menu choices
        display_main_menu()

        # Capture user selection
        choice = input("Select an option (1-5): ").strip()

        # --- OPTION 1: Transaction Management ---
        if choice == "1":
            # Pass the single shared BudgetManager instance to the transactions menu
            handle_transaction_menu(bm)

        # --- OPTION 2: Monthly Budget & Alerts ---
        elif choice == "2":
            # Pass the single shared BudgetManager instance to the budget menu
            handle_budget_menu(bm)

        # --- OPTION 3: Financial Reports & Analysis ---
        elif choice == "3":
            handle_reports_menu()

        # --- OPTION 4: Data Visualization & Charts ---
        elif choice == "4":
            handle_visualization_menu()

        # --- OPTION 5: Save & Exit ---
        elif choice == "5":
            
            # Ensure all in-memory transaction updates are saved to the CSV file before exiting
            bm.save_to_csv()
            
            print("\n💾 Data saved successfully to 'transactions.csv'. Have a great day! 👋")
            
            # Break terminates the main application while loop, allowing clean and natural program exit
            break 

        # Fallback branch for invalid menu choices
        else:
            print("❌ Invalid option. Please enter a number between 1 and 5.")


# Standard Python script execution block
if __name__ == "__main__":
    main()
   
    
        
        
        
        
        

    
        
        
        
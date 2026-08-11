# Import Transaction, Income and Expense classes from models.py file
from models import Transaction, Income, Expense

# Import built-in Python CSV library for file handling
import csv

# Import datetime library capabilities for date parsing and validation
from datetime import datetime

# Main management class responsible for budget operations and data persistence
class BudgetManager:
    
    # Initializes manager attributes: file paths, budget limits, and transaction list
    def __init__(self, filename: str = "transactions.csv", monthly_budget: float = 0.0) -> None:
        
        # Default CSV filename for saving and loading data and store as instance variable
        self.filename: str = filename
        
        # Monthly spending limit used for budget alerts and store as instance variable 
        self.monthly_budget: float = monthly_budget
        
        # In-memory list to store Transaction objects and store as instance variable
        self.transactions: list = []
        
        
    # Updates the monthly budget limit using the amount received from the user
    # Args: amount (float) - the new positive budget value provided via main UI
    def set_budget(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Monthly budget must be positive")
        self.monthly_budget = amount
        
        
    # Method to load transaction data from CSV file into memory
    def load_from_csv(self) -> None:

        # Try block to attempt reading the file if it exists on disk
        try:

            # Open CSV file safely and store the opened file object in the variable 'file'
            with open(self.filename, mode="r", encoding="utf-8", newline="") as file:

                # Create 'reader' variable holding DictReader object that converts each CSV row into a dictionary
                reader = csv.DictReader(file)

                # Reset in-memory list before loading to prevent duplicate entries
                self.transactions = []
                
                # Loop through each row dictionary inside the 'reader' object
                for row in reader:
                    
                    transType = row["type"]
                    
                    # Check if row is Income
                    if transType == 'income':
                        trans = Income(
                            # Convert CSV "id" string value to integer for transID
                            transID=int(row["id"]),

                            # Extract date string from CSV "date" column for transDate
                            transDate=row["date"],

                            # Extract category string from CSV "category" column for transCategory
                            transCategory=row["category"],

                            # Extract description string from CSV "description" column for transDescription
                            transDescription=row["description"],

                            # Convert CSV "amount" string value to float for transAmount
                            transAmount=float(row["amount"]),
                            
                            # Extract source string from CSV "source" column
                            source=row['source']
                        )
                    # Check if row is Expense
                    elif transType == 'expense':
                        trans = Expense(
                            # Convert CSV "id" string value to integer for transID
                            transID=int(row["id"]),

                            # Extract date string from CSV "date" column for transDate
                            transDate=row["date"],

                            # Extract category string from CSV "category" column for transCategory
                            transCategory=row["category"],

                            # Extract description string from CSV "description" column for transDescription
                            transDescription=row["description"],

                            # Convert CSV "amount" string value to float for transAmount
                            transAmount=float(row["amount"]),
                            
                            # Extract merchant string from CSV "merchant" column
                            merchant=row['merchant'],
                            
                            # Extract paymentMethod string from CSV "paymentMethod" column
                            paymentMethod=row['paymentMethod']
                        )
                    # Base Transaction fallback
                    else:
                        trans = Transaction(
                            # Convert CSV "id" string value to integer for transID
                            transID=int(row["id"]),

                            # Extract date string from CSV "date" column for transDate
                            transDate=row["date"],

                            # Extract type string from CSV "type" column for transType
                            transType=row["type"],

                            # Extract category string from CSV "category" column for transCategory
                            transCategory=row["category"],

                            # Extract description string from CSV "description" column for transDescription
                            transDescription=row["description"],

                            # Convert CSV "amount" string value to float for transAmount
                            transAmount=float(row["amount"])
                        )

                    # Append the populated transaction object to the main list (runs inside the for loop for all types)
                    self.transactions.append(trans)

        # Catch exception if the CSV file does not exist on disk
        except FileNotFoundError:

            # Set transactions list to empty so application runs without crashing
            self.transactions = []
        
        
    # Method to save all transactions from memory (RAM) back into the CSV file
    def save_to_csv(self) -> None:
        
        # Open CSV file in write mode ("w") which creates or overwrites the file defined as 'file' variable
        with open(self.filename, mode="w", encoding="utf-8", newline="") as file:

            # Define list of column header names matching the CSV structure
            columns = [
                "id", 
                "date",
                "type", 
                "category",
                "description", 
                "amount",
                "source", 
                "merchant",
                "paymentMethod"
            ]

            # Create 'writer' variable holding DictWriter object configured with columns
            writer = csv.DictWriter(file, fieldnames=columns)

            # Write the header row (columns) as the first line of the CSV file
            writer.writeheader()

            # Iterate through each Transaction object inside self.transactions list
            for trans in self.transactions:

                # Convert Transaction object to dictionary using to_dict() from models.py file and write to CSV
                writer.writerow(trans.to_dict())
                
    
    # Method to add a new transaction object to memory and update the CSV file
    def add_transaction(self, trans: Transaction) -> None:
        
        # Access the 'transactions' list belonging to self and append the new 'trans' object
        self.transactions.append(trans)
        
        # Call the save_to_csv method belonging to self (no arguments needed as save_to_csv accesses self directly)
        self.save_to_csv()
        
        
# Method to delete a transaction by its ID and save changes to CSV
    def delete_transaction(self, trans_id: int) -> None:

        # Extract a list of all existing transaction IDs (using trans.transID from models.py)
        transID_list = [trans.transID for trans in self.transactions]

        # Check if the requested trans_id is NOT in transID_list
        if trans_id not in transID_list:
            raise ValueError(f"Transaction with ID {trans_id} does not exist.")

        # Filter out transaction with matching trans_id using list comprehension
        self.transactions = [
            trans for trans in self.transactions if trans.transID != trans_id
        ]

        # Save changes to CSV file
        self.save_to_csv()
    
    # Method to display all transactions on the screen
    def show_all_transactions(self) -> None:
        
        # Check if the transactions list is empty
        if not self.transactions:
            
            # Reached if list is empty (False inverted to True by not)
            print("No transactions found.")
            
            # Exit function immediately (do not run lines below)
            return

        # Reached only if list is not empty (didn't hit return)
        print("--- Total Transactions ---")

        # Iterate through transactions and print each one
        for trans in self.transactions:
            print(f"- {trans}")
            
            
        
# Method to search transactions by category
    def search_category(self, category: str) -> list:
        
        # Clean input string and convert to title case
        category_clean = category.strip().title()
        
        # Filter transactions matching the cleaned category name
        category_filter = [trans for trans in self.transactions if category_clean == trans.transCategory]
        
        # If no transactions found, print message and exit function immediately returning empty list
        if not category_filter:
            print(f"No transactions found in category '{category_clean}'.")
            return []
        
        # Display header message for found transactions
        print(f"The transactions found in category '{category_clean}' are:")
        
        # Print each matching transaction
        for trans in category_filter:
            print(f"- {trans}")
            
        # Return the populated filtered list
        return category_filter
    
    
    
# Method to search transactions by date (YYYY-MM-DD)
    def search_date(self, trans_date: str) -> list:
        
        # Clean whitespace from input date string
        date_clean = trans_date.strip()
        
        # Validate that transaction date matches YYYY-MM-DD format (same logic as models.py)
        try:
            datetime.strptime(date_clean, "%Y-%m-%d")
        except ValueError:
            print("Date must be in YYYY-MM-DD format")
            return []
        
        # Filter transactions matching the cleaned date string
        date_filter = [trans for trans in self.transactions if date_clean == trans.transDate]
        
        # Check if no matching transactions were found
        if not date_filter:
            print(f"No transactions found on date '{date_clean}'.")
            return []
        
        # Display header message for found transactions
        print(f"The transactions found on date '{date_clean}' are:")
        
        # Iterate through the filtered list and print each transaction
        for trans in date_filter:
            print(f"- {trans}")
            
        # Return the list of matching transactions
        return date_filter
    
    
    
# Updates an existing transaction in the manager and saves changes to CSV
    def update_transaction(self, updated_trans: Transaction) -> None:

        # Create a list of all existing transaction IDs for validation
        transID_list = [trans.transID for trans in self.transactions]

        # Check if updated transaction ID exists; raise ValueError if missing so main.py can catch it
        if updated_trans.transID not in transID_list:
            raise ValueError(
                f"Transaction with ID {updated_trans.transID} does not exist."
            )

        # Loop using enumerate to get both index position (i) and transaction object (trans)
        for i, trans in enumerate(self.transactions):

            # Check if current transaction ID matches the updated transaction ID
            if trans.transID == updated_trans.transID:

                # Replace old transaction at index i with the new updated object
                self.transactions[i] = updated_trans

                # Exit loop early once update is complete
                break

        # Print success message with updated transaction details
        print(f"The updated transaction is: {updated_trans}")

        # Save the updated transactions list back to the CSV file
        self.save_to_csv()
        
        
# Method to filter transactions within a date range (YYYY-MM-DD)
    def filter_by_date_range(self, start_date: str, end_date: str) -> list:

        # Clean whitespace from input start and end date strings
        start_date_clean = start_date.strip()
        end_date_clean = end_date.strip()

        # Validate that start date matches YYYY-MM-DD format
        try:
            datetime.strptime(start_date_clean, "%Y-%m-%d")
        except ValueError:
            print("Start date must be in YYYY-MM-DD format")
            # Return empty list to keep consistent return type (list) when validation fails
            return []

        # Validate that end date matches YYYY-MM-DD format
        try:
            datetime.strptime(end_date_clean, "%Y-%m-%d")
        except ValueError:
            print("End date must be in YYYY-MM-DD format")
            # Return empty list to keep consistent return type (list) when validation fails
            return []

        # Ensure start date is not chronologically after end date
        if start_date_clean > end_date_clean:
            print("Error: Start date cannot be after end date")
            # Return empty list because the date range logic is invalid
            return []

        # Filter transactions falling between start and end dates (inclusive)
        date_filter = [
            trans for trans in self.transactions 
            if start_date_clean <= trans.transDate <= end_date_clean
        ]

        # Check if no transactions were found in the specified range
        if not date_filter:
            print(f"No transactions found between '{start_date_clean}' and '{end_date_clean}'.")
            # Return empty list explicitly when no matching transactions exist in the filter
            return []

        # Display header message for found transactions
        print(f"The transactions found between '{start_date_clean}' and '{end_date_clean}' are:")

        # Iterate through the filtered list and print each transaction
        for trans in date_filter:
            print(f"- {trans}")

        # Return the populated list of matching transactions
        return date_filter
    
    
    # Generates the next available transaction ID
    def get_next_id(self) -> int:
        
        # If the transactions list is empty, start with ID 1
        if not self.transactions:
            return 1
            
        # Variable to track the highest ID found so far
        max_id = 0
        
        # Iterate through all transactions to find the maximum ID
        for trans in self.transactions:
            if trans.transID > max_id:
                max_id = trans.transID
                
        # Return the next sequential ID
        return max_id + 1
            
            
            
            
            
            
            
            
        
            
            
            
            
            
        
            
        
            
        
        
       
        
        
            

         
            
            
    
            
        
        
        
        
# Import pandas library capabilities for data manipulation and analysis
import pandas as pd

# Import matplotlib pyplot module for data visualization
import matplotlib.pyplot as plt

# Import datetime module for date parsing and validation
from datetime import datetime


# Class responsible for loading financial data and generating analytical reports
class ReportGenerator:

    # Initializes ReportGenerator, stores filename, and automatically loads data
    def __init__(self, filename: str = "transactions.csv") -> None:

        # Store the CSV filename as an instance variable
        self.filename: str = filename

        # Initialize the DataFrame attribute as None before loading actual data
        self.df: pd.DataFrame = None

        # Automatically load data from CSV file into self.df upon object creation
        self.load_data()

    # Method to load CSV data into pandas DataFrame with error handling
    def load_data(self) -> None:

        # Try to read the CSV file using pandas
        try:
            self.df = pd.read_csv(self.filename)

        # Handle case where file does not exist yet
        except FileNotFoundError:
            # Create an empty DataFrame with defined column headers
            self.df = pd.DataFrame(
                columns=[
                    "id",
                    "date",
                    "type",
                    "category",
                    "description",
                    "amount",
                    "source",
                    "merchant",
                    "paymentMethod",
                ]
            )

    # Calculates total income by filtering rows where type is 'income'
    def total_income(self) -> float:

        # Filter DataFrame for income transactions
        income_df = self.df[self.df["type"] == "income"]

        # Calculate and return the sum of the amount column as float
        return float(income_df["amount"].sum())
    
    
    # Calculates total expense by filtering rows where type is 'expense'
    def total_expense(self) -> float:

        # Filter DataFrame for expense transactions
        expense_df = self.df[self.df["type"] == "expense"]

        # Calculate and return the sum of the amount column as float
        return float(expense_df["amount"].sum())
    
    # Calculates net balance by subtracting total expenses from total income
    def current_balance(self) -> float:

        # Calculate and return the financial balance
        return self.total_income() - self.total_expense()
    
    
    # Summarizes total expenses grouped by category as a DataFrame
    def expenses_by_category(self) -> pd.DataFrame:

        # Filter DataFrame for expense transactions only
        expense_df = self.df[self.df["type"] == "expense"]

        # Group by category, sum amounts, and store in an intermediate variable
        expenses_by_cat = expense_df.groupby("category")["amount"].sum().reset_index()

        # Return the resulting DataFrame
        return expenses_by_cat

    # Generates and displays a bar chart of expenses per category
    def figure_expenses_by_category(self) -> None:

        # Call expenses_by_category() method to fetch summarized data into a local DataFrame
        df_expense_figure = self.expenses_by_category()

        # Create the bar plot (x = category column, y = amount column)
        plt.bar(df_expense_figure["category"], df_expense_figure["amount"])

        # Add titles and axis labels
        plt.title("Expense per Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")

        # Save the plot as an image before showing it (bbox_inches='tight' prevents cropped labels)
        plt.savefig("expenses_by_category.png", bbox_inches="tight")

        # Display the plot
        plt.show()

    # Summarizes total incomes grouped by category as a DataFrame
    def income_by_category(self) -> pd.DataFrame:

        # Filter DataFrame for income transactions only
        income_df = self.df[self.df["type"] == "income"]

        # Group by category, sum amounts, and store in an intermediate variable
        income_by_cat = income_df.groupby("category")["amount"].sum().reset_index()

        # Return the resulting DataFrame
        return income_by_cat

    # Generates and displays a bar chart of income per category
    def figure_income_by_category(self) -> None:

        # Call income_by_category() method to fetch summarized data into a local DataFrame
        df_income_figure = self.income_by_category()

        # Create the bar plot (x = category column, y = amount column)
        plt.bar(df_income_figure["category"], df_income_figure["amount"])

        # Add titles and axis labels
        plt.title("Income per Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")

        # Save the plot as an image before showing it (bbox_inches='tight' prevents cropped labels)
        plt.savefig("income_by_category.png", bbox_inches="tight")

        # Display the plot
        plt.show()
        
        
    # Summarizes financial transactions by year-month and type as a DataFrame
    def monthly_summary(self) -> pd.DataFrame:

        # Create a copy of the original DataFrame to preserve source data
        df_summary = self.df.copy()

        # Extract 'YYYY-MM' string format from date column into a new 'month_year' column
        df_summary["Year_Month"] = df_summary["date"].str[:7]

        # Group transactions by year-month and type, calculate total amount, and reset index
        summary = (
            df_summary.groupby(["Year_Month", "type"])["amount"].sum().reset_index()
        )

        # Return the aggregated DataFrame
        return summary
        
        
    # Finds and returns the transaction(s) with the highest amount as a DataFrame
    def max_transaction(self) -> pd.DataFrame:
        
        # Edge case: If the DataFrame is empty, return an empty DataFrame to maintain return type consistency
        if self.df.empty:
            return pd.DataFrame()

        # Find the maximum value in the amount column
        max_amount = self.df["amount"].max()

        # Filter the DataFrame to extract row(s) matching the maximum amount
        df_max_trans = self.df[self.df["amount"] == max_amount]

        # Return the filtered DataFrame
        return df_max_trans
    
    # Calculates the average amount of expense transactions as a float
    def average_expense(self) -> float:
        
        # Filter DataFrame for expense transactions only
        expense_filter = self.df[self.df["type"] == "expense"]
        
        # Edge case: If there are no expense transactions, return 0.0 to prevent NaN float conversion error
        if expense_filter.empty:
            return 0.0

        # Calculate the mean of the amount column
        expense_filter_average = expense_filter["amount"].mean()

        # Return the calculated average as a float
        return float(expense_filter_average)
           
        
# Filters transactions within a specified date range and returns a DataFrame
    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:

        # Clean whitespace from input date strings
        start_date_clean = start_date.strip()
        end_date_clean = end_date.strip()

        # Validate that start date matches YYYY-MM-DD format
        try:
            datetime.strptime(start_date_clean, "%Y-%m-%d")
        except ValueError:
            print("Error: Start date must be in YYYY-MM-DD format")
            return pd.DataFrame()

        # Validate that end date matches YYYY-MM-DD format
        try:
            datetime.strptime(end_date_clean, "%Y-%m-%d")
        except ValueError:
            print("Error: End date must be in YYYY-MM-DD format")
            return pd.DataFrame()

        # Ensure start date is not chronologically after end date
        if start_date_clean > end_date_clean:
            print("Error: Start date cannot be after end date")
            return pd.DataFrame()

        # Filter rows where date is between start_date_clean and end_date_clean
        filtered_df = self.df[
            (self.df["date"] >= start_date_clean) & (self.df["date"] <= end_date_clean)
        ]

        # Return the filtered DataFrame
        return filtered_df
    
    
    # Exports a given DataFrame to a CSV file with formatted output name
    def export_to_csv(self, chosen_df: pd.DataFrame, csv_name: str) -> None:

        # Check if the provided DataFrame is empty before exporting
        if chosen_df.empty:
            print("No data available to export.")
            return

        # Clean any extra whitespace from the filename provided by user
        clean_name = csv_name.strip()

        # Save DataFrame to CSV file without row index numbers
        chosen_df.to_csv(f"{clean_name}.csv", index=False)

        # Display success confirmation message
        print(f"Report successfully saved as '{clean_name}.csv'")
        
        
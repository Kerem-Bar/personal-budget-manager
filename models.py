# Import datetime library capabilities for date parsing and validation
from datetime import datetime


# Define base class for all transactions
class Transaction:

    # Constructor method for base transaction
    def __init__(
        self, 
        transID:int, 
        transDate:str, 
        transType:str, 
        transCategory:str, 
        transDescription:str, 
        transAmount:float
    )-> None:
        
        # 1. Validate that transaction type is either 'income' or 'expense'
        if transType not in ['income', 'expense']:
            raise ValueError("You can only insert 'income' or 'expense'")
            
        # 2. Validate that transaction amount is positive
        if transAmount<=0:
            raise ValueError("Amount must be positive")
            
        # 3. Validate that transaction date matches YYYY-MM-DD format
        try:
            datetime.strptime(transDate, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
            
        # 4. Validate that category is not empty or just whitespace
        if not transCategory or not str(transCategory).strip():
            raise ValueError("Category can not be empty")
            
        # 5. Validate that description is not empty or just whitespace
        if not transDescription or not str(transDescription).strip():
            raise ValueError("Description can not be empty")

        # Set instance attributes
        self.transID=transID
        self.transDate=transDate
        self.transType=transType
        self.transCategory=transCategory.strip().title()
        self.transDescription=transDescription.strip().title()
        self.transAmount=transAmount

    # Return string representation of the transaction 
    def __str__(self)-> str:
        return (
            f"{self.transID},{self.transDate},{self.transType},"
            f"{self.transCategory},{self.transDescription},{self.transAmount}"
        )

    # Return dictionary representation matching CSV structure
    def to_dict(self)-> dict:
        return {
            "id": self.transID,
            "date": self.transDate,
            "type": self.transType,
            "category": self.transCategory, 
            "description": self.transDescription,
            "amount": self.transAmount
        }


# Define Income child class inheriting from Transaction
class Income(Transaction):

    # Constructor method for income transactions
    def __init__(
        self,
        transID:int,
        transDate:str,
        transCategory:str,
        transDescription:str,
        transAmount:float,
        source:str
    )-> None:
        
        # Call base class constructor with transType fixed automatically as 'income'
        super().__init__(
            transID, 
            transDate, 
            'income',
            transCategory,
            transDescription, 
            transAmount
        )
        
              
        # Validation: Check if source is empty or contains only whitespace characters
        if not source or not source.strip():
            # Raise ValueError to prevent creating an object with an invalid source
            raise ValueError("Source cannot be empty")
        
        # Set unique attribute for income
        self.source: str = source.strip().title()

    # Return string representation of Income (includes base fields + source)
    def __str__(self)-> str:
        return f"{super().__str__()},{self.source}" 

    # Return dictionary representation of Income (includes base dict + source)
    def to_dict(self)-> dict:
        income_data=super().to_dict()  
        income_data["source"]=self.source  
        return income_data


# Define Expense child class inheriting from Transaction
class Expense(Transaction):

    # Constructor method for Expense transactions 
    def __init__(
        self, 
        transID:int, 
        transDate:str, 
        transCategory:str, 
        transDescription:str,
        transAmount:float,
        merchant:str,
        paymentMethod:str
    )-> None:
        
        # Call base class constructor with transType fixed automatically as 'expense'
        super().__init__(
            transID, 
            transDate, 
            'expense', 
            transCategory, 
            transDescription,
            transAmount
        ) 
        
        
        
        # Validation: Ensure merchant is not empty or filled only with spaces
        if not merchant or not merchant.strip():
            raise ValueError("Merchant cannot be empty")
            
        # Validation: Ensure payment method is not empty or filled only with spaces
        if not paymentMethod or not paymentMethod.strip():
            raise ValueError("Payment method cannot be empty")
            
        
        # Assignments: Clean whitespace and convert text to Title Case
        self.merchant: str = merchant.strip().title()
        self.paymentMethod: str = paymentMethod.strip().title()
        

    # Return string representation of Expense
    def __str__(self)-> str:
        return f"{super().__str__()},{self.merchant},{self.paymentMethod}"

    # Return dictionary representation of Expense
    def to_dict(self)-> dict:
        expense_data=super().to_dict() 
        expense_data["merchant"]=self.merchant
        expense_data["paymentMethod"]=self.paymentMethod
        return expense_data
    
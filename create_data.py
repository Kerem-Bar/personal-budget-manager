# Import pandas library to create and export the dataset to CSV
import pandas as pd

# Define a list of dictionaries where each dictionary represents a single transaction row
initial_transactions = [
    {
        "id": 1,
        "date": "2026-06-01",
        "type": "income",
        "category": "Salary",
        "description": "June Salary",
        "amount": 12000.0,
        "source": "Company",
        "merchant": "",
        "paymentMethod": "",
    },
    {
        "id": 2,
        "date": "2026-06-02",
        "type": "expense",
        "category": "Food",
        "description": "Supermarket Groceries",
        "amount": 450.0,
        "source": "",
        "merchant": "Shufersal",
        "paymentMethod": "Credit Card",
    },
    {
        "id": 3,
        "date": "2026-06-03",
        "type": "expense",
        "category": "Transport",
        "description": "Monthly Bus Pass",
        "amount": 210.0,
        "source": "",
        "merchant": "Rav Kav",
        "paymentMethod": "Cash",
    },
    {
        "id": 4,
        "date": "2026-06-05",
        "type": "income",
        "category": "Freelance",
        "description": "Web Design Project",
        "amount": 2500.0,
        "source": "Client",
        "merchant": "",
        "paymentMethod": "",
    },
    {
        "id": 5,
        "date": "2026-06-10",
        "type": "expense",
        "category": "Food",
        "description": "Restaurant Dinner",
        "amount": 180.0,
        "source": "",
        "merchant": "Japanika",
        "paymentMethod": "Credit Card",
    },
    {
        "id": 6,
        "date": "2026-06-15",
        "type": "expense",
        "category": "Entertainment",
        "description": "Cinema Tickets",
        "amount": 90.0,
        "source": "",
        "merchant": "Planet Cinema",
        "paymentMethod": "Credit Card",
    },
    {
        "id": 7,
        "date": "2026-06-20",
        "type": "expense",
        "category": "Bills",
        "description": "Electricity Bill",
        "amount": 320.0,
        "source": "",
        "merchant": "Electric Co",
        "paymentMethod": "Bank Transfer",
    },
    {
        "id": 8,
        "date": "2026-07-01",
        "type": "income",
        "category": "Salary",
        "description": "July Salary",
        "amount": 12000.0,
        "source": "Company",
        "merchant": "",
        "paymentMethod": "",
    },
]

# Convert the list of dictionaries into a Pandas DataFrame object
df = pd.DataFrame(initial_transactions)

# Export the DataFrame to 'transactions.csv' in the local project directory
# Setting index=False prevents Pandas from writing row index numbers (0, 1, 2...) into the CSV file
df.to_csv("transactions.csv", index=False)

print("✅ 'transactions.csv' successfully generated in the project folder!")
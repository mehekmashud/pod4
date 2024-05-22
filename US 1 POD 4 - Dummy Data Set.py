import csv
import random
from datetime import datetime, timedelta

def generate_random_transaction(transaction_ids):
    while True:
        transaction_id = random.randint(1, 40000)  # Update transaction_id range
        if transaction_id not in transaction_ids:
            transaction_ids.add(transaction_id)
            break
    
    customer_id = random.randint(1, 500)
    amount = round(random.uniform(100, 20000), 2)  # Update amount range
    date = generate_random_date()
    
    return [transaction_id, customer_id, amount, date]  # Update column order


def generate_random_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    random_time = random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)
    return random_date.replace(hour=random_time[0], minute=random_time[1], second=random_time[2]).strftime("%Y-%m-%d %H:%M:%S")

def generate_transactions_table(num_rows):
    table = []
    transaction_ids = set()
    transactions_per_customer = {}
    transactions_per_month = {}

    while len(table) < num_rows:
        customer_id = random.randint(1, 500)
        transaction = generate_random_transaction(transaction_ids)
        table.append(transaction)

        if customer_id in transactions_per_customer:
            transactions_per_customer[customer_id] += 1
        else:
            transactions_per_customer[customer_id] = 1

        transaction_date = datetime.strptime(transaction[3], "%Y-%m-%d %H:%M:%S")
        month_key = transaction_date.strftime("%Y-%m")

        if month_key in transactions_per_month:
            if customer_id in transactions_per_month[month_key]:
                transactions_per_month[month_key][customer_id] += 1
            else:
                transactions_per_month[month_key][customer_id] = 1
        else:
            transactions_per_month[month_key] = {customer_id: 1}

    # Filter transactions for customers with less than 3 transactions per month
    idx = 0
    while idx < len(table):
        transaction = table[idx]
        customer_id = transaction[1]
        month_key = datetime.strptime(transaction[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m")

        if month_key in transactions_per_month and customer_id in transactions_per_month[month_key] and transactions_per_month[month_key][customer_id] < 3:
            table.pop(idx)
            transactions_per_month[month_key][customer_id] -= 1
            transactions_per_customer[customer_id] -= 1
        else:
            idx += 1

    # Generate additional transactions to meet the requirements
    while len(table) < num_rows:
        customer_id = random.randint(1, 500)
        month_key = random.choice(list(transactions_per_month.keys()))

        if customer_id not in transactions_per_month[month_key]:
            transactions_per_month[month_key][customer_id] = 0

        if transactions_per_month[month_key][customer_id] < 3:
            transaction = generate_random_transaction(transaction_ids)
            table.append(transaction)

            transactions_per_month[month_key][customer_id] += 1
            transactions_per_customer[customer_id] += 1

    return table

def write_to_csv(table):
    with open('transactions_table.csv', 'w', newline='') as file:  # Specify the file name as "transactions_table.csv"
        writer = csv.writer(file)
        writer.writerow(['transaction_id', 'customer_id', 'amount', 'date'])  # Specify the column names
        writer.writerows(table)
    print("CSV file 'transactions_table.csv' generated successfully.")

transactions_table = generate_transactions_table(20000)
write_to_csv(transactions_table)
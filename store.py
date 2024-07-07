import datetime
import os
import json
import csv
from tkinter import messagebox


class Store:
    def __init__(self, db):
        self.items = []
        self.db = db
        self.sold_items = []
        self.transaction_folder = "igikoni"
        os.makedirs(self.transaction_folder, exist_ok=True)
        self.load_data()

    def load_data(self):
        self.items = []  # Clear existing items before loading
        data = self.db.read_data()
        if data:
            for line in data.split('\n'):
                if line:
                    try:
                        name, quantity, price, payment_method, timestamp = line.split(',')
                        self.items.append({
                            "name": name,
                            "quantity": int(quantity),
                            "price": float(price),
                            "payment_method": payment_method,
                            "timestamp": datetime.datetime.strptime(timestamp.strip(), '%Y-%m-%dT%H:%M:%S.%f')
                        })
                    except ValueError:
                        print(f"Issue with data: {line}. Skipping...")
                        continue

    def _save_data_to_db(self):
        lines = []
        for item in self.items:
            line = f"{item['name']},{item['quantity']},{item['price']},{item['payment_method']},{item['timestamp'].isoformat()}"
            lines.append(line)
        data = '\n'.join(lines)
        self.db.save_data(data)

    def save_transaction_to_file(self, filename, transaction):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'a') as file:
            file.write(json.dumps(transaction) + '\n')

    def i_purchases(self, name, quantity, price, payment_method, debtor_name=None):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        purchase_folder = f"{self.transaction_folder}/purchases/{year}/{month}/{day}"
        os.makedirs(purchase_folder, exist_ok=True)
        purchases_filename = f"{purchase_folder}/all_purchases.txt"

        # Check if there's an existing item with the same name, price, and payment method
        for item in self.items:
            if item["name"] == name and item["price"] == price and item["payment_method"] == payment_method:
                item["quantity"] += quantity
                self._save_data_to_db()
                return

        # If no existing item is found, create a new one
        new_item = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "payment_method": payment_method,
            "timestamp": timestamp
        }
        if debtor_name:
            new_item["debtor_name"] = debtor_name
        self.items.append(new_item)
        self._save_data_to_db()

        # Log the transaction to the purchases file
        self.save_transaction_to_file(purchases_filename, {
            "type": "purchase",
            "name": name,
            "quantity": quantity,
            "price": price,
            "payment_method": payment_method,
            "debtor_name": debtor_name,
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })


    def stock(self):
        self.load_data()  # Assuming this loads data into self.items
        if not self.items:
            print("No stock available.")
            return []

        stock_summary = []
        for item in self.items:
            if item["quantity"] > 0:  # Only add items with quantity > 0
                summary_item = {
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "payment_method": item["payment_method"],
                    "timestamp": item["timestamp"].timestamp()
                }
                if item["payment_method"] == "Debtor":
                    summary_item["debtor_name"] == item.get("debtor_name", "")  # Include debtor_name if payment_method is not "Debtor"
                stock_summary.append(summary_item)

        return stock_summary

    def used(self, name, quantity, price):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        used_folder = f"{self.transaction_folder}/used/{year}/{month}/{day}"
        os.makedirs(used_folder, exist_ok=True)
        used_filename = f"{used_folder}/all_used.txt"

        total_quantity_available = sum(item["quantity"] for item in self.items if item["name"] == name)
        
        if total_quantity_available < quantity:
            return "Insufficient quantity"
        
        remaining_quantity = quantity

        for item in self.items:
            if item["name"] == name and item["quantity"] > 0:  # Ensure quantity > 0
                if item["quantity"] >= remaining_quantity:
                    item["quantity"] -= remaining_quantity
                    self.sold_items.append({"name": name, "quantity": remaining_quantity, "price": item["price"], "timestamp": timestamp})
                    self.save_transaction_to_file(used_filename, {
                        "type": "used",
                        "name": name,
                        "quantity": remaining_quantity,
                        "price": item["price"],
                        "payment_method": item["payment_method"],
                        "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    remaining_quantity = 0
                    break
                else:
                    used_quantity = item["quantity"]
                    item["quantity"] = 0
                    self.sold_items.append({"name": name, "quantity": used_quantity, "price": item["price"], "timestamp": timestamp})
                    self.save_transaction_to_file(used_filename, {
                        "type": "used",
                        "name": name,
                        "quantity": used_quantity,
                        "price": item["price"],
                        "payment_method": item["payment_method"],
                        "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    remaining_quantity -= used_quantity

        self._save_data_to_db()
        return True if remaining_quantity == 0 else False
        
    def purchase_used(self):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        purchase_file = f"{self.transaction_folder}/purchases/{year}/{month}/{day}/all_purchases.txt"
        used_file = f"{self.transaction_folder}/used/{year}/{month}/{day}/all_used.txt"

        purchases = self._read_transactions_from_file(purchase_file)
        used = self._read_transactions_from_file(used_file)

        purchases_display = "\n".join(json.dumps(p, indent=2) for p in purchases)
        used_display = "\n".join(json.dumps(u, indent=2) for u in used)

        messagebox.showinfo("Daily Report", f"Purchases:\n{purchases_display}\n\nUsed:\n{used_display}")

    def get_report(self):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        purchase_file = f"{self.transaction_folder}/purchases/{year}/{month}/{day}/all_purchases.txt"
        used_file = f"{self.transaction_folder}/used/{year}/{month}/{day}/all_used.txt"

        purchases = self._read_transactions_from_file(purchase_file)
        used = self._read_transactions_from_file(used_file)

        return purchases, used

    def _read_transactions_from_file(self, filename):
        transactions = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    transaction = json.loads(line.strip())
                    transactions.append(transaction)
        except FileNotFoundError:
            pass  # Handle file not found case if needed
        return transactions

    

class RestaurantStore:
    def __init__(self, db):
        self.items = []
        self.sold_items = []
        self.db = db
        self.transaction_folder = "Services"
        os.makedirs(self.transaction_folder, exist_ok=True)
        self.load_data()

    def load_data(self):
        self.items = []  # Clear existing items before loading
        data = self.db.read_data()
        if data:
            for line in data.split('\n'):
                if line:
                    try:
                        name, quantity, price, selling_price, timestamp, payment_method, debtor_name = line.split(',')
                        self.items.append({
                            "name": name,
                            "quantity": int(quantity),
                            "price": float(price),
                            "selling_price": float(selling_price),
                            "timestamp": datetime.datetime.fromisoformat(timestamp),
                            "payment_method": payment_method,
                            "debtor_name": debtor_name
                        })
                    except ValueError:
                        print(f"Issue with data: {line}. Skipping...")
                        continue

    def _save_data_to_db(self):
        lines = []
        for item in self.items:
            line = f"{item['name']},{item['quantity']},{item['price']},{item['selling_price']},{item['timestamp'].isoformat()},{item['payment_method']},{item['debtor_name'] or ''}"
            lines.append(line)
        data = '\n'.join(lines)
        self.db.save_data(data)
  
    def add_item(self, name, quantity, price, selling_price, payment_method, debtor_name=None):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        purchase_folder = f"{self.transaction_folder}/Purchases/{year}/{month}/{day}"
        os.makedirs(purchase_folder, exist_ok=True)
        purchases_filename = f"{purchase_folder}/Purchases.txt"

        # Check if there's an existing item with the same name, price, selling price, and payment method
        for item in self.items:
            if (item["name"] == name and 
                item["price"] == price and 
                item["selling_price"] == selling_price and 
                item["payment_method"] == payment_method):
                item["quantity"] += quantity
                self._save_data_to_db()
                # Log the transaction to the purchases file
                self.save_transaction_to_file(purchases_filename, {
                    "type": "purchase",
                    "name": name,
                    "quantity": quantity,
                    "price": price,
                    "selling_price": selling_price,
                    "payment_method": payment_method,
                    "debtor_name": debtor_name,
                    "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
                return

        # If no existing item is found, create a new one
        new_item = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "selling_price": selling_price,
            "payment_method": payment_method,
            "timestamp": timestamp,
            "debtor_name": debtor_name if debtor_name else ""
        }
        self.items.append(new_item)
        self._save_data_to_db()

        # Log the transaction to the purchases file
        self.save_transaction_to_file(purchases_filename, {
            "type": "purchase",
            "name": name,
            "quantity": quantity,
            "price": price,
            "selling_price": selling_price,
            "payment_method": payment_method,
            "debtor_name": debtor_name,
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    def view_items(self):
        data = self.db.read_data()
        items = []
        if data:
            lines = data.split('\n')
            for line in lines:
                parts = line.split(',')
                if parts[0].lower() == 'name':
                    continue
                if len(parts) >= 7:
                    try:
                        timestamp = datetime.datetime.fromisoformat(parts[4])
                    except ValueError:
                        timestamp = datetime.datetime.min
                    item = {
                        'name': parts[0],
                        'quantity': int(parts[1]),
                        'price': float(parts[2]),
                        'selling_price': float(parts[3]),
                        'payment_method': parts[5],
                        'debtor_name': parts[6],
                        'timestamp': timestamp
                    }
                    items.append(item)
        return items

    def sell_item(self, name, quantity, selling_price, payment_method, credit_name=None):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        sales_folder = f"{self.transaction_folder}/Sales/{year}/{month}/{day}"
        os.makedirs(sales_folder, exist_ok=True)
        sales_filename = f"{sales_folder}/Sales.txt"
        
        # Find the item in the inventory and check if enough quantity is available
        total_quantity_available = sum(item["quantity"] for item in self.items if item["name"] == name)
        
        if total_quantity_available < quantity:
            return "Insufficient quantity"
        
        remaining_quantity = quantity

        for item in self.items:
            if item["name"] == name and item["quantity"] > 0:  # Ensure quantity > 0
                if item["quantity"] >= remaining_quantity:
                    item["quantity"] -= remaining_quantity
                    self.sold_items.append({
                        "name": name,
                        "quantity": remaining_quantity,
                        "selling_price": selling_price,
                        "payment_method": payment_method,
                        "timestamp": timestamp,
                        "credit_name": credit_name
                    })
                    self._save_data_to_db()
                    self.save_transaction_to_file(sales_filename, {
                        "type": "sale",
                        "name": name,
                        "quantity": remaining_quantity,
                        "selling_price": selling_price,
                        "payment_method": payment_method,
                        "credit_name": credit_name,
                        "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    remaining_quantity = 0
                    break
                else:
                    sold_quantity = item["quantity"]
                    item["quantity"] = 0
                    self.sold_items.append({
                        "name": name,
                        "quantity": sold_quantity,
                        "selling_price": selling_price,
                        "payment_method": payment_method,
                        "timestamp": timestamp,
                        "credit_name": credit_name
                    })
                    self._save_data_to_db()
                    self.save_transaction_to_file(sales_filename, {
                        "type": "sale",
                        "name": name,
                        "quantity": sold_quantity,
                        "selling_price": selling_price,
                        "payment_method": payment_method,
                        "credit_name": credit_name,
                        "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    remaining_quantity -= sold_quantity

        return True if remaining_quantity == 0 else False

    def save_transaction_to_file(self, filename, transaction):
        print(f"Saving transaction to {filename}: {transaction}")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'a') as file:
            file.write(json.dumps(transaction) + "\n")

    def _read_transactions_from_file(self, filename):
        transactions = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    transaction = json.loads(line.strip())
                    transactions.append(transaction)
        except FileNotFoundError:
            pass
        return transactions

    def get_reports(self):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        purchases_file = f"{self.transaction_folder}/Purchases/{year}/{month}/{day}/Purchases.txt"
        sales_file = f"{self.transaction_folder}/Sales/{year}/{month}/{day}/Sales.txt"

        purchases = self._read_transactions_from_file(purchases_file)
        sales = self._read_transactions_from_file(sales_file)

        return purchases, sales

    def purchases_sales(self):
        timestamp = datetime.datetime.now()
        year, month, day = timestamp.strftime('%Y'), timestamp.strftime('%m'), timestamp.strftime('%d')
        purchases_file = f"{self.transaction_folder}/Purchases/{year}/{month}/{day}/Purchases.txt"
        sales_file = f"{self.transaction_folder}/Sales/{year}/{month}/{day}/Sales.txt"

        purchases = self._read_transactions_from_file(purchases_file)
        sales = self._read_transactions_from_file(sales_file)

        purchases_display = "\n".join(json.dumps(p, indent=2) for p in purchases)
        sales_display = "\n".join(json.dumps(u, indent=2) for u in sales)

        messagebox.showinfo("Daily Report", f"Purchases:\n{purchases_display}\n\nSales:\n{sales_display}")
    def _read_transactions_from_file(self, filename):
        transactions = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    transaction = json.loads(line.strip())
                    transactions.append(transaction)
        except FileNotFoundError:
            pass  # Handle file not found case if needed
        return transactions

    def all_added_items_within_program_execution(self):
        return self.added_items_within_program_execution

    def all_sold_items(self):
        return self.sold_items

    def generate_monthly_report(self, month, year):
        month_items = []
        month_sales = []

        for item in self.added_items_within_program_execution:
            if item['timestamp'].month == month and item['timestamp'].year == year:
                month_items.append(item)

        for item in self.sold_items:
            if item['timestamp'].month == month and item['timestamp'].year == year:
                month_sales.append(item)

        report_filename = f"monthly_report_{month}_{year}.txt"
        with open(report_filename, 'w') as report_file:
            report_file.write("Monthly Report\n\n")
            report_file.write("Added Items:\n")
            report_file.write("Name\tQuantity\tPrice\tSelling Price\tTimestamp\n")
            for item in month_items:
                report_file.write(f"{item['name']}\t{item['quantity']}\t{item['price']}\t{item['selling_price']}\t{item['timestamp'].isoformat()}\n")
            report_file.write("\nSold Items:\n")
            report_file.write("Name\tQuantity\tSelling Price\tTotal Selling Price\tTimestamp\n")
            total_sales = 0
            for item in month_sales:
                total_price = item['quantity'] * item['selling_price']
                total_sales += total_price
                report_file.write(f"{item['name']}\t{item['quantity']}\t{item['selling_price']}\t{total_price}\t{item['timestamp'].isoformat()}\n")
            report_file.write(f"\nTotal Sales: {total_sales}\n")


class WorkersExpensesTax:
    def __init__(self):
        self.workers_data = {}
        self.expenses_data = {}
        self.tax_data = {}
    
    def add_worker(self, name, salary, working_days):
        """Record worker's details."""
        self.workers_data[name] = {
            'salary': salary,
            'working_days': working_days
        }
    
    def add_expense(self, worker_name, expense_description, amount):
        """Record expenses for a worker."""
        if worker_name not in self.expenses_data:
            self.expenses_data[worker_name] = []
        self.expenses_data[worker_name].append({
            'description': expense_description,
            'amount': amount
        })
    
    def add_tax(self, worker_name, tax_type, tax_amount_per_month):
        """Record tax information for a worker."""
        if worker_name not in self.tax_data:
            self.tax_data[worker_name] = []
        self.tax_data[worker_name].append({
            'tax_type': tax_type,
            'tax_amount_per_month': tax_amount_per_month
        })
    
    def get_worker_info(self, name):
        """Retrieve worker's details."""
        return self.workers_data.get(name, "Worker not found")
    
    def get_expenses(self, worker_name):
        """Retrieve all expenses for a worker."""
        return self.expenses_data.get(worker_name, "No expenses recorded for this worker")
    
    def get_tax_info(self, worker_name):
        """Retrieve tax information for a worker."""
        return self.tax_data.get(worker_name, "No tax information recorded for this worker")

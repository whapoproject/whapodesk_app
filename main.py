import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import csv
from user import UserManager
from store import Store, RestaurantStore, WorkersExpensesTax
from database import Database




# Initialize database
user_db = Database("user_data.txt")
store_db = Database("store_data.txt")
restaurant_store_db = Database("restaurant_store_data.txt")

# Creating UserManager instance
user_manager = UserManager(user_db)
store = Store(store_db)
restaurant_store = RestaurantStore(restaurant_store_db)
# Creating WorkersExpensesTax instance
workers_expenses_tax = WorkersExpensesTax()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")

        # Set a fixed window size
        self.root.geometry("300x200")

        # Center the window on the screen
        self.center_window()
        

        # Variables to store input values and error message
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.error_var = tk.StringVar()

        # Create and configure widgets
        self.username_label = tk.Label(root, text="Username:", font=("Helvetica", 12))
        self.username_entry = tk.Entry(root, textvariable=self.username_var, font=("Helvetica", 12))
        self.password_label = tk.Label(root, text="Password:", font=("Helvetica", 12))
        self.password_entry = tk.Entry(root, textvariable=self.password_var, show="*", font=("Helvetica", 12))
        self.login_button = tk.Button(root, text="Login", command=self.login, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.register_button = tk.Button(root, text="Register", command=self.register, font=("Helvetica", 12), bg="#008CBA", fg="white")
        self.forgot_password_link = tk.Label(root, text="Forgot Password?", font=("Helvetica", 10), fg="blue", cursor="hand2")
        self.error_label = tk.Label(root, textvariable=self.error_var, font=("Helvetica", 10), fg="red")

        # Layout widgets
        self.username_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        self.password_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.login_button.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        self.register_button.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        self.forgot_password_link.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.error_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Bind events
        self.forgot_password_link.bind("<Button-1>", self.forgot_password)
        self.root.bind("<Configure>", self.center_window)

        # Initially hide error message
        self.error_label.grid_remove()

    def center_window(self, event=None):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position coordinates for centering the window
        x = (screen_width - 300) // 2
        y = (screen_height - 200) // 2

        # Set the window position
        self.root.geometry(f"300x200+{x}+{y}")

    def register(self):
        # Get username and password from entry fields
        username = self.username_var.get()
        password = self.password_var.get()

        # Check if username and password are not empty
        if username and password:
            # Placeholder for actual registration logic
            user_manager.register(username, password)
            messagebox.showinfo("Register", "Registration successful!")
            self.username_var.set("")
            self.password_var.set("")
            self.error_var.set("")
        else:
            self.error_var.set("Username or Password cannot be empty.")
            self.error_label.grid()

    def login(self):
        # Get username and password from entry fields
        username = self.username_var.get()
        password = self.password_var.get()

        # Check if username and password are not empty
        if username and password:
            # Placeholder for actual login validation
            if user_manager.authenticate(username, password):
                messagebox.showinfo("Login", f"Logged in as {username}")
                # Open the managing page window upon successful login
                self.open_manage_page(username)
                self.username_var.set("")
                self.password_var.set("")
                self.error_var.set("")
            else:
                self.error_var.set("Invalid username or password.")
                self.error_label.grid()
        else:
            self.error_var.set("Username or Password cannot be empty.")
            self.error_label.grid()

    def open_manage_page(self, username):
        # Close the login window
        self.root.destroy()
        # Open the managing page window
        manage_page = ManagePage(username)
        manage_page.run()

    def forgot_password(self, event):
        # Placeholder for forgot password functionality
        messagebox.showinfo("Forgot Password", "Forgot password functionality not implemented yet.")


#WORKING ON MANAGING PAGE (center of all codes )

class ManagePage:
    def __init__(self, username):
        self.username = username
        self.store = Store(store_db) 

        self.root = tk.Tk()
        self.root.title("Managing Page")
        self.restaurant_store = RestaurantStore(restaurant_store_db)
      
       

        # Create and configure widgets
        self.label = tk.Label(self.root, text="Welcome, " + self.username, font=("Helvetica", 16, "bold"))
        self.label.pack(pady=10)

        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(pady=20)

        self.button_add_item = tk.Button(self.frame_buttons, text="IGIKONI", command=self.igikoni, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        self.button_add_item.grid(row=0, column=0, padx=10)

        self.button_view_items = tk.Button(self.frame_buttons, text="TRAnsformers", command=self.trans, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        self.button_view_items.grid(row=0, column=1, padx=10)
        
      


        self.button_sell_item = tk.Button(self.frame_buttons, text="RESTAURANT", command=self.rest, font=("Helvetica", 12), width=15, bg="#FFA500", fg="white")
        self.button_sell_item.grid(row=1, column=0, padx=10, pady=5)

        self.button_report_option = tk.Button(self.frame_buttons, text="Gross Margin", command=self.gross_margin, font=("Helvetica", 12), width=15, bg="#FF5733", fg="white")
        self.button_report_option.grid(row=1, column=1, padx=10, pady=5)

        self.button_view_action_log = tk.Button(self.frame_buttons, text="Attendence", command=self.view_action_log, font=("Helvetica", 12), width=15, bg="#6A5ACD", fg="white")
        self.button_view_action_log.grid(row=2, column=0, columnspan=2, pady=5)

        self.button_logout = tk.Button(self.root, text="Logout", command=self.logout, font=("Helvetica", 12), width=10, bg="red", fg="white")
        self.button_logout.pack(pady=20)

 
#..........................................End..IGIKONI......................................................
    
    def igikoni(self):
        # Create a new Toplevel window for report options
        report_window = tk.Toplevel(self.root)
        report_window.title("igikoni page  ")

        # Label for the report options
        label_report_options = tk.Label(report_window, text="igikoni", font=("Helvetica", 16, "bold"))
        label_report_options.pack(pady=10)

        # Frame to hold the report option buttons
        frame_buttons = tk.Frame(report_window)
        frame_buttons.pack(pady=20)

        # Buttons for different report options
        button_added_items = tk.Button(frame_buttons, text="Purchases", command=self.i_purchases_Window, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_added_items.grid(row=0, column=0, padx=10, pady=5)

        button_sold_items = tk.Button(frame_buttons, text="Used", command=self.open_used_item_window, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        button_sold_items.grid(row=0, column=1, padx=10, pady=5)
        
        button_monthly_report = tk.Button(frame_buttons, text="Store", command=self.stock, font=("Helvetica", 12), width=15, bg="#FFA500", fg="white")
        button_monthly_report.grid(row=1, column=0, padx=10, pady=5)


        button_back = tk.Button(frame_buttons, text="Back", command=report_window.destroy, font=("Helvetica", 12), width=15, bg="#FF5733", fg="white")
        button_back.grid(row=1, column=1, padx=10, pady=5)

    def i_purchases_Window(self):
        self.add_item_window = tk.Toplevel(self.root)
        self.add_item_window.title("Igikoni Purchases")

        # Item Name
        self.label_item_name = tk.Label(self.add_item_window, text="Item Name:", font=("Helvetica", 12))
        self.label_item_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_item_name = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_item_name.grid(row=0, column=1, padx=10, pady=5)

        # Quantity
        self.label_quantity = tk.Label(self.add_item_window, text="Quantity:", font=("Helvetica", 12))
        self.label_quantity.grid(row=1, column=0, padx=10, pady=5)
        self.entry_quantity = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5)

        # Price
        self.label_price = tk.Label(self.add_item_window, text="Price:", font=("Helvetica", 12))
        self.label_price.grid(row=2, column=0, padx=10, pady=5)
        self.entry_price = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_price.grid(row=2, column=1, padx=10, pady=5)

        # Payment Methods
        self.label_payment_method = tk.Label(self.add_item_window, text="Payment Method:", font=("Helvetica", 12))
        self.label_payment_method.grid(row=3, column=0, padx=10, pady=5)
        self.payment_method_var = tk.StringVar()
        self.combobox_payment_method = ttk.Combobox(self.add_item_window, textvariable=self.payment_method_var, font=("Helvetica", 12))
        self.combobox_payment_method['values'] = ("Cash", "Momo", "Debtor")
        self.combobox_payment_method.grid(row=3, column=1, padx=10, pady=5)
        self.combobox_payment_method.bind("<<ComboboxSelected>>", self.toggle_debtor_entry)

        # Debtor Name
        self.label_debtor_name = tk.Label(self.add_item_window, text="Debtor Name:", font=("Helvetica", 12))
        self.label_debtor_name.grid(row=4, column=0, padx=10, pady=5)
        self.entry_debtor_name = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_debtor_name.grid(row=4, column=1, padx=10, pady=5)
        self.label_debtor_name.grid_remove()  # Initially hide the label
        self.entry_debtor_name.grid_remove()  # Initially hide the entry

        # Submit Button
        self.button_submit = tk.Button(self.add_item_window, text="Purchases and close", command=self.i_purchases, font=("Helvetica", 12), width=20, bg="#4CAF50", fg="white")
        self.button_submit.grid(row=5, column=0, columnspan=2, pady=10)

        self.button_logout = tk.Button(self.add_item_window, text="Exit", command=self.add_item_window.destroy, font=("Helvetica", 12), width=10)
        self.button_logout.grid(row=6, column=0, columnspan=2, pady=10)

    def toggle_debtor_entry(self, event):
        if self.payment_method_var.get() == "Debtor":
            self.label_debtor_name.grid()  # Show the label
            self.entry_debtor_name.grid()  # Show the entry
            self.entry_debtor_name.config(state='normal')
        else:
            self.label_debtor_name.grid_remove()  # Hide the label
            self.entry_debtor_name.grid_remove()  # Hide the entry
            self.entry_debtor_name.config(state='disabled')
            self.entry_debtor_name.delete(0, tk.END)

    def i_purchases(self):
        item_name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        payment_method = self.payment_method_var.get()
        debtor_name = self.entry_debtor_name.get() if payment_method == "Debtor" else None

        # Check if all fields are provided
        if item_name and quantity and price and payment_method and (debtor_name if payment_method == "Debtor" else True):
            # Add the item to the store
            #store_instance.i_purchases(item_name, int(quantity), float(price), payment_method, debtor_name)
            store.i_purchases(item_name, int(quantity), float(price), payment_method, debtor_name)


            messagebox.showinfo("Add Item", f"Item '{item_name}' added successfully.")
            self.entry_item_name.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.combobox_payment_method.set('')
            self.entry_debtor_name.delete(0, tk.END)

            # Close the "Purchases" window
            self.add_item_window.destroy()
        else:
            messagebox.showerror("Add Item", "Please fill in all fields.")



    
    def stock(self):
        items = self.store.stock()
        if items:
            view_items_window = tk.Toplevel(self.root)
            view_items_window.title("Igikoni Store")

            tree = ttk.Treeview(view_items_window)
            tree["columns"] = ("name", "quantity", "price", "payment_method", "total_price", "date_added")
            tree.heading("#0", text="ID")
            tree.heading("name", text="Name")
            tree.heading("quantity", text="Quantity")
            tree.heading("price", text="Price")
            tree.heading("payment_method", text="Payment method")
            tree.heading("total_price", text="Total Price")
            tree.heading("date_added", text="Date Added")

            total_amount = 0

            for i, item in enumerate(items):
                total_price = item['quantity'] * item['price']
                payment_method = item['payment_method']
                debtor_name = item.get('debtor_name', '')
                if payment_method == "Debtor":
                    payment_method += f" ({debtor_name})"

                date_added = datetime.datetime.fromtimestamp(item['timestamp']).strftime("%Y-%m-%d %H:%M:%S")

                tree.insert(parent="", index=i, iid=i, text=str(i+1), values=(item['name'], item['quantity'], item['price'], payment_method, total_price, date_added))
                total_amount += total_price

            tree.column("#0", width=40)
            tree.column("name", width=150)
            tree.column("quantity", width=80)
            tree.column("price", width=80)
            tree.column("payment_method", width=150)
            tree.column("total_price", width=100)
            tree.column("date_added", width=150)

            tree.pack(fill="both", expand=True)

            total_label = tk.Label(view_items_window, text=f"Total Amount: {total_amount}", font=("Helvetica", 12))
            total_label.pack(pady=10)

            button_download = tk.Button(view_items_window, text="Download", command=lambda: self.export_items_to_file(items), font=("Helvetica", 12), width=10)
            button_download.pack(pady=10)
        else:
            messagebox.showinfo("Info", "No stock available.")

    def export_items_to_file(self, items):
        filename = "igikoni_stock.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Quantity", "Price", "Payment Method", "Total Price", "Date Added"])
            for item in items:
                total_price = item['quantity'] * item['price']
                payment_method = item['payment_method']
                debtor_name = item.get('debtor_name', '')
                if payment_method == "Debtor":
                    payment_method += f" ({debtor_name})"
                date_added = datetime.datetime.fromtimestamp(item['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([item['name'], item['quantity'], item['price'], payment_method, total_price, date_added])
        messagebox.showinfo("Success", f"Items exported successfully to {filename}")

# WORKING ON USED ITEMS FROM IGIKONI
    def used(self):
        # Open the window for selling items
        self.open_used_item_window()

    def display_price(self, event=None):
        # Retrieve the selected item name from the Combobox
        item_name = self.combobox_item_name.get()

        # Retrieve the  price of the selected item from the list of items
        price = None
        for item in store.stock():
            if item['name'] == item_name:
                price = item.get('price')
                break

        # Display the  price in the entry field
        if price is not None:
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, str(price))

    def open_used_item_window(self):
        used_item_window = tk.Toplevel(self.root)
        used_item_window.title("Used items in Gikoni")

        # Item Name Dropdown (Combobox)
        label_item_name = tk.Label(used_item_window, text="Item Name:", font=("Helvetica", 12))
        label_item_name.grid(row=0, column=0, padx=10, pady=5)
        self.combobox_item_name = ttk.Combobox(used_item_window, state="readonly", font=("Helvetica", 12))
        self.combobox_item_name.grid(row=0, column=1, padx=10, pady=5)

        # Populate Combobox with item names
        available_items = [item['name'] for item in store.stock()]
        self.combobox_item_name['values'] = available_items

        # Quantity
        label_quantity = tk.Label(used_item_window, text="Quantity:", font=("Helvetica", 12))
        label_quantity.grid(row=1, column=0, padx=10, pady=5)
        self.entry_quantity = tk.Entry(used_item_window, font=("Helvetica", 12))
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5)

        #  Price
        label_price = tk.Label(used_item_window, text="Price:", font=("Helvetica", 12))
        label_price.grid(row=2, column=0, padx=10, pady=5)
        self.entry_price = tk.Entry(used_item_window, font=("Helvetica", 12))
        self.entry_price.grid(row=2, column=1, padx=10, pady=5)

        # Sell Button
        button_sell = tk.Button(used_item_window, text="Used", command=self.used_item_action, font=("Helvetica", 12), width=10, bg="#4CAF50", fg="white")
        button_sell.grid(row=3, column=0, columnspan=2, pady=10)

        # Close Button
        button_close = tk.Button(used_item_window, text="Close", command=used_item_window.destroy, font=("Helvetica", 12), width=10)
        button_close.grid(row=4, column=0, columnspan=2, pady=10)

        # Bind the Combobox to a function to automatically fill price after selecting an item
        self.combobox_item_name.bind("<<ComboboxSelected>>", self.display_price)

    def used_item_action(self):
        # Retrieve the selected item name from the Combobox
        item_name = self.combobox_item_name.get()
        quantity = int(self.entry_quantity.get())
        entered_price = float(self.entry_price.get())  # Retrieve entered selling price

        # Retrieve the price of the selected item from the list of items
        price = None
        for item in store.stock():
            if item['name'] == item_name:
                price = item.get('price')
                break

        # Check if the selected item name is valid
        if price is not None:
            # Check if entered price matches the selling price of the item
            if entered_price == price:
                # Check if the item is successfully sold
                if store.used(item_name, quantity, price):
                    messagebox.showinfo("Sell Item", f"{quantity} units of {item_name} sold successfully.")
                    total_price = quantity * price
  #                  log_item_transaction("sold_items_reports", self.username, item_name, quantity, 0, price, total_price)
                    self.entry_quantity.delete(0, tk.END)
                    self.entry_price.delete(0, tk.END)
                else:
                    messagebox.showerror("Sell Item", "Insufficient quantity.")
            else:
                messagebox.showerror("Sell Item", "Entered  price does not match the actual selling price.")
        else:
            messagebox.showerror("Sell Item", "Please select a valid item from the list.")

#..........................................TRANSFORMATION.............................................
    def trans(self):
        pass
#..........................................End..TRANSFORMATION..........................................
#..........................................RESTAURANT.................................................


    def rest(self):
        # Create a new Toplevel window for report options
        report_window = tk.Toplevel(self.root)
        report_window.title("Restaurant  page  ")

        # Label for the report options
        label_report_options = tk.Label(report_window, text="Restaurant", font=("Helvetica", 16, "bold"))
        label_report_options.pack(pady=10)

        # Frame to hold the report option buttons
        frame_buttons = tk.Frame(report_window)
        frame_buttons.pack(pady=20)

        # Buttons for different report options
        button_added_items = tk.Button(frame_buttons, text="Purchases", command=self.open_r_purchases_window, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_added_items.grid(row=0, column=0, padx=10, pady=5)

        button_sold_items = tk.Button(frame_buttons, text="Sales", command=self.sell_item, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        button_sold_items.grid(row=0, column=1, padx=10, pady=5)
        
        button_monthly_report = tk.Button(frame_buttons, text="Store", command=self.view_items, font=("Helvetica", 12), width=15, bg="#FFA500", fg="white")
        button_monthly_report.grid(row=1, column=0, padx=10, pady=5)


        button_back = tk.Button(frame_buttons, text="Back", command=report_window.destroy, font=("Helvetica", 12), width=15, bg="#FF5733", fg="white")
        button_back.grid(row=1, column=1, padx=10, pady=5)
        
    def open_r_purchases_window(self):
        self.add_item_window = tk.Toplevel(self.root)
        self.add_item_window.title("Restaurant Purchases Page")

        # Item Name
        self.label_item_name = tk.Label(self.add_item_window, text="Item Name:", font=("Helvetica", 12))
        self.label_item_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_item_name = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_item_name.grid(row=0, column=1, padx=10, pady=5)

        # Quantity
        self.label_quantity = tk.Label(self.add_item_window, text="Quantity:", font=("Helvetica", 12))
        self.label_quantity.grid(row=1, column=0, padx=10, pady=5)
        self.entry_quantity = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5)

        # Price
        self.label_price = tk.Label(self.add_item_window, text="Price:", font=("Helvetica", 12))
        self.label_price.grid(row=2, column=0, padx=10, pady=5)
        self.entry_price = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_price.grid(row=2, column=1, padx=10, pady=5)

        # Selling Price
        self.label_selling_price = tk.Label(self.add_item_window, text="Selling Price:", font=("Helvetica", 12))
        self.label_selling_price.grid(row=3, column=0, padx=10, pady=5)
        self.entry_selling_price = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_selling_price.grid(row=3, column=1, padx=10, pady=5)

        # Payment Methods
        self.label_payment_method = tk.Label(self.add_item_window, text="Payment Method:", font=("Helvetica", 12))
        self.label_payment_method.grid(row=4, column=0, padx=10, pady=5)
        self.payment_method_var = tk.StringVar()
        self.combobox_payment_method = ttk.Combobox(self.add_item_window, textvariable=self.payment_method_var, font=("Helvetica", 12))
        self.combobox_payment_method['values'] = ("cash", "momo", "debt")
        self.combobox_payment_method.grid(row=4, column=1, padx=10, pady=5)
        self.combobox_payment_method.bind("<<ComboboxSelected>>", self.on_payment_method_selected)

        # Debtor Name
        self.label_debtor_name = tk.Label(self.add_item_window, text="Debtor Name:", font=("Helvetica", 12))
        self.label_debtor_name.grid(row=5, column=0, padx=10, pady=5)
        self.entry_debtor_name = tk.Entry(self.add_item_window, font=("Helvetica", 12))
        self.entry_debtor_name.grid(row=5, column=1, padx=10, pady=5)
        self.label_debtor_name.grid_remove()
        self.entry_debtor_name.grid_remove()

        # Submit Button
        self.button_submit = tk.Button(self.add_item_window, text="Purchase and Close", command=self.add_item, font=("Helvetica", 12), width=20, bg="#4CAF50", fg="white")
        self.button_submit.grid(row=6, column=0, columnspan=2, pady=10)

        # Exit Button
        self.button_exit = tk.Button(self.add_item_window, text="Exit", command=self.add_item_window.destroy, font=("Helvetica", 12), width=20)
        self.button_exit.grid(row=7, column=0, columnspan=2, pady=10)

    def on_payment_method_selected(self, event):
        payment_method = self.payment_method_var.get()
        if payment_method == "debt":
            self.label_debtor_name.grid()
            self.entry_debtor_name.grid()
        else:
            self.label_debtor_name.grid_remove()
            self.entry_debtor_name.grid_remove()

    def add_item(self):
        item_name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        selling_price = self.entry_selling_price.get()
        payment_method = self.payment_method_var.get()
        debtor_name = self.entry_debtor_name.get() if payment_method == "debt" else None

        # Check if all fields are provided
        if item_name and quantity and price and selling_price and payment_method and (debtor_name if payment_method == "debt" else True):
            # Add the item to the store
            self.restaurant_store.add_item(item_name, int(quantity), float(price), float(selling_price), payment_method, debtor_name)
            

            # Log item transaction and move items to monthly report (if applicable)
            # log_item_transaction("added_items_reports", username, item_name, quantity, price, selling_price, total_purchases)
            # check_and_move_to_monthly_report()

            messagebox.showinfo("Add Item", f"Item '{item_name}' added successfully.")
            self.entry_item_name.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_selling_price.delete(0, tk.END)
            self.payment_method_var.set('')
            self.entry_debtor_name.delete(0, tk.END)
            
            # Close the "Add Item" window
            self.add_item_window.destroy()
        else:
            messagebox.showerror("Add Item", "Please fill in all fields.")

    
    def sell_item(self):
        # Open the window for selling items
        self.open_sell_item_window()

    def display_selling_price(self, event=None):
        # Retrieve the selected item name from the Combobox
        item_name = self.combobox_item_name.get()

        # Retrieve the selling price of the selected item from the list of items
        selling_price = None
        for item in restaurant_store.view_items():
            if item['name'] == item_name:
                selling_price = item.get('selling_price')
                break

        # Display the selling price in the entry field
        if selling_price is not None:
            self.entry_selling_price.delete(0, tk.END)
            self.entry_selling_price.insert(0, str(selling_price))

    def open_sell_item_window(self):
        sell_item_window = tk.Toplevel(self.root)
        sell_item_window.title("Sell Item")

        # Item Name Dropdown (Combobox)
        label_item_name = tk.Label(sell_item_window, text="Item Name:", font=("Helvetica", 12))
        label_item_name.grid(row=0, column=0, padx=10, pady=5)
        self.combobox_item_name = ttk.Combobox(sell_item_window, state="readonly", font=("Helvetica", 12))
        self.combobox_item_name.grid(row=0, column=1, padx=10, pady=5)

        # Populate Combobox with item names excluding items with zero quantity
        available_items = [item['name'] for item in restaurant_store.view_items() if item['quantity'] > 0]
        self.combobox_item_name['values'] = available_items

        # Quantity
        label_quantity = tk.Label(sell_item_window, text="Quantity:", font=("Helvetica", 12))
        label_quantity.grid(row=1, column=0, padx=10, pady=5)
        self.entry_quantity = tk.Entry(sell_item_window, font=("Helvetica", 12))
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5)

        # Selling Price
        label_selling_price = tk.Label(sell_item_window, text="Selling Price:", font=("Helvetica", 12))
        label_selling_price.grid(row=2, column=0, padx=10, pady=5)
        self.entry_selling_price = tk.Entry(sell_item_window, font=("Helvetica", 12))
        self.entry_selling_price.grid(row=2, column=1, padx=10, pady=5)

        # Payment Method
        label_payment_method = tk.Label(sell_item_window, text="Payment Method:", font=("Helvetica", 12))
        label_payment_method.grid(row=3, column=0, padx=10, pady=5)
        self.combobox_payment_method = ttk.Combobox(sell_item_window, state="readonly", font=("Helvetica", 12))
        self.combobox_payment_method['values'] = ['Cash', 'Momo', 'Credit']
        self.combobox_payment_method.grid(row=3, column=1, padx=10, pady=5)
        self.combobox_payment_method.bind("<<ComboboxSelected>>", self.toggle_creditor_name_entry)

        # Creditor Name (initially hidden)
        self.label_creditor_name = tk.Label(sell_item_window, text="Creditor Name:", font=("Helvetica", 12))
        self.entry_creditor_name = tk.Entry(sell_item_window, font=("Helvetica", 12))

        # Sell and Close Button
        button_sell = tk.Button(sell_item_window, text="Sell and Close", command=lambda: [self.sell_item_action(), sell_item_window.destroy()], font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_sell.grid(row=5, column=0, columnspan=2, pady=10)

        # Exit Button
        button_exit = tk.Button(sell_item_window, text="Exit", command=sell_item_window.destroy, font=("Helvetica", 12), width=10)
        button_exit.grid(row=6, column=0, columnspan=2, pady=10)

        # Bind the Combobox to a function to automatically fill selling price after selecting an item
        self.combobox_item_name.bind("<<ComboboxSelected>>", self.display_selling_price)


    def toggle_creditor_name_entry(self, event):
        selected_method = self.combobox_payment_method.get()
        if selected_method == "Credit":
            self.label_creditor_name.grid(row=4, column=0, padx=10, pady=5)
            self.entry_creditor_name.grid(row=4, column=1, padx=10, pady=5)
        else:
            self.label_creditor_name.grid_remove()
            self.entry_creditor_name.grid_remove()

    def sell_item_action(self):
        item_name = self.combobox_item_name.get()
        quantity = int(self.entry_quantity.get())
        entered_price = float(self.entry_selling_price.get())
        payment_method = self.combobox_payment_method.get()

        selling_price = None
        for item in self.restaurant_store.view_items():
            if item['name'] == item_name:
                selling_price = item.get('selling_price')
                break

        if selling_price is not None:
            if entered_price == selling_price:
                if payment_method == "Credit":
                    creditor_name = self.entry_creditor_name.get()
                    if not creditor_name:
                        messagebox.showerror("Sell Item", "Please enter a creditor name.")
                        return
                else:
                    creditor_name = None

                if self.restaurant_store.sell_item(item_name, quantity, selling_price, payment_method, creditor_name):
                    total_price = quantity * selling_price
 #                   log_item_transaction("sales", self.username, item_name, quantity, 0, selling_price, total_price, creditor_name)
                    messagebox.showinfo("Sell Item", "Item sold successfully!")
                else:
                    messagebox.showerror("Sell Item", "Not enough quantity available.")
            else:
                messagebox.showerror("Sell Item", "Entered price does not match the selling price.")
        else:
            messagebox.showerror("Sell Item", "Item not found.")

    def display_selling_price(self, event):
        selected_item = self.combobox_item_name.get()
        for item in restaurant_store.view_items():
            if item['name'] == selected_item:
                self.entry_selling_price.delete(0, tk.END)
                self.entry_selling_price.insert(0, item['selling_price'])
                break
    
    def view_items(self):
        items = restaurant_store.view_items()
        if items:
            view_items_window = tk.Toplevel(self.root)
            view_items_window.title("Service  Store")

            tree = ttk.Treeview(view_items_window)
            tree["columns"] = ("name", "quantity", "price", "payment_method", "total_price", "date_added")
            tree.heading("#0", text="ID")
            tree.heading("name", text="Name")
            tree.heading("quantity", text="Quantity")
            tree.heading("price", text="Price")
            tree.heading("payment_method", text="Payment method")
            tree.heading("total_price", text="Total Price")
            tree.heading("date_added", text="Date Added")  # Moved to the last position

            total_amount = 0

            for i, item in enumerate(items):
                total_price = item.get('quantity', 0) * item.get('price', 0)

                # Adjust payment method based on debtor's name
                payment_method = item.get('payment_method', '')
                debtor_name = item.get('debtor_name', '')
                if payment_method == "Debtor":
                    payment_method += f" ({debtor_name})"
 
                # Convert timestamp to human-readable date format
                date_added = datetime.datetime.fromtimestamp(item.get('date_added', 0)).strftime("%Y-%m-%d %H:%M:%S")

                # Insert formatted date into Treeview
                tree.insert(parent="", index=i, iid=i, text=str(i+1), values=(item.get('name', ''), item.get('quantity', ''), item.get('price', ''), payment_method, total_price, date_added))
                total_amount += total_price

            # Set column widths
            tree.column("#0", width=40)
            tree.column("name", width=150)
            tree.column("quantity", width=80)
            tree.column("price", width=80)
            tree.column("payment_method", width=150)  # Adjust width if needed
            tree.column("total_price", width=100)
            tree.column("date_added", width=150)  # Adjust width if needed

            tree.pack(fill="both", expand=True)

            # Display total amount
            total_label = tk.Label(view_items_window, text=f"Total Amount: {total_amount}", font=("Helvetica", 12))
            total_label.pack(pady=10)

            # Add buttons to download and print
            button_download = tk.Button(view_items_window, text="Download", command=lambda: self.export_items_to_file(items), font=("Helvetica", 12), width=10)
            button_download.pack(pady=5)

            button_close = tk.Button(view_items_window, text="Close", command=view_items_window.destroy, font=("Helvetica", 12), width=10)
            button_close.pack(pady=10)
        else:
            messagebox.showinfo("View Items", "No items available.")
    def print_items(self, items):
        # Placeholder function to print items
        # You can implement this based on your requirements
        pass
#.........................................End..RESTAURANT............................................



#..........................................GROSS MARGIN............................................
    def gross_margin(self):
        # Create a new Toplevel window for report options
        report_window = tk.Toplevel(self.root)
        report_window.title("G.M page ")

        # Label for the report options
        label_report_options = tk.Label(report_window, text="Gross Margin", font=("Helvetica", 16, "bold"))
        label_report_options.pack(pady=10)

        # Frame to hold the report option buttons
        frame_buttons = tk.Frame(report_window)
        frame_buttons.pack(pady=20)

        # Buttons for different report options
        button_added_items = tk.Button(frame_buttons, text="Dailly Report", command=self.dailly_report, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_added_items.grid(row=0, column=0, padx=10, pady=5)

        button_sold_items = tk.Button(frame_buttons, text="Monthly Report", command=self.monthly_report, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        button_sold_items.grid(row=0, column=1, padx=10, pady=5)

        button_monthly_report = tk.Button(frame_buttons, text="Repair", command=self.repair, font=("Helvetica", 12), width=15, bg="#FFA500", fg="white")
        button_monthly_report.grid(row=1, column=0, padx=10, pady=5)

        button_back = tk.Button(frame_buttons, text="Back", command=report_window.destroy, font=("Helvetica", 12), width=15, bg="#FF5733", fg="white")
        button_back.grid(row=1, column=1, padx=10, pady=5)
        
        
    def dailly_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Daily Reports ")
        # Label for the report options
        label_report_options = tk.Label(report_window, text="Daily Report", font=("Helvetica", 16, "bold"))
        label_report_options.pack(pady=10)

        # Frame to hold the report option buttons
        frame_buttons = tk.Frame(report_window)
        frame_buttons.pack(pady=20)

        # Buttons for different report options
        button_history = tk.Button(frame_buttons, text="Histories", command=self.history, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_history.grid(row=0, column=0, padx=10, pady=5)

        button_gross_profit = tk.Button(frame_buttons, text="Gross Profit", command=self.Gross_profit, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        button_gross_profit.grid(row=0, column=1, padx=10, pady=5)

        button_exit = tk.Button(frame_buttons, text="Exit", command=report_window.destroy, font=("Helvetica", 12), width=15, bg="#FF5733", fg="white")
        button_exit.grid(row=1, column=1, padx=10, pady=5)
    
    def history(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Histories ")
        # Label for the report options
        label_report_options = tk.Label(report_window, text="Daily Histories", font=("Helvetica", 16, "bold"))
        label_report_options.pack(pady=10)
        
        # Frame to hold the report option buttons
        frame_buttons = tk.Frame(report_window)
        frame_buttons.pack(pady=20)

        
        button_igikoni_histories = tk.Button(frame_buttons, text="Igikoni-histories", command=self.purchase_used, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_igikoni_histories.grid(row=0, column=0, padx=10, pady=5)

        button_Services_histories = tk.Button(frame_buttons, text="Services-histories", command=self.purchases_sales, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        button_Services_histories.grid(row=0, column=1, padx=10, pady=5)

        button_exit = tk.Button(frame_buttons, text="Exit", command=report_window.destroy, font=("Helvetica", 12), width=15, bg="#FF5733", fg="white")
        button_exit.grid(row=1, column=1, padx=10, pady=5)
        
    

    def download_report(self, purchases, used):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Item Name", "Quantity", "Price", "Payment Method", "Timestamp", "Type"])

                for purchase in purchases:
                    writer.writerow([
                        purchase["name"],
                        purchase["quantity"],
                        purchase["price"],
                        purchase["payment_method"],
                        purchase["timestamp"],
                        "Purchase"
                    ])

                for use in used:
                    writer.writerow([
                        use["name"],
                        use["quantity"],
                        use["price"],
                        use["payment_method"],
                        use["timestamp"],
                        "Used"
                    ])

                total_purchases = sum(item["quantity"] * item["price"] for item in purchases)
                total_used = sum(item["quantity"] * item["price"] for item in used)

                writer.writerow([])
                writer.writerow(["Total Purchased Quantity", "Total Purchased Price"])
                writer.writerow([sum(item["quantity"] for item in purchases), total_purchases])
                writer.writerow([])
                writer.writerow(["Total Used Quantity", "Total Used Price"])
                writer.writerow([sum(item["quantity"] for item in used), total_used])

            messagebox.showinfo("Report Saved", f"Report has been saved to {file_path}")


    def purchase_used(self):
        purchases, used = self.store.get_report()

        report_window = tk.Toplevel(self.root)
        report_window.title("Daily Report")
        report_window.geometry("800x600")

        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(report_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs for Purchased Items and Used Items
        purchases_tab = ttk.Frame(notebook)
        used_tab = ttk.Frame(notebook)

        notebook.add(purchases_tab, text='Purchased Items')
        notebook.add(used_tab, text='Used Items')

        # Create treeview for Purchased Items
        purchases_tree = ttk.Treeview(purchases_tab, columns=("Quantity", "Price", "Payment Method", "Timestamp"))
        purchases_tree.heading("#0", text="Item Name")
        purchases_tree.heading("Quantity", text="Quantity")
        purchases_tree.heading("Price", text="Price")
        purchases_tree.heading("Payment Method", text="Payment Method")
        purchases_tree.heading("Timestamp", text="Timestamp")
        
        total_purchased_quantity = 0
        total_purchased_price = 0.0

        # Insert purchased items into treeview
        for purchase in purchases:
            purchases_tree.insert("", "end", text=purchase["name"], values=(purchase["quantity"], purchase["price"], purchase["payment_method"], purchase["timestamp"]))
            total_purchased_quantity += purchase["quantity"]
            total_purchased_price += purchase["quantity"] * purchase["price"]

        purchases_tree.pack(fill=tk.BOTH, expand=True)

        # Label for total purchased items
        total_purchases_label = tk.Label(purchases_tab, text=f"Total Purchased Quantity: {total_purchased_quantity}, Total Purchased Price: Rwf{total_purchased_price:.2f}", font=("Helvetica", 10))
        total_purchases_label.pack(pady=(10, 0))

        # Create treeview for Used Items
        used_tree = ttk.Treeview(used_tab, columns=("Quantity", "Price", "Payment Method", "Timestamp"))
        used_tree.heading("#0", text="Item Name")
        used_tree.heading("Quantity", text="Quantity")
        used_tree.heading("Price", text="Price")
        used_tree.heading("Payment Method", text="Payment Method")
        used_tree.heading("Timestamp", text="Timestamp")
        
        total_used_quantity = 0
        total_used_price = 0.0

        # Insert used items into treeview
        for use in used:
            used_tree.insert("", "end", text=use["name"], values=(use["quantity"], use["price"], use["payment_method"], use["timestamp"]))
            total_used_quantity += use["quantity"]
            total_used_price += use["quantity"] * use["price"]

        used_tree.pack(fill=tk.BOTH, expand=True)

        # Label for total used items
        total_used_label = tk.Label(used_tab, text=f"Total Used Quantity: {total_used_quantity}, Total Used Price: Rwf{total_used_price:.2f}", font=("Helvetica", 10))
        total_used_label.pack(pady=(10, 0))

        # Add download button
        download_button = tk.Button(report_window, text="Download Report", command=lambda: self.download_report(purchases, used))
        download_button.pack(pady=20)
 
    def download_report(self, purchases, sales):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Item Name", "Quantity", "Price", "Payment Method", "Timestamp", "Type"])

                for purchase in purchases:
                    writer.writerow([
                        purchase["name"],
                        purchase["quantity"],
                        purchase["price"],
                        purchase["payment_method"],
                        purchase["timestamp"],
                        "Purchase"
                    ])

                for sale in sales:
                    selling_price = float(sale.get("selling_price", 0))  # Convert to float, default to 0 if not present
                    writer.writerow([
                        sale["name"],
                        sale["quantity"],
                        selling_price,
                        sale["payment_method"],
                        sale["timestamp"],
                        "Sale"
                    ])

                total_purchases = sum(item["quantity"] * item["price"] for item in purchases)
                total_sales = sum(item["quantity"] * float(item.get("selling_price", 0)) for item in sales)

                writer.writerow([])
                writer.writerow(["Total Purchased Quantity", "Total Purchased Price"])
                writer.writerow([sum(item["quantity"] for item in purchases), total_purchases])
                writer.writerow([])
                writer.writerow(["Total Sales Quantity", "Total Sales Price"])
                writer.writerow([sum(item["quantity"] for item in sales), total_sales])

            messagebox.showinfo("Report Saved", f"Report has been saved to {file_path}")

    def purchases_sales(self):
        purchases, sales = self.restaurant_store.get_reports()

        report_window = tk.Toplevel(self.root)
        report_window.title("Purchases and Sales Report")
        report_window.geometry("800x600")

        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(report_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs for Purchases and Sales
        purchases_tab = ttk.Frame(notebook)
        sales_tab = ttk.Frame(notebook)

        notebook.add(purchases_tab, text='Purchases')
        notebook.add(sales_tab, text='Sales')

        # Create treeview for Purchases
        purchases_tree = ttk.Treeview(purchases_tab, columns=("Quantity", "Price", "Payment Method", "Timestamp"))
        purchases_tree.heading("#0", text="Item Name")
        purchases_tree.heading("Quantity", text="Quantity")
        purchases_tree.heading("Price", text="Price")
        purchases_tree.heading("Payment Method", text="Payment Method")
        purchases_tree.heading("Timestamp", text="Timestamp")
        purchases_tree.pack(fill=tk.BOTH, expand=True)

        total_purchases_quantity = 0
        total_purchases_price = 0.0

        # Insert purchased items into treeview
        for purchase in purchases:
            purchases_tree.insert("", "end", text=purchase["name"], values=(purchase["quantity"], purchase["price"], purchase["payment_method"], purchase["timestamp"]))
            total_purchases_quantity += purchase["quantity"]
            total_purchases_price += purchase["quantity"] * purchase["price"]

        # Label for total purchased items
        total_purchases_label = tk.Label(purchases_tab, text=f"Total Purchased Quantity: {total_purchases_quantity}, Total Purchased Price: Rwf{total_purchases_price:.2f}", font=("Helvetica", 10))
        total_purchases_label.pack(pady=(10, 0))

        # Create treeview for Sales
        sales_tree = ttk.Treeview(sales_tab, columns=("Quantity", "Selling Price", "Payment Method", "Timestamp"))
        sales_tree.heading("#0", text="Item Name")
        sales_tree.heading("Quantity", text="Quantity")
        sales_tree.heading("Selling Price", text="Selling Price")
        sales_tree.heading("Payment Method", text="Payment Method")
        sales_tree.heading("Timestamp", text="Timestamp")
        sales_tree.pack(fill=tk.BOTH, expand=True)

        total_sales_quantity = 0
        total_sales_price = 0.0

        # Insert sold items into treeview
        for sale in sales:
            selling_price = float(sale.get("selling_price", 0))  # Convert to float, default to 0 if not present
            sales_tree.insert("", "end", text=sale["name"], values=(sale["quantity"], selling_price, sale["payment_method"], sale["timestamp"]))
            total_sales_quantity += sale["quantity"]
            total_sales_price += sale["quantity"] * selling_price

        # Label for total sold items
        total_sales_label = tk.Label(sales_tab, text=f"Total Sales Quantity: {total_sales_quantity}, Total Sales Price: Rwf{total_sales_price:.2f}", font=("Helvetica", 10))
        total_sales_label.pack(pady=(10, 0))

        # Add download button
        download_button = tk.Button(report_window, text="Download Report", command=lambda: self.download_report(purchases, sales))
        download_button.pack(pady=20)
        
    def Gross_profit(self):
        pass
    
        
        
        
        
    def monthly_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Monthly Report Application ")
       
        self.notebook = ttk.Notebook(self)
        self.igikoni_frame = ttk.Frame(self.notebook)
        self.services_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.igikoni_frame, text='igikoni')
        self.notebook.add(self.services_frame, text='Services')
        self.notebook.pack(pady=10, expand=True, fill='both')

        # Date selection widgets
        self.date_label = tk.Label(self, text="Select Date:")
        self.date_label.pack(pady=10)
        self.calendar = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=10)

        # Buttons for generating reports
        self.generate_report_button_igikoni = tk.Button(self.igikoni_frame, text="Generate Monthly Report", command=self.generate_monthly_report_igikoni)
        self.generate_report_button_igikoni.pack(pady=10)
        self.generate_report_button_services = tk.Button(self.services_frame, text="Generate Monthly Report", command=self.generate_monthly_report_services)
        self.generate_report_button_services.pack(pady=10)

    def generate_monthly_report_igikoni(self):
        pass

    def generate_monthly_report_services(self):
        pass
    def repair(self):
        pass
#.........................................End.. GROSS MARGIN.........................................
#.........................................TRANSFORER................................................
 # Create and configure widgets
    def trans(self):
        # Create a new Toplevel window for report options
        report_window = tk.Toplevel(self.root)
        report_window.title("Transforation Page  ")

        # Label for the report options
        label_report_options = tk.Label(report_window, text="transformer page", font=("Helvetica", 16, "bold"))
        label_report_options.pack(pady=10)

        # Frame to hold the report option buttons
        frame_buttons = tk.Frame(report_window)
        frame_buttons.pack(pady=20)

        # Buttons for different report options
        button_added_items = tk.Button(frame_buttons, text="Worker details", command=self.add_worker, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white")
        button_added_items.grid(row=0, column=0, padx=10, pady=5)

        button_sold_items = tk.Button(frame_buttons, text="Record Expense", command=self.record_expense, font=("Helvetica", 12), width=15, bg="#008CBA", fg="white")
        button_sold_items.grid(row=0, column=1, padx=10, pady=5)
        
        button_monthly_report = tk.Button(frame_buttons, text="Record Tax", command=self.record_tax, font=("Helvetica", 12), width=15, bg="#FFA500", fg="white")
        button_monthly_report.grid(row=1, column=0, padx=10, pady=5)



    def add_worker(self):
        # Create a popup window to add worker details
        popup = tk.Toplevel(self.root)
        popup.title("Add Worker")

        # Create input fields
        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Salary:").grid(row=1, column=0, padx=10, pady=5)
        salary_entry = tk.Entry(popup)
        salary_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="Working Days:").grid(row=2, column=0, padx=10, pady=5)
        working_days_entry = tk.Entry(popup)
        working_days_entry.grid(row=2, column=1, padx=10, pady=5)

        # Function to add worker to WorkersExpensesTax instance
        def add_worker_to_tax():
            name = name_entry.get()
            salary = float(salary_entry.get())
            working_days = int(working_days_entry.get())
            self.workers_expenses_tax.add_worker(name, salary, working_days)
            messagebox.showinfo("Worker Added", f"Worker {name} added successfully.")
            popup.destroy()

        # Button to add worker
        tk.Button(popup, text="Add Worker", command=add_worker_to_tax).grid(row=3, column=0, columnspan=2, pady=10)

    def record_expense(self):
        # Create a popup window to record expenses
        popup = tk.Toplevel(self.root)
        popup.title("Record Expense")

        # Create input fields
        tk.Label(popup, text="Expense:").grid(row=0, column=0, padx=10, pady=5)
        worker_name_entry = tk.Entry(popup)
        worker_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Expense Description:").grid(row=1, column=0, padx=10, pady=5)
        expense_desc_entry = tk.Entry(popup)
        expense_desc_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="Amount:").grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(popup)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

    def record_tax(self):
        pass

# ........................................End...TRANSFOR............................................       
    def view_action_log(self):
        messagebox.showinfo("View Action Log", "View Action Log functionality not implemented yet.")

    def logout(self):
        messagebox.showinfo("Logout", "Logging out.")
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

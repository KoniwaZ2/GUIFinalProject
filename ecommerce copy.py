import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection
db_conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="ecommerce"
)
cursor = db_conn.cursor()
print("Connected to database")


class EcommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ecommerce App")
        self.logged_in_customer_id = None

        self.tab_control = ttk.Notebook(root)
        self.register_tab = tk.Frame(self.tab_control)
        self.login_tab = tk.Frame(self.tab_control)
        self.product_tab = tk.Frame(self.tab_control)
        self.cart_tab = tk.Frame(self.tab_control)
        self.transaction_tab = tk.Frame(self.tab_control)

        self.tab_control.add(self.register_tab, text="Register")
        self.tab_control.add(self.login_tab, text="Login")
        self.tab_control.add(self.product_tab, text="Products")
        self.tab_control.add(self.cart_tab, text="Cart")
        self.tab_control.add(self.transaction_tab, text="Transactions")
        self.tab_control.pack(expand=1, fill="both")

        self.create_register_tab()
        self.create_login_tab()
        self.create_product_tab()
        self.create_cart_tab()
        self.create_transaction_tab()

    def create_register_tab(self):
        for widget in self.register_tab.winfo_children():
            widget.destroy()

        tk.Label(self.register_tab, text="Name:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.name_entry = tk.Entry(self.register_tab)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Phone Number:").grid(
            row=1, column=0, padx=10, pady=10
        )
        self.phone_entry = tk.Entry(self.register_tab)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Email:").grid(
            row=2, column=0, padx=10, pady=10
        )
        self.customer_email_entry = tk.Entry(self.register_tab)
        self.customer_email_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Password:").grid(
            row=3, column=0, padx=10, pady=10
        )
        self.password_entry = tk.Entry(self.register_tab, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Address:").grid(
            row=4, column=0, padx=10, pady=10
        )
        self.customer_address_entry = tk.Entry(self.register_tab)
        self.customer_address_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Button(self.register_tab, text="Register", command=self.register).grid(
            row=5, column=0, columnspan=2, pady=10
        )

    def create_login_tab(self):
        for widget in self.login_tab.winfo_children():
            widget.destroy()

        tk.Label(self.login_tab, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        self.login_email_entry = tk.Entry(self.login_tab)
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_tab, text="Password:").grid(
            row=1, column=0, padx=10, pady=10
        )
        self.login_password_entry = tk.Entry(self.login_tab, show="*")
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.login_tab, text="Login", command=self.login).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def create_product_tab(self):
        for widget in self.product_tab.winfo_children():
            widget.destroy()

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        for product in products:
            product_frame = tk.Frame(self.product_tab)
            product_frame.pack(pady=5)

            tk.Label(product_frame, text=f"Product ID: {product[0]}").grid(
                row=0, column=0, padx=10, sticky="w"
            )
            tk.Label(product_frame, text=f"Name: {product[1]}").grid(
                row=0, column=1, padx=10, sticky="w"
            )
            tk.Label(product_frame, text=f"Price: {product[3]}").grid(
                row=0, column=2, padx=10, sticky="w"
            )
            tk.Button(
                product_frame,
                text="Add to Cart",
                command=lambda p_id=product[0]: self.add_to_cart(p_id),
            ).grid(row=0, column=3, padx=10)

    def create_cart_tab(self):
        for widget in self.cart_tab.winfo_children():
            widget.destroy()

        tk.Label(self.cart_tab, text="Cart").pack(pady=10)

        if not self.logged_in_customer_id:
            tk.Label(self.cart_tab, text="Please log in to view your cart.").pack(
                pady=10
            )
            return

        cursor.execute(
            """
            SELECT 
                cd.cart_id, cd.product_code, p.product_name, (cd.quantity * cd.product_price)
            FROM 
                cartdetails cd
            JOIN 
                product p ON cd.product_code = p.product_code
            WHERE 
                cd.cart_id = %s
        """,
            (self.logged_in_customer_id,),
        )
        cart_items = cursor.fetchall()

        if not cart_items:
            tk.Label(self.cart_tab, text="Your cart is empty.").pack(pady=10)
            return

        for item in cart_items:
            item_frame = tk.Frame(self.cart_tab)
            item_frame.pack(pady=5)
            tk.Label(item_frame, text=f"Product ID: {item[1]}").grid(
                row=0, column=0, padx=10
            )
            tk.Label(item_frame, text=f"Product Name: {item[2]}").grid(
                row=0, column=1, padx=10
            )
            tk.Label(item_frame, text=f"Total Price: {item[3]}").grid(
                row=0, column=2, padx=10
            )
            tk.Button(
                item_frame,
                text="Remove",
                command=lambda p_id=item[1]: self.remove_from_cart(p_id),
            ).grid(row=0, column=3, padx=10)

    def create_transaction_tab(self):
        for widget in self.transaction_tab.winfo_children():
            widget.destroy()

        tk.Label(self.transaction_tab, text="Transaction History").pack(pady=10)

        if not self.logged_in_customer_id:
            tk.Label(
                self.transaction_tab, text="Please log in to view transactions."
            ).pack(pady=10)
            return

        cursor.execute(
            """
            SELECT transaction_id, order_date, total_amount
            FROM transactions
            WHERE customer_id = %s
            ORDER BY order_date DESC
        """,
            (self.logged_in_customer_id,),
        )
        transactions = cursor.fetchall()

        if not transactions:
            tk.Label(self.transaction_tab, text="No transactions found.").pack(pady=10)
            return

        for transaction in transactions:
            frame = tk.Frame(self.transaction_tab)
            frame.pack(pady=5)
            tk.Label(frame, text=f"Transaction ID: {transaction[0]}").pack(anchor="w")
            tk.Label(frame, text=f"Date: {transaction[1]}").pack(anchor="w")
            tk.Label(frame, text=f"Total Amount: {transaction[2]}").pack(anchor="w")

    def register(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.customer_email_entry.get()
        password = self.password_entry.get()
        address = self.customer_address_entry.get()

        if not all([name, phone, email, password, address]):
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute(
            "INSERT INTO customer (name, phone, email, password, address) VALUES (%s, %s, %s, %s, %s)",
            (name, phone, email, password, address),
        )
        db_conn.commit()
        messagebox.showinfo("Success", "Registration successful!")

    def login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        cursor.execute(
            "SELECT * FROM customer WHERE email=%s AND password=%s", (email, password)
        )
        user = cursor.fetchone()

        if user:
            self.logged_in_customer_id = user[0]
            messagebox.showinfo("Success", "Login successful!")
            self.create_cart_tab()
            self.create_transaction_tab()
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    def add_to_cart(self, product_id):
        if not self.logged_in_customer_id:
            messagebox.showerror("Error", "Please log in to add products to cart.")
            return

        cursor.execute(
            "SELECT product_price FROM product WHERE product_code=%s", (product_id,)
        )
        result = cursor.fetchone()
        if result:
            price = result[0]
            cursor.execute(
                "INSERT INTO cartdetails (customer_id, product_code, quantity, product_price) VALUES (%s, %s, %s, %s)",
                (self.logged_in_customer_id, product_id, 1, price),
            )
            db_conn.commit()
            messagebox.showinfo("Success", "Product added to cart!")
        else:
            messagebox.showerror("Error", "Product not found!")

    def remove_from_cart(self, product_id):
        if not self.logged_in_customer_id:
            messagebox.showerror("Error", "Please log in to remove items.")
            return

        cursor.execute(
            "DELETE FROM cartdetails WHERE customer_id=%s AND product_code=%s",
            (self.logged_in_customer_id, product_id),
        )
        db_conn.commit()
        messagebox.showinfo("Success", "Product removed from cart!")
        self.create_cart_tab()  # Refresh cart tab


if __name__ == "__main__":
    root = tk.Tk()
    app = EcommerceApp(root)
    root.mainloop()

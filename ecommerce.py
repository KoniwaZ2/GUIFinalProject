import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import time

db_conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="ecommerce"
)
print("Connected to database")
cursor = db_conn.cursor()


class EcommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ecommerce App")
        self.user_id = None

        self.tab_control = ttk.Notebook(root)

        self.register_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.register_tab, text="Register")

        self.login_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.login_tab, text="Login")

        self.tab_control.pack(expand=1, fill="both")

        self.create_register_tab()
        self.create_login_tab()

    def create_register_tab(self):  # completed
        tk.Label(self.register_tab, text="Name:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.name_entry = tk.Entry(self.register_tab)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Phone Number:").grid(
            row=2, column=0, padx=10, pady=10
        )
        self.phone_entry = tk.Entry(self.register_tab)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Email:").grid(
            row=4, column=0, padx=10, pady=10
        )
        self.customer_email_entry = tk.Entry(self.register_tab)
        self.customer_email_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Password :").grid(
            row=6, column=0, padx=10, pady=10
        )
        self.password_entry = tk.Entry(self.register_tab, show="*")
        self.password_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Label(self.register_tab, text="Address:").grid(
            row=8, column=0, padx=10, pady=10
        )
        self.customer_address_entry = tk.Entry(self.register_tab)
        self.customer_address_entry.grid(row=8, column=1, padx=10, pady=10)

        tk.Button(
            self.register_tab,
            text="Register",
            command=self.register,
        ).grid(row=10, column=0, columnspan=2, pady=10)

    def create_login_tab(self):  # completed
        tk.Label(self.login_tab, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        self.login_email_entry = tk.Entry(self.login_tab)
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_tab, text="Password:").grid(
            row=2, column=0, padx=10, pady=10
        )
        self.login_password_entry = tk.Entry(self.login_tab, show="*")
        self.login_password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(
            self.login_tab,
            text="Login",
            command=self.login,
        ).grid(row=4, column=0, columnspan=2, pady=10)

    def create_product_tab(self):  # completed
        for widget in self.product_tab.winfo_children():
            widget.destroy()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        for product in products:
            product_frame = tk.Frame(self.product_tab)
            product_frame.pack(pady=10)

            tk.Label(
                product_frame, text=f"Product ID: {product[0]}", anchor="w", width=20
            ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            tk.Label(
                product_frame, text=f"Name: {product[1]}", anchor="w", width=20
            ).grid(row=0, column=1, padx=10, pady=10, sticky="w")
            tk.Label(
                product_frame, text=f"Price: {product[3]}", anchor="w", width=20
            ).grid(row=0, column=2, padx=10, pady=10, sticky="w")
            tk.Button(
                product_frame,
                text="Add to Cart",
                command=lambda p_id=product[0], p_price=product[3]: self.add_to_cart(
                    p_id, p_price
                ),
            ).grid(row=0, column=3, padx=10, pady=10)

    def create_cart_tab(self):
        for widget in self.cart_tab.winfo_children():
            widget.destroy()

        tk.Label(self.cart_tab, text="Cart").pack(pady=10)

        if not self.user_id:
            tk.Label(self.cart_tab, text="Please log in to view your cart.").pack(
                pady=10
            )
            return

        cursor.execute(
            """SELECT 
            cd.cart_id, cd.product_code, p.product_name, cd.quantity, (cd.quantity * cd.product_price)
            FROM 
            cartdetails cd
            JOIN 
            product p ON cd.product_code = p.product_code
            JOIN 
            cart c ON cd.cart_id = c.cart_id
            WHERE 
            c.customer_id = %s""",
            (self.user_id,),
        )
        cart_items = cursor.fetchall()
        if not cart_items:
            tk.Label(self.cart_tab, text="Your cart is empty.").pack(pady=10)
            return

        for item in cart_items:
            item_frame = tk.Frame(self.cart_tab)
            item_frame.pack(pady=5)
            tk.Label(
                item_frame, text=f"Product ID: {item[1]}", anchor="w", width=20
            ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            tk.Label(
                item_frame, text=f"Product Name: {item[2]}", anchor="w", width=20
            ).grid(row=0, column=1, padx=10, pady=10, sticky="w")
            tk.Label(
                item_frame, text=f"Quantity: {item[3]}", anchor="w", width=20
            ).grid(row=0, column=3, padx=10, pady=10, sticky="w")
            tk.Label(
                item_frame, text=f"Total Price: {item[4]}", anchor="w", width=20
            ).grid(row=0, column=4, padx=10, pady=10, sticky="w")

            tk.Button(
                item_frame,
                text="Remove",
                command=lambda p_id=item[1]: self.remove_from_cart(p_id),
            ).grid(row=0, column=5, padx=10, pady=10, sticky="w")

        tk.Button(
            self.cart_tab,
            text="Checkout",
            command=lambda: self.checkout(cart_items),
        ).pack(pady=10)

    def create_transaction_tab(self):
        pass

    def login(self):  # completed
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        cursor.execute(
            "SELECT * FROM customer WHERE email=%s AND password=%s",
            (email, password),
        )
        user = cursor.fetchone()

        if user:
            self.user_id = user[0]
            self.user_name = user[1]
            messagebox.showinfo("Success", "Login successful")
            print("Login successful")
            self.login_email_entry.delete(0, tk.END)

            self.product_tab = tk.Frame(self.tab_control)
            self.tab_control.add(self.product_tab, text="Products")

            self.cart_tab = tk.Frame(self.tab_control)
            self.tab_control.add(self.cart_tab, text="Cart")

            self.transaction_tab = tk.Frame(self.tab_control)
            self.tab_control.add(self.transaction_tab, text="Transactions")

            self.tab_control.select(self.product_tab)

            self.tab_control.forget(self.register_tab)
            self.tab_control.forget(self.login_tab)

            self.create_product_tab()
            self.create_cart_tab()
            self.create_transaction_tab()
        else:
            print("Wrong email or password")
            messagebox.showerror("Error", "Wrong email or password")

    def register(self):  # completed
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.customer_email_entry.get()
        password = self.password_entry.get()
        address = self.customer_address_entry.get()

        cursor.execute(
            "INSERT INTO customer (customer_name, phone_number, email, password, address) VALUES (%s, %s, %s, %s, %s)",
            (name, phone, email, password, address),
        )
        db_conn.commit()

        messagebox.showinfo("Success", "Registration successful")
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.customer_email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.customer_address_entry.delete(0, tk.END)

    def add_to_cart(self, product_id, product_price):  # completed
        cursor.execute(
            """SELECT customer_id FROM cart where customer_id = %s""", (self.user_id,)
        )
        cart = cursor.fetchone()
        if not cart:
            cursor.execute(
                "INSERT INTO cart (customer_id) VALUES (%s)", (self.user_id,)
            )
            db_conn.commit()
            cursor.execute(
                """SELECT cart_id FROM cart where customer_id = %s""", (self.user_id,)
            )
            cart = cursor.fetchone()
            cart_id = cart[0]

            cursor.execute(
                """SELECT product_code, product_price FROM cartdetails where product_code = %s AND product_price = %s""",
                (product_id, product_price),
            )
            product = cursor.fetchone()
            if not product:
                cursor.execute(
                    """INSERT INTO cartdetails (cart_id, product_code, quantity, product_price) VALUES (%s, %s, %s, %s)""",
                    (cart_id, product_id, 1, product_price),
                )
                db_conn.commit()
                self.create_cart_tab()
                messagebox.showinfo("Success", "Product added to cart")
            else:
                cursor.execute(
                    """UPDATE cartdetails SET quantity = quantity + 1 WHERE product_code = %s AND cart_id = %s""",
                    (product_id, cart_id),
                )
                db_conn.commit()
                self.create_cart_tab()
                messagebox.showinfo("Success", "Product quantity updated in cart")
        else:
            cursor.execute(
                """SELECT cart_id FROM cart where customer_id = %s""", (self.user_id,)
            )
            cart = cursor.fetchone()
            cart_id = cart[0]
            self.cart_id = cart_id
            cursor.execute(
                """SELECT product_code, product_price FROM cartdetails where product_code = %s AND product_price = %s""",
                (product_id, product_price),
            )
            product = cursor.fetchone()
            if not product:
                cursor.execute(
                    """INSERT INTO cartdetails (cart_id, product_code, quantity, product_price) VALUES (%s, %s, %s, %s)""",
                    (cart_id, product_id, 1, product_price),
                )
                db_conn.commit()
                self.create_cart_tab()
                messagebox.showinfo("Success", "Product added to cart")
            else:
                cursor.execute(
                    """UPDATE cartdetails SET quantity = quantity + 1 WHERE product_code = %s AND cart_id = %s""",
                    (product_id, cart_id),
                )
                db_conn.commit()
                self.create_cart_tab()
                messagebox.showinfo("Success", "Product quantity updated in cart")

    def remove_from_cart(self, product_id):  # completed
        cursor.execute(
            """SELECT cart_id FROM cart where customer_id = %s""", (self.user_id,)
        )
        cart = cursor.fetchone()
        cart_id = cart[0]
        cursor.execute(
            "DELETE FROM cartdetails WHERE product_code = %s AND cart_id = %s",
            (product_id, cart_id),
        )
        db_conn.commit()
        self.create_cart_tab()
        self.create_product_tab()
        messagebox.showinfo("Success", "Product removed from cart")
        cursor.execute(
            """SELECT cd.cart_id FROM cartdetails cd JOIN cart c on cd.cart_id = c.cart_id WHERE c.customer_id = %s""",
            (self.user_id,),
        )
        cart = cursor.fetchone()
        if not cart:
            cursor.execute(
                """DELETE FROM cart where customer_id = %s""", (self.user_id,)
            )
            db_conn.commit()
            messagebox.showinfo("Success", "Cart is empty, cart deleted")
            self.create_cart_tab()
            self.create_product_tab()

    def checkout(self, cart_items):
        cursor.execute(
            """INSERT INTO transactions (customer_id, recipient_name, total_amount, order_status) VALUES (%s, %s, %s, "Pending")""",
            (
                self.user_id,
                self.user_name,
                sum(float(item[4]) for item in cart_items if item[4] is not None),
            ),
        )
        db_conn.commit()

        cursor.execute(
            """SELECT transaction_id FROM transactions WHERE customer_id = %s AND recipient_name = %s and order_status = "Pending" AND total_amount = %s""",
            (
                self.user_id,
                self.user_name,
                sum(item[4] for item in cart_items),
            ),
        )
        transaction = cursor.fetchone()
        transaction_id = transaction[0]
        print(cart_items)
        for item in cart_items:
            cursor.execute(
                """INSERT INTO transactiondetails (transaction_id, product_code, quantity, total) VALUES (%s, %s, %s, %s)""",
                (
                    transaction_id,
                    item[1],
                    item[3],
                    float(item[4]) if item[4] is not None else 0.0,
                ),
            )
            db_conn.commit()
        messagebox.showinfo("Success", "Checkout successful")
        self.create_cart_tab()
        self.create_transaction_tab()


if __name__ == "__main__":
    root = tk.Tk()
    app = EcommerceApp(root)
    root.mainloop()

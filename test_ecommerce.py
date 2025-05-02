import unittest
from unittest.mock import patch, MagicMock
from ecommerce import EcommerceApp


class TestEcommerceApp(unittest.TestCase):
    @patch("ecommerce.mysql.connector.connect")
    def setUp(self, mock_connect):
        # Mock database connection
        self.mock_db_conn = MagicMock()
        mock_connect.return_value = self.mock_db_conn
        self.mock_cursor = MagicMock()
        self.mock_db_conn.cursor.return_value = self.mock_cursor

        # Mock tkinter root
        self.mock_root = MagicMock()

        # Initialize the app
        self.app = EcommerceApp(self.mock_root)

    def test_register(self):
        # Set input values
        self.app.name_entry.get = MagicMock(return_value="John Doe")
        self.app.phone_entry.get = MagicMock(return_value="1234567890")
        self.app.customer_email_entry.get = MagicMock(return_value="john@example.com")
        self.app.password_entry.get = MagicMock(return_value="password123")
        self.app.customer_address_entry.get = MagicMock(return_value="123 Main St")

        # Call the register method
        self.app.register()

        # Check if the correct SQL query was executed
        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO customer (customer_name, phone_number, email, password, address) VALUES (%s, %s, %s, %s, %s)",
            (
                "John Doe",
                "1234567890",
                "john@example.com",
                "password123",
                "123 Main St",
            ),
        )
        self.mock_db_conn.commit.assert_called_once()

    def test_login_success(self):
        # Mock database response for successful login
        self.mock_cursor.fetchone.return_value = (1, "John Doe")

        # Set input values
        self.app.login_email_entry.get = MagicMock(return_value="john@example.com")
        self.app.login_password_entry.get = MagicMock(return_value="password123")

        # Call the login method
        self.app.login()

        # Check if the correct SQL query was executed
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM customer WHERE email=%s AND password=%s",
            ("john@example.com", "password123"),
        )
        self.assertEqual(self.app.user_id, 1)

    def test_login_failure(self):
        # Mock database response for failed login
        self.mock_cursor.fetchone.return_value = None

        # Set input values
        self.app.login_email_entry.get = MagicMock(return_value="wrong@example.com")
        self.app.login_password_entry.get = MagicMock(return_value="wrongpassword")

        # Call the login method
        self.app.login()

        # Check if the correct SQL query was executed
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM customer WHERE email=%s AND password=%s",
            ("wrong@example.com", "wrongpassword"),
        )
        self.assertIsNone(self.app.user_id)

    def test_add_to_cart_new_cart(self):
        # Mock database response for no existing cart
        self.mock_cursor.fetchone.side_effect = [None, (1,)]

        # Call the add_to_cart method
        self.app.user_id = 1
        self.app.add_to_cart(101, 20.0)

        # Check if the correct SQL queries were executed
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO cart (customer_id) VALUES (%s)", (1,)
        )
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO cartdetails (cart_id, product_code, quantity, product_price) VALUES (%s, %s, %s, %s)",
            (1, 101, 1, 20.0),
        )
        self.mock_db_conn.commit.assert_called()

    def test_remove_from_cart(self):
        # Mock database response for cart ID
        self.mock_cursor.fetchone.return_value = (1,)

        # Call the remove_from_cart method
        self.app.user_id = 1
        self.app.remove_from_cart(101)

        # Check if the correct SQL query was executed
        self.mock_cursor.execute.assert_called_with(
            "DELETE FROM cartdetails WHERE product_code = %s AND cart_id = %s",
            (101, 1),
        )
        self.mock_db_conn.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()

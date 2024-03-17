import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty

from pymongo import MongoClient, errors
from datetime import datetime, timedelta
import uuid

from receipt_generator import generate_fictional_receipts

# global variables for MongoDB host (default port is 27017)
DOMAIN = 'localhost:'
PORT = 27017

# Connect to MongoDB and target the 'ReceiptSys' database
try:
    client = MongoClient(host=[str(DOMAIN) + str(PORT)], serverSelectionTimeoutMS=3000)
    db = client['receiptsys']  # Specify the 'ReceiptSys' database
    print("server version:", client.server_info()["version"])
except errors.ServerSelectionTimeoutError as err:
    client = None
    db = None
    print("pymongo ERROR:", err)

class LoginScreen(Screen):
    def login(self, username, password):
        # Check if the username field is empty
        if not username:
            popup = Popup(title='Login Error',
                          content=Label(text='Username cannot be empty.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # Attempt to find the user in the database
        user = db['user_profiles'].find_one({"username": username})

        # Check if the user does not exist
        if not user:
            popup = Popup(title='Login Error',
                          content=Label(text='Username does not exist.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # Check if the password matches (assuming password checking logic is here)
        if user.get("password") == password:
            # Proceed with successful login logic...
            print(f"User {username} logged in successfully.")
            App.get_running_app().current_user = username  # Set the current user
            App.get_running_app().current_user_id = user["user_id"]  # Set the current user ID
            self.manager.current = 'main'  # Navigate to the main screen
        else:
            # Password does not match
            popup = Popup(title='Login Error',
                          content=Label(text='Incorrect password.'),
                          size_hint=(None, None), size=(400, 200))

class MainScreen(Screen):
    pass

class NewUser(Screen):
    price_sensitivity = None  # Default value; adjust as needed
 
    def create_user_profile(self, username, password, price_sensitivity):
        # This assumes that `self.price_sensitivity` holds the value from button selection
        price_sensitivity = self.price_sensitivity if hasattr(self, 'price_sensitivity') else 'Medium'  # Default to 'Medium' if not set

        # Generate a unique user ID
        user_id = str(uuid.uuid4())

        # Create or update the user profile with the provided information
        profile = {
            "user_id": user_id,
            "username": username,
            "password": password,  # Remember to hash passwords in a real application
            "preferences": {
                "price_sensitivity": price_sensitivity
            },
            "purchase_history": []
        }

        # Check if the user already exists to decide on create or update
        existing_user = db['user_profiles'].find_one({"username": username})
        if existing_user:
            popup_content = Label(text="User already exists. Please log in or use a different username.")
            popup = Popup(title="User already exists",
                          content=popup_content,
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return
        else:
            # Insert new user profile
            db['user_profiles'].insert_one(profile)
            print("Created new user profile.")

        self.manager.current = 'main'  # Redirect to main screen after creating profile

    def set_price_sensitivity(self, sensitivity):
        self.price_sensitivity = sensitivity
        print(f"Price sensitivity set to: {self.price_sensitivity}")  # For debugging

class NewRecpScreen(Screen):
    def add_purchase_to_history(self, user_id, receipt_data):
        # receipt_data should be a dict containing at least 'receipt_id' and 'date'
        db['user_profiles'].update_one(
            {"user_id": user_id},
            {"$push": {"purchase_history": receipt_data}})
        print("Purchase added to history.")

    def generate_and_insert_receipts(self, user_id):
        if not user_id:
            popup_content = Label(text="No user is currently logged in. Please log in to generate receipts.")
            popup = Popup(title="User Not Logged In",
                          content=popup_content,
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return
        
        receipts = generate_fictional_receipts(user_id, 10)  # Generate 10 receipts
        for receipt in receipts:
            db['receipts'].insert_one(receipt)
        print("Receipts generated and inserted into the database.")

class ViewRecpScreen(Screen):
        # def on_pre_enter(self, *args):
        #     # Assuming user_id is accessible as a global or passed around
        #     user_id = self.get_user_id()
        #     receipts = App.get_user_receipts(user_id)
        #     user_profile = db['user_profiles'].find_one({"user_id": user_id})
        #     if user_profile:
        #         self.ids.receipts_list.data  = [
        #         {'text': f"Receipt {idx + 1}", 'on_release': lambda idx=idx: self.open_receipt_popup(receipts[idx])}
        #         for idx in range(len(receipts))
        #     ]
        #     else:
        #         print("User profile not found.")
        
        def open_receipt_popup(self, receipt):
            # content = BoxLayout(orientation='vertical')
            # for item in receipt['items']:
            #     content.add_widget(Label(text=f"{item['name']}: ${item['price']}"))
            # content.add_widget(Button(text="Delete", on_release=lambda x: self.delete_receipt(receipt)))
            # popup = Popup(title='Receipt Details', content=content, size_hint=(None, None), size=(400, 400))
            # popup.open()

            # Create and configure the popup content dynamically
            content = self.manager.get_screen('your_dynamic_popup_screen_name')  # Adjust with your actual dynamic class/screen name
            content.ids.receipt_items.clear_widgets()  # Clear previous items
            for item in receipt['items']:
                # Dynamically add items to the popup
                content.ids.receipt_items.add_widget(ReceiptItem(text=f"{item['name']}: ${item['price']}"))
            content.ids.delete_button.bind(on_release=lambda x: self.delete_receipt(receipt))  # Assuming 'delete_button' is an id in your KV
            popup = Popup(title='Receipt Details', content=content, size_hint=(None, None), size=(400, 400))
            popup.open()

        def delete_receipt(self, receipt):
            # Assuming receipt is a dictionary with a unique ID
            db['receipts'].delete_one({"receipt_id": receipt["receipt_id"]})
            print("Receipt deleted.")

            # Close the popup
            self.on_pre_enter()  # Refresh the view

class CreBasketScreen(Screen):
    def find_lowest_prices_for_basket(self, basket_items, days_back=None):
        receipts = db['receipts']
        results = {}
        
        for item in basket_items:
            results[item] = {}
            query = {"items.name": item}
            if days_back is not None:
                start_date = datetime.now() - timedelta(days=days_back)
                query["purchase_date"] = {"$gte": start_date}


            pipeline = [
                {"$match": query},
                {"$unwind": "$items"},
                {"$match": {"items.name": item}},
                {"$group": {"_id": "$items.name", "lowest_price": {"$min": "$items.price"}}}
            ]
            lowest_price = list(receipts.aggregate(pipeline))
            if lowest_price:
                # Assuming lowest_price contains at least one result
                results[item] = lowest_price[0]['lowest_price']
            else:
                results[item] = "No data"

        return results

    
    def check_prices(self, selected_days, *args):
        # Define a list of valid values for comparison
        valid_values = ['1 day', '7 days', '14 days', '30 days', 'All time']

        # Check if the selected value is in the list of valid values
        if selected_days not in valid_values:
            popup = Popup(title='Invalid Selection',
            content=Label(text='Please select a valid number of days.'),
            size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # Assuming selected_days and basket_items are passed correctly from the UI
        basket_items = args[0] if args else []
        days_back = None if selected_days == "All time" else int(selected_days.split()[0])

        if basket_items:
            prices = self.find_lowest_prices_for_basket(basket_items, days_back)

            # Proceed to display these prices on a new screen
            display_text = '\n'.join([f"{item}: {price_info}" for item, price_info in prices.items()])
            App.get_running_app().price_check_results = display_text

            # Navigate to the PriceResultsScreen
            self.manager.current = 'price_results'
        else:
            print("No items in the basket to check.")

class PriceResultsScreen(Screen):
    def on_enter(self, *args):
        # Display the results
        self.ids.results_label.text = App.get_running_app().price_check_results

class WindowManager(ScreenManager):
    pass

class ReceiptItem(Label):
    pass

class MyBasketApp(App):
    current_user = None  # Global variable to keep track of the current user
    current_user_id = None  # Global variable to keep track of the current user's ID
    price_check_results = StringProperty("")  # Property to hold the price check results

    def build(self):
        self.title = 'My Basket App'
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(NewUser(name='new_user'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(NewRecpScreen(name='new_receipt'))
        sm.add_widget(ViewRecpScreen(name='view_receipts'))
        sm.add_widget(CreBasketScreen(name='create_basket'))
        sm.add_widget(PriceResultsScreen(name='price_results'))

        # Decide on the initial screen
        initial_screen = 'login' if not self.check_user_session() else 'main'
        sm.current = initial_screen
        return sm
    
    def check_user_session(self):
        return True if self.current_user else False

    def get_user_id(self):
        """Getter method for the current user's ID."""
        return self.current_user_id
    
    def get_user_receipts(user_id):
        # Get all receipts for the user
        receipts = db['receipts'].find({"user_id": user_id})
        return list(receipts)
    
if __name__ == '__main__':
    MyBasketApp().run()
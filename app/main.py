import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty

from pymongo import MongoClient, errors
from datetime import datetime, timedelta

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
        user = db['user_profiles'].find_one({"user_id": username})
        if user and user.get("password") == password:
            # Assuming you have a way to keep track of the current user
            global current_user
            current_user = username
            print(f"User {username} logged in successfully.")
            self.manager.current = 'main'  # Redirect to main screen after login
        else:
            print("Failed to log in. Incorrect username or password.")

class MainScreen(Screen):
    pass

class NewUser(Screen):
    price_sensitivity = None  # Default value; adjust as needed
 
    def create_user_profile(self, username, favorite_categories, password):
        # This assumes that `self.price_sensitivity` holds the value from button selection
        price_sensitivity = self.price_sensitivity if hasattr(self, 'price_sensitivity') else 'Medium'  # Default to 'Medium' if not set

        # Create or update the user profile with the provided information
        profile = {
            "user_id": username,
            "password": password,  # Remember to hash passwords in a real application
            "preferences": {
                "favorite_categories": favorite_categories.split(', '),  # Assuming categories are comma-separated
                "price_sensitivity": price_sensitivity
            },
            "purchase_history": []
        }

        # Check if the user already exists to decide on create or update
        existing_user = db['user_profiles'].find_one({"user_id": username})
        if existing_user:
            # Update existing user profile
            db['user_profiles'].update_one({"user_id": username}, {"$set": profile})
            print("Updated user profile.")
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

class ViewRecpScreen(Screen):
    def on_pre_enter(self, *args):
        # Assuming user_id is accessible as a global or passed around
        user_id = "some_user_id"
        user_profile = db['user_profiles'].find_one({"user_id": user_id})
        if user_profile:
            purchase_history = user_profile.get("purchase_history", [])
            # Now, you would update the UI with this purchase history
            # For simplicity, let's just print it
            print(purchase_history)
        else:
            print("User profile not found.")

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

class ViewBasketScreen(Screen):
    pass

class PriceResultsScreen(Screen):
    def on_enter(self, *args):
        # Display the results
        self.ids.results_label.text = App.get_running_app().price_check_results

class WindowManager(ScreenManager):
    pass

class MyBasketApp(App):
    current_user = None  # Global variable to keep track of the current user
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
        sm.add_widget(ViewBasketScreen(name='view_baskets'))
        sm.add_widget(PriceResultsScreen(name='price_results'))

        # Decide on the initial screen
        initial_screen = 'login' if not self.check_user_session() else 'main'
        sm.current = initial_screen
        return sm
    
    def check_user_session(self):
        return True if self.current_user else False


    
if __name__ == '__main__':
    MyBasketApp().run()
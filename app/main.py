import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty

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

    def create_user_profile(self, user_id, favorite_categories, price_sensitivity, password):
        profile = {
            "user_id": user_id,
            "password": password,  # Store the password (use hashing in a real app)
            "preferences": {
                "favorite_categories": favorite_categories.split(', '),
                "price_sensitivity": price_sensitivity
            },
            "purchase_history": []
        }
        db['user_profiles'].insert_one(profile)
        print("Profile created with login credentials")


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
    def find_lowest_prices_for_basket(self, basket_items):
        receipts = db['receipts']
        
        time_frames = [1, 7, 14, 30]
        results = {}

        for item in basket_items:
            results[item] = {}
            for days in time_frames:
                start_date = datetime.now() - timedelta(days=days)
                pipeline = [
                    {"$match": {"items.name": item, "purchase_date": {"$gte": start_date}}},
                    {"$unwind": "$items"},
                    {"$match": {"items.name": item}},
                    {"$group": {"_id": "$items.name", "lowest_price": {"$min": "$items.price"}}}
                ]
                lowest_price = list(receipts.aggregate(pipeline))
                if lowest_price:
                    results[item][f'{days} days'] = lowest_price[0]['lowest_price']
                else:
                    results[item][f'{days} days'] = "No data"
        return results
    
    def check_prices(self, selected_days, *args):
        # Extract item names from args (which is a list containing another list)
        basket_items = args[0] if args else []

        # Convert selected_days to an integer
        days_back = int(selected_days.split()[0])  # Extract the number of days from the string

        if basket_items:
            prices = self.find_lowest_prices_for_basket(basket_items, days_back)
            print(prices)  # Placeholder for demonstrating results in the console
        else:
            print("No items in the basket to check.")  # Handle the case of an empty basket

class ViewBasketScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyBasketApp(App):
    current_user = None  # Global variable to keep track of the current user

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

        # Decide on the initial screen
        initial_screen = 'login' if not self.check_user_session() else 'main'
        sm.current = initial_screen
        return sm
    
    def check_user_session(self):
        return True if self.current_user else False


    
if __name__ == '__main__':
    MyBasketApp().run()
import kivy
kivy.require('2.3.0')

# Standard library imports
from bson.objectid import ObjectId

# Third party imports
from kivy.app import App
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import logging

# Local application imports
from backend.database.mongo_db import DatabaseOperations

# Set the logging level for pymongo to WARNING
logging.getLogger('pymongo').setLevel(logging.WARNING)
Logger.setLevel(logging.INFO)

# Connect to MongoDB and target the 'ReceiptSys' database
database = DatabaseOperations(db_name='receiptsys')

class LoginScreen(Screen):
    def login(self, username, password):
        # Check if username is empty
        if not username:
            App.get_running_app().show_error_popup('Error', 'Username cannot be empty.')
            return

        user = database.find_one('user_profiles', {'username': username})

        # Check if the user exists
        if not user:
            App.get_running_app().show_error_popup('Error', 'Username does not exist.')
            return

        # Check if the password is correct
        if user.get("password") != password:
            App.get_running_app().show_error_popup('Error', 'Incorrect password.')
            return
        
        else:
            # Set the current user and user ID
            App.get_running_app().current_user = username
            App.get_running_app().current_user_id = user.get('_id')
            # Redirect to the main screen
            self.manager.current = 'main'          

class MainScreen(Screen):
    pass

class NewUser(Screen):
    price_sensitivity = None

    def create_user_profile(self, username, password, price_sensitivity):
        # This assumes that 'self.price_sensitivity' holds the value from button selection
        price_sensitivity = self.price_sensitivity if hasattr(self, 'price_sensitivity') and self.price_sensitivity is not None else 'Medium'  # Default to 'Medium' if not set

        # Create or update the user profile with the provided information
        profile = {
            "username": username,
            "password": password,  # Remember to hash passwords in a real application
            "preferences": {
                "price_sensitivity": price_sensitivity
            },
            "purchase_history": []
        }

        # Check if the user already exists to decide on create or update
        existing_user = database.find_one('user_profiles', {'username': username})
        if existing_user:
            App.get_running_app().show_error_popup('User already exists', 
                                                   'Please log in or use a different username.')
            return
        else:
            # Insert new user profile
            database.insert_one('user_profiles', profile)
            print("Created new user profile.")

        self.manager.current = 'login'  # Redirect to main screen after creating profile

    def set_price_sensitivity(self, sensitivity):
        self.price_sensitivity = sensitivity
        print(f"Price sensitivity set to: {self.price_sensitivity}")  # For debugging

class NewRecpScreen(Screen):
    pass

class ViewRecpScreen(Screen):
    pass

class CreBasketScreen(Screen):
    user_location = ObjectProperty(None)  # Store user's location as a property
    user_location = (62.73877287906317, 7.1406954451815)  # Placeholder for user's location

    def check_prices(self, selected_days, basket_items):
        if not self.validate_days(selected_days):
            return
        
        days_back = None if selected_days == "All time" else int(selected_days.split()[0])

        user_id = App.get_running_app().current_user_id
        user_profile = database.find_one('user_profiles', {'_id': user_id})
        price_sensitivity = user_profile['preferences']['price_sensitivity']

        # Fetch the lowest prices for the basket items
        prices = database.find_lowest_prices_for_basket(basket_items, days_back)
        # Fetch store distances
        store_distances = database.fetch_store_distances(self.user_location, prices)
        # If no store with prices is found, show an error popup
        if not store_distances:
            App.get_running_app().show_error_popup('Error', 'No store found.')
            return
        # Calculate store scores
        rec_store, rec_score, detail_scores, avg_scores = database.calculate_store_scores(prices, store_distances, price_sensitivity)

        self.display_price_results(rec_store, rec_score, detail_scores, avg_scores)

    # Validate the selected number of days
    def validate_days(self, selected_days):
        valid_values = ['1 day', '7 days', '14 days', '30 days', 'All time']
        if selected_days not in valid_values:
            App.get_running_app().show_error_popup('Invalid Selection', 'Please select a valid number of days.')
            return False
        return True

    # Display the price check results
    def display_price_results(self, recommended_store, recommended_score, detailed_scores, average_scores):
        recommended_texts = [f"Recommended Store: {recommended_store.title()} (Best Average Score, {recommended_score:.2f})"]
        display_texts = []
        # Display the recommended store and its details
        for store, item in detailed_scores.items():
            display_texts.append(f"Store: {store.title()} \n  Average Score: {average_scores[store]:.1f}")
            keys = list(item.keys())
            display_texts.append(f"    Distance: {item[keys[0]][0]['distance']: .1f}km")
            for item, details in item.items():
                for detail in details:
                    display_texts.append(f"    Item: {item.title()}, Price: {detail['price']:.1f}kr, Score: {detail['score']:.2f}")
            display_texts.append("")  # Add a blank line between stores

        # Store these details for later use in the GUI
        App.get_running_app().price_check_results = str(recommended_texts[0])
        App.get_running_app().detailed_store_info = "\n".join(display_texts)
        self.manager.current = 'price_results'
    
class PriceResultsScreen(Screen):
    # Display the recommended store and detailed store information
    def show_all_stores(self):
        detailed_info = App.get_running_app().detailed_store_info
        self.ids.results_label.text = detailed_info
    
    # Display only the recommended store
    def refresh_store(self):
        recommended_store = App.get_running_app().price_check_results
        self.ids.results_label.text = recommended_store

class ViewProfileScreen(Screen):
    # Fetch the user's price sensitivity from the database
    # on_pre_enter is used to ensure the data is fetched before the screen is entered
    def on_pre_enter(self):
        user_id = App.get_running_app().current_user_id
        user_profile = database.find_one('user_profiles', {'_id': user_id})
        if user_profile:
            self.price_sensitivity = user_profile['preferences']['price_sensitivity']
        else:
            print("User profile not found.")
    
    # Display the user's username and price sensitivity
    # on_enter is used to ensure the data is displayed when the screen is entered
    def on_enter(self):
        self.ids.username_label.text = f"Username: {App.get_running_app().get_username()}"
        self.ids.price_sensitivity_label.text = f"Price Sensitivity: {self.price_sensitivity}"

class ChangePriceSensScreen(Screen):
    # Initialize the price sensitivity property
    def set_price_sensitivity(self, sensitivity):
        self.price_sensitivity = sensitivity
        print(f"Price sensitivity set to: {self.price_sensitivity}")
    
    # Save the updated price sensitivity to the database
    def save_price_sensitivity(self):
        user_id = App.get_running_app().current_user_id
        database.update_one('user_profiles', 
                            {'_id': user_id}, 
                            {'preferences.price_sensitivity': self.price_sensitivity}
                            )
        print("Price sensitivity updated.")
        self.manager.current = 'view_profile'
class WindowManager(ScreenManager):
    pass

class MyBasketApp(App):
    current_user = None  # Global variable to keep track of the current user
    current_user_id = None  # Global variable to keep track of the current user's ID
    price_check_results = StringProperty("")  # Property to hold the price check results
    detailed_store_info = ObjectProperty(None)  # Property to hold detailed store information

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
        sm.add_widget(ViewProfileScreen(name='view_profile'))
        sm.add_widget(ChangePriceSensScreen(name='change_price_sensitivity'))

        # Decide on the initial screen
        initial_screen = 'login' if not self.check_user_session() else 'main'
        sm.current = initial_screen
        return sm

    # Check if a user is logged in
    def check_user_session(self):
        return True if self.current_user else False

    # Get the current user's ID
    def get_user_id(self):
        return self.current_user_id
    
    # Get the current user's username
    def get_username(self):
        user_profile = database.find_one('user_profiles', {'_id': ObjectId(self.current_user_id)})
        if user_profile:
            return user_profile['username']
        return "Unknown"
    
    # Get the current user's price sensitivity
    def get_price_sensitivity(self):
        user_profile = database.find_one('user_profiles', {'_id': ObjectId(self.current_user_id)})
        if user_profile and 'preferences' in user_profile:
            return user_profile['preferences'].get('price_sensitivity', 'Not Set')
        return "Not Set"
    
    def show_error_popup(self, title, message):
        popup = Popup(title=title, 
                      content=Label(text=message), 
                      size_hint=(None, None), 
                      size=(400, 200))
        popup.open()

    def logout(self):
        print(f"User {self.current_user} logged out.")
        login = self.root.get_screen('login')
        login.ids.login_username.text = ''
        login.ids.login_password.text = ''
        self.current_user = None
        self.current_user_id = None
        self.root.current = 'login'

if __name__ == '__main__':
    MyBasketApp().run()
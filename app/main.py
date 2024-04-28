import kivy
kivy.require('2.3.0')

# Standard library imports
from bson.objectid import ObjectId
from collections import defaultdict
from datetime import datetime, timedelta
import re

# Third party imports
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

# Local application imports
from backend.database.mongo_db import DatabaseOperations

# Connect to MongoDB and target the 'ReceiptSys' database
database = DatabaseOperations(db_name='receiptsys')

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
        user = database.db['user_profiles'].find_one({"username": username})

        # Check if the user does not exist
        if not user:
            popup = Popup(title='Login Error',
                          content=Label(text='Username does not exist.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # Check if the password matches
        if user.get("password") == password:
            print(f"User {username} logged in successfully.")
            App.get_running_app().current_user = username  # Set the current user
            App.get_running_app().current_user_id = user["_id"]  # Set the current user ID
            print(f"Current user ID: {App.get_running_app().current_user_id}")
            self.manager.current = 'main'  # Navigate to the main screen
        else:
            popup = Popup(title='Login Error',
                          content=Label(text='Incorrect password.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            

class MainScreen(Screen):
    pass

class NewUser(Screen):
    price_sensitivity = None  # Default value; adjust as needed

    def create_user_profile(self, username, password, price_sensitivity):
        # This assumes that `self.price_sensitivity` holds the value from button selection
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
        existing_user = database.db['user_profiles'].find_one({"username": username})
        if existing_user:
            popup_content = Label(text="User already exists. Please log in or use a different username.")
            popup = Popup(title="User already exists",
                          content=popup_content,
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return
        else:
            # Insert new user profile
            database.db['user_profiles'].insert_one(profile)
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
    user_location = (62.7333432951364, 7.14822177402025)  # Placeholder for user's location

    def check_prices(self, selected_days, basket_items):
        if not self.validate_days(selected_days):
            return

        days_back = None if selected_days == "All time" else int(selected_days.split()[0])
        user_id = App.get_running_app().current_user_id
        user_profile = database.db['user_profiles'].find_one({'_id': user_id})
        price_sensitivity = user_profile['preferences']['price_sensitivity']

        prices = self.find_lowest_prices_for_basket(basket_items, days_back)
        print(prices)
        store_distances = self.fetch_store_distances(prices)
        rec_store, rec_score, detail_scores, avg_scores = self.calculate_store_scores(prices, store_distances, price_sensitivity)

        self.display_price_results(rec_store, rec_score, detail_scores, avg_scores)

    def validate_days(self, selected_days):
        valid_values = ['1 day', '7 days', '14 days', '30 days', 'All time']
        if selected_days not in valid_values:
            self.show_popup('Invalid Selection', 'Please select a valid number of days.')
            return False
        return True

    def find_lowest_prices_for_basket(self, basket_items, days_back=None):
        # groceries = db['groceries']
        results = []
        for item in basket_items:
            if not item.strip():
                continue
            results.append(self.query_grocery_prices(item.upper(), days_back))
        return results

    def query_grocery_prices(self, item_name, days_back):
        groceries = database.db['groceries']
        start_date = datetime.now() - timedelta(days=days_back) if days_back else None
        query = {"name": item_name, "price_history.date": {"$gte": start_date}} if start_date else {"name": item_name}
        pipeline = [
            {'$match': query},
            {'$unwind': '$price_history'},
            {'$sort': {'price_history.store': 1, 'price_history.date': -1}},
            {'$group': {
                '_id': '$price_history.store',
                'latestDate': {'$first': '$price_history.date'},
                'minPrice': {'$min': '$price_history.price'},
                'itemName': {'$first': '$name'}
            }},
            {'$group': {
                '_id': '$itemName',
                'stores': {'$push': {'store': '$_id', 'date': '$latestDate', 'price': '$minPrice'}}
            }}
        ]
        result = list(groceries.aggregate(pipeline))
        return result[0] if result else {'_id': item_name, 'stores': []}

    def fetch_store_distances(self, prices):
        involved_stores = {store['store'].lower() for price_info in prices for store in price_info['stores']}

        # Prepare an $or query with case-insensitive regex matches for each store
        regex_query = [{'name': re.compile(f'^{re.escape(store)}$', re.IGNORECASE)} for store in involved_stores]
        temp_data = database.db['stores'].find({'$or': regex_query})
        store_data = {store['name'].lower(): store for store in temp_data}

        # Calculate distances using names directly from store_data
        distances = {}
        for store_name, store_info in store_data.items():
            if 'location' in store_info and 'coordinates' in store_info['location']:
                store_location = store_info['location']['coordinates']
                distances[store_name] = self.calculate_distance(self.user_location, store_location)
            else:
                print(f"Location data missing for store: {store_name}")
                distances[store_name] = None  # or handle as needed

        return distances

    def calculate_store_scores(self, prices, distances, price_sensitivity):
        # Log the distances to verify their availability
        print("Distances available:", distances)

        # Sensitivity weights as defined
        sensitivity_weights = {'High':      {'price': 0.7, 'distance': 0.3},
                               'Medium':    {'price': 0.5, 'distance': 0.5},
                               'Low':       {'price': 0.3, 'distance': 0.7}
                               }
        weight = sensitivity_weights[price_sensitivity]

        # Store scores by store name and details, we introduce defaultdict to avoid key errors
        store_scores = defaultdict(list)
        detailed_scores = defaultdict(dict)

        # Iterate over each item and their respective stores
        for item in prices:
            for store in item['stores']:
                store_name = store['store'].lower()
                store_price = store['price']

                # Retrieve the distance for the current store, using float('inf') if not available
                store_distance = distances.get(store_name, float('inf'))

                # Calculate the score using both price and distance, taking into account the weight based on price sensitivity
                score = (weight['price'] * store_price) + (weight['distance'] * store_distance)
                store_scores[store_name].append(score)

                # Append a dictionary with all store details plus the calculated score
                if item['_id'] not in detailed_scores[store_name]:
                    detailed_scores[store_name][item['_id']] = []
                detailed_scores[store_name][item['_id']].append({
                    'price': store_price,
                    'distance': store_distance,
                    'score': score
                })

        # Calculate average scores
        average_scores = {store: sum(scores) / len(scores) for store, scores in store_scores.items()}

        # Find the store with the lowest average score
        recommended_store = min(average_scores, key=average_scores.get)
        recommended_score = average_scores[recommended_store]

        return recommended_store, recommended_score, detailed_scores, average_scores


    def display_price_results(self, recommended_store, recommended_score, detailed_scores, average_scores):
        recommended_texts = [f"Recommended Store: {recommended_store.title()} (Best Average Score, {recommended_score:.2f})"]
        display_texts = []
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

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    # https://www.geeksforgeeks.org/program-distance-two-points-earth/

    def calculate_distance(self, user_location, store_location):
        from math import radians, cos, sin, sqrt, atan2

        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = map(radians, user_location)
        lat2, lon2 = map(radians, store_location)

        # Difference in coordinates
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Earth's radius in kilometers
        R = 6371.0

        # Calculate the distance
        distance = R * c
        return distance
    
class PriceResultsScreen(Screen):
    def show_all_stores(self):
        detailed_info = App.get_running_app().detailed_store_info
        print(detailed_info)

        self.ids.results_label.text = detailed_info
    
    def refresh_store(self):
        recommended_store = App.get_running_app().price_check_results
        self.ids.results_label.text = recommended_store

class ViewProfileScreen(Screen):
    def get_price_sensitivity(self):
        return self.price_sensitivity
    
    def on_pre_enter(self):
        user_id = App.get_running_app().current_user_id
        user_profile = database.db['user_profiles'].find_one({'_id': user_id})
        if user_profile:
            self.price_sensitivity = user_profile['preferences']['price_sensitivity']
        else:
            print("User profile not found.")
    
    def on_enter(self):
        self.ids.username_label.text = f"Username: {App.get_running_app().get_username()}"
        self.ids.price_sensitivity_label.text = f"Price Sensitivity: {self.price_sensitivity}"

class ChangePriceSensScreen(Screen):
    def set_price_sensitivity(self, sensitivity):
        self.price_sensitivity = sensitivity
        print(f"Price sensitivity set to: {self.price_sensitivity}")

    def get_price_sensitivity(self):
        return self.price_sensitivity
    
    def save_price_sensitivity(self):
        user_id = App.get_running_app().current_user_id
        price_sensitivity = self.get_price_sensitivity()
        database.db['user_profiles'].update_one(
            {'_id': user_id},
            {'$set': {'preferences.price_sensitivity': price_sensitivity}}
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

    # def on_start(self):
    #     gps.configure(on_location=self.on_gps_location)
    #     gps.start()

    # def on_gps_location(self, **kwargs):
    #     kwargs['lat'], kwargs['lon']
    #     print(f"Latitude: {kwargs['lat']}, Longitude: {kwargs['lon']}")


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

    def check_user_session(self):
        return True if self.current_user else False

    def get_user_id(self):
        return self.current_user_id

    def get_user_receipts(user_id):
        # Get all receipts for the user
        receipts = database.db['receipts'].find({"user_id": user_id})
        return list(receipts)
    
    def get_username(self):
        user_profile = database.db['user_profiles'].find_one({'_id': ObjectId(self.current_user_id)})
        if user_profile:
            return user_profile['username']
        return "Unknown"
    
    def get_price_sensitivity(self):
        user_profile = database.db['user_profiles'].find_one({'_id': ObjectId(self.current_user_id)})
        if user_profile and 'preferences' in user_profile:
            return user_profile['preferences'].get('price_sensitivity', 'Not Set')
        return "Not Set"

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
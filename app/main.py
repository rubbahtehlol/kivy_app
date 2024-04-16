import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty

from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from collections import defaultdict
import re
# from plyer import gps

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
            App.get_running_app().current_user_id = user["_id"]  # Set the current user ID
            print(f"Current user ID: {App.get_running_app().current_user_id}")
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

        self.manager.current = 'login'  # Redirect to main screen after creating profile

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
    user_location = ObjectProperty(None)  # Store user's location as a property
    user_location = (62.738904078963586, 7.140731219084178)  # Placeholder for user's location

    def check_prices(self, selected_days, basket_items):
        if not self.validate_days(selected_days):
            return
        
        days_back = None if selected_days == "All time" else int(selected_days.split()[0])
        user_id = App.get_running_app().current_user_id
        user_profile = db['user_profiles'].find_one({'_id': user_id})
        price_sensitivity = user_profile['preferences']['price_sensitivity']
        
        prices = self.find_lowest_prices_for_basket(basket_items, days_back)
        print(prices)
        store_distances = self.fetch_store_distances(prices)
        rec_store, rec_score, detail_scores = self.calculate_store_scores(prices, store_distances, price_sensitivity)
        
        self.display_price_results(rec_store, detail_scores)

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
        groceries = db['groceries']
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
        temp_data = db['stores'].find({'$or': regex_query})
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

        print("Store scores:", store_scores)
        print("Detailed scores:", detailed_scores)

        # Calculate average scores
        average_scores = {store: sum(scores) / len(scores) for store, scores in store_scores.items()}

        # Find the store with the lowest average score
        recommended_store = min(average_scores, key=average_scores.get)
        recommended_score = average_scores[recommended_store]

        return recommended_store, recommended_score, detailed_scores

        # # Sort the stores based on the score in ascending order (lower is better)
        # scored_stores.sort(key=lambda x: x['score'])
        # return scored_stores


    def display_price_results(self, recommended_store, detailed_scores):
        display_texts = [f"Recommended Store: {recommended_store.title()} (Best Average Score)"]
        for store, item in detailed_scores.items():
            display_texts.append(f"Store: {store.title()}")
            for item, details in item.items():
                for detail in details:
                    display_texts.append(f"  Item: {item.title()}, Price: {detail['price']:.1f}kr, Distance: {detail['distance']:.1f} km, Score: {detail['score']:.2f}")


        print(display_texts)

        # Store these details for later use in the GUI
        App.get_running_app().price_check_results = "\n".join(display_texts)
        App.get_running_app().detailed_store_info = detailed_scores
        self.manager.current = 'price_results'


        # print("Average scores:", average_scores)
        # display_text = (f"Recommended Store: {recommended_store}\n"
        #                 f"Average Score: {recommended_score:.1f}\n\n"
        #                 "Scores by Store:\n" +
        #                 "\n".join(f"{store}: {score:.1f}" for store, score in average_scores.items()))

        # # Set the result text for the application and switch screens
        # App.get_running_app().price_check_results = display_text
        # self.manager.current = 'price_results'

    # def display_price_results(self, scored_stores):

    #     display_texts = [
    #         f"Item: {store['item']}, Store: {store['store']}, Price: {store['price']}kr, Distance: {store['distance']:.1f} km, Score: {store['score']:.1f}"
    #         for store in scored_stores
    #     ]
    #     App.get_running_app().price_check_results = "\n".join(display_texts)
    #     self.manager.current = 'price_results'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def calculate_distance(self, user_location, store_location):
        from math import radians, cos, sin, sqrt, atan2
        # Earth's radius in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = map(radians, user_location)
        lat2, lon2 = map(radians, store_location)

        # Difference in coordinates
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Calculate the distance
        distance = R * c
        return distance


class PriceResultsScreen(Screen):
    def show_all_stores(self):
        detailed_info = App.get_running_app().detailed_store_info
        # Convert detailed_info to a string or update a widget to display it
        all_stores_text = self.format_all_stores(detailed_info)
        self.ids.results_label.text = all_stores_text

    def format_all_stores(self, detailed_info):
        texts = []
        for store, items in detailed_info.items():
            texts.append(f"Store: {store}")
            for item, details in items.items():
                for detail in details:
                    texts.append(f"  Item: {item}, Price: {detail['price']}kr, Distance: {detail['distance']:.1f} km, Score: {detail['score']:.1f}")
        return "\n".join(texts)


class WindowManager(ScreenManager):
    pass

class ReceiptItem(Label):
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
    
    def logout(self):
        print(f"User {self.current_user} logged out.")
        self.current_user = None
        self.current_user_id = None
        self.root.current = 'login'
    
if __name__ == '__main__':
    MyBasketApp().run()
import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty

from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from plyer import gps

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

    def find_store_recommendations(self, user_id, basket_items, selected_days):
        # Convert days to integer or None for 'All time'
        days_back = None if selected_days == "All time" else int(selected_days.split()[0])
        
        # Fetch lowest prices
        prices = self.find_lowest_prices_for_basket(basket_items, days_back)

        # Fetch user's location
        user_location = [7.157794939293244, 62.73654532445558]  # This should ideally come from the GPS module

        # Fetch distance data for each store involved
        involved_stores = set(store['store'] for price_info in prices for store in price_info['stores'])
        store_data = {store['_id']: store for store in db['receiptsys']['stores'].find({'_id': {'$in': list(involved_stores)}})}
        distances = {store: self.calculate_distance(user_location, store_data[store]['location']['coordinates']) for store in involved_stores}

        # Fetch user's price sensitivity
        user_profile = db['user_profiles'].find_one({'_id': user_id})
        price_sensitivity = user_profile['preferences']['price_sensitivity']

        # Calculate scores
        scored_stores = calculate_store_scores(prices, distances, price_sensitivity)

        # Format for display
        display_texts = [
            f"Item: {store['item']}, Store: {store['store']}, Price: {store['price']}, Distance: {store['distance']:.2f} meters, Score: {store['score']:.2f}"
            for store in scored_stores
        ]
        App.get_running_app().price_check_results = "\n".join(display_texts)
        self.manager.current = 'price_results'



    def find_lowest_prices_for_basket(self, basket_items, days_back=None):
        groceries = db['groceries']
        results = []
        
        if days_back is not None:
            start_date = datetime.now() - timedelta(days=days_back)

        for item in basket_items:
            if item == '':
                continue

            query = {"name": item.upper()}
            query["price_history.date"] = {"$gte": start_date}


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
                            'stores': {
                                '$push': {
                                    'store': '$_id',
                                    'date': '$latestDate',
                                    'price': '$minPrice'
                                }
                            }
                        }}
            ]

            # Execute the aggregation query
            result = list(groceries.aggregate(pipeline))

            if result:
                # Assuming lowest_price contains at least one result
                results.append(result[0])
            else:
                results.append({'_id': item.title(), 'stores': None})
        
        print(results)
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
        print(basket_items)
        days_back = None if selected_days == "All time" else int(selected_days.split()[0])

        if basket_items:
            results = self.find_lowest_prices_for_basket(basket_items, days_back)
            display_texts = []

            for prices in results:
                item_name = prices['_id']
                stores = prices['stores']

                if stores is None:
                    display_text = f"{item_name}: No data available"
                    display_texts.append(display_text)
                    continue
            
                # Sort stores by price (ascending), then by date (descending)
                sorted_stores = sorted(stores, key=lambda x: (x['price'], -datetime.strptime(x['date'], '%d.%m.%Y %H:%M').timestamp()))

                # Get the store with the lowest price and newest date
                if sorted_stores:
                    cheapest_newest_store = sorted_stores[0]  # Last item after sorting
                    display_text = f"{item_name.title()}: {cheapest_newest_store['price']}kr at {cheapest_newest_store['store'].title()} (Newest: {cheapest_newest_store['date']})"
                    display_texts.append(display_text)

                # Join the display texts for all items
                final_display_text = '\n'.join(display_texts)

            print(final_display_text)
            # Proceed to display these prices on a new screen
            # display_text = '\n'.join([f"{item}: {price_info}" for item, price_info in prices.items()])
            App.get_running_app().price_check_results = final_display_text

            # Navigate to the PriceResultsScreen
            self.manager.current = 'price_results'
        
        else:
            print("No items in the basket to check.")


    def fetch_nearest_stores(db, user_location, max_distance=5000):
        """
        Fetches stores from MongoDB within a specified maximum distance from the user's location.
        
        Args:
        db (MongoClient): The database connection.
        user_location (list): The longitude and latitude of the user's current location.
        max_distance (int): Maximum distance in meters from the user's location to consider (default 5000 meters).
        
        Returns:
        list: A list of documents representing the nearest stores.
        """
        stores = db['receiptsys']['stores']
        # Ensure the collection has a 2dsphere index on the 'location' field
        stores.create_index([("location", "2dsphere")])

        # Geospatial query to find nearest stores
        query = {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": user_location},
                "distanceField": "distance",
                "maxDistance": max_distance,
                "spherical": True
            }
        }

        results = stores.aggregate([query])
        return list(results)

    # Example usage:
    # db = MongoClient().your_database_name
    # user_location = [7.157794939293244, 62.73654532445558]  # Longitude first, then latitude
    # nearest_stores = fetch_nearest_stores(db, user_location)
    # for store in nearest_stores:
    #     print(store)

def calculate_store_scores(prices, distances, price_sensitivity):
    """
    Calculate a combined score for stores based on prices and distances with respect to price sensitivity.

    Args:
    prices (list): List of dictionaries containing price data and store names.
    distances (dict): Dictionary mapping store names to distances.
    price_sensitivity (str): User's price sensitivity ('High', 'Medium', 'Low').

    Returns:
    list: Adjusted list of stores with scores based on price sensitivity.
    """
    # Define sensitivity weights (tune these based on further analysis or user feedback)
    sensitivity_weights = {
        'High': {'price': 0.7, 'distance': 0.3},
        'Medium': {'price': 0.5, 'distance': 0.5},
        'Low': {'price': 0.3, 'distance': 0.7}
    }
    
    weight = sensitivity_weights[price_sensitivity]
    scored_stores = []

    for item in prices:
        item_name = item['_id']
        for store in item['stores']:
            store_name = store['store']
            store_price = store['price']
            store_distance = distances.get(store_name, float('inf'))  # Default to inf if no distance is known

            # Calculate score
            score = (weight['price'] * store_price) + (weight['distance'] * store_distance)
            scored_stores.append({
                'item': item_name,
                'store': store_name,
                'price': store_price,
                'distance': store_distance,
                'score': score
            })

    # Sort stores by score for each item
    scored_stores.sort(key=lambda x: x['score'])
    return scored_stores

# Example usage:
# prices = [{'_id': 'APPELSINJUICE PREMIUM', 'stores': [{'store': 'KIWI LANGMYRVEIEN', 'price': 22.8}, {'store': 'BUNNPRIS & GOURMET FUGLSET', 'price': 36.9}]}]
# distances = {'KIWI LANGMYRVEIEN': 1200, 'BUNNPRIS & GOURMET FUGLSET': 2000}
# price_sensitivity = 'High'
# store_scores = calculate_store_scores(prices, distances, price_sensitivity)
# print(store_scores)



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
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
import re
from collections import defaultdict

class DatabaseOperations:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='receiptsys'):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            self.db = self.client[db_name]
            print("Connected to MongoDB:", self.client.server_info()["version"])
        except errors.ServerSelectionTimeoutError as err:
            print("Failed to connect to MongoDB:", err)
            self.db = None

    def insert_one(self, collection, data):
        try:
            self.db[collection].insert_one(data)
            return True
        except errors.PyMongoError as err:
            print("Failed to insert data:", err)
            return False
    
    def insert_many(self, collection, data):
        try:
            self.db[collection].insert_many(data)
            return True
        except errors.PyMongoError as err:
            print("Failed to insert data:", err)
            return False
        
    def find_one(self, collection, query):
        return self.db[collection].find_one(query)
    
    def find_many(self, collection, query):
        return self.db[collection].find(query)
    
    def update_one(self, collection, query, data):
        try:
            self.db[collection].update_one(query, {"$set": data})
            return True
        except errors.PyMongoError as err:
            print("Failed to update data:", err)
            return False
    
    def find_lowest_prices_for_basket(self, basket_items, days_back=None):
        results = []
        for item in basket_items:
            if not item.strip():
                continue
            results.append(self.query_grocery_prices(item.upper(), days_back))
        return results
    
    def query_grocery_prices(self, item_name, days_back):
        groceries = self.db['groceries']

        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%d.%m.%Y %H:%M") if days_back else None
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
    
    def fetch_store_distances(self, user_location, prices):
        involved_stores = {store['store'].lower() for price_info in prices for store in price_info['stores']}

        if not involved_stores:
            return None

        # Prepare an $or query with case-insensitive regex matches for each store
        regex_query = [{'name': re.compile(f'^{re.escape(store)}$', re.IGNORECASE)} for store in involved_stores]
        temp_data = self.db['stores'].find({'$or': regex_query})
        store_data = {store['name'].lower(): store for store in temp_data}

        # Calculate distances using names directly from store_data
        distances = {}
        for store_name, store_info in store_data.items():
            if 'location' in store_info and 'coordinates' in store_info['location']:
                store_location = store_info['location']['coordinates']
                distances[store_name] = self.calculate_distance(user_location, store_location)
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
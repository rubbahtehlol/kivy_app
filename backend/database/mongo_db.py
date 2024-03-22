from pymongo import MongoClient, errors
from datetime import datetime, timedelta

class DatabaseOperations:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='receiptsys'):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            self.db = self.client[db_name]
            print("Connected to MongoDB:", self.client.server_info()["version"])
        except errors.ServerSelectionTimeoutError as err:
            print("Failed to connect to MongoDB:", err)
            self.db = None

    def login_user(self, username, password):
        user = self.db['user_profiles'].find_one({"user_id": username})
        return user if user and user.get("password") == password else None

    def create_user_profile(self, user_id, favorite_categories, price_sensitivity, password):
        profile = {
            "user_id": user_id,
            "password": password,  # Remember to hash in a real app
            "preferences": {
                "favorite_categories": favorite_categories,
                "price_sensitivity": price_sensitivity
            },
            "purchase_history": []
        }
        return self.db['user_profiles'].insert_one(profile).inserted_id

    def find_lowest_prices_for_basket(self, basket_items):
        receipts = self.db['receipts']
        
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
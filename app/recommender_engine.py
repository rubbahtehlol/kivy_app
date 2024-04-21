from geopy.distance import great_circle
from backend.database.mongo_db import DatabaseOperations

# Placeholder for database connection
db = DatabaseOperations()

def fetch_stores_with_any_items(item_ids, user_location):
    """
    Fetch stores that carry any of the items in the user's basket.
    :param item_ids: List of item IDs in the user's basket.
    :param user_location: User's current location as (latitude, longitude).
    :return: List of stores with details including total cost and distance.
    """
    stores = db['stores'].find({
        "items.groceryId": {"$in": item_ids}
    })

    store_details = []
    for store in stores:
        store_distance = great_circle(user_location, store['location']['coordinates']).miles
        basket_cost = sum(item['price'] for item in store['items'] if item['groceryId'] in item_ids)
        num_items = sum(1 for item in store['items'] if item['groceryId'] in item_ids)

        store_details.append({
            'store_id': store['_id'],
            'name': store['name'],
            'num_items': num_items,
            'total_cost': basket_cost,
            'distance': store_distance
        })
    
    return store_details

def recommend_stores(basket, user_location):
    """
    Recommend stores based on the user's basket and location.
    Highlight the closest and the cheapest store if it's different.
    :param basket: List of item IDs in the user's basket.
    :param user_location: User's current location as (latitude, longitude).
    :return: List of store recommendations with highlights.
    """
    item_ids = [item['id'] for item in basket]  # Assuming each item in the basket has an 'id' key
    stores = fetch_stores_with_any_items(item_ids, user_location)

    if not stores:
        return "No stores found with the items in your basket."

    # Sort stores by distance to find the closest
    closest_store = min(stores, key=lambda x: x['distance'])
    
    # Sort stores by total cost to find the cheapest
    cheapest_store = min(stores, key=lambda x: x['total_cost'])

    recommendations = []
    for store in stores:
        store_info = f"{store['name']}: {store['num_items']} items, total {store['total_cost']}kr, {store['distance']}km"
        if store['store_id'] == closest_store['store_id']:
            store_info += " (Closest)"
        if store['store_id'] == cheapest_store['store_id'] and closest_store['store_id'] != cheapest_store['store_id']:
            store_info += " (Cheapest)"
        recommendations.append(store_info)
    
    return recommendations

# Example usage
if __name__ == "__main__":
    user_basket = [{'id': 'item1'}, {'id': 'item2'}]  # Example basket
    user_location = (62.7388, 7.1409)  # Example location (Molde, Norway)
    
    recommendations = recommend_stores(user_basket, user_location)
    for rec in recommendations:
        print(rec)

from pymongo import MongoClient
from datetime import datetime

# Establish a connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access the 'receiptsys' database and 'receipts' collection
db = client['receiptsys']

groceries = db.db['groceries']

# 
receipts_collection = db['receipts']

# Access or create the 'groceries' collection
groceries_collection = db['groceries']

receipts = receipts_collection.find()

# Iterate through each receipt in the 'receipts' collection
for receipt in receipts:
    # store_name = get_store_name(receipt)

    store_name = receipt['store']['name']
    receipt_date = receipt['created_at']

    # Iterate through each item in the 'items' array of the receipt
    for item in receipt['items']:
        item_name = item['name']
        brand = item.get('brand', None)  # 'brand' may not always be present

        # Build the new or updated item document
        new_item = {
            "name": item_name,
            # "current_price": item['price'],
            # "original_price": item['price_original'],
            "size": item['size'],
            "unit": item['unit'],
            "price_history": [
                {
                    "price": item['price'],
                    "store": store_name,
                    "date": receipt_date
                }
            ],
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "updated_at": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        # If 'brand' exists, add it to the document
        if brand:
            new_item["brand"] = brand

        # Check if the item already exists in the 'groceries' collection
        existing_item = groceries_collection.find_one({"name": item_name, "brand": brand})
        if existing_item:
            # Update the existing item with the new price and append to price history
            groceries_collection.update_one(
                {"_id": existing_item['_id']},
                {
                    "$set": {"current_price": item['price'], "updated_at": datetime.now().strftime("%d.%m.%Y %H:%M")},
                    "$push": {"price_history": new_item['price_history'][0]}
                }
            )
        else:
            # Insert the new item into the 'groceries' collection
            groceries_collection.insert_one(new_item)

import random
from datetime import datetime, timedelta

def generate_fictional_receipts(user_id, count=5):
    # Sample data remains the same
    item_names = ["Milk", "Bread", "Eggs", "Cheese", "Apples", "Bananas", "Coffee", "Tea"]
    stores = ["Store A", "Store B", "Store C"]
    receipts = []

    for _ in range(count):
        items_purchased = random.sample(item_names, k=random.randint(1, 5))
        items = [{"name": item, "price": round(random.uniform(1, 10), 2)} for item in items_purchased]
        total_price = sum(item["price"] for item in items)
        purchase_date = datetime.now() - timedelta(days=random.randint(1, 30))

        receipt = {
            "user_id": user_id,
            "items": items,
            "total_price": round(total_price, 2),
            "store": random.choice(stores),
            "purchase_date": purchase_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        receipts.append(receipt)

    return receipts

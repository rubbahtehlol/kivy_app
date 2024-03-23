from backend.database.mongo_db import DatabaseOperations
from datetime import datetime

db = DatabaseOperations()


# Create a collection of receipts
receipts = db.db['receipts']


receipt_1 = {
    "user_id": "unique_user_identifier",
    "store": {
      "name": "KIWI LANGMYRVEIEN",
      "code": "KIWI"
  },
    "items": [
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "HANSA MANGO IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "HANSA MANGO IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "FRYDENLUND JUICY IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "FRYDENLUND JUICY IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "FRYDENLUND FATøL",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 33.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "FRYDENLUND FATøL",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 33.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "AVOCADO 2PK MODEN SEASO",
        "size": "2",
        "unit": "PK",
        "quantity": 1,
        "price": 29.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "PAPRIKA RØD FILMET",
        "size": "214",
        "unit": "gram",
        "quantity": 1,
        "price": 14.94,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "AGURK STK",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 24.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "NACHIPS CRUNCHY",
        "size": "185",
        "unit": "gram",
        "quantity": 1,
        "price": 18.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      {
        "receipt_id": "<ObjectId>",
        "item_id": "<ObjectId>",
        "name": "KARBONADEDEIG",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 81.50,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      }
    ],
    "total": 409.56,
    "total_discount": "unknown",
    "created_at": "01.03.24 15:30",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M")
  }
  

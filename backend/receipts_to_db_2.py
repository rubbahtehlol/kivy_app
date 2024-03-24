from backend.database.mongo_db import DatabaseOperations
from datetime import datetime

db = DatabaseOperations()


receipts = db.db['receipts']

receipt_2149 = {
    "_id": "2149",
    "user_id": "user_1",
    "created_at": "06.02.2024 08:52",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0007",
        "name": "KIWI LANGMYRVEIEN",
        "code": "KIWI"
  },
    "items": [
        { "name": "MILO TØYVASK",
          "size": "595",
          "unit": "milliliter",
          "quantity": 1,
          "price": 56.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "RISGRØT",
          "brand": "FJORDLAND",
          "size": "970",
          "unit": "gram",
          "quantity": 2,
          "price": 16.80,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "TØRKERULL",
          "size": "4",
          "unit": "RULL",
          "quantity": 1,
          "price": 42.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "FROKOSTEGG FRITTGÅENDE",
          "size": "12",
          "unit": "STK",
          "quantity": 1,
          "price": 42.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "LETTRØMME",
          "size": "300",
          "unit": "gram",
          "quantity": 1,
          "price": 19.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "KARBONADEDEIG",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 81.50,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "TORTILLA ORIGINAL LARGE",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 27.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "PAPRIKA RØD",
          "size": "194",
          "unit": "gram",
          "quantity": 1,
          "price": 13.17,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "CRISPISALAT",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 24.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MANGO TØRKET",
          "size": "60",
          "unit": "gram",
          "quantity": 1,
          "price": 22.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "AVOCADO 2PK MODEN SEASON",
          "size": "2",
          "unit": "PK",
          "quantity": 1,
          "price": 39.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "AGURK",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 24.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "LIME",
          "size": "78",
          "unit": "gram",
          "quantity": 1,
          "price": 5.45,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MELKESJOKOLADE KVIKKLUNSJ",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 24.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }

    ],
    "total": 465.47,
    "total_discount": None
  }

receipt_2150 = {
    "_id": "2150",
    "user_id": "user_2",
    "created_at": "04.12.23 12:52",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0008",
        "name": "EUROSPAR MOLDE",
        "code": "EUROSPAR"
    },
    "items": [
        { "name": "RULLEKEBAB DØNER MIX",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 69.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 69.90,
    "total_discount": None
}

from backend.database.mongo_db import DatabaseOperations
from datetime import datetime

db = DatabaseOperations()

receipts = db.db['receipts']


receipt_2136 = {
    "_id": "2136",
    "user_id": "user_1",
    "created_at": "01.03.2024 15:30",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0007",
        "name": "KIWI LANGMYRVEIEN",
        "code": "KIWI"
  },
    "items": [
      { "name": "HANSA MANGO IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 2,
        "price": 79.80,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FRYDENLUND JUICY IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 2,
        "price": 79.80,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FRYDENLUND FATøL",
        "size": "0.5",
        "unit": "liter",
        "quantity": 2,
        "price": 67.80,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "AVOCADO 2PK MODEN SEASON",
        "size": "2",
        "unit": "PK",
        "quantity": 1,
        "price": 29.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "PAPRIKA RØD",
        "size": "214",
        "unit": "gram",
        "quantity": 1,
        "price": 14.94,
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
      { "name": "NACHIPS CRUNCHY",
        "size": "185",
        "unit": "gram",
        "quantity": 1,
        "price": 18.90,
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
      }
    ],
    "total": 409.56,
    "total_discount": None
  }
  
receipt_2137 = {
    "_id": "2137",
    "user_id": "user_2",
    "created_at": "29.02.2024 17:04",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0004",
        "name": "COOP MEGA MOLDELIVEIEN",
        "code": "COOP"
  },
    "items": [
      { "name": "CROISSANT NATURELL",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 20.50,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "KARBONEDEDEIG",
        "brand": "GILDE",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 98.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "SPAGETTI SAUS",
        "brand": "TORO",
        "size": "52,5",
        "unit": "gram",
        "quantity": 1,
        "price": 19.50,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      }, 
      { "name": "Farris/Bris/Frus Mix",
        "size": "1.5",
        "unit": "liter",
        "quantity": 3,
        "price": 43.80,
        "discount": None,
        "discounted_price": 21.90,
        "price_original": 65.70
      }
      
    ],
    "total": 191.70,
    "total_discount": 21.90
  }

receipt_2138 = {
    "_id": "2138",
    "user_id": "user_3",
    "created_at": "15.02.2024 17:54",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0023",
        "name": "BUNNPRIS & GOURMET FUGLSET",
        "code": "BUNNPRIS"
  },
    "items": [
      { "name": "FRENCH FRIES SALT",
        "size": "90",
        "unit": "gram",
        "quantity": 1,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FARRIS NATURELL",
        "size": "1.5",
        "unit": "liter",
        "quantity": 1,
        "price": 19.50,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "POTETBALL",
        "size": "LITEN",
        "unit": "STK",
        "quantity": 1,
        "price": 135.00,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "POTETBALL",
        "size": "MEDUIM",
        "unit": "STK",
        "quantity": 1,
        "price": 149.00,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "KIWI",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 9.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "PÆRER",
        "size": "184",
        "unit": "gram",
        "quantity": 1,
        "price": 6.79,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      }
    ],
    "total": 375.99,
    "total_discount": None
  }

receipt_2139 = {
    "_id": "2139",
    "user_id": "user_1",
    "created_at": "16.02.2024 18:30",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0007",
        "name": "KIWI LANGMYRVEIEN",
        "code": "KIWI"
  },
    "items": [
      { "name": "APPELSINJUICE PREMIUM",
        "size": "1",
        "unit": "liter",
        "quantity": 1,
        "price": 22.80,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "BANANER",
        "size": "876",
        "unit": "gram",
        "quantity": 1,
        "price": 20.06,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FINISH GLANS LEMON",
        "size": "400",
        "unit": "milliliter",
        "quantity": 1,
        "price": 45.40,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FRYDENLUND FATØL",
        "size": "0.5",
        "unit": "liter",
        "quantity": 0,
        "price": 33.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FRYDENLUND JUICY IPA",
        "size": "0.5",
        "unit": "liter",
        "quantity": 1,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "TACO SAUCE HOT",
        "size": "230",
        "unit": "gram",
        "quantity": 1,
        "price": 19.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "AVOCADO STK SEASON",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 33.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "TORTILLA ORIGINAL LARGE",
        "size": "1",
        "unit": "PK",
        "quantity": 1,
        "price": 22.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "MAISKORN",
        "size": "160",
        "unit": "gram",
        "quantity": 3,
        "price": 39.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "NORVEGIA",
        "size": "500",
        "unit": "gram",
        "quantity": 1,
        "price": 66.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "KARBONADEDEIG",
        "size": "GILDE",
        "unit": "STK",
        "quantity": 1,
        "price": 81.50,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "FROKOSTEGG FRITTGAENDE",
        "size": "12",
        "unit": "STK",
        "quantity": 1,
        "price": 42.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "NACHIPS CRUNCHY",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 11.30,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "TACO SPICE MIX",
        "brand": "ST.MARIA",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 4.10,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      },
      { "name": "CRISPISALAT",
        "size": "",
        "unit": "STK",
        "quantity": 1,
        "price": 32.90,
        "discount": None,
        "discounted_price": None,
        "price_original": None
      }
    ],
    "total": 522.26,
    "total_discount": None
  }

receipt_2140 = {
    "_id": "2140",
    "user_id": "user_2",
    "created_at": "06.02.2024 08:52",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0004",
        "name": "COOP MEGA MOLDELIVEIEN",
        "code": "COOP"
  },
    "items": [
        { "name": "MONSTER PIPELINE PUNCH",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 26.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 28.90,
    "total_discount": None
  }

receipt_2141 = {
    "_id": "2141",
    "user_id": "user_3",
    "created_at": "06.02.2024 16:10",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": None,
        "name": "MENY SOLSIDEN",
        "code": "MENY"
  },
    "items": [
        { "name": "MONSTER ENERGY",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 30.80,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 32.80,
    "total_discount": None
  }

receipt_2142 = {
    "_id": "2142",
    "user_id": "user_1",
    "created_at": "20.02.2024 11:02",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0004",
        "name": "COOP MEGA MOLDELIVEIEN",
        "code": "COOP"
  },
    "items": [
        { "name": "LION",
          "size": "2",
          "unit": "STK",
          "quantity": 1,
          "price": 17.50,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MONSTER ENERGY",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 22.50,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MONSTER PIPELINE PUNCH",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 26.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 71.00,
    "total_discount": None
  }

receipt_2143 = {
    "_id": "2143",
    "user_id": "user_2",
    "created_at": "07.02.2024 15:31",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
      "id": "0023",
      "name": "BUNNPRIS & GOURMET FUGLSET",
      "code": "BUNNPRIS"
  },
    "items": [
        { "name": "MANGO",
          "size": "300",
          "unit": "gram",
          "quantity": 1,
          "price": 29.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "SMOOTHIE MIX JØRD/BRING/BAN",
          "size": "400",
          "unit": "gram",
          "quantity": 1,
          "price": 30.00,
          "discount": None,
          "discounted_price": 9.90,
          "price_original": 39.90
        },
        { "name": "SMOOTHIE MIX ANANAS/MANGO/PAP",
          "size": "",
          "unit": "",
          "quantity": 1,
          "price": 31.50,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "BANANER",
          "size": "508",
          "unit": "gram",
          "quantity": 1,
          "price": 9.92,
          "discount": None,
          "discounted_price": 4.25,
          "price_original": 14.17
        },
        { "name": "FISKEBURGER 86% TORSK&HYSE",
          "size": "500",
          "unit": "gram",
          "quantity": 1,
          "price": 87.50,
          "discount": None,
          "discounted_price": 37.50,
          "price_original": 125.00
        },
        { "name": "APPELSINJUICE PREMIUM",
          "brand": "SUNNIVA",
          "size": "1",
          "unit": "liter",
          "quantity": 1,
          "price": 36.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }, 
        { "name": "NORVEGIA",
          "size": "500",
          "unit": "gram",
          "quantity": 1,
          "price": 77.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "FROKOSTYOGHURT VANILJE",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 37.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "PRIME ICE POP",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 14.90,
          "discount": None,
          "discounted_price": 22.00,
          "price_original": 36.90
        },
        { "name": "MØLLERS OMEGA-3",
          "size": "160",
          "unit": "STK",
          "quantity": 1,
          "price": 97.30,
          "discount": None,
          "discounted_price": 41.70,
          "price_original": 139.00
        },
        { "name": "GROVE FROKOSTBRØD",
          "size": "",
          "unit": "STK",
          "quantity": 3,
          "price": 25.00,
          "discount": None,
          "discounted_price": 13.70,
          "price_original": 38.70
        },
        { "name": "",
          "size": "",
          "unit": "",
          "quantity": 1,
          "price": 0.00,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "",
          "size": "",
          "unit": "",
          "quantity": 1,
          "price": 0.00,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 485.22,
    "total_discount": 129.05
  }

receipt_2144 = {
    "_id": "2144",
    "user_id": "user_3",
    "created_at": "20.01.2024 17:48",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0008",
      "name": "EUROSPAR MOLDE",
      "code": "EUROSPAR"
  },
    "items": [
        { "name": "FARRIS BRIS SITRON",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 22.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "SMÅGODT",
          "size": "665",
          "unit": "gram",
          "quantity": 1,
          "price": 63.44,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 88.34,
    "total_discount": None
  }

receipt_2145 = {
    "_id": "2145",
    "user_id": "user_1",
    "created_at": "30.01.2024 14:06",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0008",
      "name": "EUROSPAR MOLDE",
      "code": "EUROSPAR"
  },
    "items": [
        { "name": "OMO COLOR FLYTENDE",
          "size": "595",
          "unit": "milliliter",
          "quantity": 1,
          "price": 34.74,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MANGO TØRKET",
          "size": "60",
          "unit": "gram",
          "quantity": 1,
          "price": 25.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 60.64,
    "total_discount": None
  }

receipt_2146 = {
    "_id": "2146",
    "user_id": "user_2",
    "created_at": "06.12.2023 15:44",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0004",
      "name": "COOP MEGA MOLDELIVEIEN",
      "code": "COOP"
  },
    "items": [
        { "name": "DAGENS GRYTERETT",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 46.49,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "GOD GAMMELDAGS SURKÅL",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 19.50,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "KIMS PEPPER PUNCH",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 33.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "SKRUF NO10 SUPSLIMS",
          "size": "",
          "unit": "",
          "quantity": 2,
          "price": 175.80,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "GROVT SPELTBRØD",
          "brand": "COOP SMAK",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 34.90,
          "discount": 25.6,
          "discounted_price": 12.00,
          "price_original": 46.90
        },
        { "name": "STEKT RIBBE",
          "size": "0.5",
          "unit": "liter",
          "quantity": 1,
          "price": 99.10,
          "discount": 16.74,
          "discounted_price": 19.90,
          "price_original": 119.00
        }
    ],
    "total": 413.94,
    "total_discount": None
  }

receipt_2147 = {
    "_id": "2147",
    "user_id": "user_3",
    "created_at": "22.12.2023 18:44",
    "uploaded_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "store": {
        "id": "0007",
      "name": "KIWI LANGMYRVEIEN",
      "code": "KIWI"
  },
    "items" : [
        { "name": "TOALETTPAPIR SOFT",
          "size": "8",
          "unit": "RULL",
          "quantity": 1,
          "price": 46.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MAISKORN",
          "size": "198",
          "unit": "gram",
          "quantity": 3,
          "price": 26.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "FRYDENLUND JUICY IPA",
          "size": "0.5",
          "unit": "liter",
          "quantity": 6,
          "price": 233.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "TACO SAUCE HOT",
          "size": "230",
          "unit": "gram",
          "quantity": 1,
          "price": 19.20,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "FRYDENLUND FATØL",
          "size": "0.5",
          "unit": "liter",
          "quantity": 6,
          "price": 197.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "APPELSINJUICE PREMIUM",
          "size": "1",
          "unit": "liter",
          "quantity": 1,
          "price": 23.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "KREMFLØTE",
          "size": "7.5",
          "unit": "deciliter",
          "quantity": 1,
          "price": 34.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "HVETEMEL SIKTET",
          "size": "1",
          "unit": "KG",
          "quantity": 1,
          "price": 14.40,
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
        { "name": "GOURMETSTYKKER",
          "brand": "HATTING",
          "size": "",
          "unit": "PK",
          "quantity": 1,
          "price": 44.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "FLØTEMYSOST SKIVET",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 20.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "PIZZA GRANDIOSA",
          "size": "",
          "unit": "",
          "quantity": 1,
          "price": 59.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "ALWAYS ULTRASECURE NIGHT",
          "size": "",
          "unit": "PK",
          "quantity": 1,
          "price": 38.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "NORVEGIA",
          "size": "500",
          "unit": "gram",
          "quantity": 1,
          "price": 66.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "METERISMØR",
          "brand": "TINE",
          "size": "500",
          "unit": "gram",
          "quantity": 1,
          "price": 0,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "HÅNDSÅPE",
          "brand": "LANO",
          "size": "300",
          "unit": "milliliter",
          "quantity": 1,
          "price": 23.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "LIBRESSE NORMAL",
          "size": "14",
          "unit": "STK",
          "quantity": 1,
          "price": 25.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "APETINA SNACK",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 20.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "POTETSALAT KLASSISK",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 23.70,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "KARBONADEDEIG",
          "size": "",
          "unit": "STK",
          "quantity": 2,
          "price": 163.00,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "ROASTBIFF",
          "size": "",
          "unit": "PK",
          "quantity": 1,
          "price": 35.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "STRANDASKINKE",
          "size": "",
          "unit": "PK",
          "quantity": 1,
          "price": 69.80,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "STRANDASKINKE RENSKÅRET",
          "size": "",
          "unit": "PK",
          "quantity": 1,
          "price": 39.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "NACHIPS CRUNCHY",
          "size": "185",
          "unit": "gram",
          "quantity": 1,
          "price": 26.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "RUNDSTYKKER GROVE",
          "size": "",
          "unit": "PK",
          "quantity": 1,
          "price": 38.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "LEVERPOSTEI OVNSBAKT",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 25.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "LIME",
          "size": "148",
          "unit": "gram",
          "quantity": 1,
          "price": 10.35,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "PAPRIKA RØD SØT",
          "size": "300",
          "unit": "gram",
          "quantity": 1,
          "price": 33.90,
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
        { "name": "KLEMENTINER",
          "size": "886",
          "unit": "gram",
          "quantity": 1,
          "price": 17.63,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "CHILIPEPPER RØD",
          "size": "50",
          "unit": "gram",
          "quantity": 1,
          "price": 21.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "RUCCULA",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 21.90,
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
        { "name": "AVOCADO STK SEASON",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 33.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "RUDOLF & NISSENS JULEBRUS",
          "size": "0.33",
          "unit": "liter",
          "quantity": 2,
          "price": 31.80,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "RUDOLF & NISSEMOR U/SUKKER",
          "size": "0,33",
          "unit": "liter",
          "quantity": 1,
          "price": 14.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "APPELSINJUICE",
          "brand": "CEVITA",
          "size": "1",
          "unit": "liter",
          "quantity": 1,
          "price": 39.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "PAPRIKA RØD",
          "size": "180",
          "unit": "gram",
          "quantity": 1,
          "price": 12.58,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "TOMAT",
          "size": "175",
          "unit": "gram",
          "quantity": 1,
          "price": 32.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "AVOCADO STK SEASON",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 33.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "GULOST EKTE REVET",
          "size": "220",
          "unit": "gram",
          "quantity": 1,
          "price": 34.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "EKTE REVET OST ORIGINAL",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 46.40,
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
        { "name": "KIMS POTETGULL PEPPER",
          "size": "",
          "unit": "",
          "quantity": 1,
          "price": 14.95,
          "discount": None,
          "discounted_price": 14.95,
          "price_original": 29.90
        },
        { "name": "SØRLANDSCHIPS HAVSALT",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 24.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MELKESJOKOLADE",
          "size": "200",
          "unit": "gram",
          "quantity": 1,
          "price": 24.50,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "MELKESJOKOLADE KVIKKLUNSJ",
          "size": "200",
          "unit": "gram",
          "quantity": 1,
          "price": 24.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "GODT & BLANDET SUPERSUR",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 37.40,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "POPCORN FIRST PRICE",
          "size": "200",
          "unit": "gram",
          "quantity": 1,
          "price": 23.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "EVERGOOD DARK ROAST",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 54.60,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        },
        { "name": "PINJEKJERNER NATURELL",
          "size": "",
          "unit": "STK",
          "quantity": 1,
          "price": 22.90,
          "discount": None,
          "discounted_price": None,
          "price_original": None
        }
    ],
    "total": 2126.31,
    "total_discount": None
  }


receipts.insert_many([receipt_2136, receipt_2137, receipt_2138, receipt_2139, receipt_2140, receipt_2141, receipt_2142, receipt_2143, receipt_2144, receipt_2145, receipt_2146, receipt_2147])
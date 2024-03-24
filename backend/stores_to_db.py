from backend.database.mongo_db import DatabaseOperations

db = DatabaseOperations()

# Create a collection of stores
stores = db.db['stores']

store_1 ={
    "_id": "0001",
    "name": "Coop Extra Hollingen",
    "chain": "Coop",
    "location": {
    "type": "Point",
    "coordinates": [62.780383649259356, 7.00154841176671]
    },
    "address": {
    "street": "",
    "city": "Hollingen",
    "state": "",
    "zip": "6409",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "06:00-00:00",
    "tuesday": "06:00-00:00",
    "wednesday": "06:00-00:00",
    "thursday": "06:00-00:00",
    "friday": "06:00-00:00",
    "saturday": "06:00-00:00",
    "sunday": "12:00-21:00"
    },
    "contact": {
    "phone": "92071229"
    }
}

store_2 ={
    "_id": "0002",
    "name": "Bunnpris Kvam",
    "chain": "Bunnpris",
    "location": {
    "type": "Point",
    "coordinates": [62.73747194112421, 7.0963668064297085]
    },
    "address": {
    "street": "Mekvegen 12",
    "city": "Molde",
    "state": "",
    "zip": "6411",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-22:00",
    "tuesday": "08:00-22:00",
    "wednesday": "08:00-22:00",
    "thursday": "08:00-22:00",
    "friday": "08:00-22:00",
    "saturday": "09:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71254322"
    }
}

store_3 ={
    "_id": "0003",
    "name": "REMA 1000 REKNES",
    "chain": "REMA 1000",
    "location": {
    "type": "Point",
    "coordinates": [62.73423128120116, 7.142046802513306]
    },
    "address": {
    "street": "Gideonvegen 4",
    "city": "Molde",
    "state": "",
    "zip": "6412",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71216725"
    }
}

store_4 ={
    "_id": "0004",
    "name": "Coop Mega Moldeliveien",
    "chain": "Coop",
    "location": {
    "type": "Point",
    "coordinates": [62.739812238992464, 7.142566829710281]
    },
    "address": {
    "street": "Moldelivegen 97",
    "city": "Molde",
    "state": "",
    "zip": "6412",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-22:00",
    "tuesday": "08:00-22:00",
    "wednesday": "08:00-22:00",
    "thursday": "08:00-22:00",
    "friday": "08:00-22:00",
    "saturday": "09:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71201460"
    }
}

store_5 ={
    "_id": "0005",
    "name": "Bunnpris Sentrum Molde",
    "chain": "Bunnpris",
    "location": {
    "type": "Point",
    "coordinates": [62.73654532445558, 7.157794939293244]
    },
    "address": {
    "street": "Fjordgata 1-3",
    "city": "Molde",
    "state": "",
    "zip": "6413",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-21:00",
    "tuesday": "08:00-21:00",
    "wednesday": "08:00-21:00",
    "thursday": "08:00-21:00",
    "friday": "08:00-21:00",
    "saturday": "08:00-19:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71251669"
    }
}

store_6 ={
    "_id": "0006",
    "name": "Bunnpris Romsdalsgata",
    "chain": "Bunnpris",
    "location": {
    "type": "Point",
    "coordinates": [62.7384531397747, 7.166075194096095]
    },
    "address": {
    "street": "Romsdalsgata 7",
    "city": "Molde",
    "state": "",
    "zip": "6415",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:30-21:00",
    "tuesday": "07:30-21:00",
    "wednesday": "07:30-21:00",
    "thursday": "07:30-21:00",
    "friday": "07:30-21:00",
    "saturday": "09:00-21:00",
    "sunday": "10:00-21:00"
    },
    "contact": {
    "phone": "71218440"
    }
}

store_7 ={
    "_id": "0007",
    "name": "KIWI Langmyrveien",
    "chain": "KIWI",
    "location": {
    "type": "Point",
    "coordinates": [62.74375576453336, 7.170711145151421]
    },
    "address": {
    "street": "Langmyrvegen 19B",
    "city": "Molde",
    "state": "",
    "zip": "6413",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71215115"
    }
}

store_8 ={
    "_id": "0008",
    "name": "EUROSPAR Molde",
    "chain": "EUROSPAR",
    "location": {
    "type": "Point",
    "coordinates": [62.73970223781227, 7.175471051693145]
    },
    "address": {
    "street": "Frænavegen 16",
    "city": "Molde",
    "state": "",
    "zip": "6415",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-22:00",
    "tuesday": "08:00-22:00",
    "wednesday": "08:00-22:00",
    "thursday": "08:00-22:00",
    "friday": "08:00-22:00",
    "saturday": "09:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71247920"
    }
}

store_9 ={
    "_id": "0009",
    "name": "KIWI Grandfjæra",
    "chain": "KIWI",
    "location": {
    "type": "Point",
    "coordinates": [62.73697686491985, 7.183106735488633]
    },
    "address": {
    "street": "Grandfjæra 24B",
    "city": "Molde",
    "state": "",
    "zip": "6415",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "10:00-23:00",
    "sunday": "10:00-23:00"
    },
    "contact": {
    "phone": "71215547"
    }
}

store_10 ={
    "_id": "0010",
    "name": "Coop Mega Molde",
    "chain": "Coop",
    "location": {
    "type": "Point",
    "coordinates": [62.73789670638923, 7.1853131505001615]
    },
    "address": {
    "street": "Birger Hatlebakks veg 5",
    "city": "Molde",
    "state": "",
    "zip": "6415",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-22:00",
    "tuesday": "08:00-22:00",
    "wednesday": "08:00-22:00",
    "thursday": "08:00-22:00",
    "friday": "08:00-22:00",
    "saturday": "08:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "97994950"
    }
}

store_11 ={
    "_id": "0011",
    "name": "REMA 1000 MOLDEGÅRD",
    "chain": "REMA 1000",
    "location": {
    "type": "Point",
    "coordinates": [62.73930480324813, 7.185784182918354]
    },
    "address": {
    "street": "Oscar Hanssens veg 11",
    "city": "Molde",
    "state": "",
    "zip": "6415",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71251600"
    }
}

store_12 ={
    "_id": "0012",
    "name": "Coop Prix Granlia",
    "chain": "Coop",
    "location": {
    "type": "Point",
    "coordinates": [62.7446413349138, 7.189155783385407]
    },
    "address": {
    "street": "Langmyrvegen 81",
    "city": "Molde",
    "state": "",
    "zip": "6415",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "08:00-21:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "97994960"
    }
}

store_13 ={
    "_id": "0013",
    "name": "REMA 1000 FUGLSET",
    "chain": "REMA 1000",
    "location": {
    "type": "Point",
    "coordinates": [62.74132598621447, 7.197559994400955]
    },
    "address": {
    "street": "Enenvegen 1A",
    "city": "Molde",
    "state": "",
    "zip": "6416",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71254989"
    }
}

store_14 ={
    "_id": "0014",
    "name": "Kiwi Bergmo",
    "chain": "Kiwi",
    "location": {
    "type": "Point",
    "coordinates": [62.74457672676557, 7.214415261930726]
    },
    "address": {
    "street": "Nøisomhedvegen 19",
    "city": "Molde",
    "state": "",
    "zip": "6419",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71212443"
    }
}

store_15 ={
    "_id": "0015",
    "name": "KIWI Nordbyen",
    "chain": "KIWI",
    "location": {
    "type": "Point",
    "coordinates": [62.75284078753002, 7.2348431945404394]
    },
    "address": {
    "street": "Råkhaugvegen 2C",
    "city": "Molde",
    "state": "",
    "zip": "6425",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71212320"
    }
}

store_16 ={
    "_id": "0016",
    "name": "Bunnpris Kviltorp",
    "chain": "Bunnpris",
    "location": {
    "type": "Point",
    "coordinates": [62.74282826355387, 7.229637046760429]
    },
    "address": {
    "street": "Kometvegen 5",
    "city": "Molde",
    "state": "",
    "zip": "6419",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-22:00",
    "tuesday": "07:00-22:00",
    "wednesday": "07:00-22:00",
    "thursday": "07:00-22:00",
    "friday": "07:00-22:00",
    "saturday": "07:00-22:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71251001"
    }
}

store_17 ={
    "_id": "0017",
    "name": "Bunnpris Årø",
    "chain": "Bunnpris",
    "location": {
    "type": "Point",
    "coordinates": [62.747108408892494, 7.2524201430836195]
    },
    "address": {
    "street": "Eikremsvingen 2",
    "city": "Molde",
    "state": "",
    "zip": "6422",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-22:00",
    "tuesday": "08:00-22:00",
    "wednesday": "08:00-22:00",
    "thursday": "08:00-22:00",
    "friday": "08:00-22:00",
    "saturday": "09:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71250760"
    }
}

store_18 ={
    "_id": "0018",
    "name": "Coop Prix Årølia",
    "chain": "Coop",
    "location": {
    "type": "Point",
    "coordinates": [62.75452315043002, 7.280716145084724]
    },
    "address": {
    "street": "Årømyran 31E",
    "city": "Molde",
    "state": "",
    "zip": "6421",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "open",
    "tuesday": "open",
    "wednesday": "open",
    "thursday": "open",
    "friday": "open",
    "saturday": "open",
    "sunday": "open"
    },
    "contact": {
    "phone": "24113330"
    }
}

store_19 ={
    "_id": "0019",
    "name": "KIWI Malmefjorden",
    "chain": "KIWI",
    "location": {
    "type": "Point",
    "coordinates": [62.81841299814718, 7.238914160453697]
    },
    "address": {
    "street": "",
    "city": "Malmefjorden",
    "state": "",
    "zip": "6445",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "24113330"
    }
}

store_20 ={
    "_id": "0020",
    "name": "KIWI Skjevik",
    "chain": "KIWI",
    "location": {
    "type": "Point",
    "coordinates": [62.78814866313007, 7.53618243609756]
    },
    "address": {
    "street": "Baklivegen 1",
    "city": "Hjelset",
    "state": "",
    "zip": "6450",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-23:00",
    "tuesday": "07:00-23:00",
    "wednesday": "07:00-23:00",
    "thursday": "07:00-23:00",
    "friday": "07:00-23:00",
    "saturday": "07:00-23:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71251400"
    }
}

store_21 ={
    "_id": "0021",
    "name": "Joker Kleive",
    "chain": "Joker",
    "location": {
    "type": "Point",
    "coordinates": [62.794764337681045, 7.633553600559111]
    },
    "address": {
    "street": "Istadvegen 611",
    "city": "Nes",
    "state": "",
    "zip": "6453",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "07:00-22:00",
    "tuesday": "07:00-22:00",
    "wednesday": "07:00-22:00",
    "thursday": "07:00-22:00",
    "friday": "07:00-22:00",
    "saturday": "09:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71242100"
    }
}

store_22 ={
    "_id": "0022",
    "name": "SPAR Skåla",
    "chain": "SPAR",
    "location": {
    "type": "Point",
    "coordinates": [62.70203129621089, 7.423781621378948]
    },
    "address": {
    "street": "Kaptein Dreyers veg 2",
    "city": "Skåla",
    "state": "",
    "zip": "6456",
    "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
    "monday": "08:00-22:00",
    "tuesday": "08:00-22:00",
    "wednesday": "08:00-22:00",
    "thursday": "08:00-22:00",
    "friday": "08:00-22:00",
    "saturday": "09:00-20:00",
    "sunday": "closed"
    },
    "contact": {
    "phone": "71241550"
    }
}

store_23 ={
    "_id": "0023",
    "name": "BUNNPRIS & GOURMET FUGLSET",
    "chain": "Bunnpris",
    "location": {
    "type": "Point",
    "coordinates": [62.744558511287316, 7.198440666665252]
    },
    "address": {
        "street": "Frænavegen 107, 6416 Molde",
        "city": "Molde",
        "state": "",
        "zip": "6416",
        "country": "Norway"
    },
    "items": [
    
    ],
    "hours": {
        "monday": "07:00-23:00",
        "tuesday": "07:00-23:00",
        "wednesday": "07:00-23:00",
        "thursday": "07:00-23:00",
        "friday": "07:00-23:00",
        "saturday": "08:00-23:00",
        "sunday": "10:00-23:00"
    },
    "contact": {
        "phone": "71191700"
    }
}


stores.insert_many([store_1, store_2, store_3, store_4, store_5, store_6, store_7, store_8, store_9, store_10, store_11, store_12, store_13, store_14, store_15, store_16, store_17, store_18, store_19, store_20, store_21, store_22, store_23])
# Create MongoDB Collection
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['NewDatabase']
col = db['student']
print("Collection created sucessfully")


docs = [{'name': 'David', 'age': 20},
        {'name': 'Alice', 'age': 25},
        {'name': 'Tyler', 'age': 23}]
result = col.insert_many(docs)
print(result.inserted_ids)


# Read MongoDB Collection
print("Read MongoDB Collection")
cursor = col.find({})
for record in cursor:
    print(record)

# Update MongoDB Collection     
print("Update MongoDB Collection")
col.update_one({'name': 'David'}, {'$set': {'age': 21}})
cursor = col.find({})
for record in cursor:
    print(record)

# # Delete MongoDB Collection
# print("Delete MongoDB Collection")
# col.delete_one({'name': 'David'})
# cursor = col.find({})
# for record in cursor:
#     print(record)

# # Drop MongoDB Collection
# print("Drop MongoDB Collection")
# col.drop()
# cursor = col.find({})
# for record in cursor:
#     print(record)

# # Drop MongoDB Database
# print("Drop MongoDB Database")
# client.drop_database('NewDatabase')

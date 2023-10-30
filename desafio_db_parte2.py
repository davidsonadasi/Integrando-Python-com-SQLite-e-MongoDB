import pymongo as pyM
from pymongo import MongoClient
import datetime
import pprint
from bson.objectid import ObjectId


client = pyM.MongoClient("mongodb+srv://<usuario>:<password>@cluster0.oak7hno.mongodb.net/")

db = client.bank
collection = db.bank_collection
print(db.bank_collection)

post = {
    "nome": "davidson",
    "cpf": "12345678900",
    "endereco": "rua um",
    "tipo" : "poupanca",
    "agencia" : 2020,
    "num" : 2,
    "saldo" : 100,    
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),

}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

print(db.list_collection_names())

pprint.pprint(db.posts.find_one({"_id" : post_id}))

post_id_as_str = str(post_id)
print(posts.find_one({"_id" : post_id_as_str})) #None

"""
def get(post_id):
    document = client.db.collection.find_one({'_id' : ObjectId(post_id)})
"""

new_posts = [
    {
    "nome" : "Mary",
    "cpf" : "98765432100",
    "tipo" : "Corrente",
    "agencia" : 1010,
    "num" : 1,
    "saldo" : 100,    
    "tags" : ["bulk", "post", "insert"],
    "date" : datetime.datetime.utcnow(),
    }
]

print("\nEncontrando um post especifico: ")
result = posts.insert_many(new_posts)
print(result.inserted_ids)
pprint.pprint(db.posts.find_one({"author":"Elliot"}))


print("\nDocumentos presentes em Post.")
for post in posts.find():
    pprint.pprint(post)
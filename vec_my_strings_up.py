import pymongo
import requests

# Server connection and script config
# conn = "mongodb+srv://"  Get this from Atlas UI
database = "sample_airbnb"  # Mongo database with collection to vec
collection = "listingsAndReviews"  # Mongo collection
fields = ["description", "summary"]  # Fields to vectorize, can specify multiple
field_suffix = "_vec_lg" # Name of new vector field will be original field name + this suffix

# Vector service to connect to.  The VectorService tool will work here.
vec_service = "http://vec.dungeons.ca/lvec/"
vec_param = "text"

# Connect to mongo
client = pymongo.MongoClient(conn)
db = client[database]
col = db[collection]

# Find every document in the collection...
for doc in col.find():
    # For each field we have configured...
    for field in fields:
        # Query the Vectorizing Service with the text we want
        query = {"text": doc[field]}
        response = requests.get(vec_service, params=query)
        try:
            vector = response.json()

            # Update the original document with the vector field
            # WARNING: This can expand your collection size by a lot!
            filter = {"_id": doc["_id"]}
            fieldname = field + field_suffix
            newvalue = { "$set": { fieldname : vector } }
            col.update_one(filter, newvalue)
        except:
            print("Error on: " + doc[field])
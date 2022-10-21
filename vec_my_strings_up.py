import pymongo
import requests

# Server connection and script config
# conn = "mongodb+srv://"  Get this from Atlas UI
database = "sample_mflix"  # Mongo database with collection to vec
collection = "movies"  # Mongo collection
fields = ["plot", "fullplot", "title"]  # Fields to vectorize, can specify multiple
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
        try:
            query = {"text": doc[field]}
        except:
            # Show us the broken stuff!
            print(doc)
            break

        try:
            response = requests.get(vec_service, params=query)
            vector = response.json()

            # Don't bother storing vectors for all zero results
            # It's probably not valid
            if sum(vector) == 0:
                print(doc)
                break

            # Update the original document with the vector field
            # WARNING: This can expand your collection size by a lot!
            filter = {"_id": doc["_id"]}
            fieldname = field + field_suffix
            newvalue = { "$set": { fieldname : vector } }
            col.update_one(filter, newvalue)
        except:
            print("Error on: " + doc[field])
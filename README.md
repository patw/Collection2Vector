# Collection2Vector
A small script where you provide a mongo collection, and a set of fields to vectorize and it will update the source documents in the collection with additional text vector fields.

So far, it only works on strings (not arrays) and only at root level in the document.  If the Vector Service is not fast enough, feel free to download that application and run it locally for additional performance.

## Installation

```
pip install pymongo requests
```

## Running

Edit vec_my_strings_up.py first, to provide your own mongo connection and collection.  Be sure to update the fields array!

```
python vec_my_strings_up.py
```
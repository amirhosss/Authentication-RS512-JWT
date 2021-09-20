from .database import client


db = client['myDatabase']

user_coll = db['users']

denylist_coll = db['denylist']

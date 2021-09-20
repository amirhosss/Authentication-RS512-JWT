from db.collections import user_coll, denylist_coll
from models.user import UserOutDb, AdminOutDb
from models.denylist import DenylistOutdb
from .base import CrudOpreations


crud = CrudOpreations(user_coll, UserOutDb, AdminOutDb)

denylist_crud = CrudOpreations(denylist_coll, DenylistOutdb)
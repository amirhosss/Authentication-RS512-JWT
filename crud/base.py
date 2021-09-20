

class CrudOpreations():
    def __init__(self, collection, crud_model, admin_model=None):
        self.collection = collection
        self.crud_model = crud_model
        self.admin_model = admin_model

    async def create(self, data: dict, **kwargs):
        if not kwargs:
            await self.collection.insert_one(data)
        else:
            await self.collection.insert_many([data].append(list(kwargs.values())))

    async def read(self, is_admin=False, **kwargs):
        if kwargs.items():
            key, value = list(kwargs.items())[0]

            document = await self.collection.find_one({key: value})
            if document and is_admin:
                return self.admin_model(**document)
            elif document and not is_admin:
                return self.crud_model(**document)
            else:
                return None

    async def update(self, update_items: dict, **kwargs):
        if kwargs.items():
            key, value = list(kwargs.items())[0]

            await self.collection.update_one(
                {key: value},
                {'$set': dict(update_items)}
            )

    async def delete(self, **kwargs):
        if kwargs.items():
            key, value = list(kwargs.items())[0]

        await self.collection.delete_many({key: value}) 
        
import motor.motor_asyncio
import os
from dotenv import find_dotenv, load_dotenv

path = find_dotenv()
load_dotenv(path)

DATABASE_URL = os.environ['DATABASE_URL']

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

from datetime import datetime

# from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database


class ProductRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_products(self, input: dict):
        payload = {
            "name": input["name"],
            "price": input["price"],
            "description": input["description"],
            "imageUrl": input["imageUrl"],
            "created_at": datetime.utcnow(),
        }

        self.database["products"].insert_one(payload)

    def get_all_products(self):
        cursor = self.database["products"].find()  # Find all products
        result = list(cursor)  # Convert cursor to a list
        return result


    def get_recommended_products_for_user(self, user_id: str):
        # Example: Recommend the latest 10 products
        cursor = self.database["products"].find().sort("created_at", -1).limit(10)

        recommended_products = list(cursor)
        return recommended_products

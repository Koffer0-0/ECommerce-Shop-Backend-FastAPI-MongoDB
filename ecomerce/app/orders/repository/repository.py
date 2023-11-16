from datetime import datetime

# from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database


class OrderRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_order(self, input: dict):
        # Assuming 'input' contains order items and other details
        order_payload = {
            "items": input["items"],  # Example: [{"product_id": "...", "quantity": 1}, ...]
            "user_id": ObjectId(input["user_id"]),
            "created_at": datetime.utcnow()
        }
        self.database["orders"].insert_one(order_payload)

    def get_orders(self, user_id: str):
        # Calculate the offset based on the page and page_size

        # Create a filter to retrieve posts only for the specified user_id
        filter_query = {"user_id": ObjectId(user_id)}

        total_count = self.database["orders"].count_documents(filter_query)

        cursor = self.database["orders"].find(filter_query).skip(offset).sort("created_at")

        result = list(cursor)

        return {
            "total": total_count,
            "objects": result
        }
    #
    # def get_recommendations(self):

from typing import List, Optional

from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router



class OrderItem(AppModel):
    product_id: str
    quantity: int


class CreateOrderRequest(AppModel):
    items: List[OrderItem]


@router.post("/createOrder")
def create_order(
    input: CreateOrderRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    payload = input.dict()
    payload["user_id"] = jwt_data.user_id
    svc.repository.create_order(payload)
    return Response(status_code=200)


class Order(AppModel):
    # Define the structure of an Order
    items: List[OrderItem]
    created_at: datetime


class GetOrderResponse(AppModel):
    total: int
    objects: List[Order]


@router.get("/getOrder", response_model=GetOrderResponse)
def get_order(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_orders(user_id=jwt_data.user_id)
    return result


from typing import List, Optional

from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateOrderRequest(AppModel):
    address: str
    name: str
    lat: float
    lng: float
    imageUrl: str


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
    address: str
    name: str
    lat: float
    lng: float
    imageUrl: str


class GetOrderResponse(AppModel):
    total: int
    objects: List[Order]
    

@router.get("/getOrder", response_model=GetOrderResponse)
def get_order(
    page: int,
    limit: int,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_posts(user_id=jwt_data.user_id, page=page, page_size=limit)
    return result


from typing import List, Optional

from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateProductRequest(AppModel):
    address: str
    name: str
    lat: float
    lng: float
    imageUrl: str


@router.post("/createProduct")
def create_product(
    input: CreateProductRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    payload = input.dict()
    payload["user_id"] = jwt_data.user_id
    svc.repository.create_products(payload)
    return Response(status_code=200)


class Product(AppModel):
    address: str
    name: str
    lat: float
    lng: float
    imageUrl: str


class GetProductResponse(AppModel):
    total: int
    objects: List[Product]
    

@router.get("/getProduct", response_model=GetProductResponse)
def get_product(
    page: int,
    limit: int,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_posts(user_id=jwt_data.user_id, page=page, page_size=limit)
    return result


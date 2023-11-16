from typing import List, Optional

from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateProductRequest(AppModel):
    name: str
    price: int
    description: str
    imageUrl: str


@router.post("/createProduct")
def create_product(
    input: CreateProductRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    payload = input.dict()
    payload["user_id"] = jwt_data.user_id
    result = svc.repository.create_products(payload)
    return result, Response(status_code=200)


class Product(AppModel):
    name: str
    price: int
    description: str
    imageUrl: str


class GetProductResponse(AppModel):
    total: int
    objects: List[Product]
    

@router.get("/getAllProducts", response_model=GetProductResponse)
def get_all_products(
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_all_products()  # Call the correct method
    return result

@router.get("/recommendations")
async def get_recommendations(jwt_data: JWTData = Depends(parse_jwt_user_data), svc: Service = Depends(get_service)):
    recommended_products = svc.get_recommended_products_for_user(jwt_data.user_id)
    return recommended_products
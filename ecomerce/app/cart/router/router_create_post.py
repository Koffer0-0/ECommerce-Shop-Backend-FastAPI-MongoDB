from typing import List, Optional

from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateHistoryRequest(AppModel):
    address: str
    name: str
    lat: float
    lng: float
    imageUrl: str


@router.post("/createHistory")
def create_history(
    input: CreateHistoryRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    payload = input.dict()
    payload["user_id"] = jwt_data.user_id
    svc.repository.create_post(payload)
    return Response(status_code=200)


class History(AppModel):
    address: str
    name: str
    lat: float
    lng: float
    imageUrl: str


class GetHistoryResponse(AppModel):
    total: int
    objects: List[History]
    

@router.get("/getHistory", response_model=GetHistoryResponse)
def get_history(
    page: int,
    limit: int,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_posts(user_id=jwt_data.user_id, page=page, page_size=limit)
    return result


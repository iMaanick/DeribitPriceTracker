from dataclasses import dataclass

from fastapi import APIRouter, Request

index_router = APIRouter()


@dataclass
class Response:
    documentation: str


@index_router.get("/", response_model=Response)
async def index() -> Response:
    return Response(documentation="http://localhost:8000/docs")


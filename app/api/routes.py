from fastapi import APIRouter
from app.api.endpoints.search import router as seach_router

routers = APIRouter()
router_list = [seach_router]

for router in router_list:
    routers.include_router(router)
from fastapi import APIRouter


router = APIRouter(prefix="/health")


@router.get("", summary="Health Check availabilty")
async def health():
    """
    Health endpoint
    """
    return {"Status": "Up"}
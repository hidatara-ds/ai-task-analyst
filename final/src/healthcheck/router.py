from fastapi import APIRouter

router = APIRouter(tags=["HealthCheck"])


@router.get("/healthcheck")
def health_check():
    return {"status": "live"}

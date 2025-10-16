from fastapi import APIRouter
from sqlalchemy import text
from starlette import status

from db.uow import UnitOfWork
from schema.health_check import HealthCheckResponseDB

router = APIRouter(
    prefix="/health-check",
    tags=["Health"],
)

@router.get(
    path="/db",
    response_model=HealthCheckResponseDB,
    status_code=status.HTTP_200_OK,
    description="Check health of the database connection",
)
async def check_db_connection() -> HealthCheckResponseDB:
    async with UnitOfWork() as uow:
        result = await uow.session.execute(text("SELECT 1"))
        scalar_result = result.scalar()
        return HealthCheckResponseDB(response=scalar_result == 1)

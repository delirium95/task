from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.uow import AsyncSessionLocal
from dependencies import get_db_dependency

router = APIRouter(prefix="/contacts", tags=["Contacts"])

from fastapi import Query

@router.get("/search")
async def search_contacts(
    query: str = Query(..., description="Full-text search query"),
):
    session = AsyncSessionLocal()
    result = await session.execute(
        text("""
            SELECT first_name, last_name, email, description
            FROM contacts
            WHERE search_vector @@ plainto_tsquery('english', :query)
            ORDER BY ts_rank(search_vector, plainto_tsquery('english', :query)) DESC;
        """),
        {"query": query},
    )
    rows = result.mappings().all()
    session.close()
    return [dict(r) for r in rows]

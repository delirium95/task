from pathlib import Path

from fastapi import APIRouter
from fastapi.params import Depends

from dependencies import get_import_service
from services.import_service import ImportService

router = APIRouter(
    prefix="/import",
    tags=["Import"],
)
BASE_DIR = Path(__file__).resolve().parent.parent

@router.get(
    '/status',
    status_code=200,
)
async def get_import_status(
        import_service: ImportService = Depends(get_import_service)
):
    await import_service.import_data(BASE_DIR / "nimble_contacts.xlsx")
    return {"message": "Import is done"}

@router.get(
    '/request'
)
async def request_import(
        import_service: ImportService = Depends(get_import_service)
):
    return await import_service.import_data_from_nimble_url()

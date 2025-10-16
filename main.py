import schedule
from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every

from config import app_settings
from dependencies import get_import_service
from routers import health_router, import_router, search_router
from schema.nimble_contact import NimbleContact
from services import ImportService

app = FastAPI()
app.include_router(health_router)
app.include_router(import_router)
app.include_router(search_router)

@repeat_every(seconds=86400)
async def import_data(import_service: ImportService = Depends(get_import_service)):
    await import_service.import_data("nimble_contacts.xlsx")
@app.get("/")
async def root():
    return {"db_url": app_settings.db.db_url,}

@app.get("/keys")
async def get_model_keys():
    return list(NimbleContact.model_fields.keys())


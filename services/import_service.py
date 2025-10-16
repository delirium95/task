import csv
import pandas as pd
import requests

from db.uow import UnitOfWork
from model.contact import Contact
from schema.nimble_contact import NimbleContact


class ImportService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow


    async def import_data(self, path):
        df = pd.read_excel(path)
        contacts = []
        for _, row in df.iterrows():
            data = {k: v for k, v in row.to_dict().items() if k in NimbleContact.model_fields.keys()}
            contacts.append(Contact(**data))
        async with self.uow as uow:
            await uow.contacts.add_all(contacts)

    async def import_data_from_nimble_url(self):
        response = requests.get("https://app.nimble.com/api/v1/contacts",
                                headers={"Authorization": "Bearer NxkA2RlXS3NiR8SKwRdDmroA992jgu"},
                                params= {
                                         "fields": "first name, last name, email, description",
                                         "per_page": 50,
                                         "page": 1}
                                )
        data = response.json()["resources"]
        for item in data:
            fields = item.get("fields", {})
            contact = Contact(
                first_name=fields.get("first name", [{}])[0].get("value"),
                last_name=fields.get("last name", [{}])[0].get("value"),
                email=fields.get("email", [{}])[0].get("value"),
                description=fields.get("description", [{}])[0].get("value")
            )
            async with self.uow as uow:
                uow.contacts.add(contact)
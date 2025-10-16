from select import select

from db.BaseRepository import BaseRepository
from model.contact import Contact


class ContactRepository(BaseRepository[Contact]):
    def __init__(self, session):
        super().__init__(session, model=Contact)

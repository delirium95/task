from pydantic import Field

from config import ConfigBase


class DbConfig(ConfigBase):
    db_url: str = Field(alias="DB_URL")


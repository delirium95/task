from pydantic import Field

from config import ConfigBase, DbConfig
import os

class AppSettings(ConfigBase):
    db: DbConfig = Field(default_factory=DbConfig)


app_settings: AppSettings = AppSettings()

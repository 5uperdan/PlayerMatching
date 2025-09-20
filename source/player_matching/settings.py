from pydantic import Field
from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    team_names: list[str] = Field(default_factory=lambda: ["MK", "Bedford"])
    xlsx_name: str = Field(default=...)


general_settings = GeneralSettings()

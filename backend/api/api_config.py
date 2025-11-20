import json
from pathlib import Path
from pydantic import BaseModel


class ApiConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


config_path = Path(__file__).with_name("config_api.json")
with config_path.open("r", encoding="utf-8") as fp:
    api_config = ApiConfig(**json.load(fp))

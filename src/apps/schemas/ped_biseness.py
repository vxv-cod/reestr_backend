
from typing import Any
from pydantic import BaseModel
from apps.schemas._name import SchemaNameStr, SchemaNameStr_ID


class Schema_ped_business_process(BaseModel):
    ped_id: int
    business_process_id: str
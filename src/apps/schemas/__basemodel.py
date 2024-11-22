import datetime
from typing import Any, Union
from pydantic import BaseModel, ConfigDict, Field

class Base_Model(BaseModel):
    # class Config:
    #     from_attributes = True 
    #     all_ignored_types = True

    model_config = ConfigDict(
        from_attributes = True
        
    )
        

class Base_Model_id(Base_Model):
    # id: int | str
    id: Union[int, str]














    # class Config:
    #     from_attributes = True 
        # arbitrary_types_allowed=True    #   Разрешены ли произвольные типы
        # use_enum_values = True



    # model_config = ConfigDict(
    #     from_attributes = True
        # use_enum_values = True    
    # )

    # id : int | str = Field(hidden=True)
    # @staticmethod
    # def schema_extra(schema: dict, _):
    #     props = {}
    #     for k, v in schema.get('properties', {}).items():
    #         if not v.get("hidden", False):
    #             props[k] = v
    #     schema["properties"] = props


    # model_config = ConfigDict(json_schema_extra=schema_extra, from_attributes = True)

    # id : int | str = Field(exclude=True)
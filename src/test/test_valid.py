from typing import Annotated, Any
from pydantic import BeforeValidator, PlainValidator, WrapValidator, computed_field, field_validator, model_validator
from apps.schemas.__basemodel import Base_Model



# class Schema_Info_relations(Base_Model):
#     business_process: list[SchemaNameStr_ID] | str
#     doc_file: list[Schema_file_data_ID_relation]


def validate_timestamp(v, handler):
    # return handler([i.name for i in v])
    if isinstance(v, list):
        return handler([i.name for i in v])
    else:
        return handler(v.name)

# ddd = lambda v, handler: handler([i.name for i in v])
ddd = lambda v: [i.name for i in v]
    
# MyName = Annotated[Any, WrapValidator(validate_timestamp)]
# MyName = Annotated[Any, BeforeValidator(lambda v: [i.name for i in v])]


def hhhh(v):
    if isinstance(v, list):
        return [i.id for i in v]
    else:
        return v.id

# MyName = Annotated[Any, BeforeValidator(lambda v: [i.id for i in v])]
MyName = Annotated[Any, PlainValidator(hhhh)]


class Schema_Info_relations(Base_Model):
    doc_file: MyName
    business_process: MyName
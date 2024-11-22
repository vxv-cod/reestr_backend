from asyncio.log import logger
import datetime
import json
from typing import Any, Optional
from pydantic import computed_field, Field, model_validator, Json, ConfigDict

from apps.schemas.__basemodel import Base_Model
from apps.schemas._name import SchemaName, SchemaName_ID
# from apps.schemas._info import Schema_Info_catalog


class Schema_file_data_in(Base_Model):
    nomer: str | None = None
    info_id: int
    doc_type_id: int
    date: datetime.date | None = None


class Schema_file_data(Schema_file_data_in):
    name: str | None = None


class Schema_file_data_ID(Schema_file_data):
    id: int | None = None


class Schema_file_delete(Base_Model):
    id: int
    name: str

class Schema_file_delete_list(Base_Model):
    data: list[Schema_file_delete]


class Schema_file_data_ID_relation(Schema_file_data_ID):
    doc_type: SchemaName_ID
    

class Schema_upload_pdf(Base_Model):
    id: int | None
    info_id: int | None
    doc_type_id: int | None
    name: str | None = None

    model_config = ConfigDict(
        exclude_none  = True
    )

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value  


class Schema_Info_catalog(Base_Model):
    id: int
    catalog: str

class Schema_file_delete_out(Base_Model):
    info_id: int
    doc_type_id: int


class Schema_pdf(Schema_file_data_ID):
    doc_type: str
    catalog: str

    @model_validator(mode='before')
    @classmethod
    def relaion_catalog_doc_type(cls, data: Any) -> Any:
        data['catalog'] = data['info'].catalog
        data['doc_type'] = data['doc_type'].name
        return data  





# class Schema_upload_pdf_test_222(Base_Model):
#     id: int | None
#     info_id: int | None
#     doc_type_id: int | None

# class Schema_upload_pdf_test_222(Base_Model):
#     id: int  = Form(...)
#     info_id: int = Form(...)
#     doc_type_id: int  = Form(...)
#     # file: UploadFile = Form(...)



    # name: str | None
    # file: UploadFile



    # id: int | None = Form(...)
    # name: str | None = Form(...)
    # file: UploadFile = Form(...)


    # doc_type: SchemaName_ID = Field(exclude=True)
    # @computed_field
    # def doc_type_name(self) -> str:
    #     return self.doc_type.name
    
    # doc_type: SchemaName_ID | None
    
    # doc_type: SchemaName_ID | str
    # @model_validator(mode='after')
    # def valid_doc_type(self):
    #     self.doc_type = self.doc_type.name
    #     return self
    
    


    '''
import json
from pydantic import BaseModel, model_validator



class TestSchema(BaseModel):
    foo: str
    bar: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        print(value)
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

@app.post("/test")
def endpoint(file: UploadFile = File(...), body: TestSchema = Form(...)):
    print(file)
    print(body)
    return body
    
    '''
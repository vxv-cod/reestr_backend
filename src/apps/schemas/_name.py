from pydantic import Field, model_validator
from apps.schemas.__basemodel import Base_Model, Base_Model_id


class SchemaName(Base_Model):
    name: str | None

class SchemaName_ID(SchemaName, Base_Model_id):
    # id: int
    ...


class SchemaNameStr(Base_Model):
    name: str

class SchemaNameStr_ID(SchemaNameStr, Base_Model_id):
    # id: str
    ...

    
    
    

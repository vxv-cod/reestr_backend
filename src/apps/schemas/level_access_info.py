from typing import Any
from apps.schemas.__basemodel import Base_Model
from apps.schemas._name import SchemaName, SchemaName_ID


    
class SchemaLevelAccessInfo(Base_Model):
    # id: int
    # Уроверь конфиденциальности
    level_privacy_id: int | None = None

    # level_privacy: SchemaName_ID().model_dump()


    # Наличие обработки персональных данных
    processing_personal_data: bool | None = False
    # Наличие обработки сведений конфиденциального характера 
    processing_confidential_information: bool | None = False


# from apps.schemas.info import Schema_Info

# class SchemaLevelAccessInfo_relationship(SchemaLevelAccessInfo):
#     general: Schema_Info

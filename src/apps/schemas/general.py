from apps.db import Base
from apps.schemas.level_access_info import SchemaLevelAccessInfo
from apps.schemas.service_support import SchemaServiceSupport
from apps.schemas._info import Schema_Info, Schema_Info_relations
from apps.schemas.__basemodel import Base_Model_id



class Schema_General(SchemaServiceSupport, SchemaLevelAccessInfo, Schema_Info):
    ...


class Schema_General_ID(Schema_General, Base_Model_id):
    ...


class Schema_General_ID_relations(Schema_Info_relations, Schema_General_ID):
    ...






# from typing import Annotated, Any

# Schema_General_ID.model_rebuild()
# class Schema_General_ID_relations(Schema_Info_relations, SchemaServiceSupport_relations, Schema_General_ID):
#     @model_validator(mode='before')
#     @classmethod
#     def find_id(cls, data: Base):
#         # print(self.__dict__)
#         # print(self.__getattribute__("business_process"))

#         for k, v in data.__dict__.items():
#             if not isinstance(v, Union[str, int, None, list]):
#                 print(k, v, type(v))
#                 # print(k, type(v))
#                 # print(k, v.__args__)
#                 # print(k, v.__dict__)
#                 # cls.k = Annotated[type(v), ...]
#         # print(data.__annotations__)
#         # print(data.__annotations__)
#         # for i in data.__annotations__:
#             # print(i.__contains__("_id"), i)
#             # try:
#             #     print(data[i].values())
#             # except:

#         # print(data.defo())
#         return data   
#     ...








# class Schema_General_ID_relations(SchemaServiceSupport_relations, Schema_General_ID):
#     ...


# class Test(Base_Model):
#     # hardware: Any
#     @model_validator(mode='before')
#     @classmethod
#     def prodo(cls, data: dict):
#         # print(data.__annotations__)
#         # keys = data.__annotations__
#         ddd  = data.__class__.pydantic_schema_id.__dict__
#         print(ddd)
#         # values = dir(data)
#         # values = data.__dict__
#         # print(values)
#         # data = data.__dict__
#         # cls.__setattr__("count_DO", 0)
#         # setattr(Test, "count_DO", None)

#         # print(data["hardware"])

#         # for i in keys:
#         #     data[i] = values[i]
#         # print(data.__dict__)
#         # for i in data.__dict__:
#         #     print(i)
#         # data = dict(**data.__dict__)
        
        
#         return data
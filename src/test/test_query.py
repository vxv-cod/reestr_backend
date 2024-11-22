if __name__ == "__main__":
    import sys, os
    sys.path.insert(1, os.path.join(sys.path[0], '..'))

import asyncio
from typing import Union
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from rich import print



from apps.models._base._info import Info
# from apps.models._base.doc_file import Doc_file
from apps.repositories.repo_uow import UnitOfWork
from apps.repositories.repo_SQL import SQLRepo
from apps.db import sync_engine, sync_session_maker, async_engine, async_session_maker
from apps.schemas._info import *
from apps.schemas.general import *



def sql_in_py(schema: BaseModel, data):
    return [schema.model_validate(i, from_attributes=True).model_dump() for i in data]
    # return [schema.model_validate(i if isinstance(i, dict) else sql_in_py(i.schema, i), from_attributes=True).model_dump() for i in data]


# def select_mTo_or_oTo():
#     with sync_session_maker() as session:
#         model = Info
#         query = (
#             select(model)
#             .options(joinedload(model.hardware))
#             .options(joinedload(model.software))
#             .options(joinedload(model.names_BM))
#             .options(joinedload(model.business_process))
#             .options(joinedload(model.doc_file))
#             # .options(selectinload(model.doc_file))
#         )
#         # print(query)
#         result = session.scalars(query).unique().all()
#         res = sql_in_py(Schema_General_ID_relations, result)
#         print(res)
#         return res
# select_mTo_or_oTo()


async def select_Info(uow = UnitOfWork()):
    async with uow:
        model = Info
        query = (
            select(model)
            # .options(joinedload(model.hardware))
            # .options(joinedload(model.software))
            # .options(joinedload(model.names_BM))
            # .options(joinedload(model.business_process))
            # .options(joinedload(model.doc_file))
            # .options(selectinload(model.doc_file))
        )
        # print(query)
        result = await uow.session.scalars(query)
        res = result.unique().all()
        valid = sql_in_py(Schema_General_ID_relations, res)
        print(valid)
        return valid
        
asyncio.run(select_Info())


        
'''Ручная валидация'''
# from pydantic import BeforeValidator, AfterValidator, PlainValidator, WrapValidator, computed_field, field_validator, model_validator

# def valid_relations(v: list[Base] | Base, h):
    # if isinstance(v, NoneType): return v
    # if isinstance(v, list): return [i.id for i in v]
    # else: return v.id

# MyName = Annotated[Any, BeforeValidator(lambda v: [i.id for i in v])]
# plan_valid_field = Annotated[Any, WrapValidator(valid_relations)]
'''------------------------------------------'''

# from apps.models import references


# tads = [references.availability.Availability, references.doc_type.Doc_type]
# # tasks = [asyncio.create_task(session.execute(select(i))) for i in tads]

# async def fetch_all(session, tab):
#     return await session.scalars(select(tab))




# async def maiin(uow = UnitOfWork()):
#     references_tav = []
#     async with uow:
#         session = uow.session
#         for tab in tads:
#             res = await fetch_all(session, tab)
#             references_tav.append([row.to_read_model().model_dump() for row in res])
#     print(references_tav)
# asyncio.run(maiin())

        # result: tuple[Base, Base] = res.all()
        # for i in result:
        #     res = (i[0].to_read_model(), i[1].to_read_model())
        #     print(res)


        # print(f"dto = {dto}")
        # print(len(dto))


# def select_mTo_or_oTo():
#     with sync_session_maker() as session:
#         model = Ped
#         query = (
#             select(model)
#             .options(selectinload(model.doc_file))
#         )
#         res = session.execute(query)
#         result = res.scalars().all()
#         # result = res.unique().scalars().all()
#         print(result)
#         # Add_ped.model_rebuild()        
#         dto = sql_in_py(SchemaPed_relationship, result)
#         print(dto)





        # def uuu(i):
        #     obj = {}
        #     for kk, x in i.__dict__.items():
        #         if isinstance(x, Union[str, int, list]):
        #             if isinstance(x, list):
        #                 eee = []
        #                 for k in x:
        #                     xx = {}
        #                     for ll, tt in k.__dict__.items():
        #                         if ll != "_sa_instance_state":
        #                             xx[ll] = tt
        #                     eee.append(xx)
        #                 x = eee
        #             obj[kk] = x
        #     return obj
        
        # ggg = []
        # for i in result:
        #     ggg.append(uuu(i))

        # print(ggg)
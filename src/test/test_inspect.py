import asyncio
import sys, os
import types
from loguru import logger
from sqlalchemy import VARCHAR, INTEGER, delete, inspect, Engine
from rich import print
from sqlalchemy.engine import Connection



if __name__ == "__main__":
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    
from apps.db import async_engine, sync_engine, sync_session_maker
from apps.models._base._info import Info
from apps.models.references.availability import Availability
from apps.repositories.repo_SQL import SQLRepo
from apps.repositories.repo_uow import UnitOfWork

async def sqlgo(table, data, uow: UnitOfWork):
    uow_attr: SQLRepo = getattr(uow, table)
    await uow.session.execute(delete(uow_attr.model))
    await uow.session.flush()
    res = await uow_attr.add_list(data)
    await uow.session.flush()  


  
    
def test_inspect():
    from apps.schemas.service_support import SchemaServiceSupport

    # columns = Base.metadata.tables[Info.__tablename__].columns
    # for i in columns:
    #     print(i.comment)
    
    insp = inspect(sync_engine)
    # columns = insp.get_columns(table_name="info")
    # print(columns)

    # ccc = insp.get_multi_columns()
    # print(ccc)
    # ccc = insp.get_foreign_keys(table_name="info")
    
    
    columns = insp.get_columns(table_name="info")
    print(f"{columns = }")
    
    multi_columns = insp.get_multi_columns()
    # print(f"{multi_columns = }")
    # print(multi_columns)


    foreign_keys = insp.get_foreign_keys(table_name="info")
    # print(f"{foreign_keys = }")
    xxx = insp.__annotations__    #   {'dialect': 'PGDialect'}
    xxx = insp.dialect.name       #   postgresql
    # print(xxx)

    from sqlalchemy.engine.interfaces import ReflectedColumn

    # insp = ReflectedColumn()
    # print(insp)

    tables = Availability.metadata.tables[Availability.__tablename__]
    # print(tables.comment)

    print(Availability.__table_args__["comment"])

    # for i in columns:
    #     print(i.comment)



def test_name_for_file():
    path = r"\\rosneft\tmn-dfs$\TNNC\references\ref_IS_Doc\СРК\pdf\СРК_РПД.pdf"
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    file = os.path.join(dirname, filename)
    print(f"{filename = }")
    print(f'{dirname = }')
    print(f"{file = }")
    

# def use_inspector(table):
#     from apps.schemas.service_support import SchemaServiceSupport
#     insp = inspect(sync_engine)
#     insp_columns = insp.get_columns(table_name = table)
#     # print(f"{columns = }")
    
#     columns = []
#     for column in insp_columns:
#         obj = {}
#         obj['name'] = column['name']
#         obj["dataType"] = column['type'].python_type
#         obj['label'] = column['comment']
#         columns.append(obj)

#     print(columns)


from sqlalchemy.ext.asyncio import AsyncConnection   
from sqlalchemy.engine import Connection

def use_inspector(conn: Connection, table):
    
    insp = inspect(conn)
    insp_columns = insp.get_columns(table_name = table)
    columns = []
    for column in insp_columns:
        obj = {}
        obj['name'] = column['name']
        # obj["dataType"] = column['type'].python_type
        obj["dataType"] = column['type'].python_type.__name__
        obj['label'] = column['comment']
        columns.append(obj)
    print(columns)
    return columns


async def load_headers(table):
    async with async_engine.connect() as conn:
        return await conn.run_sync(use_inspector, table)
        
        # columns = await conn.run_sync(use_inspector(conn, table))

    



if __name__ == "__main__":
    # test_name_for_file()
	# test_inspect()
    # test_headers("info")
    
    asyncio.run(load_headers("info"))

    # xxx = VARCHAR()
    # print(xxx)



    




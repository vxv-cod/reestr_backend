if __name__ == "__main__":
    import sys, os
    sys.path.insert(1, os.path.join(sys.path[0], '..'))

import asyncio
from loguru import logger
from sqlalchemy import func, inspect, select, Sequence, text
from sqlalchemy.sql.functions import max, next_value

from apps.db import Base
from apps.models._base.doc_file import Doc_file
from apps.repositories.repo_uow import UnitOfWork

# SELECT nextval('public.doc_file_id_seq');

www = '''
SELECT setval('public.doc_file_id_seq', (SELECT MAX(id) FROM public.doc_file));
'''
async def sequence_current(uow = UnitOfWork()):
    async with uow:
        model = Doc_file
        # print(Doc_file.metadata.schema._set_parent)
        
        # www = f"SELECT setval('public.doc_file_id_seq', (SELECT MAX(id) FROM public.doc_file));"

        query = select(
            # func.max(model.id)
            func.current_time
            # next_value(Sequence("doc_file_id_seq"))
            
            )
            # max(model.id)
            # text(www)
            # Sequence(model)
            # Sequence('doc_file_id_seq').start

            # )
        # xxx = next_value(Sequence("doc_file_id_seq")).name
        # xxx = Doc_file.__table__.schema.__dir__()
        # inspect_manager = inspect(Doc_file)

        # xxx = Base.metadata.schema.__dir__()
        # xxx = Sequence("doc_file").start
        # print(f"{xxx = }")
        # print(f"{inspect_manager = }")
        # inspect_manager.s

        # query = text(www)
        # print(query)
        result = await uow.session.scalar(query)
        
        
        # result = await uow.session.execute(select(Sequence('doc_file_id_seq')))
        logger.debug(f"{result = }")
        # valid = sql_in_py(Schema_General_ID_relations, res)
        # print(valid)
        # return valid
        
asyncio.run(sequence_current())
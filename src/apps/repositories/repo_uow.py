__all__ = ["UnitOfWork"]

from apps.db import async_session_maker, sync_session_maker
from apps.models import models_clases
from apps.repositories.repo_SQL import SQLRepo



class UnitOfWork:
        
    def __init__(self):
        self.session_factory = async_session_maker
        self.models_clases = models_clases

    async def __aenter__(self):
        # logger.debug("DataBase: ON")
        self.session = self.session_factory()
        for model in models_clases:
            setattr(self, model.__tablename__, SQLRepo(self.session, model))

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()
        # logger.debug("DataBase: END")

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()



class UOW_Sync:
    def __init__(self):
        self.session_factory = sync_session_maker
        self.schema = None
    
    def __enter__(self):
        self.session = self.session_factory()
        # self.query = DBScheduler_query(session=self.session)

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()



    '''----------------------------------------------------------------------------'''
    '''Вариант с колбэком менеджера контекста'''
    # def __call__(self, *args, **kwargs):
    #     self.args, self.kwargs = args, kwargs
    #     return self
    
    # def __enter__(self):
    #     self.query = DBScheduler_query(self.session, **self.kwargs)
    '''----------------------------------------------------------------------------'''
    #     def __call__(self, schema):
    #     self.schema = schema
    #     return self

    # def __enter__(self):
    #     self.session: Session = self.session_factory
    #     self.query = DBScheduler_query(session=self.session)
    '''----------------------------------------------------------------------------'''
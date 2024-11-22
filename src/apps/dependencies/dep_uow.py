from typing import Annotated
from fastapi import Depends
from apps.repositories.repo_uow import UnitOfWork


'''DataBase'''
DataBase_depend_UOW = Annotated[UnitOfWork, Depends()]







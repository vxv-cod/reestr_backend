import asyncio
import os
import sys

# from rich import print
from loguru import logger
from openpyxl import load_workbook
from sqlalchemy import delete, insert, update, select




if __name__ == "__main__":
    sys.path.insert(1, os.path.join(sys.path[0], '..'))


from utils.exel_to_db import load_db, get_exel
from apps.models.references.business_process import Business_process
from apps.db import async_engine, sync_engine, sync_session_maker
from apps.db import Base
from apps.repositories.repo_SQL import SQLRepo
from apps.repositories.repo_uow import UnitOfWork
from store.create_exel_references import data as default_data

from phonebook import get_phonebook, get_divisions
# from exel_to_db import load_checklist, load_for_default_table
from funcs import read_json, write_json

store = "src/store/"
# str = 'src\store\checklist.xlsx'


def drop_tables(create_all = False):
    Base.metadata.drop_all(sync_engine)
    if create_all: Base.metadata.create_all(sync_engine)


def business_process_set(fist_row: int = 4):
    filename = r"src\store\business_process.xlsx"
    convert = lambda row: {"id": row[1], "name": row[2]}

    '''Загружаем из файла объект екселя'''
    wb = load_workbook(filename = filename)
    values = [i for i in wb["Лист1"].values][fist_row - 1:]
    '''Выбираем из всех данных листа по строчкно нужные поля'''
    rows = sorted([convert(row) for row in values if "бывший" not in row[2]], key = lambda row: row["id"])
    return rows


def savedata_to_json():
    if not os.path.isfile(f"{store}phonebook.json"):
        phonebook = get_phonebook()
        write_json(phonebook, f"{store}phonebook")

    if not os.path.isfile(f"{store}divisions.json"):
        phonebook = read_json(f"{store}phonebook.json")
        divisions = get_divisions(phonebook)
        write_json(divisions, f"{store}divisions")

    if not os.path.isfile(f"{store}business_process.json"):
        business_process = business_process_set()
        write_json(business_process, f"{store}business_process")



async def load(uow: UnitOfWork = UnitOfWork()):
    savedata_to_json()

    # for key, val in default_data.items():
    #     data = [{"id": i, "name": v} for i, v in enumerate(val)]
    #     default_data[key] = data
    default_data = {}
    # default_data["phonebook"] = read_json(f"{store}phonebook.json")
    default_data["structural_divisions"] = read_json(f"{store}divisions.json")
    default_data["business_process"] = read_json(f"{store}business_process.json")

    drop_tables(1)
    logger.warning(default_data.keys())
    logger.warning(f"Всего = {len(default_data.keys())}")

    async with uow:
        for key, val in default_data.items():
            uow_attr: SQLRepo = getattr(uow, key)
            await uow.session.execute(delete(uow_attr.model))
            await uow.session.flush()
            await uow_attr.add_list(val)
            await uow.session.flush()
            logger.debug(f"{key} = {len(val)}")
        await uow.commit()
    print("*********************************")



async def go():
    await load()
    await load_db(get_exel(r'src\store\default_references.xlsx'))
    await load_db(get_exel(r'src\store\default_data_table.xlsx'))


if __name__ == "__main__":
    drop_tables()
    asyncio.run(go())
    
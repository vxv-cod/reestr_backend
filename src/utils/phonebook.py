import os
import sys
import requests
import json

from loguru import logger


if __name__ == "__main__":
    sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.funcs import write_json

from config import settings
from apps.schemas.contacts import SchemaPhonebook

    



def get_data(child: dict, xxxx: list):
    for rec in child['phonebookRecord']:
        xxxx.append(SchemaPhonebook(**rec['phonebookData']).model_dump())
    return xxxx


def search_childs(xxxx: list, items: list[dict], func):
    '''Поиск вложенных ключей'''
    for item in items:
        '''Ищем вложенные ключи childs'''
        child = item.get("childs", None)
        '''Если значение ключа child список, то Реверс функции'''
        if isinstance(child, list):
            search_childs(xxxx, child, func)
        '''Если елемент списка dict вытаскиваем даннче пользователя'''
        if isinstance(item, dict):
            xxxx = func(item, xxxx)
    return xxxx


def get_response():
    response = requests.post(settings.URL_Phonebook)
    if response.status_code == 200:
        data = response.json()
        items: list[dict] = data["message"]["childs"]
    else:
        raise response.raise_for_status()
    return items


def get_phonebook():
    logger.debug("OK")
    '''Выборка всех контактов из телефоноой книги'''
    return search_childs([], get_response(), get_data)
    

def get_divisions(contacts = get_phonebook):
    logger.debug("OK")

    departmentName = list(set([i['departmentName'] for i in contacts]))
    divisions = list([i for i in departmentName if 'Управление по' in i ])
    divisions = [{"id": i, "name": v} for i, v in enumerate(divisions, 1)]
    return divisions



if __name__ == "__main__":
    contacts = get_phonebook()
    logger.debug(f"{len(contacts) = }")
    '''Сохраняем в файл в store'''
    write_json(contacts, r"src/store/contacts")

    divisions = get_divisions(contacts)
    logger.debug(f"{len(divisions) = }")
    '''Сохраняем в файл в store'''
    write_json(divisions, r"src/store/divisions")
    ...
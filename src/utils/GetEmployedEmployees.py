import datetime
import json
from loguru import logger
import requests
from pydantic import BaseModel



class SchemaPhonebook(BaseModel):
    userId: str
    fullFio: str | None
    lastName: str | None
    firstName: str | None
    secondName: str | None
    lastName: str | None
    staffName: str | None
    departmentName: str | None

    
def write_json(data, file_name):
    '''Запись объектов Python в файл json'''
    with open(f'{file_name}.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def get_html(url):
    data=f'"{datetime.datetime.now()}"'
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, headers=headers, data=data)
    data = response.json()
    return data

def parse():
    URL = 'http://10.28.79.100:443/ServiceStaff/api/Employee/GetEmployedEmployees'
    html = get_html(URL)
    users: list[dict] = html["message"]
    users_comvert = [SchemaPhonebook(**user).model_dump() for user in users]
    # users_comvert = [user for user in users]
    write_json(users_comvert, "users_data")
    # write_json(users_comvert, "users_full_data")



if __name__ == "__main__":
    parse()

# http://10.28.79.100:443/ServiceStaff/api/Phonebook/GetPhonebook
# http://10.28.79.100:443/ServiceStaff/api/Phonebook/GetPhonebookByDepartment

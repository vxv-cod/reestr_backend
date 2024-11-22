import datetime

from pydantic import BaseModel


class Schema_save(BaseModel):
    count: int
    insert_list: list[int | str]
    update_list: list[int | str]

    

import datetime
from typing import Annotated


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text


'''Поля DataBase'''
# , comment="№ п/п"
intpk = Annotated[int, mapped_column(primary_key=True, comment="№ п/п")]
strpk = Annotated[str, mapped_column(primary_key=True, comment="№ п/п")]
name = Annotated[str | None, mapped_column(comment="Наименование")]

# datepk = Annotated[datetime.date, mapped_column(primary_key=True)]
# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# updated_at = Annotated[datetime.datetime, mapped_column(
#         server_default=text("TIMEZONE('utc', now())"),
#         onupdate=datetime.datetime.utcnow,
#     )]

datepk = Annotated[datetime.date, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text('now()')
)]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text('now()'),
    onupdate=datetime.datetime.now,
)]




__all__ = ["Phonebook"]

from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk
from apps.schemas.contacts import SchemaPhonebook

fio = Annotated[str | None, mapped_column(comment="ФИО")]



class Persons(Base):
    __tablename__ = "persons"
    __table_args__ = {"comment": "Ответственное лицо"}

    # pydantic_schema = SchemaPhonebook
    # pydantic_schema_id = SchemaPhonebook

    id: Mapped[intpk]
    name: Mapped[fio]
    phone: Mapped[str | None] = mapped_column(comment="Телефон")

# 89221234567
# 89221234568
# 89221234569
# 89221234570
# 89221234571
# 89221234572
# 89221234573
# 89221234574
# 89221234575
# 89221234576


    # info: Mapped[list["Info"] | None] = relationship(
    #     back_populates = __tablename__,
    #     # secondary="responsible",
    # )

    # employeeFullName: Mapped[str | None] = mapped_column(comment="ФИО")
    # departmentName: Mapped[str | None] = mapped_column(comment="Подразделение")
    # staffPosName: Mapped[str | None] = mapped_column(comment="Должность")
    # phone: Mapped[str | None] = mapped_column(comment="Телефон.:")
    # phoneInternal: Mapped[str | None] = mapped_column(comment="Тел. внутр.:")
    # phoneMobile: Mapped[str | None] = mapped_column(comment="Тел. мобил.:")
    # numberCabinet: Mapped[str | None] = mapped_column(comment="Номер кабинета")
    # username: Mapped[str | None] = mapped_column(comment="Имя пользователя")
    # house: Mapped[str | None] = mapped_column(comment="Здание")

    # responsible: Mapped[list["Responsible"]] = relationship(back_populates = __tablename__)

    # info: Mapped[list["Info"] | None] = relationship(
    #     back_populates = __tablename__,
    #     # secondary="responsible",
    #     # lazy="joined"
    # )


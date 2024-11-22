__all__ = ["Phonebook"]

from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import strpk, intpk
from apps.schemas.contacts import SchemaPhonebook



class Phonebook(Base):
    __tablename__ = "phonebook"
    __table_args__ = {"comment": "Телефонный справочник"}

    pydantic_schema = SchemaPhonebook
    pydantic_schema_id = SchemaPhonebook

    id: Mapped[strpk]
    employeeFullName: Mapped[str | None] = mapped_column(comment="ФИО")
    departmentName: Mapped[str | None] = mapped_column(comment="Подразделение")
    staffPosName: Mapped[str | None] = mapped_column(comment="Должность")
    phone: Mapped[str | None] = mapped_column(comment="Телефон.:")
    phoneInternal: Mapped[str | None] = mapped_column(comment="Тел. внутр.:")
    phoneMobile: Mapped[str | None] = mapped_column(comment="Тел. мобил.:")
    numberCabinet: Mapped[str | None] = mapped_column(comment="Номер кабинета")
    username: Mapped[str | None] = mapped_column(comment="Имя пользователя")
    house: Mapped[str | None] = mapped_column(comment="Здание")

    # responsible: Mapped[list["Responsible"]] = relationship(back_populates = __tablename__)

    # info: Mapped[list["Info"] | None] = relationship(
    #     back_populates = __tablename__,
    #     # secondary="responsible",
    #     # lazy="joined"
    # )


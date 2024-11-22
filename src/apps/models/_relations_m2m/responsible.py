__all__ = ["Responsible"]

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.dependencies.dep_models import intpk, name
from apps.schemas.responsible import Schema_responsible



class Responsible(Base):
    __tablename__ = "responsible"
    __table_args__ = {"comment": "Ответственные лица"}

    pydantic_schema = Schema_responsible
    pydantic_schema_id = Schema_responsible

    # id: Mapped[intpk]

    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"),
        primary_key=True,
        comment="ОБЩАЯ ИНФОРМАЦИЯ"
    )
    signers_type_id: Mapped[int] = mapped_column(
        ForeignKey("signers_type.id", ondelete="CASCADE"), 
        primary_key=True,
        comment="Роль"

    )
    persons_id: Mapped[str] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"), 
        # primary_key=True,
        comment="ФИО"

    )
    # phonebook_id: Mapped[str] = mapped_column(
    #     ForeignKey("phonebook.id", ondelete="CASCADE"), 
    #     primary_key=True,
    #     comment="ФИО"

    # )
    
    # phonebook: Mapped["Phonebook"] = relationship(back_populates = __tablename__)
    # signers_type: Mapped["Signers_type"] = relationship(back_populates = __tablename__)
    # # signers_type: Mapped[list["Signers_type"]] = relationship(back_populates = __tablename__, lazy="joined")

    # info: Mapped[list["Info"]] = relationship(
    #     back_populates = __tablename__,
    #     # secondary="responsible",
    # )    
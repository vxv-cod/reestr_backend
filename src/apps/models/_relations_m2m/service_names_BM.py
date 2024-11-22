__all__ = ["Service_names_BM"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from apps.db import Base
from apps.schemas.service_names_BM import Schema_service_names_BM



class Service_names_BM(Base):
    __tablename__ = "service_names_BM"
    __table_args__ = {"comment": "Имена BM"}

    pydantic_schema = Schema_service_names_BM
    pydantic_schema_id = Schema_service_names_BM

    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"),
        primary_key=True,
    )
    names_BM_id: Mapped[int] = mapped_column(
        ForeignKey("names_BM.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Наименование"
    )

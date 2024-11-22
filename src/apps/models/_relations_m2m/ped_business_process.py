__all__ = ["Relations_software"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.db import Base
from apps.schemas.ped_biseness import Schema_ped_business_process



class Ped_business_process(Base):
    __tablename__ = "ped_business_process"
    __table_args__ = {"comment": "Бизнесс процессы"}

    pydantic_schema = Schema_ped_business_process
    pydantic_schema_id = Schema_ped_business_process

    info_id: Mapped[int] = mapped_column(
        ForeignKey("info.id", ondelete="CASCADE"),
        primary_key=True,
        comment="info_id"
    )
    business_process_id: Mapped[str] = mapped_column(
        ForeignKey("business_process.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Шифр"
    )

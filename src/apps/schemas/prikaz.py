import datetime
from apps.schemas.__basemodel import Base_Model


class SchemaPrikaz(Base_Model):
    doc_file_id: int
    date: datetime.date
    nomer: str
    

class SchemaPrikaz_ID(SchemaPrikaz):
    id: int

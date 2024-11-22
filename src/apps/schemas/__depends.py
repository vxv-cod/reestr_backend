from typing import Annotated
from fastapi import Depends, Form, File, UploadFile

from apps.schemas.__basemodel import Base_Model
from apps.schemas.file_data import Schema_file_data, Schema_file_data_ID, Schema_upload_pdf


dep_file_data = Annotated[Schema_file_data_ID, Depends()]
dep_upload_pdf = Annotated[Schema_upload_pdf, Form(...)]
dep_UploadFile = Annotated[UploadFile, File(...)]

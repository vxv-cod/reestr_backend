__all__ = ["all_routers"]

from apps.repositories.repo_api import (Api_default, Api_frontend_store)
from apps.models import models_clases

from apps.models._base.doc_file import Doc_file


all_routers = [
    Api_frontend_store("frontend").router,
    # Api_doc_file_options(Doc_file).router,
    *[Api_default(model_orm).router for model_orm in models_clases]
]
import sys
# from rich import print
from apps.db import Base
from utils.funcs import find_classes

from .references import *
from ._base import *
from ._relations_m2m import *


models_clases = find_classes(__name__)

# __all__ = ["models_clases"]

# import os, pkgutil
# moduls = [module for x, module, e in  pkgutil.iter_modules([os.path.dirname(__file__)], os.path.dirname(__file__) + '\\')]
# __all__ = [module for pack in moduls for _, module, _ in  pkgutil.iter_modules([pack])]
# print("__all__")
# print(__all__)



# class Models_dict:
#     ...    

# for cls in models_clases:
#     setattr(Models_dict, cls.__tablename__, cls)


# print(dir(Models_dict))

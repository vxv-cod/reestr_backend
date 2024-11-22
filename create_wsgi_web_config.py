import os
import pathlib
import sys
from a2wsgi.asgi import ASGIMiddleware
from importlib import import_module

sys.path.insert(1, os.getcwd() + r"\src")

def work(module_name):
    p = pathlib.Path(__file__)
    server_name = f"{p.parents[1].name}_{p.parents[0].name}"

    directory = os.getcwd()
    # name_base_direct = directory.rsplit("\\")[-1]
    name_base_direct = server_name
    '''Создаем директорю с файлом для логов'''
    fullname = f'{directory}\LogFiles\wfastcgi.log'

    os.makedirs(os.path.dirname(fullname), exist_ok=True)  # Создаём структуру каталогов
    open(fullname, 'a').close()  # И вот появился файл

    PYTHONPATH = directory + r'\src'
    name_app = ''
    module = import_module(module_name)
    print(module)
    for name in dir(module):
        var = getattr(module, name)
        if hasattr(var, '__class__') and isinstance(var, ASGIMiddleware):
            name_app = name

    print('name_app_ASGIMiddleware = ', name_app)

    test = rf'''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <remove name="{name_base_direct}" />
            <add name="{name_base_direct}" path="*" verb="*" modules="FastCgiModule" 
                scriptProcessor="{directory}\venv\Scripts\python.exe|{directory}\venv\Scripts\wfastcgi.exe" 
                resourceType="Unspecified" 
                requireAccess="Script" 
            />
        </handlers> 
    </system.webServer>
    <appSettings>
        <add key="PYTHONPATH" value="{PYTHONPATH}"/>
        <add key="WSGI_HANDLER" value="{module_name}.{name_app}" />
        <add key="WSGI_LOG" value="{directory}\LogFiles\wfastcgi.log"/>
    </appSettings>
</configuration>
'''
    return test


if __name__ == '__main__':
    module_name = 'main'
    with open("web.config", "w") as file:
        file.write(work(module_name))

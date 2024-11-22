@ECHO off 
chcp 65001

IF EXIST "%cd%\venv" (
	CALL venv\Scripts\activate.bat
	CALL py -V
	ECHO Виртуальное окружение активировано в папке : %cd%
	CALL pip list
	CALL python create_wsgi_web_config.py
) ELSE (echo Папка с именем "venv" не найдена)

CMD 

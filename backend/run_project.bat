@echo off

echo Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate

echo Instalando dependencias...
pip install django djangorestframework djangorestframework-simplejwt pillow rembg mysqlclient django-cors-headers

echo Rodando migrations...
cd django_project
python manage.py makemigrations
python manage.py migrate

echo Populando banco de dados...
cd ..
python scripts/database_seed.py

echo Iniciando servidor...
cd django_project
python manage.py runserver

pause

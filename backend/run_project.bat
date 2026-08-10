@echo off

echo entrando no espaço virtual
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

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

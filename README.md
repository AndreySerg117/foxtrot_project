# foxtrot_project

# setup git
git init
git remote add origin SSH
git pull origin main

# setup uv
uv init backend
cd .\backend\
uv add django
uv run django-admin startproject app

# run project
uv run python manage.py runserver
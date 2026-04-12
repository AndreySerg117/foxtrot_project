# foxtrot_project

# setup git
git init
git remote add origin SSH
git pull origin main

# setup uv
uv init backend
cd .\backend\
uv add django, uv add logtail python
uv run django-admin startproject app, uv run -m app.main

# run project
uv run python manage.py runserver

# migrate
uv run python manage.py startapp users 
uv run python manage.py makemigrations 
uv run python manage.py migrate
uv run python manage.py createsuperuser

# css
python manage.py collectstatic

# tailwind
- add in app templates directory
- add in app static directory
- add it to settings_static_templates.py  - it is just separate block to manage 
- in templates add base.html https://docs.djangoproject.com/en/5.2/ref/templates/language/#:~:text=base.html%E2%80%9D.
- install node and npm
- https://tailwindcss.com/docs/installation/tailwind-cli
- \Desktop\groupLevel3_django> cd .\backend\app\
- npm install tailwindcss @tailwindcss/cli
- add files to git
- add watch:css script to packege.json
- npm run watch:css

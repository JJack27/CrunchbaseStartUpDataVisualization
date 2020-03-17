release: python3 datavisual/manage.py makemigrations
release: python3 datavisual/manage.py migrate
web: gunicorn --pythonpath datavisual/ datavisual.wsgi
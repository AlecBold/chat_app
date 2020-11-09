/*web: gunicorn src.chat_project.wsgi —log-file -*/
web: python3 src/manage.py runserver 0.0.0.0:$PORT
release: python3 src/manage.py migrate

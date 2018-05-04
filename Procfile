release: python manage.py flush
release: python manage.py makemigrations codedoor
release: python manage.py migrate
web: gunicorn mysite.wsgi --log-file -
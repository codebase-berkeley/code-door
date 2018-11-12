release: python manage.py flush
release: python manage.py makemigrations codedoor
release: python manage.py migrate
release: python manage.py loaddata codedoor/fixtures/companies.json
web: gunicorn mysite.wsgi --log-file -
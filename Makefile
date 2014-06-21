# Core tasks
run:
	python manage.py runserver

gunicorn:
	gunicorn smsbank.wsgi

# Setup tasks
init:
	pip install -r requirements/dev.txt
	cd etc && npm install && bower install && grunt build
	python manage.py collectstatic --noinput

static:
	cd etc && grunt build
	python manage.py collectstatic --noinput

update:
	pip install -r requirements/dev.txt
	cd etc && bower update

# Utlity tasks
purge:
	rm -rf venv/
	rm -rf etc/node_modules/
	rm -rf etc/bower_modules/
	rm -rf etc/dist/
	rm -rf etc/static_collected/

# Core tasks
init:
	pip install -r requirements/dev.txt
	cd etc && npm install && bower install && grunt build
	cd - && python manage.py collectstatic

static:
	cd etc && grunt build
	cd - && python manage.py collectstatic

update:
	pip install -r requirements/dev.txt
	cd etc && bower update

run:
	python manage.py runserver

# Utlity tasks
purge:
	rm -rf venv/
	rm -rf etc/node_modules/
	rm -rf etc/bower_modules/
	rm -rf etc/dist/
	rm -rf etc/static_collected/

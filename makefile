PSQL = psql
CMD = python3 manage.py
APP = models 

## delete and create a new empty database
#clear_db:
#	@echo Clear Database
#	dropdb --if-exists $(PGDATABASE)
#	createdb

# create alumnodb super user
create_super_user:
	$(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('alumnodb', 'admin@myproject.com', 'alumnodb')"

populate:
	@echo populate database
	$(CMD) populate

runserver:
	$(CMD) runserver

update_models:
	$(CMD) makemigrations $(APP)
	$(CMD) migrate

#reset_db: clear_db update_models create_super_user

static:
	@echo manage.py collectstatic
	python3 ./manage.py collectstatic

fully_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations $(APP) 
	python3 ./manage.py migrate

test_authentication:
	$(CMD) test models.test_authentication --keepdb

test_model:
	$(CMD) test models.test_models --keepdb

test_services:
	$(CMD) test create.test_services --keepdb



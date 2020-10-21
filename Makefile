BASH=bash -l -c
PROJECT=blog_web

build:
	docker-compose build

up:
	docker-compose up -d

run: up
	docker-compose exec $(PROJECT) ./manage.py runserver 0.0.0.0:8000

clean:
	docker-compose stop && docker-compose rm -f

stop:
	docker-compose stop

start:
	docker-compose start

ps:
	docker-compose ps

restart: stop start ps


migrate:
	docker-compose exec $(PROJECT) ./manage.py migrate

pipi:
	docker-compose exec $(PROJECT) pip install -r requirements.txt

createsuperuser:
	docker-compose exec $(PROJECT) ./manage.py createsuperuser

bash:
	docker-compose exec $(PROJECT) bash

CMD=
manage:
	docker-compose exec $(PROJECT) ./manage.py $(CMD)

shell:
	docker-compose exec $(PROJECT) ./manage.py shell

makemigrations:
	docker-compose exec $(PROJECT) ./manage.py makemigrations

test:
	docker-compose exec $(PROJECT) ./manage.py test

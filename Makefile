api:
	uvicorn app.main:app --reload
celery:
	celery -A app.tasks.tasks:celery worker --loglevel=INFO
flower:
	celery -A app.tasks.tasks:celery flower
build:
	sudo -S docker compose -f docker-compose.yanl build
up:
	sudo -S docker compose -f docker-compose.yaml up -d
down:
	sudo -S docker compose -f docker-compose.yaml down && sudo docker network prune --force
	
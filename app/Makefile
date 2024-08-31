.PHONY: start-venv migrate migrate-new clean db view-db install-prod install-dev dev, down

start-venv:
	pipenv shell

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

downgrade-all:
	alembic downgrade base

migrate-new:
	@echo "Enter migration name: "; \
	read name; \
	alembic revision --autogenerate -m "$$name"

db:
	docker container run --name my_auth_db -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=my_auth -e POSTGRES_USER=user -d -p 5432:5432 postgres:13
	docker container run --name my_auth_fstore -d -p 6379:6379 redis:7

view-db:
	docker container exec -it my_auth_db psql -U user -d my_auth -w

view-fstore:
	docker container exec -it my_auth_fstore redis-cli

clean:
	docker container stop my_auth_db
	docker container rm my_auth_db -v
	docker container stop my_auth_fstore
	docker container rm my_auth_fstore -v

install-prod:
	pipenv install

install-dev:
	pipenv install --dev

dev:
	uvicorn main:app --reload --host localhost --port 8000 --ssl-keyfile ../certs/key.pem --ssl-certfile ../certs/cert.pem

	



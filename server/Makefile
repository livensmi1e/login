.PHONY: start-venv migrate migrate-new clean db view-db install-prod install-dev dev

start-venv:
	pipenv shell

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

migrate-new:
	@echo "Enter migration name: "; \
	read name; \
	alembic revision --autogenerate -m "$$name"

db:
	docker container run --name my_auth_db -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=my_auth -e POSTGRES_USER=user -d -p 5432:5432 postgres:13

view-db:
	docker container exec -it my_auth_db psql -U user -d my_auth -w

clean:
	docker container stop my_auth_db
	docker container rm my_auth_db -v

install-prod:
	pipenv install

install-dev:
	pipenv install --dev

dev:
	fastapi dev main.py --reload --host 0.0.0.0 --port 8000

	



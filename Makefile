update-deps:
	pip install poetry && poetry install

revision:
	cd src/app/ && alembic revision --autogenerate --rev-id $(id) --message $(m)

migrate:
	cd src/app/ && alembic upgrade head

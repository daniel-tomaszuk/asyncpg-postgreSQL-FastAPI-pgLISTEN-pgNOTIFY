update-deps:
	pip install poetry && poetry install

revision:
	cd src/app/ && alembic revision --autogenerate --rev-id $(id) --message $(m)

migrate:
	cd src/app/ && alembic upgrade head

locust:
	locust -f tests/locust/locustfile.py

locust-master:
	locust -f tests/locust/locustfile.py --master

locust-worker:
	locust -f tests/locust/locustfile.py --worker

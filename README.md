# asyncpg-postgreSQL-FastAPI-pgLISTEN-pgNOTIFY


# TODO:
1. Use PostgreSQL, alembic, SQLAlchemy, GINO (https://python-gino.org/docs/en/1.0/tutorials/fastapi.html) to setup DB and connect app with it. Use async connector only! [DONE]
2. Create socket handlers in the app so later it's possible to use Postgres pgLISTEN-pgNOTIFY events. [DONE]
3. Create alembic migration with required Postgres plugin (hstore: https://www.postgresql.org/docs/13/hstore.html)installation and proper SQL triggers. [WONT DO]
4. Handle LRU cache within BE app. Update cache when data in DB is being updated - socket pgLISTEN / pgNOTIFY. [DONE]
5. Create some CRUD endpoints and perform load testing (by hand or with tool - ex. Locust).

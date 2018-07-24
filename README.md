## Useful commands:

Seed the database with commands.json:

```python manage.py loaddata commands```

To Create PostgreSQL database:

```
pipenv install psycopg2

brew install postgresql --with-python

brew services start postgresql
OR
pg_ctl -D /usr/local/var/postgres start

createdb

psql -h localhost

In psql shell:
# Nigel=# CREATE USER Nigel;
# CREATE ROLE
# Nigel=# CREATE DATABASE commands_db OWNER Nigel;
# CREATE DATABASE

python manage.py migrate
```
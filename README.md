## Viewing/editing game database files
#### GET/POST to view and create new things
```
http://localhost:8000/abilities/
```
#### PUT/DELETE to view and update or delete existing things
```
http://localhost:8000/abilities/1
```

## Useful commands:

Backup the database:
```
./backup_database.sh
```

Load from database backup:
```
pipenv run python manage.py syncdata full_backup.json
```

Seed the database with commands.json:

```
`python manage.py loaddata commands
```

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

## Use curl to send POST requests
```curl --data "test_val=test123" http://127.0.0.1:8888/api/input_command/```

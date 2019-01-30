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

# Use curl to send POST requests
```curl --data "test_val=test123" http://127.0.0.1:8888/api/input_command/```

## Useful constructs:

WEAPON_PROTOTYPES = {
    "weapon": {
        "typeclass": "evennia.contrib.tutorial_world.objects.Weapon",
        "key": "Weapon",
        "hit": 0.2,
        "parry": 0.2,
        "damage": 1.0,
        "magic": False,
        "desc": "A generic blade."},
    "knife": {
        "prototype": "weapon",
        "aliases": "sword",
        "key": "Kitchen knife",
        "desc": "A rusty kitchen knife. Better than nothing.",
        "damage": 3}
}
#!/usr/bin/env bash

python manage.py dumpdata --indent 2 > full_backup.json

python manage.py dumpdata --indent 2 character.character > character/fixtures/character.json
python manage.py dumpdata --indent 2 character.playerclasses > character/fixtures/playerclasses.json
python manage.py dumpdata --indent 2 character.abilities > character/fixtures/abilities.json
python manage.py dumpdata --indent 2 character.abilityeffects > character/fixtures/abilityeffects.json
python manage.py dumpdata --indent 2 character.abilityenhancements > character/fixtures/abilityenhancements.json

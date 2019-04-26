import os
from django.test import TestCase
from actions_api.combat import do_combat_round
from character.models import Character, PlayerClasses


class AnimalTestCase(TestCase):
    fixtures = [os.path.join("/Users", "Nigel", "HOBBY_PROJECTS", "GAME", "world", "full_backup.json")]

    player = Character.objects.get(pk=1)
    player_class = PlayerClasses.objects.get(player_class=player.character_class)
    target = Character.objects.get(pk
    def test_combat_round(self):
        """
        A round of combat is done successfully

        """
        # Arrange=2)
        target_class = PlayerClasses.objects.get(player_class=target.character_class)

        attack = 'attack'

        # Perform a round of combat
        combat_result = do_combat_round(player=player,
                                        target=target,
                                        attack_type=attack)

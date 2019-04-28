import os
from django.test import TestCase
from actions_api.combat import do_combat_round
from character.models import Character, PlayerClasses


class AnimalTestCase(TestCase):
    fixtures = [os.path.join("/Users", "Nigel", "HOBBY_PROJECTS", "GAME", "world", "full_backup.json")]

    def test_combat_round(self):
        """
        A round of combat is done successfully

        """
        # Arrange
        player = Character.objects.get(pk=1)
        player_class = PlayerClasses.objects.get(player_class=player.character_class)
        target = Character.objects.get(pk=2)
        target_class = PlayerClasses.objects.get(player_class=target.character_class)
        attack = 'attack'
        expected_player_hp = 0
        expected_target_hp = 100

        # Act
        # Perform a round of combat
        player, target = do_combat_round(player=player,
                                         target=target,
                                         player_attack_type=attack)

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)

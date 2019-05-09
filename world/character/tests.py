import mock
import os
from django.test import TestCase
from actions_api.combat import do_combat_round
from character.models import Character, StatusEffects


class CombatTests(TestCase):
    fixtures = [os.path.join("/Users", "Nigel", "HOBBY_PROJECTS", "GAME", "world", "full_backup.json")]

    @mock.patch('actions_api.combat.randint')
    def test_combat_round(self, mocked_randint):
        """
        A round of combat is done successfully

        """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        attack = 'attack'
        expected_player_hp = 0
        expected_target_hp = 100

        mocked_randint.return_value = 2

        # Act
        # Perform a round of combat
        player, target = do_combat_round(player=player,
                                         target=target,
                                         player_attack_type=attack)

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)

    @mock.patch('actions_api.combat.randint')
    def test_healing(self, mocked_randint):
        """
        A round of combat is done successfully

        """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        attack = 'attack'
        expected_player_hp = 0
        expected_target_hp = 100

        mocked_randint.return_value = 2

        # Act
        # Perform a round of combat
        player, target = do_combat_round(player=player,
                                         target=target,
                                         player_attack_type=attack)

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)

    @mock.patch('actions_api.combat.randint')
    def test_enhancement(self, mocked_randint):
        """
        A round of combat is done successfully

        """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        attack = 'disrupt'
        expected_player_hp = 100
        expected_target_hp = 0
        expected_status_list = [(1, 1, 'prone', 1)]

        mocked_randint.return_value = 2

        # Act
        # Perform a round of combat
        player, target = do_combat_round(player=player,
                                         target=target,
                                         player_attack_type=attack,
                                         enhanced=True)
        status_effects_list = list(StatusEffects.objects.all().values_list())

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)
        self.assertListEqual(expected_status_list, status_effects_list)

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
        Player wins with:
            Attack (1) beats Area (0)

        """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        attack = 'attack'
        expected_player_hp = 100
        expected_target_hp = 0

        mocked_randint.return_value = 0

        # Act
        # Perform a round of combat
        player, target = do_combat_round(player=player,
                                         target=target,
                                         player_attack_type=attack)

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)

    @mock.patch('actions_api.combat.randint')
    def test_matchups(self, mocked_randint):
        """
        Test that the following holds true:

        Area (0) beats Disrupt (4) and Dodge (3)
        Attack (1) beats Disrupt (4) and Area (0)
        Block (2) beats Attack (1) and Area (0)
        Dodge (3) beats Attack (1) and Block (2)
        Disrupt (4) beats Block (2) and Dodge (3)

        """
        # Arrange
        attacks = ['area', 'attack', 'block', 'disrupt', 'dodge']
        expected_player_hps = [[0, 0, 0, 100, 100],
                               [100, 0, 0, 0, 100],
                               [100, 100, 0, 0, 0],
                               [0, 0, 100, 100, 0],
                               [0, 100, 100, 0, 0]]
        expected_target_hps = [[0, 100, 100, 0, 0],
                               [0, 0, 100, 100, 0],
                               [0, 0, 0, 100, 100],
                               [100, 100, 0, 0, 0],
                               [100, 0, 0, 0, 100]]

        # Act
        # Perform a round of combat
        for i, attack in enumerate(attacks):
            for j, target_attack_number in enumerate(range(0, 5)):
                mocked_randint.return_value = target_attack_number
                player = Character.objects.get(pk=1)
                target = Character.objects.get(pk=2)
                player, target = do_combat_round(player=player,
                                                 target=target,
                                                 player_attack_type=attack)
                # Assert
                self.assertEqual(player.hit_points, expected_player_hps[i][j])
                self.assertEqual(target.hit_points, expected_target_hps[i][j])

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
        expected_status_list = [(1, 2, 'prone', 1)]

        mocked_randint.return_value = 2  # Block

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

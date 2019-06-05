import os
from django.test import TestCase
from actions_api.combat import Combat
from character.models import Character, StatusEffects


class CombatTests(TestCase):
    fixtures = [os.path.join("/Users", "Nigel", "HOBBY_PROJECTS", "GAME", "world", "full_backup.json")]

    def test_combat_round(self):
        """
        A round of combat is done successfully

        Player wins with:
            Attack (1) beats Area (0)
        """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        expected_player_hp = 100
        expected_target_hp = 0

        object_to_test = Combat(player=player,
                                target=target,
                                player_attack_type="attack",
                                target_attack_type="area")

        # Act
        # Perform a round of combat
        player, target = object_to_test.do_combat_round()

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)

    def test_matchups(self):
        """
        Test that the following holds true:

        Area beats Disrupt and Dodge
        Attack beats Disrupt and Area
        Block beats Attack and Area
        Disrupt beats Block and Dodge
        Dodge beats Attack and Block
        """
        # Arrange
        player_attacks = ['area', 'attack', 'block', 'disrupt', 'dodge']
        target_attacks = ['area', 'attack', 'block', 'disrupt', 'dodge']
        expected_player_hps = [[0, 0, 0, 100, 100],
                               [100, 0, 0, 100, 0],
                               [100, 100, 0, 0, 0],
                               [0, 0, 100, 0, 100],
                               [0, 100, 100, 0, 0]]
        expected_target_hps = [[0, 100, 100, 0, 0],
                               [0, 0, 100, 0, 100],
                               [0, 0, 0, 100, 100],
                               [100, 100, 0, 0, 0],
                               [100, 0, 0, 100, 0]]

        # Act
        # Perform a round of combat
        for i, player_attack in enumerate(player_attacks):
            for j, target_attack in enumerate(target_attacks):
                player = Character.objects.get(pk=1)
                target = Character.objects.get(pk=2)
                object_to_test = Combat(player=player,
                                        target=target,
                                        player_attack_type=player_attack,
                                        target_attack_type=target_attack)

                player, target = object_to_test.do_combat_round()

                # Assert
                self.assertEqual(player.hit_points, expected_player_hps[i][j])
                self.assertEqual(target.hit_points, expected_target_hps[i][j])

    # TODO: Make a healing ability and alter this test
    def test_healing(self):
        """ A round of combat with healing is done successfully """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        expected_player_hp = 0
        expected_target_hp = 100

        object_to_test = Combat(player=player,
                                target=target,
                                player_attack_type="disrupt",
                                target_attack_type="area")

        # Act
        # Perform a round of combat
        player, target = object_to_test.do_combat_round()

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)

    def test_enhancement(self):
        """ A round of combat is done successfully """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        expected_player_hp = 100
        expected_target_hp = 0
        expected_status_list = [(1, 2, 'prone', 1)]

        # Act
        # Perform a round of combat
        object_to_test = Combat(player=player,
                                target=target,
                                player_attack_type="disrupt",
                                target_attack_type="block",
                                enhanced=True)

        # Act
        # Perform a round of combat
        player, target = object_to_test.do_combat_round()
        status_effects_list = list(StatusEffects.objects.all().values_list())

        # Assert
        self.assertEqual(player.hit_points, expected_player_hp)
        self.assertEqual(target.hit_points, expected_target_hp)
        self.assertListEqual(expected_status_list, status_effects_list)

    def test_check_and_apply_status(self):
        """ Check that check_and_apply_status() updates the combat rules """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        expected_rules = {"area": {"beats": ["disrupt", "dodge", "block"],
                                   "loses": ["attack"]},
                          "attack": {"beats": ["disrupt", "area"],
                                     "loses": ["block", "dodge"]},
                          "block": {"beats": ["area", "attack"],
                                    "loses": ["disrupt", "dodge"]},
                          "disrupt": {"beats": ["block", "dodge"],
                                      "loses": ["attack", "area"]},
                          "dodge": {"beats": ["attack", "block"],
                                    "loses": ["area", "disrupt"]}}

        object_to_test = Combat(player=player,
                                target=target,
                                player_attack_type="disrupt",
                                target_attack_type="block",
                                enhanced=True)

        # Apply a status effect
        _ = object_to_test.do_combat_round()

        # Act
        # Check and apply the status effect
        _ = object_to_test.check_and_apply_status()

        # Assert
        self.assertEqual(object_to_test.rules, expected_rules)

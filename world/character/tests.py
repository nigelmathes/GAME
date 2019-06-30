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
        expected_player_hp = player.hit_points
        expected_target_hp = target.hit_points - 100

        expected_player_ex = 50
        expected_target_ex = 100

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
        self.assertEqual(player.ex_meter, expected_player_ex)
        self.assertEqual(target.ex_meter, expected_target_ex)

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

                # Assert - The 400 is a kluge because I don't want to remake the list above
                self.assertEqual(player.hit_points, 400 + expected_player_hps[i][j])
                self.assertEqual(target.hit_points, 400 + expected_target_hps[i][j])

    # TODO: Make a healing ability and alter this test
    def test_healing(self):
        """ A round of combat with healing is done successfully """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        expected_player_hp = player.hit_points - 100
        expected_target_hp = target.hit_points

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
        # Arrange - add statuses here
        expected_statuses = [[2, "prone", 1],
                             [2, "disorient", 1]]
        ability_combos = [["disrupt", "block"],
                          ["area", "disrupt"]]

        # Act
        for expected_status, ability_combo in zip(expected_statuses, ability_combos):
            player = Character.objects.get(pk=1)
            target = Character.objects.get(pk=2)
            expected_player_hp = player.hit_points
            expected_target_hp = target.hit_points - 100

            # Perform a round of combat
            object_to_test = Combat(player=player,
                                    target=target,
                                    player_attack_type=ability_combo[0],
                                    target_attack_type=ability_combo[1],
                                    player_enhanced=True)

            # Act
            # Perform a round of combat
            player, target = object_to_test.do_combat_round()
            status_effects_list = list(StatusEffects.objects.all().values_list())

            # Assert
            self.assertEqual(player.hit_points, expected_player_hp)
            self.assertEqual(target.hit_points, expected_target_hp)
            self.assertEqual(expected_status[0], status_effects_list[0][1])
            self.assertEqual(expected_status[1], status_effects_list[0][2])
            self.assertEqual(expected_status[2], status_effects_list[0][3])

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
                                player_enhanced=True)

        # Inflict a status effect
        _ = object_to_test.do_combat_round()

        # Act
        # Check and apply the status effect
        _ = object_to_test.check_and_apply_status()

        # Assert
        self.assertDictEqual(object_to_test.rules, expected_rules)

    def test_consume_status(self):
        """
        Check that check_and_apply_status() applies a status,
        updates the duration, and culls the database of 0 duration statuses
        """
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)

        object_to_test = Combat(player=player,
                                target=target,
                                player_attack_type="disrupt",
                                target_attack_type="block",
                                player_enhanced=True)

        # Inflict a status effect
        _ = object_to_test.do_combat_round()

        check_status_before_apply = StatusEffects.objects.filter(character_id=target.pk)
        self.assertTrue(check_status_before_apply.exists())

        # Act
        # Check and apply the status effect
        _ = object_to_test.check_and_apply_status()

        check_status_after_apply = StatusEffects.objects.filter(character_id=target.pk)
        self.assertFalse(check_status_after_apply.exists())

    def test_new_rules_combat_resolution(self):
        """ Check that new combat rules are resolved correctly"""
        # Arrange
        player = Character.objects.get(pk=1)
        target = Character.objects.get(pk=2)
        expected_outcome = "player_wins"
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
                                player_enhanced=True)

        # Act
        # Inflict a status effect
        _ = object_to_test.do_combat_round()

        # Check and apply the status effect
        new_rules, _, _ = object_to_test.check_and_apply_status()

        # Change the attack type to something that applies to the altered ruleset
        object_to_test.player_attack_type = "area"

        # Calculate the winner with the new rules
        result = object_to_test.calculate_winner()

        # Assert
        self.assertEqual(result, expected_outcome)
        self.assertDictEqual(new_rules, expected_rules)
        self.assertDictEqual(object_to_test.rules, expected_rules)

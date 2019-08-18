"""
Actions to perform for characters
"""
from random import choice
from typing import Union, Tuple

from django.db import transaction
from django.db.models import F, QuerySet

import actions_api.combat_effects as combat_effects
from character.models import PlayerClasses, Abilities, StatusEffects, Character


class Combat:
    """ Class to do one round of combat """
    CharacterType = Union[QuerySet, Character]
    AbilitiesType = Union[QuerySet, Abilities]

    def __init__(self, player: CharacterType,
                 target: CharacterType,
                 player_attack_type: str,
                 target_attack_type: str = choice(["area", "attack", "block", "disrupt", "dodge"]),
                 player_enhanced: bool = False) -> None:
        """
        Take in a player and target object and do a combat round

        :param player: First player, who is in the "left" position
        :param target: Second player, who is in the "right" position
        :param player_attack_type: area/attack/block/disrupt/dodge
        :param target_attack_type: area/attack/block/disrupt/dodge
        :param player_enhanced: Whether the left players' attack is enhanced or not
        """
        self.player = player
        self.target = target
        self.player_attack_type = player_attack_type
        self.target_attack_type = target_attack_type
        self.player_enhanced = player_enhanced

        self.rules = {"area": {"beats": ["disrupt", "dodge"],
                               "loses": ["attack", "block"]},
                      "attack": {"beats": ["disrupt", "area"],
                                 "loses": ["block", "dodge"]},
                      "block": {"beats": ["area", "attack"],
                                "loses": ["disrupt", "dodge"]},
                      "disrupt": {"beats": ["block", "dodge"],
                                  "loses": ["attack", "area"]},
                      "dodge": {"beats": ["attack", "block"],
                                "loses": ["area", "disrupt"]}}

        self.added_effects = list()

    def calculate_winner(self):
        """
        Function to calculate the winner

        :return: Outcome of combat
        """
        player_rules = self.rules[self.player_attack_type]

        if self.target_attack_type in player_rules['beats']:
            return "player_wins"
        elif self.target_attack_type in player_rules['loses']:
            return "target_wins"
        else:
            return "tie"

    def do_combat_round(self):
        """
        Function to complete one round of combat

        :return: Updated player, target objects

        Area (0) beats Disrupt (3) and Dodge (4)
        Attack (1) beats Disrupt (3) and Area (0)
        Block (2) beats Attack (1) and Area (0)
        Disrupt (3) beats Block (2) and Dodge (4)
        Dodge (4) beats Attack (1) and Block (2)
        """
        player_class = PlayerClasses.objects.get(player_class=self.player.character_class)
        target_class = PlayerClasses.objects.get(player_class=self.target.character_class)

        print(f"Player uses {self.player_attack_type},"
              f" target uses {self.target_attack_type}")

        # Check status effects and apply them to the rules of the game
        self.check_and_apply_status()

        # Apply added effects from the statuses - action here
        self.apply_added_effects()

        # Check if anyone died from added effects
        if self.check_dead():
            if self.player.hit_points == 0:
                print("Player died.")
            else:
                print("Target died.")
            return self.player, self.target

        # Determine the winner
        outcome = self.calculate_winner()

        # Player wins!
        if outcome == "player_wins":
            ability = Abilities.objects.get(class_id=player_class, type=self.player_attack_type)
            self.collect_and_resolve_effects(ability, winner=self.player, loser=self.target, enhanced=self.player_enhanced)

            # Update EX meters
            self.player.ex_meter += 50
            self.target.ex_meter += 100

            print(f"Player wins! Using {ability} ({self.player_attack_type}) on {self.target}")

        # Target wins
        elif outcome == "target_wins":
            ability = Abilities.objects.get(class_id=target_class, type=self.target_attack_type)
            self.collect_and_resolve_effects(ability, winner=self.target, loser=self.player, enhanced=self.player_enhanced)

            # Update EX meters
            self.player.ex_meter += 100
            self.target.ex_meter += 50

            print(f"Target wins! Using {ability} ({self.target_attack_type}) on {self.player}")

        # Player and computer tie (clash)
        else:
            # Player's attack
            ability1 = Abilities.objects.get(class_id=player_class, type=self.player_attack_type)
            self.collect_and_resolve_effects(ability1, winner=self.player, loser=self.target, enhanced=self.player_enhanced)

            # Target's attack
            ability2 = Abilities.objects.get(class_id=target_class, type=self.target_attack_type)
            self.collect_and_resolve_effects(ability2, winner=self.target, loser=self.player, enhanced=self.player_enhanced)

            # Update EX meters
            self.player.ex_meter += 150
            self.target.ex_meter += 150

            print(f"Player and target tie! Using both {ability1} on {self.target} and {ability2} on {self.player}")

        print(f"Player HP after combat round: {self.player.hit_points}")
        print(f"Target HP after combat round: {self.target.hit_points}\n")

        return self.player, self.target

    def check_and_apply_status(self):
        """
        Function to check player and target status effects, and apply those effects before combat

        All status effect functions start with apply_ and take args (target, rules)
            e.g. apply_prone(target, rules):

        :return: Updated rules for combat based on effects
        """
        # Check status
        player_status_check = StatusEffects.objects.filter(character_id=self.player.pk).first()
        target_status_check = StatusEffects.objects.filter(character_id=self.target.pk).first()

        # Apply status effects to player if they exist
        if player_status_check:
            player_statuses = StatusEffects.objects.filter(character_id=self.player.pk)

            # Loop over statuses and apply them
            for status in player_statuses.values():
                self.player, \
                self.rules, \
                self.added_effects = getattr(combat_effects,
                                             'apply_' + status.name)(target=self.player,
                                                                     rules=self.rules,
                                                                     added_effects=self.added_effects,
                                                                     left=True)

            # Decrease duration of status effects by 1 turn
            with transaction.atomic():
                player_statuses.update(duration=F('duration') - 1)

            # Delete status effects with 0 duration
            player_statuses.filter(duration=0).delete()

        # Apply status effects to target if they exist
        if target_status_check:
            target_statuses = StatusEffects.objects.filter(character_id=self.target.pk)

            # Loop over statuses and apply them
            for status in target_statuses:
                self.target, \
                self.rules, \
                self.added_effects = getattr(combat_effects,
                                             'apply_' + status.name)(target=self.target,
                                                                     rules=self.rules,
                                                                     added_effects=self.added_effects,
                                                                     left=False)

            # Decrease duration of status effects by 1 turn
            with transaction.atomic():
                target_statuses.update(duration=F('duration') - 1)

            # Delete status effects with 0 duration
            target_statuses.filter(duration=0).delete()

        return self.rules, self.added_effects

    @staticmethod
    def collect_and_resolve_effects(ability: AbilitiesType,
                                    winner: CharacterType,
                                    loser: CharacterType,
                                    enhanced: bool = False) -> Tuple[CharacterType, CharacterType]:
        """
        Function to go through the effects tied to a given ability
        and resolve the cumulative effect of all of them

        All ability effect functions start with inflict_ and take args (value, target)
            e.g. inflict_damage(value, target)

        :param ability: Queryset for the ability being evaluated, of the form:
                        Abilities.objects.get(class_id=target_class, type=player_attack_type)
        :param winner: The player using the ability
        :param loser: The target/enemy
        :param added_effects: Additional status enhancements to the ability
        :param enhanced: Boolean to tell if to enhance an attack

        :return: Cumulative effect and an update/save call to the database
        """
        translation_dictionary = {'target': loser, 'self': winner}

        # Call ability effect functions
        for effect in ability.ability_effects.values():
            translation_dictionary[effect['target']] = \
                getattr(combat_effects, 'inflict_' + effect['function'])(value=effect['value'],
                                                                         target=translation_dictionary[
                                                                             effect['target']])

        # Add enhancement if it exists
        if enhanced:
            for enhancement in ability.ability_enhancements.values():
                translation_dictionary[enhancement['target']] = \
                    getattr(combat_effects, 'inflict_' + enhancement['function'])(value=enhancement['value'],
                                                                                  target=translation_dictionary[
                                                                                      enhancement['target']])
        return winner, loser

    def apply_added_effects(self):
        """
        Method to apply things from the self.added_effects list

        :return: Updated player and target objects
        """
        # Call the added effect functions
        for added_effect in self.added_effects:
            added_effect['target'] = \
                getattr(combat_effects, 'inflict_' + added_effect['function'])(value=added_effect['value'],
                                                                               target=added_effect['target'])
            # Consume the effect by removing it
            self.added_effects.remove(added_effect)

        return self.player, self.target

    def check_dead(self):
        """
        Method to check if either player is dead

        :return: True if somebody is dead, else False
        """
        if self.player.hit_points <= 0:
            return True
        elif self.target.hit_points <= 0:
            return True
        else:
            return False

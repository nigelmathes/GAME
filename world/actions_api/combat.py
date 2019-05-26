"""
Actions to perform for characters

"""
from random import choice

import actions_api.combat_effects as combat_effects
from character.models import PlayerClasses, Abilities, StatusEffects


class Combat:
    """ Class to do one round of combat """
    def __init__(self, player, target,
                 player_attack_type,
                 target_attack_type=choice(["area", "attack", "block", "disrupt", "dodge"]),
                 enhanced=False):
        """
        Take in a player and target object and do a combat round

        :param player:
        :param target:
        :param player_attack_type:
        :param target_attack_type:
        :param enhanced:
        """
        self.player = player
        self.target = target
        self.player_attack_type = player_attack_type
        self.target_attack_type = target_attack_type
        self.enhanced = enhanced

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

    def calculate_winner(self):
        """
        Function to calculate the winner based upon SOMETHING

        :return: Outcome of combat
        """
        options_dict = self.rules[self.player_attack_type]

        for result, options in options_dict.items():
            if self.target_attack_type in options:
                if result == "beats":
                    return "player_wins"
                # result == "loses"
                else:
                    return "target_wins"

        # Return tie if result is not in options_dict
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

        # Check status effects and apply them to the rules of the game
        self.check_and_apply_status()
        self.check_and_apply_status()

        print(f"Player uses {self.player_attack_type},"
              f" target uses {self.target_attack_type}")

        # Determine the winner
        outcome = self.calculate_winner()

        # Player wins!
        if outcome == "player_wins":
            ability = Abilities.objects.get(class_id=player_class, type=self.player_attack_type)
            self.collect_and_resolve_effects(ability, winner=self.player, loser=self.target, enhanced=self.enhanced)
            print(f"Player wins! Using {ability} ({self.player_attack_type}) on {self.target}")

        # Target wins
        elif outcome == "target_wins":
            ability = Abilities.objects.get(class_id=target_class, type=self.target_attack_type)
            self.collect_and_resolve_effects(ability, winner=self.target, loser=self.player, enhanced=self.enhanced)
            print(f"Target wins! Using {ability} ({self.target_attack_type}) on {self.player}")

        # Player and computer tie (clash)
        else:
            # Player's attack
            ability1 = Abilities.objects.get(class_id=player_class, type=self.player_attack_type)
            self.collect_and_resolve_effects(ability1, winner=self.player, loser=self.target, enhanced=self.enhanced)

            # Target's attack
            ability2 = Abilities.objects.get(class_id=target_class, type=self.target_attack_type)
            self.collect_and_resolve_effects(ability2, winner=self.target, loser=self.player, enhanced=self.enhanced)
            print(f"Player and target tie! Using both {ability1} on {self.target} and {ability2} on {self.player}")

        print(f"Player HP after combat round: {self.player.hit_points}")
        print(f"Target HP after combat round: {self.target.hit_points}\n")

        return self.player, self.target

    def check_and_apply_status(self):
        """
        Function to check player and target status effects, and apply those effects before combat

        :return: Updated rules for combat based upon effects

        """
        player_statuses = self.player.status_effects
        target_statuses = self.target.status_effects

        pass

        #for status in player_statuses:
        #    pass

        #for status in target_statuses:
        #    pass

    @staticmethod
    def collect_and_resolve_effects(ability, winner, loser, enhanced=False):
        """
        Function to go through the effects tied to a given ability
        and resolve the cumulative effect of all of them

        :param ability: Queryset for the ability being evaluated, of the form:
                        Abilities.objects.get(class_id=target_class, type=player_attack_type)
        :param winner: The player using the ability
        :param loser: The target/enemy
        :param enhanced: Boolean to tell if to enhance an attack

        :return: Cumulative effect and an update/save call to the database

        """
        translation_dictionary = {'target': loser, 'self': winner}

        # Call effect functions
        for effect in ability.ability_effects.values():
            translation_dictionary[effect['target']] = \
                getattr(combat_effects, effect['function'])(value=effect['value'],
                                                            target=translation_dictionary[effect['target']])

        # Add enhancement if it exists
        if enhanced:
            for enhancement in ability.ability_enhancements.values():
                translation_dictionary[enhancement['target']] = \
                    getattr(combat_effects, enhancement['function'])(value=enhancement['value'],
                                                                     target=translation_dictionary[enhancement['target']])
        return winner, loser

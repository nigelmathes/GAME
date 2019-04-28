"""
Takes input commands and routes to a function which completes the action.

Imports from the subapp/combat.py file, and then calls functions within those files.

"""
from actions_api import combat
from character.models import Character
from character.models import PlayerClasses

from rasa_core_sdk import Action


class ActionAttack(Action):
    def name(self):
        return "action_attack"

    def run(self, dispatcher, tracker, domain):
        # Get target and attack information
        #player = tracker.get_slot('player_id')
        #target = tracker.get_slot('target_id')
        player = Character.objects.get(pk=1)
        player_class = PlayerClasses.objects.get(player_class=player.character_class)
        target = Character.objects.get(pk=2)
        target_class = PlayerClasses.objects.get(player_class=target.character_class)
        attack = tracker.get_slot('attack')

        # Perform a round of combat
        combat_result = combat.do_combat_round(player=player,
                                               target=target,
                                               player_attack_type=attack)

        return [combat_result]

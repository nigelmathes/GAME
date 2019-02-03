"""
Takes input commands and routes to a function which completes the action.

Imports from the subapp/character_actions.py file, and then calls functions within those files.

"""
from character import character_actions

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet


class ActionAttack(Action):
    def name(self):
        return "action_attack"

    def run(self, dispatcher, tracker, domain):
        target = tracker.get_slot('target')
        do_combat_round(type='attack', target=target)

        return []


class ActionCreateCharacter(Action):
    """
    Create a character from the character subapp.

    """

    def name(self):
        return "action_attack"

    def run(self, dispatcher, tracker, domain):
        character_actions.create_character()

        return []

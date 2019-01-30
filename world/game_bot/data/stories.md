## happy path
* greet              
  - utter_greet
* mood_great
  - utter_happy
* mood_affirm
  - utter_happy
* mood_affirm
  - utter_goodbye

## sad path 1 
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* mood_affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* mood_deny
  - utter_goodbye
  
## strange user
* mood_affirm
  - utter_happy
* mood_affirm
  - utter_unclear

## say goodbye
* goodbye
  - utter_goodbye

## area
* area
  - action_area

## attack
* attack
  - action_attack

## block
* block
  - action_block

## disrupt
* disrupt
  - action_disrupt

## dodge
* dodge
  - action_dodge

## run
* run
  - action_run

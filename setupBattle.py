import random
import sys
import csv
import argparse
import time

# Custom scripts
import monsterYamlParser as mYP
import battleHelperFunctions as bHF
import battle_csv_parser as bCP
#import create_helper_spreadsheet as cHS


# For debugging purposes:
import pdb

# In case we want to run GUI process in background
from PyQt5.QtCore import QRunnable, QObject

parser = argparse.ArgumentParser(description=''''Args to set up the
                battle. The only mandatory args is the path to the
                csv file and the number of player characters''')
parser.add_argument('-c', '--battle_csv', help="""Name of the csv defining
                the battle scenario""", required=True)
parser.add_argument('-p', '--players', type=str, action='append',
            help="Names of human players in battle", required=True)
#parser.add_argument('-f', metvar='F', help="""Path to the csv defining
#                       the battle scenario""")
#parser.add_argument('-c', metavar='C', type=str, action='append', nargs='+',
#                       help=)
#parser.add_argument('-t', metavar='T', type=str, action='append', nargs='+')
#parser.add_argument('-a', metvar='A', type=str, action='append', nargs='+')



class BattleScenario(object):
    '''Class that allows importing of creatures for battle, keeps track of
       initiatives and available attacks, and hitpoints of creatures involved
    '''

    def __init__(self, creatureDict, playerDict, use_gui=False):

        # Dict of creatures involved in the battle. The keys of the dict are
        # the creature IDs given by the DM, and the contents of the dict are
        # "Creature" objects (see monsterYamlParser.py)
        self.creatureDict = creatureDict

        # Dict of human players involved in the battle. The keys of the
        # dict are the player names, and the contents of the dict are
        # "Player" objects
        self.playerDict = playerDict
        self.player_list = []
        for player in playerDict.keys():
            self.player_list.append(player)

        self.foe_list = []

        self.ally_list = []

        self.neutral_list = []

        # ordered list of creatures based on their initiatives
        # (uninitialized until "rollInitiative" method is called)
        self.ordered_creature_list = []

        # Variable that keeps track of the challenge rating of the
        # battle. Rewards after the battle will be calculated based
        # on this number (see 'determine_battle_challenge_rating
        # method)
        self.challenge_rating = 0

        # Variable keeping track of whose turn we are on
        self.iterator = 0

        # Flag to let the creator know that the battle is done
        self.battleFlag = 0

        # Initialize battle messager object
        self.bMessager = battleMessages()

        # Flag telling us whether or not to use spreadsheet gui
        self.use_gui = use_gui


    def roll_initiative(self):
        '''Automatically rolls initiatives for all creatures involved in
           scenario
        '''

        # Creature container to be passed to ordering function
        creature_list = list()

        # Roll initiative for all npcs
        #pdb.set_trace()
        for creatureID in self.creatureDict.keys():
            creature = self.creatureDict[creatureID]
            # initiative: d20 + dex modifier
            #pdb.set_trace()
            try:
                dexterity = creature.abilities["DEXTERITY"]
                dex_modifier = bHF.get_ability_modifer(dexterity)

            except (KeyError, TypeError) as e:
                dex_modifier = 0

            creature.initiative = bHF.die_roll(1,20,dex_modifier)
            creature_list.append(creature)

        # Have the players roll for initiative
        for player_name in self.playerDict.keys():
            print(player_name)
            player = self.playerDict[player_name]
            print(self.bMessager.ask_player_to_roll_initiative(
                                    player_name))
            player.initiative = int(input("rolled initiative: "))
            # place in list of creatures
            creature_list.append(player)

        # return list of all creatures and players based on initiative
        self.ordered_creature_list = bHF.order_by_initiative(
                                    creature_list)
        return


    def list_by_allegiance(self):
        '''Initiated at beginning of battle scenario. Organizes
           all characters into lists based on allegiance. These
           lists will then be used to see what actions can be
           performed to others

           NOTE: These lists are not strict. Creatures can be
                 moved to other allegiance lists based on the
                 actions of the players
        '''
        self.ally_list = list()
        self.foe_list = list()
        self.neutral_list = list()
        for creature in self.ordered_creature_list:
            if creature.allegiance == 'ally':
                self.ally_list.append(creature)
            elif creature.allegiance == 'foe':
                self.foe_list.append(creature)
            else:
                self.neutral_list.append(creature)

        return


    def determine_challenge_rating(self):
        '''Determine the challenge rating of the battle based
           on the difficulty ratings of the creatures in the
           foe list.

           NOTE: Unlike the allegiance lists, this rating is
                 static. The challenge rating, and the subsequent
                 loot and xp awarded after the battle does not
                 change if the player characters are able to remove
                 enemies from the foe list (via convincing them
                 to change allegiance, forcing them to flee, etc.)
        '''
        challenge_rating = 0
        for creature in self.foe_list:
            challenge_rating = challenge_rating +  \
                        creature.challenge_rating
        self.challenge_rating = challenge_rating
        return


    def check_if_all_foes_dead(self):
        '''Internal check to see if all enemy npcs have been
           defeated
        '''
        for foe in self.foe_list:
            if foe.dead == False:
                return False

        return True


    def npc_action(self, npc_character):
        '''Allows npc character to take an action against other
           characters in the scenario, based on their allegiance.
           (player actions may cause their allegiance to change
           over the course of the battle
        '''
        # Initiate loop that terminates at end of NPC's turn
        npc_turn = True
        while npc_turn:

            # Pull out full dictionary of available actions
            print('\n',self.bMessager.npc_turn_initiate(npc_character.name))
            print('\n----------Available Attacks---------------\n')
            attacks_list = []
            attacks_dict = {}
            config_attacks = npc_character.actions['attacks']
            ########### NOTE: May change this later. ##############
            # Really inefficent to have to go through the keys for
            # the dicts returned by npc.character.attacks to find
            # the name of each spell AND THEN DEFINE A NEW DICT
            # WITH THOSE NAMES AS KEYS. There's got to be a better
            # way to set up the yaml file so we don't have to do
            # that...
            for attack in config_attacks:
                #pdb.set_trace()
                attack_name = attack['NAME']
                attacks_dict[attack_name] = attack

            try:
                for i, attack_type in enumerate(attacks_dict.keys()):
                    attacks_list.append(attack_type)
                    print('\n{0}) {1}'.format(i, attack_type))
            except TypeError:
                print("No attacks available")

            print('\n----------Available Spells----------------\n')
            spells_list = list()
            spells_dict = npc_character.actions['spells']
            for j, spell_type in enumerate(spells_dict.keys()):
                spells_list.append(spell_type)
                print('\n{0}) {1}'.format(j, spell_type))

            # Does the DM want to see a detailed description of the
            # actions presented?
            print('''\nDo you want to see more details of actions and
                     spells?
                     \nFormat A1-A# for actions
                     \nFormat S1-S# for spells
                     \ntype 'continue' to choose action
                  '''
                 )
            see_details = True
            while see_details:
                what_next = input('\nChoose action: ')

                if what_next[0] == 'A':
                    try:
                        idx = what_next[1]
                        print(attacks_list[idx]['DESCRIPTION'])
                    except KeyError:
                        print('\nError: index not recognized. Try again')
                        continue

                elif what_next[0] == 'S':
                    try:
                        idx = what_next[1]
                        print(spells_list[idx]['DESCRIPTION'])
                    except KeyError:
                        print('\nError: index not recognized. Try again')
                        continue

                elif what_next.lower() == 'continue':
                    break

                else:
                    print('\nError: input not recognized. Try again')
                    continue

            # Have the DM choose whether to case a spell, attack, or do
            # a DM directed action

            # Initiate a loop until the creature has exhausted all actions
            print("\nChoose what action to perform: ")
            next_action_id = input("\n: ")

            if next_action_id[0] == 'A':
                idx = next_action_id[1]
                try:
                    next_action_key = attacks_list[idx]
                    next_action = attacks_dict[next_action_key]
                except KeyError:
                    print('\nError: index not recognized. Try again')
                    continue

            elif next_action_id[0] == 'S':
                idx = next_action_id[1]
                try:
                    next_action_key = spells_list[idx]
                    next_action = spells_dict[next_action_key]
                except KeyError:
                    print('\nError: index not recognized. Try again')
                    continue

            elif next_action.lower() == 'terminate':
                print("\nTerminating npc's turn")
                return

            else:
                print('\nError: input not recognized. Try again')
                continue

            print("\nSelect a target: ")
            next_target = bHF.select_a_target(npc_character,
                    self.ordered_creature_list)
            numDie = next_action['ATTKDMG']['number']
            dtype = next_action['ATTKDMG']['dieType']
            modifier = next_action['ATTKDMG']['modifier']
            self.actionRoll(numDie, dtype, modifier, next_action,
            next_target)

            # Ask DM if they want to continue the creature's turn
            print('\nContinue {} turn?'.format(npc_character))
            confirm = input('\n(Y/n)?: ')

            if confirm.lower() == 'y' or confirm.lower() == 'yes':
                continue
            elif confirm.lower() == 'n' or confirm.lower() == 'no':
                return
            else:
                print('\nError: input not recognized. Try again')
                continue


    def actions(self, currCreat):
        '''determines which creature's turn it is and presents lists of attacks
           for that creature.
        '''
        # Fetch number of actions available to the creature
        numActions = currCreat["BONUS ACTIONS"]

        # initialize a variable for the actions available to the creature
        # during a turn
        actions_list = []

        # Fetch the attacks available to the creature
        attacks = currCreat["ATTACKS"]

        # Fetch the spells available to the creature
        spells = currCreat["SPELLS"]

        i = 0
        for attack in attacks:
            actions_list.append(attack)

        for spell in spells:
            actions_list.append(spell)

        # Display the options available to the player
        for action in actions_list:
            print(action + '\n')
            affirmation = raw_input("More info? (Y/n): ")
            while(False):
                if affirmation == "Y" or "y" or "Yes" or "yes":
                    for key in action:
                        print(key + ':\n')
                        print(action[key] + '\n')
                        break
                elif affirmation != "N" or "n" or "No" or "no":
                    print("Error: input not recognized\n")
                    affirmation = raw_input()


        for _ in range(numActions):
            print("Action available\n")
            print("Choose an action:\n")
            for idx, action in enumerate(actions_list):
                print(idx, ") ", action, "\n")
            idx = raw_input("Choose action ID: ")
            print("Target of action?: ")
            i = 0
            for idy, creature in enumerate(self.orderedCreatureList):
                if idy == self.iterator:
                    pass
                ++i
                print(i + ") " + creature + "\n")
            idy = raw_input("Choose target ID: ")

            actionName = actions_list[idx]
            effect = actionName["EFFECT"]
            target = self.orderedCreatureList[idy]
            numDie = actionName["DAMAGE"]["number"]
            dtype = actionName["DAMAGE"]["dietype"]
            modifier = actionName["DAMAGE"]["modifier"]

            self.actionRoll(numDie, dtype, modifier, actionName,
                        target, effect=effect)

        ++self.iterator
        return


    def actionRoll(self, numDie, dtype, modifier, actionName,
            target, effect="damage"):
        '''Action roll performed by npc target. Performs the roll
           according to the input values and does damage or heals
           character according to the effect specified by the action
        '''
        roll = numDie * random.randint(1,dtype) + modifier
        if effect == "damage":
            print("{0} did {1}hp damage to {2}\n".format(actionName,
                                roll, target))
            target.currHP = target.currHP - roll
            if target.currHP <= 0:
                print("{0} is dead\n".format(target.name))
                target.dead = True

        elif effect == "heal":
            print("{0} healed {1} for {2}hp\n".format(actionName,
                                target, roll))
            target.currHP = target.currHP + roll
            if target.currHP >= target.maxHP:
                target.currHP = target.maxHP
        else:
            print("{0} applied {1} to {2} for {3} points\n".format(
                                actionName, effect, target, roll))
        return


    def player_action_roll(self, roll_value, target, effect="damage"):
        '''Action performed by the player. The only difference between
           this function and action roll is that the rollValue is
           determined by physical roll of the dice rather than an
           internal algorithm
        '''
        if effect == "damage":
            print("{0} damage dealt to {1}\n".format(roll_value, target.name))
            print("type target.current_hitpoints: ", target.current_hitpoints)
            target.current_hitpoints = target.current_hitpoints - roll_value
            if target.current_hitpoints <= 0:
                print("{0} is dead\n".format(target.name))
                target.dead = True

        elif effect == "heal":
            print("{0} healed for {1}hp\n".format(target.name, roll_value))
            target.currHP = target.current_hitpoints + roll_value
            if target.current_hitpoints >= target.max_hitpoints:
                target.current_hitpoints = target.max_hitpoints
        else:
            print("{0} applied to {1} for {2} points\n".format(
                                effect, target, roll_value))

        print("exiting player_action roll function")

        return


#    def battleFlow(self):
#        for it in iterator:
#            if it - 1 == len(self.orderedCreatureList) and \
#                self.orderedCreatureList[it-1].allegiance != 'player':
#                if self.orderedCreatureList[it-1].dead == True:


    def initBattleSequence(self):
        # Inits a loop that only terminates when all creatures with allegiance
        # 'enemy' are dead'

        # First, roll initiative
        self.rollInitiative()

        # Check how many friends and foes are on the field
        for creat in self.orderedCreatureList:
            if creat.allegiance == 'friend':
                ++ self.friends
            elif creat.allegiance == 'foe':
                ++ self.foes
            elif creat.allegiance == 'neutral':
                ++ self.swiss

        # Battle loop:
        while True:
            # Check that there are still enemies on the field
            for creat in self.orderedCreatureList:
                foeDead = 0
                friendDead = 0
                if creat.allegiance == 'foe' and creat.currHp <= 0:
                    ++ foeDead
                    if foeDead == self.foes:
                        self.victory()
                        return
#               else if creat.allegiance == 'friend' and creat.currHp =< 0:
#                   if friendDead == self.friends:
#                       self.defeat()
#                       return

            # Allow creatures to take their actions
            if self.iterator == len(self.orderedCreatureList):
                self.iterator = 0
            currCreat = self.orderedCreatureList[self.iterator]
            print("It is now {0} turn".format(currCreat.name))
            self.actions(currCreat)
            ++self.iterator


    def player_action(self, player):
        '''Initiates when it is a human player's turn. Allows actions
           to be taken against other characters in battle scenario.
           When the player ends their turn, moves to next creature
           in initiative list
        '''
        print("It is now ", player.name, "'s turn\n")

        # Do you want to skip this player's turn (i.e, they
        # are incapacitated in some matter, but not unconscious)
        print("\nSkip turn?")
        response = input(" (y/N): \n")

        # Go back to script if the answer is 'yes', and move to
        # next character
        if response.lower() == 'y' or response.lower() == 'yes':
            return 1

        player_turn = True
        while player_turn:

            # Determine if the target of the action is another character
            # If it is, determine if the target is an npc. If it is, the
            # system will keep track of it. Otherwise, players keep track
            targetedAction = request_confirmation_from_user("Targeted action?")
            if targetedAction:
                print("List of characters in battle: \n")
                target_character_dict = {}
                for i, key in enumerate(self.creatureDict.keys()):
                    target_character_dict[i] = key
                    print("{}) {}\n".format(i, key))

                # Check to see if input character ID is valid
                while True:
                    try:
                        character_ID = int(input("Target character ID: "))
                    except ValueError:
                        print("I'm sorry, that input was not understood. Try again")
                        continue

                    try:
                        character_key = target_character_dict[character_ID]
                        break
                    except KeyError:
                        print("Input ID does not correspond with any listed character. Try again")

                target = self.creatureDict[character_key]
                rollValue = int(input("Input value of roll: "))
                effect = input("effect (damage/heal/etc.): ")
                self.player_action_roll(rollValue, target, effect=effect)

                player_turn = request_confirmation_from_user("Continue turn?")


    def check_for_allegiance_change(self, character):
        print("\nChange allegiance for {}?".format(character.name))
        confirmation = input("\n(y/N): ")

        while True:
            if confirmation.lower() == 'n' or confirmation.lower() == 'no':
                return

            elif confirmation.lower() == 'y' or confirmation.lower() == 'yes':
                while True:
                    newAllegiance = input('\nSelect what allegiance ' + \
                            'to set {} to (fr/fo/ne)'.format(character.name))
                    if newAllegiance.lower() == 'fr' or \
                            newAllegiance.lower() == 'friend':
                        character.allegiance = 'friend'
                        return

                    elif newAllegiance.lower() == 'fo' or \
                             newAllegiance.lower() == 'foe':
                        character.allegiance == 'foe'
                        return

                    elif newAllegiance.lower() == 'ne' or \
                            newAllegiance.lower() == 'neutra;':
                        character.allegiance == 'neutral'
                        return

                    else:
                        print("\nError: input not recognized")
                        continue

            else:
                print("\nError: input not recognized. Try again")
                continue


    def victory(self):

        print("You and your comrades are victorious!\n")
        print("Oh, joyous day!\n")
        return


    def defeat(self):
        print("Congrats, you died!\n")
        print("Good job scrubs!\n")
        return

    def script(self):
        '''It might keep everything a little more organized if I
           just kept the actual flow of the battle in this script
           and just called on other functions as needed for sub-tasks
           (e.g., rolling initiative, rolling attacks, letting players
           know of their turn order
        '''
        # First check to see if there are any debugging actions the DM
        # needs to take before beginning battle (i.e., manually inputting
        # attribute values for npcs that had configuration errors
        for _, creature in creature_dict.items():

            for error in creature.errors:
                prints("""Failed to import {0} statistic for {1}
                          of type {2}""".format(error, creature.name, creature.creature_type))




        print("-----------Initiate Battle-----------\n")
        # First action: Roll initiative for all npcs
        self.roll_initiative()

        # Organize all characters in battle scenario into lists based
        # on allegiance (these lists are fluid, and can be changed
        # during the flow of battle)
        self.list_by_allegiance()

        # Determine the challenge rating of the engagement based on the
        # challenge ratings of all the creatures in the 'foe' list (note
        # that, unlike the allegiance lists themselves, this rating is
        # not fluid, and remains the same throughout the engagement
        self.determine_challenge_rating()
        print("\n"+self.bMessager._display_challenge_rating(
                            self.challenge_rating))

        # Check if we want to initialize battle spreadsheet gui. If we do,
        #

        # We are now ready for the battle phase. Initiate loop that does not
        # terminate until all members of the foe list are defeated
        initBattle = True
        idx = 0
        while initBattle:
            # Move to next character in initiative list
            nextCharacter = self.ordered_creature_list[idx]
            # Check if character is dead
            if nextCharacter.dead == True:
                # Perform check to see if all characters of 'foe'
                # allegiance are dead or defeated. If so, end battle
                # loop and run loot generator:
                if self.check_if_all_foes_dead() == True:
                    break

                if nextCharacter.npc == 1:
                    ++idx
                    continue

                # If player character, have them perform a
                # saving throw to see if they live or not
                if nextCharacter.succesful_save_throws < 3 or \
                        nextCharacter.failed_save_throws < 3:

                    print('\n'+bMessager._ask_player_to_roll_saving_throw(
                                        nextCharacter.name))
                    success = input(
                            "\nSuccesful Saving Throw? (y/n): ")

                    if success == 'y' or success == 'Y':
                        ++nextCharacter.succesful_save_throws
                        if nextCharacter.succesful_save_throws == 3:
                            print('\n' + bMessager._succeed_save_throws_msg(
                                            nextCharacter.name))
                        continue

                    else:
                        ++nextCharacter.failed_save_throws
                        if nextCharacter.failed_save_throws == 3:
                            print('\n' + bMessager._fail_save_throws_msg(
                                            nextCharacter.name))
                        continue

                # If character has failed all saving throws already,
                # display death message
                elif nextCharacter.failed_save_throws > 3:
                    print("{} is dead. Not surprising, scrub".format(nextCharacter))
                    continue

            # Once death checks are complete, display message telling
            # user whose turn it is
            print("It is now {}'s turn".format(nextCharacter.name))
            time.sleep(1.0)

            # Check if the character has had a change of allegiance
            self.check_for_allegiance_change(nextCharacter)
            time.sleep(1.0)

            idx += 1
            print(idx)

            # Check if index is larger than last index in list. If so,
            # reset to 0
            if idx == len(self.ordered_creature_list):
                idx = 0

            # Check if npc or player, and have them perform actions
            # accordingly
            if nextCharacter.npc == 1:

                # Let npc take action
                self.npc_action(nextCharacter)

            else:
                self.player_action(nextCharacter)



        # Let the players know that they won the battle!
        print(self.bMessager._victory_message())
        # Run automatic loot generator based on challenge
        # rating of the engagement
        lg.battle_loot_generator(self.battle_challenge_rating)
        ########### END OF ENGAGEMENT ######################



class battleMessages():

    def _action(self, actionName, roll, target):
        return "{0} did {1}hp damage to {2}".format(actionName,
                        roll, target)

    def _newPlayerTurn(self, name):
        return "It is now {0}'s turn"

    def _initBattle(self):
        return "Battle initiated"

    def _ask_player_to_roll_saving_throw(self, name):
        return "{}, roll d20 for saving throw".format(name)

    def _succeed_save_throws_msg(self, name):
        return """
                  {} has made 3 saving throws! They are alive
                  (for now), but they are still incapacitated. They will
                  need to wait until the end of the battle to be fully
                  revived
               """

    def _fail_save_throws_msg(self, name):
        return """
                  Oof...{} has failed their saving throw 3 times.
                  Their story unfortunately ends here
               """

    def _victory_message(self):
        return """You and your comrades are victorious! Oh, joyous day!"""

    def _display_challenge_rating(self, challenge_rating):
        return "Calculated Challenge Rating: {}".format(
                                        challenge_rating)

    # Helper messages: let DM know what part of the script is finished,
    # or whether something went wrong loading the battle
    def _errorLoadingConfig(self, name, creatType):
        return """Error: creature config failed to load for {0} of
                creature type {1}""".format(name, creatType)

    def ask_player_to_roll_initiative(self, player_name):
        return "Ask player {} to roll for initiative".format(player_name) + \
            " (d20 + dex modifier"

    def npc_turn_initiate(self, npc_name):
        return "It is NPC {}'s turn. Choose an action ".format(npc_name) + \
                'for them'


class PlayerCharacter(object):
    '''Resembles the Creature class, but only has a few of the
       attributes for station keeping
    '''
    def __init__(self, name):
       self.name = name
       self.dead = False
       self.succesful_save_throws = 0
       self.failed_save_throws = 0
       self.allegiance = 'friend'
       self.initiative = 0
       self.npc = 0
       self.dead = False


    def switchAllegiance(self, allegiance='foe'):
        self.allegiance = allegiance

def request_confirmation_from_user(message_str):
    """
       Helper function for recieving confirmation (yes/no) from
       users.
    """
    # Strip question mark from message_str. We'll add it back in later
    message_str = message_str.strip('?')

    # Initiate loop that continues until user inputs a recognizeable
    # response
    while True:

        # Display message to user and ask for input
        response = input(message_str + "(y/N)?: ")

        # Check for positive responses
        if response.lower() == 'y' or response.lower() == 'yes':
            return 1
        # Check for negative responses
        elif response.lower() == 'n' or response.lower() == 'no':
            return 0
        # If response was none of the above, then it is unrecognized.
        # Restart loop
        else:
            pass



if __name__ == '__main__':

    args = parser.parse_args()
    csv_file = args.battle_csv
    # Retrieve list of dicts with npc characteristics
    npc_creatures = bCP.parse_battle_csv(csv_file)
    print("npc_creatures: ", npc_creatures)
#    print("args.players: ", args.players)
#    print("type of args.players: ", type(args.players))
#    print("len of args.players: ", len(args.players))
#
#    for i, player in enumerate(args.players):
#        print("player %d: %s" % (i, player))
#
#    player_str = ''.join(str(char) for char in args.players)
#    print("player_str: ", player_str)
#    print("type of player_str: ", type(player_str))
#    #print("len of player_str: ", len(player_str))
#
    print("element 0 of args.players: ", args.players[0])
    print("type of elem 0 of args.players: ", type(args.players[0]))
    player_characters = args.players[0].split(',')
    player_characters = [name.strip(',').strip() for name in player_characters]
#
#    print("player_characters: ", player_characters)

    creature_dict = dict()

    # Go for the list of creature dicts provided in the
    # battle csv file and feed it to the Creature class
    #pdb.set_trace()
    exit_battle = False
    for npc_creature in npc_creatures:
        name = npc_creature['name']
        #pdb.set_trace()
        creature_type = npc_creature['type']
        #pdb.set_trace()
        allegiance = npc_creature['allegiance']
        creature_stats = mYP.Creature(name,
                                    creature_type, allegiance=allegiance,
                                    )
        #pdb.set_trace()
        if creature_stats.openSuccess == 0:
            print("Exiting battle setup...")
            exit_battle = True
            break

        else:
            creature_dict[npc_creature['name']] = creature_stats

    if not exit_battle:
        player_dict = dict()
        # Create playerCharacter objects for all input players and add
        # to creature dict

        #pdb.set_trace()

        for player in player_characters:
            player_dict[player] = PlayerCharacter(player)

        curr_battle_scenario = BattleScenario(creature_dict, player_dict)

        # Initialize battle spreadsheet object
#        battle_spreadsheet = cHS.BattleInfoSpreadsheet(curr_battle_scenario,
#                        'test_battle',

        # And finally...initialize battle script
        curr_battle_scenario.script()



#   args = parser.parse_args()
#   scenarioCSV = args[0]
#   names = list()
#   types = list()
#   allegiances = list()
#   with open('/home/peter//Programming/Python_Files/DnDHelper/BattleScenarios'+
#               scenarioCSV+'.csv', 'r') as f:
#           reader = csv.reader(f)
#           for row in reader:
#               names.append(row[0])
#               types.append(row[1])
#               allegiances.append(row[2])
#   # Add in info from the command line
#   names.append(creatName for creatName in creatNames)
#   types.append(creatType for creatType in creatTypes)
#   allegiances.append(creatAllegiance for creatAllegiance in creatAllegiances)
#   characteristics = [names, types, allegiances]
#
#   creatDict = dict()
#   for creatName, creatType, allegiance in zip(characteristics):
#       ymlFile = creatType + '.yml'
#       creatureMuaHaHa = mYP.Creature(ymlFile, allegiance=allegiance)
#       creatureMuaHaHa.openYaml()
#       creatureMuaHaHa.importFeatures()
#       creatureMuaHaHa.allegiance = allegiance
#       creatDict[creatName] = creatureMuaHaHa
#   # Well guess what? Now we get to load this shizzle into battlefohizzle
#   currBattleBitches = BattleScenario(creatDict)
#   currrBattleBitches.initBattleSequence()


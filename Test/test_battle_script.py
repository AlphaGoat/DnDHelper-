import sys

sys.path.append('..')

from setupBattle import PlayerCharacter, BattleScenario
from monsterYamlParser import Creature
from battleHelperFunctions import die_roll

import time

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--run_all_tests',
                    action='store_true',
                    help="Run and return results for all tests in suite"
                    )

parser.add_argument('--test_player_action',
                    action='store_true')

parser.add_argument('--test_npc_action',
                    action='store_true')

parser.add_argument('--test_loading_creature',
                    action='store_true')

parser.add_argument('--test_roll_of_die',
                    action='store_true')


class TestError(Exception):
    pass


def test_player_action():
    '''Quick test script to test player action in
       Battle Setup
    '''
    # initialize generic player dict
    player_dict = {
                "Jon": PlayerCharacter("Jon"),
                "Garfield": PlayerCharacter("Garfield")
                }

    # initialize npc character dict
    creature_dict = {
                "npc_foe": Creature("npc_foe",
                                    "manticore",
                                    "foe"),
                "npc_friend": Creature("npc_friend",
                                       "banshee",
                                       "friend")
                    }

    battle_scenario = BattleScenario(creature_dict,
                                 player_dict)

    try:
        battle_scenario.player_action(player_dict["Jon"])
        return 1

    except TestError as e:
        print(e)
        return 0

def test_npc_action():
    """
    Test script to test npc actions in Battle Setup
    """
    # initialize generic player dict
    player_dict = {
                "Jon": PlayerCharacter("Jon"),
                "Garfield": PlayerCharacter("Garfield")
                }

    # initialize npc character dict
    creature_dict = {
                "npc_foe": Creature("npc_foe",
                                    "manticore",
                                    "foe"),
                "npc_friend": Creature("npc_friend",
                                       "banshee",
                                       "friend")
                    }

    battle_scenario = BattleScenario(creature_dict,
                                 player_dict)

    try:
        battle_scenario.npc_action(creature_dict["npc_foe"])
        return 1
    except TestError as e:
        print(e)
        return 0


def test_loading_creature(creature_type):
    try:
        name = "test_name"
        allegiance = "friend"
        test_creature = Creature(name, creature_type, allegiance)
        return 1
    except:
        return 0

def test_roll_of_die():
    """
       Test die roll to ensure that it is generating values that
       we want (i.e., corresponds with a real dice throw)
    """
    die_type = 20
    num_die = 3
    modifier = 5

    result = die_roll(num_die, die_type, modifier)

    if 1 <= result <= (num_die * die_type) + modifier:
        return 1, result
    else:
        return 0, result





if __name__ == '__main__':

    flags = parser.parse_args()

    print("----Running through tests....------\n")
    time.sleep(1.0)

    # Test player actions
    if flags.test_player_action or flags.run_all_tests:
        print("---- Testing Player action -------\n")

        if test_player_action() == 1:
            print("Player action test successful")
        else:
            print("FAIL: test_player_action exited unsuccesfully")

    # Test npc actions
    if flags.test_npc_action or flags.run_all_tests:
        print("------ Testing NPC action ------\n")

        if test_npc_action() == 1:
            print("NPC action test succesful")
        else:
            print("FAIL: test_npc_action exited unsuccesfully")

    # Test loading of creature configuration files
    if flags.test_loading_creature or flags.run_all_tests:
        print("------ Testing Creature Config Loading ------")

        if test_loading_creature("banshee") == 1:
            print("Creature Config Load test succesful")

    # Test roll of die
    if flags.test_roll_of_die or flags.run_all_tests:
        print("------ Testing Die Roll (die_type=20, num_die=3, modifier=5) ------")

        success_flag, result = test_roll_of_die()
        if success_flag == 1:
            print("Die rolling function test succesful")
        else:
            print("FAIL: Die rolling function test unsuccesful")
            print("Output result: ", result)





import yaml
import os

from battleHelperFunctions import die_roll

import pdb


class Creature(object):

    def __init__(self, name, creature_type,
        allegiance='foe', openYaml=1, x=0, y=0):

        """
        Creature Object:

        Stores all attributes needed for reference during battle scenario

        Parameters
        __________

        name (str)                -- Name of the character in the battle scenario
        creat_type (str)          -- Type of creature
        ymlDir (str)              -- Directory where creature config files are
                                     stored
        allegiance (str)          -- allegiance of the creature to the character
                                     party (possible options: ally, neutral,
                                     foe)
        openYaml (bool int)       -- flag telling script whether or not
                                     to open creature yaml file
        importFeatures (bool int) -- flag telling script to import
                                     creature features from yaml file
        """

        self.creature_type = creature_type
        self.name = name
        # initialize attributes of the creature
        self.creature_config = None
        self.attributes = None
        self.abilities = None
        self.feats = None
        self.attacks = None
        self.spells = None
        self.challenge_rating = None
        self.armor_class = None
        self.creature_class = None
        self.experience_points = None
        self.max_hitpoints = None
        self.current_hitpoints = None
        self.speed = None
        self.save_throws = None
        self.args = None

        # variable attributes: can change during the course of the battle
        self.allegiance = allegiance
        self.x, self. y = x, y
        self.position = (x,y)

        # creature actions dictionary: keeps track of all actions
        # available to the creature
        self.actions = dict()

        # Flag to let the battle setup script know that this character
        # is an npc
        self.npc = 1

        # creature features that are initialized by the BattleScenario
        self.initiative = 0

        # features that are changed throughout instance of BattleScenario
        self.dead = False
        self.defeated = False

        # Empty list to keep track of import failures
        self.errors = []

        # Flags to process instructions
        self.openYaml = openYaml

        # Flags set for succesful completion of class methods
        self.open_success = 0

        if self.openYaml == 1:
            self.yaml_file_path = self.loadYaml()
            #pdb.set_trace()
            if self.yaml_file_path != 0:
                self.importFeatures(self.yaml_file_path)
                self.open_success = 1

        if self.open_success == 0:
            raise ConfigOpenError

    def loadYaml(self):

        #pdb.set_trace()

        path = os.path.join('../MonsterConfigFiles',
                self.creature_type + '.yml')
        case_invariant_path = os.path.join('../MonsterConfigFiles',
                self.creature_type.lower() + '.yml')
        print("path of monster config: ", path)
        if os.path.exists(path):
            return path
        elif os.path.exists(case_invariant_path):
            return case_invariant_path
        else:
            # self.error_msg.yaml_load_error()
            print("Error: unable to import creature config for type {}. File does not exist".format(self.creature_type))
            return 0


    def importFeatures(self, yaml_file_path):

        with open(yaml_file_path, 'r') as stream:
            creature_data = yaml.safe_load(stream)

            # List to contain errors encountered during import
            errors = []

            # Import different creature features from yaml file
            print("creature_data type: ", type(creature_data))
            for key, value in creature_data.items():
                print("key: ", key)
                print("value: ", value)

            #pdb.set_trace()

            #pdb.set_trace()
            # Creature Name
            #pdb.set_trace()
            try:
                #pdb.set_trace()
                self.attributes = creature_data["ATTRIBUTES"]
            except KeyError:
                print("Unable to load attributes")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    attribute_input = input("Attributes: ")
                else:
                    errors.append("attributes")
                    pass

            # Creature Abilities
            try:
                self.abilities = creature_data["ABILITIES"]
            except KeyError:
                print("Unable to load abilities")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    abilities_input = input("Abilities: ")
                    # Put in some post processing here
                    self.abilities = abilities_input
                else:
                    errors.append("abilities")
                    pass

            try:
                self.feats = creature_data["FEATS"]
            except KeyError:
                print("Unable to load feats")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    feats_input = input("feats: ")
                    # Put in some post processing here
                    self.feats = feats_input
                else:
                    errors.append("feats")
                    pass

            # Creature Actions
            try:
                self.actions = creature_data["ACTIONS"]
            except KeyError:
                print("Unable to load actions")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    actions_input = input("actions: ")
                    # Put in some post processing here
                    self.actions["misc actions"] = actions_input
                else:
                    errors.append("actions")
                    pass

            # Creature Attacks
            try:
                self.actions['attacks'] = creature_data["ATTACKS"]
            except KeyError:
                print("Unable to load attacks")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    attacks_input = input("attacks: ")
                    # Put in some post processing here
                    self.actions["attacks"] = attacks_input
                else:
                    errors.append("attacks")
                    self.actions["attacks"] = None
                    pass

            # Creature spells
            try:
                self.actions['spells'] = creature_data["SPELLS"]
            except KeyError:
                print("Unable to load spells")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    spells_input = input("spells: ")
                    # Put in some post processing here
                    self.actions["spells"] = spells_input
                else:
                    errors.append("spells")
                    self.actions["spells"] = None
                    pass

            # Creature challenge rating
            try:
                self.challenge_rating = creature_data["CHALLENGE"]
            except KeyError:
                print("Unable to load challenge_rating")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    challenge_rating_input = input("challenge_rating: ")
                    # Put in some post processing here
                    self.challenge_rating = challenge_rating_input
                else:
                    errors.append("challenge_rating")
                    pass

            # Creature challenge rating
            try:
                self.armor_class = creature_data["ARMORCLASS"]
            except KeyError:
                print("Unable to load armor_class")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    armor_class_input = input("armor_class: ")
                    # Put in some post processing here
                    self.armor_class = armor_class_input
                else:
                    errors.append("armor_class")
                    pass

            # Creaturetype
            try:
                self.creature_class = creature_data["CREATURETYPE"]
            except KeyError:
                print("Unable to load creature type")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    creature_class_input = input("creature_class: ")
                    # Put in some post processing here
                    self.creature_class = creature_class_input
                else:
                    errors.append("creature_class")
                    pass

            # Creature experience points
            try:
                self.experience_points = creature_data["EXPERIENCEPOINTS"]
            except KeyError:
                print("Unable to load experience_points")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    experience_points_input = input("experience_points: ")
                    # Put in some post processing here
                    self.experience_points = experience_points_input
                else:
                    errors.append("experience_points")
                    pass

            # Creature experience points
            try:
                self.hit_dice = creature_data["HITPOINTS"]
                self.max_hitpoints = self.current_hitpoints = die_roll(self.hit_dice[2],
                                                                       self.hit_dice[0],
                                                                       self.hit_dice[1])
            except KeyError:
                print("Unable to import HP stat for {0} of type {1}".format(self.name, self.creature_type))
                print("Unable to load hit dice")
                print("Input some now?")
                confirmation = input("(y/N): ")
                if confirmation.lower() == 'y':
                    num_hit_die = int(input("number of hit die: "))
                    die_type = int(input("dietype: "))
                    modifier = int(input("modifier: "))
                    self.hit_dice = [die_type, modifier, num_hit_die]
                    self.max_hitpoints = self.current_hitpoints = die_roll(self.hit_dice[2],
                                                                           self.hit_dice[0],
                                                                           self.hit_dice[1])
                    # Put in some post processing here
                else:
                    errors.append("hit_points")
                    pass
                errors.append("hitpoints")
                pass

            # Creature speed stats
            try:
                self.speed = creature_data["SPEED"]
            except KeyError:
                errors.append("speed")
                pass

            # Creature saving throws
            try:
                self.save_throws = creature_data["SAVETHROWS"]
            except KeyError:
                errors.append("save_throws")
                pass

            # Creature args
            try:
                self.args = creature_data["ARGS"]
            except KeyError:
                errors.append("args")
                pass

            self.errors = errors
            return


    def compile_actions(self):
        '''Takes all actions available to creature and compiles
           them into a dictionary for reference
        '''
        return


    def change_allegiance(self, new_allegiance):
        '''Changes allegiance of creature to new, input allegiance'''
        self.allegiance = new_allegiance
        return


    def list_actions(self):
        '''List actions available to the creature'''
        #for action_type in actions.keys():
        return

    def debug(self):
        '''
           List out attributes that could not imported from the config
           file
        '''
        for error in self.errors:
            print("Unable to import {0} for {1} type".format(error, self.name))


class ConfigOpenError(Exception):
    pass

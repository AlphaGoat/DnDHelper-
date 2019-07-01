import yaml
import os

import pdb

std_dir = "/home/peter/Programming/Python_Files/DnDHelper/MonsterConfigFiles"

class Creature(object):

    def __init__(self, name, creature_type, yamlDir=std_dir, 
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

        self.yamlDir = yamlDir
        self.creature_type = creature_type
        self.name = name
        # initialize attributes of the creature
        self.creatureConfig = None
        self.name = name
        self.attributes = None
        self.abilities = None
        self.feats = None
        self.attacks = None
        self.spells = None
        self.challenge_rating = None
        self.armorClass = None
        self.creature_class = None
        self.experiencePoints = None
        self.maxHP = None
        self.currHP = None
        self.speed = None
        self.savethrows = None
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
        self.openSuccess = 0

        if self.openYaml == 1:
            yaml_file_path = self.loadYaml()
            #pdb.set_trace()
            if yaml_file_path != 0:
                self.importFeatures(yaml_file_path)
                self.openSuccess = 1

    def loadYaml(self):

        #pdb.set_trace()

        path = os.path.join(self.yamlDir, 
                self.creature_type + '.yml')
        case_invariant_path = os.path.join(self.yamlDir, 
                self.creature_type.lower() + '.yml')
        if os.path.exists(path):
            return path
        elif os.path.exists(case_invariant_path):
            return case_invariant_path
        else:
            # self.error_msg.yaml_load_error()
            print("Error: unable to import creature config. File does not exist")
            return 0


    def importFeatures(self, yaml_file_path):

        with open(yaml_file_path, 'r') as stream:
            creature_data = yaml.safe_load(stream)

            # List to contain errors encountered during import
            errors = []

            # Import different creature features from yaml file

            #pdb.set_trace()
            # Creature Name
            #pdb.set_trace()
            try:
                #pdb.set_trace()
                self.attributes = creature_data["ATTRIBUTES"]
            except KeyError:
                errors.append("attributes")
                pass

            # Creature Abilities
            try:
                self.abilities = creature_data["ABILITIES"]
            except KeyError:
                errors.append("abilities")
                pass

            try:
                self.feats = creature_data["FEATS"]
            except KeyError:
                errors.append("feats")
                pass

            # Creature Actions
            try:
                self.actions = creature_data["ACTIONS"]
            except KeyError:
                errors.append("actions")
                pass

            # Creature Attacks
            try:
                self.attacks = creature_data["ATTACKS"]
            except KeyError:
                errors.append("attacks")
                pass

            # Creature spells
            try:
                self.spells = creature_data["SPELLS"]
            except KeyError:
                errors.append("spells")
                pass

            # Creature challenge rating
            try:
                self.challenge_rating = creature_data["CHALLENGE"]
            except KeyError:
                errors.append("challenge")
                pass

            # Creature challenge rating
            try:
                self.armorClass = creature_data["ARMORCLASS"]
            except KeyError:
                errors.append("armorClass")
                pass

            # Creaturetype
            try:
                self.creature_class = creature_data["CREATURETYPE"]
            except KeyError:
                errors.append("creature_class")
                pass

            # Creature experience points
            try:
                self.experiencePoints = creature_data["EXPERIENCEPOINTS"]
            except KeyError:
                errors.append("experiencePoints")
                pass

            # Creature experience points
            try:
                self.hp = creature_data["HITPOINTS"]
            except KeyError:
                errors.append("hp")
                pass

            # Creature speed stats
            try:
                self.speed = creature_data["SPEED"]
            except KeyError:
                errors.append("speed")
                pass

            # Creature saving throws
            try:
                self.savethrows = creature_data["SAVETHROWS"]
            except KeyError:
                errors.append("savethrows")
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

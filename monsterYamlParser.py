import yaml
import os

class Creature(object):

    def __init__(self, name, creat_type, ymlDir="""/home/peter/Programming/Python_Files/
        DnDHelper/MonsterConfigFiles""", allegiance='foe', openYaml=1,
        importFeatures=1):

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

        # initialize attributes of the creature
        self.creatureConfig = None
        self.name = name
        self.type = creat_type
        self.attributes = None
        self.abilities = None
        self.attacks = None
        self.spells = None
        self.challenge = None
        self.armorClass = None
        self.creatureType = None
        self.experiencePoints = None
        self.maxHP = None
        self.currHP = None
        self.speed = None
        self.savethrows = None
        self.args = None
        self.allegiance = allegiance

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
        self.importFeatures = importFeatures

        # Flags set for succesful completion of class methods
        self.openSuccess = 0

        if self.openYaml == 1:
                self.openYaml()

        if self.importFeatures == 1 and self.openSuccess == 1:
                self.importFeatures()


    def openYaml(self):

        if os.path.exists(self.yamlDir + self.creature_type + '.yml'):
            yamlfile = self.yamlDir + self.creature_type + '.yml'
            return

        elif os.path.exists(self.yamlDir + self.creature_type.lower() +
                                '.yml')
            yamlfile = self.yamlDir + self.creature_type.lower() + '.yml'

        else:
            # self.error_msg.yaml_load_error()
            print("Error: unable to import creature config. File does not exist")

        with open(yamlfile, 'r') as yf:
            self.creatureConfig = yaml.load(yf)
            self.openSuccess = 1


    def importFeatures(self):

        if self.creatureConfig == None:
            print("import creature features first!")
            return

        # List to contain errors encountered during import
        errors = []

        # Import different creature features from yaml file

        # Creature Name
        try:
            self.name = self.creatureConfig["ATTRIBUTES"]
        except KeyError:
            errors.append("attributes")
            pass

        # Creature Abilities
        try:
            self.abilities = self.creatureConfig["ABILITIES"]
        except KeyError:
            errors.append("abilities")
            pass

        # Creature Actions
        try:
            self.actions = self.creatureConfig["ACTIONS"]
        except KeyError:
            errors.append("actions")
            pass

        # Creature Attacks
        try:
            self.attacks = self.creatureConfig["ATTACKS"]
        except KeyError:
            errors.append("attacks")
            pass

        # Creature spells
        try:
            self.spells = self.creatureConfig["SPELLS"]
        except KeyError:
            errors.append("spells")
            pass

        # Creature challenge rating
        try:
            self.challenge = self.creatureConfig["CHALLENGE"]
        except KeyError:
            errors.append("challenge")
            pass

        # Creature challenge rating
        try:
            self.armorClass = self.creatureConfig["ARMORCLASS"]
        except KeyError:
            errors.append("armorClass")
            pass

        # Creaturetype
        try:
            self.creatureType = self.creatureConfig["CREATURETYPE"]
        except KeyError:
            errors.append("creatureType")
            pass

        # Creature experience points
        try:
            self.experiencePoints = self.creatureConfig["EXPERIENCEPOINTS"]
        except KeyError:
            errors.append("experiencePoints")
            pass

        # Creature experience points
        try:
            self.hp = self.creatureConfig["HITPOINTS"]
        except KeyError:
            errors.append("hp")
            pass

        # Creature speed stats
        try:
            self.speed = self.creatureConfig["SPEED"]
        except KeyError:
            errors.append("speed")
            pass

        # Creature saving throws
        try:
            self.savethrows = self.creatureConfig["SAVETHROWS"]
        except KeyError:
            errors.append("savethrows")
            pass

        # Creature args
        try:
            self.args = self.creatureConfig["ARGS"]
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

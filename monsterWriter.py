import yaml
import json

def setup_yaml():
    """https://stackoverflow.com/a/8661021"""
    represent_dict_order = lambda self, data: self.represent_mapping(
                                'tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)


def writeMonsterConfig(name, creatureType, AC, HP,
		   speed, challenge, XP, abilities,
		   savingThrows, resistances, immunities,
		   attacks, spells, *args, **kwargs):

    items = []
    for _,item in enumerate(args):
        items.append(item)

    kwargDict = {}
    for name,value in kwargs.items():
        kwargDict[name] = value

    # Place all compiled actions into an overarching 'action'
    # dic. These will represent all actions a creature is able
    # to take during their turn
    actions = {
               'attacks'       : attacks,
               'spells'        : spells,
               'bonus_actions' : bonus_actions
               }

    # Handle the dictionary of attacks provided:
    data = dict(
        NAME=name,
        CREATURETYPE=creatureType,
        ARMORCLASS=AC,
        HITPOINTS=dict(
                        number=HP[0],
                        dieType=HP[1],
                        modifer=HP[2],
                        ),
        SPEED=speed,
        CHALLENGE=challenge,
        EXPERIENCEPOINTS=XP,
        ABILITIES=abilities,
        SAVETHROWS=savingThrows,
        ATTACKS=attacks,
        SPELLS=spells,
        ADDINFO=kwargDict,
        ARGS=items
    )

    with open('/home/peter/Python_Files/DnDHelper/MonsterConfigFiles/'+
                name + '.yml', 'w') as yamlFile:
        yaml.dump(data, yamlFile, default_flow_style=False)


def writeMonsterConfigJson(name,
                           creatureType,
                           AC,
                           HP,
		                   speed,
                           challenge,
                           XP,
                           abilities,
		                   savingThrows,
                           resistances,
                           immunities,
		                   attacks,
                           spells,
                           *args,
                           **kwargs):

    items = []
    for _, item in enumerate(args):
        items.append(item)

    kwargDict = {}
    for name, value in kwargs.items():
        kwargDict[name] = value

    # Place all compiled actions into an overarching 'action'
    # dic. These will represent all actions a creature is able
    # to take during their turn
    actions = {
               'attacks'       : attacks,
               'spells'        : spells,
               'bonus_actions' : bonus_actions
               }

    # Handle the dictionary of attacks provided:
    data = {
        "NAME" : name,
        "CREATURETYPE" : creatureType,
        "ARMORCLASS" : AC,
        "HITPOINTS" : {
            "number" : HP[0],
            "dieType" : HP[1],
            "modifer" : HP[2],
        },
        "SPEED" : speed,
        "CHALLENGE" : challenge,
        "EXPERIENCEPOINTS" : XP,
        "ABILITIES" : abilities,
        "SAVETHROWS" : savingThrows,
        "ATTACKS" : attacks,
        "SPELLS" : spells,
        "ADDINFO" : kwargDict,
        "ARGS" : items
    }

    with open(flags.config_directory + name + '.json', 'w') as json_file:
        json.dump(data, json_file)


def handleAttack(name, hit, reach, aoe, damage, numTargets, desc,
				  bonus=False, *args, **kwargs):

    attkDmg = {
        "number":damage[0],
        "dietype":damage[1],
        "modifier":damage[2]
    }

    attacks = {
        "NAME" : name,
        "HIT" : hit,
        "REACH" : reach,
        "AOE" : aoe,
        "ATTKDMG" : attkDmg,
        "NUMTARGETS" : numTargets,
        "BONUS" : bonus,
        "DESCRIPTION" : desc,
    }

    argcounter = 0
    for arg in args:
        attacks["ADDATTKINFO"+argcounter] = arg
        argcounter += 1

    for key in kwargs:
        attacks[key] = kwargs[key]


    return attacks


def handleSpells(name, desc, castingTime, castRange, components, duration,
				 aoe, damage, heal=False, bonus=False,
                                  *args, **kwargs):

    spellDmg = {
        "number" : damage[0],
        "dieType" : damage[1],
        "modifier" : damage[2],
    }

    spells = {
        "NAME" : name,
        "CASTINGTIME" : castingTime,
        "CASTRANGE" : castRange,
        "COMPONENTS" : components,
        "DURATION" : duration,
        "AOE" : aoe,
        "DAMAGE" : spellDmg,
        "HEAL" : heal,
        "BONUS" : bonus,
        "DESC" : desc,
    }

    argcounter = 0
    for arg in args:
        spells["ADDATTKINFO"+argcounter] = arg
        argcounter += 1

    for key in kwargs:
        spells[key] = kwargs[key]

    return spells


#def handleBonusActions(name, desc):
#    '''Actions that can be done in addition to the customary two
#       done in a normal turn
#    '''



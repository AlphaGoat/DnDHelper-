import json
import argparse
import os

class NPCCreature(object):

    def __init__(self, npc_id, creature_name):

        self.npc_id = npc_id
        self.name = creature_name
        self.npc = 1

        creature_config_file = creature_name + 'json'
        creature_config_path=  os.path.join('./MonsterConfigFiles',
                                            creature_config_file)

        with open(creature_config_path, 'r') as input_file:

            data =json.load(input_file)

        self.data = data

        # save variable attributes as their own variable within the class
        self.hitpoints = data['HP']

        #
        self.dead = False


class HandleArgParseSpells(argparse._AppendAction):

    def __init__(self, option_strings, dest, **kwargs):

        super(HandleArgParseAttacks).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        attacks_list = list()
        specific_attack_dict = dict()
        i = 0
        for value in values:

            if i == 0:
                specific_attack_dict['name'] = value
                i += 1

            elif i == 1:
                specific_attack_dict['dNumber'] = int(value)
                i += 1

            elif i == 2:
                specific_attack_dict['dType'] = int(value)
                i += 1

            elif i == 3:
                specific_attack_dict['modifier'] = int(value)

            else:
                specific_attack_dict['description'] = value
                attacks_list.append(specific_attack_dict)
                i = 0
                specific_attack_dict = dict()

        setattr(namespace, self.dest, attacks_list)

class HandleArgParseAttacks(argparse._AppendAction):

    def __init__(self, option_strings, dest, **kwargs):

        super(HandleArgParseAttacks).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        attacks_list = list()
        specific_attack_dict = dict()
        i = 0
        for value in values:

            if i == 0:
                specific_attack_dict['name'] = value
                i += 1

            elif i == 1:
                specific_attack_dict['dNumber'] = int(value)
                i += 1

            elif i == 2:
                specific_attack_dict['dType'] = int(value)
                i += 1

            elif i == 3:
                specific_attack_dict['modifier'] = int(value)
                i = 0
                specific_attack_dict = dict()

        setattr(namespace, self.dest, attacks_list)


def write_npccreature_json(flags, *args, **kwargs):

    data = {'name': flags.name,
            'AC': flags.armor_class,
            'HP': flags.hit_points,
            'Challenge': flags.challenge_rating,
            'XP': flags.experience_points,
            'ground_speed': flags.ground_speed,
            'air_speed': flags.air_speed,
            'water_speed': flags.water_speed,
            'Attributes': {'STR': flags.strength,
                           'DEX': flags.dexterity,
                           'CON': flags.constitution,
                           'INT': flags.intelligence,
                           'WIS': flags.wisdom,
                           'CHA': flags.charisma
                           }
            'languages': flags.languages,
            'attacks': flags.attacks,
            'spells': flags.spells,
            }

    additional_info_list = list()
    for arg in args:
        additional_info_list.append(arg)

    data['additional_info'] = additional_info_list

    for key, value in kwargs.items()
        data[key] = value

    creature_config_file = name + 'json'
    creature_config_path =  os.path.join('./MonsterConfigFiles',
                                         creature_config_file)

    with open(creature_config_path, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''Arguments to instantiate
                                     a creature json file''')

    parser.add_argument('--name', type=str,
                        help="Name of the creature")

    parser.add_argument('--armor_class', type=int,
                        help="Armor class of the creature")

    parser.add_argument('--hit_points', type=int,
                        help="creature hit points")

    parser.add_argument('--challenge_rating', type=int)

    parser.add_argument('--experience_points', type=int)

    parser.add_argument('--ground_speed', type=int, default=0)

    parser.add_argument('--air_speed', type=int, default=0)

    parser.add_argument('--water_speed', type=int, default=0)

    parser.add_argument('--strength', type=int)

    parser.add_argument('--dexterity', type=int)

    parser.add_argument('--constitution', type=int)

    parser.add_argument('--intelligence', type=int)

    parser.add_argument('--wisdom', type=int)

    parser.add_argument('--charisma', type=int)

    parser.add_argument('--languages', nargs='+',
                        type=str, default=None)

    parser.add_argument('--attacks', nargs='+', action=HandleArgParseAttacks)

    parser.add_argument('--spells', nargs='+', action=HandleArgParseSpells)

    args = parser.parse_args()

    write_npccreature_json(args)




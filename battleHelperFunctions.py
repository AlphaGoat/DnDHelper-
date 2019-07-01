import random

import pdb

def get_ability_modifer(ability_value):
    '''Provides the corresponding modifier for a provided 
       attribute value
    '''
    modifier = -5
    for i in range(ability_value):
        if i % 2 == 0:
            modifier + 1

    return modifier


def die_roll(num_die, dtype, modifier):
    '''Basic DnD die roll'''
    roll_value = 0
    for _ in range(num_die):
        roll_value += roll_value + random.randint(1,dtype)
    roll_value = roll_value + modifier
    return roll_value 


def order_by_initiative(creature_list):
    '''Ordering operation (mostly used to order creatures by 
       initiative
    '''
    # Create an empty list to place ordered creatures
    ordered_creature_list = []

    # initializer ordered list with first creature in list
    ordered_creature_list.append(creature_list[0])

    for curr_creature in creature_list[1:]:
        num_ordered_creatures = len(ordered_creature_list)
        for (ord_creature, idx) in zip(ordered_creature_list,
                            range(num_ordered_creatures)):
            if curr_creature.initiative >= ord_creature.initiative:
                ordered_creature_list.insert(idx, curr_creature)
                break
            if idx + 1 == num_ordered_creatures:
                ordered_creature_list.append(curr_creature)

    return ordered_creature_list

#    # Add creature to orderedCreatureList based on initiative value
#    num_creatures = len(creature_list)
#
#
#    # Place first creature in ordered list
#    creature = creature_list[0]
#    ordered_creature_list.append(creature)
#    for idx in range(1, num_creatures):
#
#        creature = creature_list[idx]
#        length_of_ordered_list = len(ordered_creature_list)
#        #i = num_creatures//2
#        i = length_of_ordered_list//2
#
#        ordered = False
#        while not ordered:
#            if creature.initiative > \
#                        ordered_creature_list[i].initiative:
#                i = (i + length_of_ordered_list)//2
#            elif creature.initiative < \
#                        ordered_creature_list[i].initiative:
#                i = i//2
#            else:
#                ordered_creature_list.insert(i+1, creature)
#                ordered = True

    #return ordered_creature_list


def select_next_target(curr_creature, character_list):

    creature_action_list = list()
    print('\n0) Self')
    creature_action_list.append(curr_creature)
    for creature,idx in enumerate(character_list):
        allegiance = creature.allegiance
        creature_action_list.append(creature)
        print('\n{0} {1}    | Allegiance: {2}'.format(idx, creature.name,
                                allegiance))
    target_idx = int(input('\nChoose target: '))
    target = character_list[target_idx]
    return target


def read_single_keypress():
   pass 




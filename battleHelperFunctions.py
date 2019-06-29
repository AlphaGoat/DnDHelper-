import random


def actionRoll(numDie, dtype, modifier, target, effect):
    '''Basic DnD die roll'''
    return numDie * random.randint(1,dtype) + modifier


def ordering_operation(creature_list)
    '''Ordering operation (mostly used to order creatures by 
       initiative
    '''
    # Create an empty list to place ordered creatures
    ordered_creature_list = list()

    # Add creature to orderedCreatureList based on initiative value
    num_creatures = len(creature_list)

    # Place first creature in ordered list
    creature = creature_list[0]
    ordered_creature_list.append(creature)
    for creature_idx in range(1, num_creatures):

        creature = creature_list[idx]
        length_of_ordered_list = len(ordered_creature_list)
        i = num_creatures//2
        i = lengthOfList//2

        ordered = False
        for(!ordered):
            if creature.initiative > \
                        ordered_creature_list[i].initiative:
                i = (i + length_of_ordered_list)//2
            elif creature.initiative < \
                        ordered_creature_list[i].initiative:
                i = i//2
            else:
                ordered_creature_list.insert(i+1, creature)
                ordered = True

    return ordered_creature_list


def select_next_target(curr_creature, character_list):

    creature_action_list = list()
    print('\n0) Self')
    creature_action_list.append(curr_creature)
    for creature,idx in enumerate(character_list):
        allegiance = creature.allegiance
        creature_action_list.append(creature)
        print('\n{0} {1}    | Allegiance: {2}'.format(idx, creature.name,
                                allegiance)
    target_idx = int(input('\nChoose target: '))
    target = character_list[target_idx]
    return target


def read_single_keypress():
    




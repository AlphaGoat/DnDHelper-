import battleHelperFunctions as bHF


class QuickBattle(object):

    def __init__(self, npc_creatures, player_characters):

        self.npc_creatures
        self.player_characters

        # begin battle, you fool!"
        self.battle_script()


    def roll_initiative(self):

        all_characters_list =

        for npc in npc_creatures:

           dexterity = npc.attributes['DEX']
           dex_modifier = bHF.get_ability_modifer(dexterity)
           npc.initiative = bHF.die_roll(1, 20, dex_modifier)
           all_characters_list.append(npc)

        for player in player_characters:

            print("What is {}'s initiative roll?".format(player.name))
            roll_value = raw_input('roll_value: ')
            player.initiative = roll_value
            all_characters_list.append(player)

        self.ordered_creature_list = bHF.order_by_initiative(all_characters_list)

    def npc_action(self, npc):

        action_dict = dict()
        i = 0
        print('----Attacks----')
        for key, _ in npc.data['attacks'].items():
            print("{0}) {1}".format(i, key))
            action_dict[i] = (0, key)
            i += 1

        print('----Spells----')
        if npc.data['spells'] == None:
            print('npc {} has no spells'.format(npc.npc_id))

        else:
            for key, _ in npc.data['spells'].items()
                print("{0}) {1}".format(i, key))
                action_dict[i] = (1, key)
                i += 1

        action_idx = raw_input("Chosen action idx: ")
        action_bool, action = action_dict[action_idx]
        if action_bool == 1:
            action_data = npc.data['attacks'][action]
        else:
            action_data = npc.data['spells'][action]
            print("Spell description:\n{}".format(
                action_data['description']))

        # roll for action
        dtype = action_data['dType']
        number = action_data['dNumber']
        modifier = action_data['modifier']

        roll_value = bHF.die_roll(number, dtype, modifier)

        return roll_value

    def battle_script(self):

        # first, roll initiative
        self.roll_initiative()

        # Go through everyone's turn
        iterator = 0
        stop_battle = False
        while stop_battle == False:
            for next_character in self.ordered_creature_list:
                #next_character = self.ordered_creature_list[iterator]
                if next_character.dead:
                    # Check if all npcs are dead
                    stop_battle = True
                    for npc in self.npc_creatures:
                        if not npc.dead:
                            stop_battle = False
                            break

                    if stop_battle == True:
                        break

                elif next_character.npc == 0:
                    print("It is {}'s turn.".format(next_character.name))
                    print("Is {} dead?").format(next_character.name))

                    if raw_input('(y/N)').lower() == 'y':
                        next_character.dead = True

                    raw_input('press any key to continue: ')
                    continue

                else:
                    print("It is {}'s turn.".format(next_character.npc_id))
                    while True:
                        print("Take an action?")
                        if raw_input('(y/N)').lower() == 'n':
                            continue
                        else:
                            roll_value = self.npc_action()
                            print("{0} rolled {1}".format(next_character.npc_id,
                                                          roll_value))


        print("Engagement over")


class PlayerCharacter(object):

    def __init__(self, name):

        self.name = name
        self.dead = False
        self.npc = 0


if __name__ == '__main__':



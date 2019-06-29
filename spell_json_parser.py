import json

def open_spells_json(path="/home/peter/Programming/Python_Files/" +
        "DnDHelper/SpellConfigFiles/5e-spells-master/spells.json"):

    with open(path) as spells_data_json:
        spells_data = json.load(spells_data_json)

        # Make the name of spells invariant by spacing and capitalization
        list_of_spells = list()
        for key, _ in spells_data.items():
            new_key = key.lower().replace(' ','')
            spell_tuple = (new_key, key)
            list_of_spells.append(spell_tuple)

        for spell_tuple in list_of_spells:
            new_key = spell_tuple[0]
            old_key = spell_tuple[1]
            spells_data[new_key] = spells_data[old_key]
            del spells_data[old_key]

    return spells_data


def spell_lookup(spell, spells_data):

    return spells_data[spell]


if __name__ == '__main__':

    spells_data = open_spells_json()
    continueLoop = True
    while continueLoop:
        spell_name = input("Type in a spell name: ")
        invariant_spell_name = spell_name.lower().replace(' ','')

        try:
            info = spells_data[spell_name]
            for key, value in info:
                print("{0} : {1}".format(key, value))

        except KeyError:
            print("Error: name of spell not recognized. Try again")

        while True:
            confirmation = input("Continue? (Y/n): ")
            if confirmation.lower() == "y" or confirmation.lower() == "yes":
                break
            elif confirmation.lower() == 'n' or confirmation.lower() == 'no':
                continueLoop = False
            else:
                print("Error: input not understood. Try again.")
                pass




    
    
    

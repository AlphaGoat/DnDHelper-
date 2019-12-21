import PyPDF2
import re

# DEBUGGING Only
import pdb

def monster_manual_lookup(manual_file_path, monster):
    """
    function that opens and reads monster manual,
    allowing lookup of creature entries

    :param manual_file_path: file path for the monster
                             manual

    :param monster: monster that we are looking up in the
                    manual

    :return monster_text: a string containing all the text contained
                          in the page describing the monster in the
                          Monster Manual
    """
    # Prepare the monster string to match format in
    # the monster manual
    sub_words = monster.split(' ')
    capitalized_words = []
    for word in sub_words:
        first_char = word[0].upper()
        capitalized_word = first_char + word[1:]
        capitalized_words.append(capitalized_word)

    monster = " ".join(capitalized_words)

    # Open monster manual pdf:
    with open(manual_file_path, 'rb') as pdf:
        # Create a pdf reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf)

        # Retrieve pdf outlines
        outlines = pdf_reader.outlines

        # Find indices that allow us to extract text about
        # chosen monster from monster manual
        index_list, key = find_index_by_value(outlines, monster)

        if not index_list:
            print("Error: {} not found in monster manual. Try different entry".format(monster))
            return

        # Dive into lists to find text for the monster entry
        current_level = outlines[index_list[0]]
        #pdb.set_trace()
        for idx in index_list[1:]:
            current_level = current_level[idx]

        # Get the page id of the monster that we are interested in
        # (Note: this id is not the same as the actual page number
        # itself. We will need to run a conversion method to extract
        # the number from the id that we are given
        page_id = current_level.page.idnum

        page_id_to_number_dict, _ = assign_page_id_to_number(pdf_reader)

        page_number = page_id_to_number_dict[page_id]

        # Extract text from given pdf page number
        page = pdf_reader.getPage(page_number)
        monster_info_text = page.extractText()

        # Try to extract all information that we need from this page.
        monster_info_dict = {}

        # Initialize error dict to keep track of information that
        # we were unable to fetch
        error_dict = {}

        ####################
        # FETCH ATTRIBUTES #
        ####################

        # Initialize list of attributes we need to fetch
        attribute_list = ["strength", "dexterity", "constitution",
                          "intelligence", "wisdom", "charisma"]

        # Initialize empty dict entry to hold attribute information
        monster_info_dict["attributes"] = {}

        # Initialize loop to grab all attribute information
        pass_code == 0
        unfetched_attribute_list = attribute_list
        attribute_page_number = page_number
        attribute_page = pdf_reader.getPage(attribute_page_number)
        attribute_text = attribute_page.extractText()
        while not pass_code:

            attribute_dict, pass_code = fetch_attributes(attribute_text,
                                                         attribute_list)
            for key, value in attribute_dict.items():
                monster_info_dict["attributes"][key] = value

                # Remove "key" (attribute) from attribute list, as
                # it has been succesfully fetched
                unfetched_attribute_list.remove(key)

            # see if pass code has been issued. If not, increment page
            # number by one and fetch next page of text to shift through
            if not pass_code:
                attribute_page_number += 1

                # If we have gone five pages without seeing anything, issue
                # error code for attributes and continue
                if (attribute_page_number - page_number) > 5:

                    # Issue error codes for specific attributes we were unable
                    # to fetch
                    for attribute in attribute_list:

                        if attribute in unfetched_attribute_list:
                            error_dict["attributes"][attribute] = 0
                        else:
                            error_dict["attributes"][attribute] = 1
                            break

                # If we have not busted the five page limit yet, fetch the next
                # page
                attribute_page = pdf_reader.getPage(attribute_page_number)
                attribute_text = attribute_page.extractText()

    #####################
    # FETCH ARMOR CLASS #
    #####################

    # Initialize empty dictionary entry for armor class
    # values we want to add: base_value of armor class (an int),
    # as well as type of armor (natural armor, chainmail, etc.)
    ac_page_number = attribute_page_number
    ac_page = pdf_reader.getPage(ac_page_number)
    ac_text = ac_page.extractText()

    pass_code = 0
    while not pass_code:

        ac_dict, pass_code = fetch_armor_class(ac_text)

        # if the pass code was not issued, increment page number by one and try again
        if not pass_code:
            ac_page_number += 1

            # Check if we have passed the five page limit
            if (ac_page_number - attribute_page_number) > 3:
                # Go back to first page of the "creature" and
                # see if we may have missed it
                ac_page_number = page_number
                ac_page = pdf_reader.getPage(ac_page_number)
                ac_text = ac_page.extractText()
                continue

            elif (ac_page_number - page_number) > 5 and (ac_page_number - attribute_page_number) > 2:
                error_dict["armor_class"] = 0
                break


    monster_info_dict["armor_class"] = ac_dict

    ####################
    # FETCH HIT POINTS #
    ####################

    # Initialize empty dictionary entry for hit point
    # values that we want to add: base_value for hit points
    # as well as the hit die of the creature
    hp_page_number = page_number
    hp_page = pdf_reader.getPage(hp_page_number)
    hp_text = hp_page.extractText()

    pass_code = 0
    while not pass_code:

        hp_dict, pass_code = fetch_hit_points(hp_text)

        # if the pass code was not issued, increment page number by one and try again
        if not pass_code:















        monster_info_dict, error_code = parse_description_text(monster_info_text,
                                                               monster_info_dict)

        # If we aren't able to grab everything, keep iterating until
        # we do. We will force this iteration with an error code
        # returned from the parsing function. An error_code of 1 means
        # the script failed to grab a piece of information from the text,
        # incrementing the page number by one. An error_code of 0 means
        # that all information was grabbed OR we incremented by 5 and didnt
        # grab everything, exiting the loop
        while error_code:
            page_number += 1
            page = pdf_reader.getPage(page_number)
            monster_info_text = page.extractText()
            monster_info_dict, error_code = parse_description_text(monster_info_text,
                                                                   monster_info_dict)

        return monster_text

def find_index_by_value(outlines, value):
    """
    Recurses through outline looking through value provided.
    When that value is found, the function returns the index
    of the element in the list where the value was found
    for further processing
    """
    # list of indices, tiered so that the first index goes to
    # the highest level list, and indices after go to lists
    # nested within
    index_list = []
    for outline_idx, outline_entry in enumerate(outlines):

        # if the outline_entry is a list, go through it to check if the value
        # is in it by recursive call
        if type(outline_entry) == list:
            #pdb.set_trace()
            subindex_list, key = find_index_by_value(outline_entry, value)

            # See if any entries were returned by the recursive call. If so,
            # we have our indices!
            if subindex_list:
                index_list.append(outline_idx)

            for index in subindex_list:
                index_list.append(index)

        # Check list of values in dictionary to see if the monster name
        # is in there. Continue on if a value error is thrown
        else:
            try:
                key = list(outline_entry.keys())[list(outline_entry.values()).index(value)]
                index_list.append(outline_idx)

                return index_list, key

            except ValueError:
                continue

    return index_list, None

def assign_page_id_to_number(pdf_object, root=True, _result=None,
                             page_counter=None, num_pages=None):


    # dict to keep track of ids to page number
    if not _result:
        _result = {}

        # we will have to iterate through page objects until
        # we get ours to get the page number associated with
        # this id. Initialize page counter
        page_counter = 0

    # Get pages
    if root:
        pages = pdf_object.trailer["/Root"].getObject()["/Pages"].getObject()

        # number of pages in pdf
        num_pages = pages['/Count']

    else:
        pages = pdf_object.getObject()

    _type = pages["/Type"]
    if _type == "/Pages":

        for page in pages["/Kids"]:
            _result[page.idnum] = page_counter
            _, page_counter = assign_page_id_to_number(page, root=False,_result=_result,
                                     page_counter=page_counter, num_pages=num_pages)

    elif _type == '/Page':
        page_counter += 1

    return _result, page_counter

def parse_description_text(monster_desc_text, monster_info_dict):
    """
    Parsing function that takes in all text from monster manual page
    on a given creature and returns information that we need (stats,
    action and spell descriptions, etc.)
    """
    # TODO: find some way to deal with newline characters
    #       (they are seriously messing everything up
    print(monster_desc_text.encode())

def fetch_attributes(text,
                     attribute_list=None):

    # Retrieve creatures attributes

    attribute_dict = {}
    for attribute in attribute_list:
        # Perform regex to find stats in description text:
        # TODO: find a way to get charisma working (it has to do
        #       with the new line character in the text
        print("attribute: ", attribute[:3].upper())
        r_attribute_str = r'{}(.*?)\s*\n?\)'.format(attribute[:3].upper())
        result = re.search(r_attribute_str, text, re.M)

        # See if the regex search returned a string.
        try:
            print("result.group(): ", result.group())

            # Perform further post processing on the returned string
            # to extricate base state value and modifier
            split_str = result.group().split(' ')

            base_stat = split_str[1]

            modifier = re.search(r'(\-|\+)(.*?)[^\)]', split_str[2])


            attribute_stats = {
                'base_stat': base_stat,
                'modifier': modifier,
            }

            attribute_dict[attribute] = attribute_stats

        # If no string was returned, then we know that the pattern wasn't
        # present and we need to increment page number by 1
        except AttributeError:
            return attribute_dict, 0

    return attribute_dict, 1

def fetch_armor_class(text):
    """
    Fetches information about a creature's armor class from
    provided text from the Monster Manual

    :return armor_class: a dict with two entries, armor value and armor type
    """
    # MATCH FOR ARMOR CLASS
    # Retrieve armor class
    r_armor_class_str = r'Armor Class(.*?)\)'
    result_ac = re.search(r_armor_class_str, monster_desc_text, re.M)

    armor_class = {}

    # See if the regex pattern search returned anything
    try:
        # find the armor class value by excluding values after '('
        ac_value_match = re.search(r'\s(.*?)[&\s\(]', result_ac.group(1))
        ac_value = int(ac_value_match.group().strip())

        ac_type_match = re.search(r'\((.*?)\)', result_ac.group())
        ac_type = ac_type_match.group(1)

        armor_class['value'] = ac_value
        armor_class['type'] = ac_type

    except AttributeError:
        return armor_class, 0

    return armor_class, 1


    # MATCH FOR HITPOINTS
    # See if we've already retrieved hitpoint info
    try:
        monster_info_dict["hit_points"]

    except KeyError:
        # retrieve hit points
        r_hitpoints_pattern = r'Hit Points (.*?)\)'
        hitpoints_match = re.search(r_hitpoints_pattern, monster_desc_text, re.M)
        s_hitpoints = hitpoints_match.group()
        print("s_hitpoints: ", s_hitpoints)

        # Refine found expression further to get base hitpoints and die
        base_hitpoints = int(re.search('Hit Points (.*?)\(', s_hitpoints).group(1).strip())
        print("base_hitpoints: ", base_hitpoints)

        # Determine modifier, number of die, and die type
        hitpoints_die_stats = re.search('\((.*?)\)', s_hitpoints).group(1)
        die_stats_strings = hitpoints_die_stats.split(' ')
        modifier = int(die_stats_strings[2])
        num_die, die_type = [int(stat) for stat in die_stats_strings[0].split('d')]

        # Incorporate all info we need about creature hitpoints in dictionary
        hitpoints = {
            'base_hitpoints': base_hitpoints,
            'die_stats': {
                'num_die': num_die,
                'die_type': die_type,
                'modifier': modifier
            }
        }

    # MATCH FOR ALIGNMENT
    # list out all possible alignments the creature could have
    possible_alignments = ['lawful good', 'lawful neutral', 'lawful evil',
                           'neutral good', 'neutral', 'neutral evil',
                           'chaotic good', 'chaotic neutral', 'chaotic evil']

    # Create a reg expression that matches for any of them
    alignment_pattern = "{}".format(possible_alignments[0])
    for possible_alignment in possible_alignments[1:]:
        alignment_pattern = alignment_pattern + "|{}".format(possible_alignment)

    r_alignment_pattern = r"" + alignment_pattern

    # use reg expression to find the alignment of our beast!
    r_alignment_match = re.search(r_alignment_pattern, monster_desc_text, re.M)
    alignment = r_alignment_match.group()

    if alignment == 'chaotic evil':
        print("You naughty boy!")

    # Match for creature types
    # Following similar pattern as with alignments, list out all possible
    # creatures types to match with
    # TODO: add some functionality that allows the input of custom creature types
    possible_creature_types = ["Aberration", "Beast", "Celestial", "Construct", "Dragon",
                               "Elemental", "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity",
                               "Ooze", "Plant", "Undead"]

    creature_type_pattern = "{}".format(possible_creature_types[0])
    for possible_creature_type in possible_creature_types[1:]:
        creature_type_pattern = creature_type_pattern + "|{}".format(possible_creature_type)

    r_creature_type_pattern = r". (?i)" + creature_type_pattern + ',\s' + alignment
    print("creature_type_pattern: ", creature_type_pattern)


    # use reg expression to find the creature type of our beast!
    r_creature_type_match = re.search(". " + creature_type_pattern + ',\s' + alignment,
                                      monster_desc_text, re.M | re.IGNORECASE)
    creature_type = r_creature_type_match.group()

    print("creature_type: ", creature_type)

    # Grab languages spoken by the creature














if __name__ == '__main__':

    monster_text = monster_manual_lookup("/home/alphagoat/Projects/DnDHelper/DnD_pdfs/dnd_monster_manual.pdf",
                          "mind flayer")

    parse_description_text(monster_text)





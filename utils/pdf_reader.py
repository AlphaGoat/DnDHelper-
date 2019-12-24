import PyPDF2

import argparse
import re
import subprocess
import sys


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

        # Print out creature text for parsing purposes
        page = pdf_reader.getPage(page_number)
        text = page.extractText().replace('\n','')
        print("creature text: ", text)

        return page_number

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

def fetch_attributes(text, attribute_dict={}):

    # List of creature attributes
    attribute_list = ["Strength", "Dexterity", "Constitution",
                      "Intelligence", "Wisdom", "Charisma"]

    # Retrieve creatures attributes
    for attribute in attribute_list:

        # If the attribute is already accounted for in the attribute_dict,
        # then there is no reason to search for it. Continue to next attribute
        if attribute in attribute_dict.keys():
            continue

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

            modifier = re.search(r'(\-|\+)(.*?)[^\)]', split_str[2]).group()


            attribute_stats = {
                'base_stat': base_stat,
                'modifier': modifier,
            }

            attribute_dict[attribute] = attribute_stats

        # If no string was returned, then we know that the pattern wasn't
        # present and we need to increment page number by 1
        except AttributeError:
            print("attributes fetched: ", attribute_dict)
            return attribute_dict, 0

    print("attribute_dict: ", attribute_dict)
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
    result_ac = re.search(r_armor_class_str, text, re.M)

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

    print("armor_class info: ", armor_class)
    return armor_class, 1

def fetch_hit_points(text):

    # MATCH FOR HITPOINTS
    r_hitpoints_pattern = r'Hit Points (.*?)\)'
    hitpoints_match = re.search(r_hitpoints_pattern, text, re.M)

    hitpoints = {}

    # See if regex pattern search actually found anything
    try:
        s_hitpoints = hitpoints_match.group()

        # Refine found expression further to get base hitpoints and die
        base_hitpoints = int(re.search('Hit Points (.*?)\(', s_hitpoints).group(1).strip())

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

        print("hitpoints success: ", hitpoints)
        return hitpoints, 1

    except AttributeError:
        print("hitpoints fail: ", hitpoints)
        return hitpoints, 0

def fetch_alignment(text):

    # MATCH FOR ALIGNMENT
    # list out all possible alignments the creature could have
    possible_alignments = ['lawful good', 'lawful neutral', 'lawful evil',
                           'neutral good', 'neutral', 'neutral evil',
                           'chaotic good', 'chaotic neutral', 'chaotic evil']

    # Try to match with regex pattern
    try:
        # Create a reg expression that matches for any of them
        alignment_pattern = "{}".format(possible_alignments[0])
        for possible_alignment in possible_alignments[1:]:
            alignment_pattern = alignment_pattern + "|{}".format(possible_alignment)

        r_alignment_pattern = r"" + alignment_pattern

        # use reg expression to find the alignment of our beast!
        r_alignment_match = re.search(r_alignment_pattern, text, re.M)
        alignment = r_alignment_match.group()

        if alignment == 'chaotic evil':
            print("You naughty boy!")

        print("alignment: ", alignment)
        return alignment, 1

    # If regex pattern matched with nothing, return fail code
    except AttributeError:
        return alignment, 0


def fetch_creature_type(text, alignment):

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
                                      text, re.M | re.IGNORECASE)

    try:
        creature_type = r_creature_type_match.group()

    except AttributeError:
        creature_type = None

    if not creature_type:
        print("No creature_type returned")
        return creature_type, 0

    else:
        print("creature_type: ", creature_type)
        return creature_type, 1

def fetch_known_languages(bag_of_words):
    """
    Grab languages spoken by the creature
    """
    # No regexes needed for this pattern!
    # Convert the presented text into a 'bag of words' (i.e, a list of words)
    #bag_of_words = text.split()

    # Find the index of the first instance of the word 'Languages' in the list
    language_label_index = bag_of_words.index('Languages')

    # Find the index of the first instance of the world "Challenge" in the list
    challenge_label_index = bag_of_words.index('Challenge')

    # The languages the creature speaks are the words between these two indices
    start_languages_index = language_label_index + 1
    end_languages_index = challenge_label_index - 1


    print("start_languages_index: ", start_languages_index)
    print("end_languages_index: ", end_languages_index)

    # If the starting language index is the same as the end,
    # then the creature only speaks one language
    if start_languages_index == end_languages_index:
        languages = bag_of_words[start_languages_index]

    else:
        # pre-initialize list to store all languages we parse
        languages = []

        for i in range(start_languages_index, challenge_label_index):
            languages.append(bag_of_words[i])

    # Check to see if we actually grabbed anything (i.e., the list is populated)
    if languages:
        print("return languages: ", languages)
        return languages, 1

    else:
        print("no languages returned")
        return languages, 0

def fetch_challenge_rating_and_xp(bag_of_words):
    """
    Grab the challenge rating and experience points
    of a creature from a provided 'bag of words'
    (ordered list of words in text)
    """
    # Find the index of the first instance of the word "Challenge"
    challenge_label_index = bag_of_words.index('Challenge')






def fetch_wrapper(monster_manual_path, creature_page_number):
    """
    Wrapper function to iterate over page numbers until
    the desired creture trait we want to fetch has been found

    :param creature_page_number: page number for creature info in
                                 Monster Manual, determined by the
                                 monster_manual_lookup method

    :param pdf_reader: pdf reader object for the Monster Manual

    :return creature_dict: dictionary with all the traits that we are
                           interested in (i.e., attributes, hit_points,
                           etc.) as keys and stats for those traits as
                           values
    """
    # dict to hold all information we need about a creature
    creature_dict = {}

    # list of traits that we would like to fetch for creature
    trait_list = ['attributes', 'armor_class', 'hit_points',
                  'alignment', 'creature_type', 'languages',
                  'passive_perception', ]

    # Open up Monster Manual pdf and initialize a new reader
    with open(monster_manual_path, 'rb') as pdf:

        # Create a pdf reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf)

        for trait in trait_list:
            # Initialize loop to grab all desired traits of a given creature
            pass_code = 0
            trait_page_number = creature_page_number

            # Initialize empty dict to keep track of traits we are unable to
            # fetch
            error_dict = {}

            # Initialize empty dict for atttributes
            if trait == 'attributes':
                attribute_dict = {}

            while not pass_code:

                trait_page = pdf_reader.getPage(trait_page_number)
                print("trait_page_number: ", trait_page_number)
                trait_text = trait_page.extractText().replace('\n','')

                # Fetch attributes
                if trait == 'attributes':

                    attribute_dict, pass_code = fetch_attributes(trait_text,
                                                                 attribute_dict=attribute_dict)

                # Fetch armor class
                elif trait == 'armor_class':

                    armor_class, pass_code = fetch_armor_class(trait_text)

                # Fetch hit points
                elif trait == 'hit_points':

                    hit_points, pass_code = fetch_hit_points(trait_text)

                # Fetch alignment
                elif trait == 'alignment':

                    alignment, pass_code = fetch_alignment(trait_text)

                elif trait == 'creature_type':

                    creature_type, pass_code = fetch_creature_type(trait_text,
                                                                    alignment)
                    print("pass_score after creature_type: ", pass_code)

                elif trait == 'languages':
                    bag_of_words = trait_text.split()
                    languages, pass_code = fetch_known_languages(bag_of_words)

                elif trait == 'challenge':
                    bag_of_words = trait_text.split()
                    challenge, pass_code = fetch_challenge_rating(bag_of_words)

                elif trait == 'passive_perception':
                    pass

                # see if pass code has been issued. If not, increment page
                # number by one and fetch next page of text to shift through
                if not pass_code:
                    trait_page_number += 1

                    # If we have gone five pages without seeing anything, issue
                    # error code for attributes and continue
                    if (trait_page_number - creature_page_number) > 5:

                        # Issue error codes for specific attributes we were unable
                        # to fetch
                        if trait == 'attributes':
                            error_dict['attributes'] = {}

                            for key in attribute_dict.keys():

                                if not attribute_dict[key]:
                                    error_dict['attributes'][key] = 1

                                else:
                                    error_dict['attributes'][key] = 0

                        else:
                            error_dict[trait] = 0

                        # Since we have busted the five page limit, break the
                        # loop for this trait and move onto the next
                        break


    # Populate the creature_dict with traits that we have fetched
    creature_dict['attributes'] = attribute_dict
    creature_dict['armor_class'] = armor_class
    creature_dict['hit_points'] = hit_points
    creature_dict['alignment'] = alignment
    creature_dict['creature_type'] = creature_type

def open_pdf_to_page(page_number,
                     monster_manual_path):
    """
    Uses document viewer to open up Monster Manual pdf to specific
    page
    """
    if sys.platform =='linux':
        # Try to open pdf with evince document viewer
        cmd = "evince --page_label={0} {1}".format(page_number, monster_manual_path)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--monster_manual_path', type=str,
                        default='../DnD_pdfs/dnd_monster_manual.pdf',
                        help="System path to DnD 5th Edition Monster Manual"
                        )

    parser.add_argument('--monster_to_loopup', type=str,
                        default='minotaur',
                        help="""
                             Monster that we would like to lookup in the Monster Manual and extract
                             stats for
                             """
                        )


    flags, _ = parser.parse_known_args()

    monster = flags.monster_to_loopup
    path = flags.monster_manual_path

    page_number = monster_manual_lookup(path, monster)

    creature_dict = fetch_wrapper(path, page_number)

    open_pdf_to_page(page_number, path)






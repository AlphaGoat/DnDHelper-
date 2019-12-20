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
        monster_text = page.extractText()

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

def parse_description_text(monster_desc_text):
    """
    Parsing function that takes in all text from monster manual page
    on a given creature and returns information that we need (stats,
    action and spell descriptions, etc.)
    """
    print(monster_desc_text)

    # Retrieve creatures attributes
    attribute_list = ["strength", "dexterity", "constitution",
                      "intelligence", "wisdom", "charisma"]

    attribute_dict = {}
    for attribute in attribute_list:
        # Perform regex to find stats in description text:
        print("attribute: ", attribute[:3].upper())
        r_attribute_str = r'{}(.*?)\)'.format(attribute[:3].upper())
        result = re.search(r_attribute_str, monster_desc_text)

        # Perform further post processing on the returned string
        # to extricate base state value and modifier
        split_str = result.group().split(' ')
        print("split_str: ", split_str)

        base_stat = split_str[1]

        modifier = re.search(r'(?<=\(\+)(.*?)(?=\))', split_str[2])

        print("modifier: ", modifier.group())

        attribute_stats = {
            'base_stat': base_stat,
            'modifier': modifier,
        }




if __name__ == '__main__':

    monster_text = monster_manual_lookup("/home/alphagoat/Projects/DnDHelper/DnD_pdfs/dnd_monster_manual.pdf",
                          "minotaur")

    parse_description_text(monster_text)





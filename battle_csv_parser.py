import csv

def parse_battle_csv(csv_file):
	'''parses the battle csv and returns a dictionary with
	   the creature name as the keys and a list with the
       creature allegiance as the first element and the 
       creature type as the second element
	'''
	with open(csv_file, 'r') as f:
		creature_reader = csv.reader(f, delimiter=',', quotechar='|')
		fields = next(creature_reader)
		creature_dicts = []
		for row in creature_reader:
			# Zip together the field names and values
			creature_items = zip(fields, row)
			creature_dict = {}
			# Add the value to our dictionary
			for (field, value) in creature_items:
				creature_dict[field] = value.strip()
			creature_dicts.append(creature_dict)
	return creature_dicts



import re
import pandas

def parseMonsterCFG(monsterType):

	# Address for all monster configurations
	monsterAddr = "/home/pthomas/Python_Files/DnDHelper/MonsterConfigFiles/"

	# Remove all spaces in the input str
	monsterType.replace(" ", "")

	# convert all upper space characters to lower space
	monsterType.lower()

	data = []
	with open(

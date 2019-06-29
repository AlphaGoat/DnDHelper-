import random as rd


class Monster():

	def __init__(self, name, creatureType, hitdie, modifiers, 
			     attacks, spells):

		# Set creature attributes
		self.name = name
		self.creatureType = creatureType
		self.hitdie = hitdie # takes form of three element list (number
						     # of die, die type, and additional modifier
		self.modifiers = modifiers
		self.attacks = attacks
		self.spells = spells	

		# Randomized creature attributes
		self.initiative = None
		self.hp = None

		# Is the creature alive or dead?
		self.alive = True


	def hitpoints(self):
		'''determines the hitpoints of the creature'''	
		numdie = self.hitdie[0]
		typeDie = self.hitdie[1]
		modifier = self.hitdie[2]
	
		self.hitpoints = DieRoll(numDie, typeDie, modifier)

		if self.hitpoints <= 0:

			self.alive = False


	def rollInitiative(self):
		'''Rolls initiative for the creature (any number
		   from 1-20
		'''
		self.initiative = rd.randint(1,20)

	
	def attackRoll(self, attackType):
		'''
		   Determines if an attack hits or not
		'''
		modifierToHit = self.attacks[attackType][1]
		attackRoll = rd.randint(1,20) + modifierToHit

		return attackRoll	

	
	def attackDmg(self, attackType):
		'''
			Rolls for attack dmg
		'''
		attackDmgList = self.attacks[attackType][0]
		numDie = attackDmgList[0]
		typeDie = attackDmgList[1]
		modifier = attackDmgList[2]

		attackDmg = DieRoll(numDie, typeDie, modifier)

		return attackDmg		
				 	


def DieRoll(numDie, typeDie, modifier):

		value = 0
		for i in numDie:

			value = value + rd.randint(1, typeDie)

		value = value + modifier
		
		return value



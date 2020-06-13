"""
Dungeons & Dragons combat simulator
By Josh Zhang, 2020/06/12
potential feature: intiative, mutliple attacks a turn, great weapon fighting
06/13
moar functions! each attack now is a function
to do: observer pattern? rage dmg reduction & ripose.	Intiative, action surge
"""

#test to see if the program is running
print "The Arena"

#setup
import math

# generate random integer values
from random import seed
from random import randint

# seed random number generator
import random
from datetime import datetime
random.seed(datetime.now())

#to note, current numbers are based off of 0 = battlerager barbarian 7, 1 = battlemaster fighter 7

#stats for all combatants
maxHp = [82,74]
ac = [17,17]

attackBonus = [7,8]
damageBonus = [6,5]

intiativeBonus = [2,2]

level = [7,7]
constitutionMod = [4,4]

#setting up variables
hp = maxHp
roundCount = 0
tempHp = [0,0]
reaction = [1,1]

superiority = [0,4]

#setting up diffrent options in combat

def attack(x):
	return randint(1,20) + x

def attackAdvantage(x):
	return max(randint(1,20),randint(1,20)) + x

def attackDisadvantage(x):
	return min(randint(1,20),randint(1,20)) + x

def greatSwordDamage(x):
	return randint(1,6) + randint(1,6) + x

def greatWeaponFightingGreatSwordDamage(x):
	a = randint(1,6)
	if a <= 2:
		a = randint(1,6)
	b = randint (1,6)
	if b <= 2:
		b = randint(1,6)
	return a + b + x

def spikeArmourDamage(x):
	return randint (1,4) + x

#combat options

def barbarianGreatSwordAttack():
	if attackAdvantage(attackBonus[0]) >= ac[1]:
		hp[1] = hp[1] - greatSwordDamage(damageBonus[0])
		if reaction[1] == 1 and hp[1] > 0 and superiority[1] > 0:
			reaction[1] = 0
			superiority[1] = superiority[1] - 1
			if attackAdvantage(attackBonus[1]) >= ac[0]:
				tempHp[0] = tempHp[0] - math.floor(0.5*greatWeaponFightingGreatSwordDamage(damageBonus[1]))
			if tempHp[0] < 0:
				hp[0] = hp[0] + tempHp[0]
				tempHp[0] = 0

def barbarianSpikedArmourAttack():
	if attackAdvantage(attackBonus[0]) >= ac[1]:
		hp[1] = hp[1] - spikeArmourDamage(damageBonus[0])
		if reaction[1] == 1 and hp[1] > 0 and superiority[1] > 0:
			reaction[1] = 0
			superiority[1] = superiority[1] - 1
			if attackAdvantage(attackBonus[1]) >= ac[0]:
				tempHp[0] = tempHp[0] - math.floor(0.5*greatWeaponFightingGreatSwordDamage(damageBonus[1]))
			if tempHp[0] < 0:
				hp[0] = hp[0] + tempHp[0]
				tempHp[0] = 0

#note, the barbarian's rage if halving all physical damage he is taking, on top that his reckless abandon is giving him temporary hp
def fighterGreatSwordAttack():
	if attackAdvantage(attackBonus[1]) >= ac[0]:
		tempHp[0] = tempHp[0] - math.floor(0.5*greatWeaponFightingGreatSwordDamage(damageBonus[1]))
	if tempHp[0] < 0:
		hp[0] = hp[0] + tempHp[0]
		tempHp[0] = 0

#intiative
intiative = [randint(1,20) + intiativeBonus[0] , randint(1,20) + intiativeBonus[1]]

print "intiative" , intiative[0] , intiative[1]

#COMBAT!
############################################

print "Fight!"

#second wind (tehcincally a healing ability but as barb can not OTK its just added here as addional hp for now)
hp[1] = hp[1] + randint(1,10) + level[1]

#checking if either player has already been killed
while hp[0] > 0 and hp[1] > 0:
	
	roundCount = roundCount + 1

	#player 0 (barbarian)'s turn
	reaction[0] = 1

	#reckless adandon (refreshes his temporary hp)
	tempHp[0] = constitutionMod[0]

	#barbarian attacks!
	barbarianGreatSwordAttack()
	barbarianGreatSwordAttack()
	barbarianSpikedArmourAttack()

	#checking if player 1 died from the attack
	if hp[1] > 0:
			
		#player 1 (fighter)'s turn
		reaction[1] = 1
		
		#fighter attacks!
		fighterGreatSwordAttack()
		fighterGreatSwordAttack()

	#debug / play by play
	print "roundCount" , roundCount
	print "hp[0]" , hp[0]
	print "hp[1]" , hp[1]
	print "superiority[1]" , superiority[1]

##########################################

#printing results
print "results"
print "roundCount:" , roundCount

barbarianEndQuote = ["Rarrrg!", "My rage compels me!"]
fighterEndQuote = ["Vanquished", "Fool"]

if hp[0] <= 0:
	print random.choice(fighterEndQuote)
if hp[1] <= 0:
	print random.choice(barbarianEndQuote)

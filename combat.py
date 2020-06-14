"""
Dungeons & Dragons combat simulator
By Josh Zhang

CHIRAG WAS HERE
Change log:
2020/06/12
potential feature: intiative, mutliple attacks a turn, great weapon fighting

06/13
moar functions! each attack now is a function
to do: observer pattern? rage dmg reduction & ripose.	Intiative, action surge

If ripose kills barbarian still gets the rest of his turn

Intiative, action surge and ripose have been added

Wish: observer pattern for rage? crits. barbarian ghost bug - a specific set of this bug is where both players die

Done (edit: not quite :( )! Crits have been added and the bug has been squashed. Rage remains as is. After refines it only needs to be in a single line of code, which I'm pretty happy with
bug: barbarian is in rage first turn even if fighter wins intiative
Aaaaand the bug has been squashed as well!
(also annoying actionsurge waning...)
NOW we are really done!
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
ac = [16,17]

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

hit = 0
#x = attackbonus
def attack(x):
	hit = randint(1,20)
	return hit + x

def attackAdvantage(x):
	hit = max(randint(1,20),randint(1,20))
	return hit + x

def attackDisadvantage(x):
	hit = min(randint(1,20),randint(1,20))
	return hit + x

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

#################################combat options

def barbarianGreatSwordAttack():
	if attackAdvantage(attackBonus[0]) >= ac[1]:
		if hit != 20:
			hp[1] = hp[1] - greatSwordDamage(damageBonus[0])
			ripose()
		else:
			hp[1] = hp[1] - (12 + damageBonus[0])
			ripose()		

def barbarianSpikedArmourAttack():
	if attackAdvantage(attackBonus[0]) >= ac[1]:
		if hit != 20:
			hp[1] = hp[1] - spikeArmourDamage(damageBonus[0])
			ripose()
		else:
			hp[1] = hp[1] - (4 + damageBonus[0])
			ripose()

#note, the barbarian's rage if halving all physical damage he is taking, on top that his reckless abandon is giving him temporary hp
def fighterGreatSwordAttack():
	if attackAdvantage(attackBonus[1]) >= ac[0]:
		if hit != 20:
			recklessAbandon(greatWeaponFightingGreatSwordDamage(damageBonus[1]))
		else:
			recklessAbandon(12 + (damageBonus[1]))

def fighterGreatSwordAttackNoRage():
	if attackAdvantage(attackBonus[0]) >= ac[1]:
		if hit != 20:
			hp[0] = hp[0] - greatSwordDamage(damageBonus[1])
		else:
			hp[0] = hp[0] - (12 + damageBonus[1])

#############class abilities
			
# x is the damage of the incoming attack, note that rage if halving the damage
rageActivation = 0

def recklessAbandon(x):
	if rageActivation == 1:
		tempHp[0] = tempHp[0] - math.floor(0.5 * x)
		if tempHp[0] < 0:
			hp[0] = hp[0] + tempHp[0]
			tempHp[0] = 0
	else:
		fighterGreatSwordAttackNoRage()


	tempHp[0] = tempHp[0] - math.floor(0.5 * x)
	if tempHp[0] < 0:
		hp[0] = hp[0] + tempHp[0]
		tempHp[0] = 0

def ripose():
	if reaction[1] == 1 and hp[1] > 0 and superiority[1] > 0:
		reaction[1] = 0
		superiority[1] = superiority[1] - 1
		if attackAdvantage(attackBonus[1]) >= ac[0]:
			recklessAbandon(greatWeaponFightingGreatSwordDamage(damageBonus[1]) + randint(1,8))

def recklessAbandonRegen():
	tempHp[0] = constitutionMod[0]

actionSurgeUse = 1

def actionSurge():
	if actionSurgeUse == 1:
		fighterAttacks()


#intiative
intiative = [max(randint(1,20),randint(1,20)) + intiativeBonus[0] , randint(1,20) + intiativeBonus[1]]

print "intiative" , intiative[0] , intiative[1]

#COMBAT!
############################################

def barbarianAttacks():
	barbarianGreatSwordAttack()
	if hp[0] > 0 and hp[1] > 0:
		barbarianGreatSwordAttack()
	if hp[0] > 0 and hp[1] > 0:
		barbarianSpikedArmourAttack()

def fighterAttacks():
	fighterGreatSwordAttack()
	if hp[0] > 0 and hp[1] > 0:
		fighterGreatSwordAttack()

print "Fight!"

#second wind (tehcincally a healing ability but as barb can not OTK its just added here as addional hp for now)
hp[1] = hp[1] + randint(1,10) + level[1]

#if player 0 wins intiative
#checking if either player has already been killed
while hp[0] > 0 and hp[1] > 0 and intiative[0] > intiative [1]:
	
	roundCount = roundCount + 1

	#player 0 (barbarian)'s turn
	reaction[0] = 1

	rageActivation = 1

	recklessAbandonRegen()

	#barbarian attacks!
	barbarianAttacks()

	#checking if either player has been killed
	if hp[0] > 0 and hp[1] > 0:
			
		#player 1 (fighter)'s turn
		reaction[1] = 1
		
		#fighter attacks!
		fighterAttacks()

		actionSurge()
		actionSurgeUse = 0

	#debug / play by play
	print "roundCount" , roundCount
	print "hp[0]" , hp[0]
	print "hp[1]" , hp[1]
	print "superiority[1]" , superiority[1]

#if player 1 wins intiative
#checking if either player has already been killed
while hp[0] > 0 and hp[1] > 0 and intiative[1] > intiative [0]:
	
	roundCount = roundCount + 1

	#player 1 (fighter)'s turn
	reaction[1] = 1
		
	#fighter attacks!
	fighterAttacks()

	actionSurge()
	actionSurgeUse = 0

	#checking if either player has been killed
	if hp[0] > 0 and hp[1] > 0:
			
		#player 0 (barbarian)'s turn
		reaction[0] = 1

		rageActivation = 1

		recklessAbandonRegen()

		#barbarian attacks!
		barbarianAttacks()

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

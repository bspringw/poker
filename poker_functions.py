import numpy as np
import copy
import random
import math

value_points = {
	'J' : 11,
	'Q' : 12,
	'K' : 13,
	'A' : 14}

hh_dict = {	
	'straight_flush' : 9,
	'four_of_a_kind' : 8,
	'full_house' : 7,
	'flush' : 6,
	'straight' : 5,
	'three_of_a_kind' : 4,
	'two_pair' : 3,
	'pair' : 2,
	'high_card' : 1}

#Takes list of 5 Card objects and returns
#a 6 element list, where the first element is the hand hierarchy
#(straight_flush = 9, high_card=1) and the subsequent five elements
#are the numerical card ranks (A=14, K=13, etc.), "double-sorted"
#by kind (set, pair, etc.) then by rank.  For example, the hand
#[(2, C), (K, C), (3, S), (2, D), (K, H)] gets translated to: 
#[3, 13, 13, 2, 2, 3].
def hand_strength(hand):

	#Break down hand into sub-lists of values, suits, and frequencies

	#Create list of ranks
	values_list = [x.rank for x in hand]

	#Create sorted values list
	sl = list(sorted(values_list))

	#Create list of suits
	suits_list = [x.suit for x in hand]

	#Create list of unique values  
	uvalues_list = list(set(values_list))

	#Create dict of {value : frequency}
	val_freq_dict = {}
	for x in uvalues_list:
		val_freq_dict[x] = values_list.count(x)

	#Create list of (frequency, value) tuples.
	freq_list = []
	for x in values_list:
		freq_list.append(val_freq_dict.get(x))
	freq_val_list = zip(freq_list, values_list)
	freq_val_sorted = sorted(freq_val_list, reverse=True)
	val_sorted = [x[1] for x in freq_val_sorted]

	#Determine hand hierarchy
	if 2 in freq_list:
		if len(uvalues_list) == 4:
			hh = 'pair'
		elif len(uvalues_list) == 3:
			hh = 'two_pair'
		else:
			hh = 'full_house'
	elif 3 in freq_list:
		hh = 'three_of_a_kind'
	elif len(set(suits_list)) == 1:
		hh = 'flush'
	elif sl[0] == sl[1] - 1 == sl[2] - 2 == sl[3] - 3 == sl[4] - 4 or sl == [2, 3, 4, 5, 14]:
		hh = 'straight'
	elif len(uvalues_list) == 5:
		hh = 'high_card'
	elif 4 in freq_list:
		hh = 'four_of_a_kind'
	else:
		hh = 'straight_flush'

	hh = hh_dict.get(hh)

	#Generate list representing full strength of hand.
	#hh will be at index 0, followed by the ordered values.
	hand_strength = val_sorted[:]
	hand_strength.insert(0, hh)
	
	return hand_strength

#Takes list of 7 cards (hole cards + community cards)
#and returns the list of 21 unique 5-card permutations.
def permuts(hand):

	permutsl = []

	#I know this is not the Pythonic way... (though it should be fast)
	permutsl.append([hand[0]] + [hand[1]] + [hand[2]] + [hand[3]] + [hand[4]]) #1
	permutsl.append([hand[0]] + [hand[1]] + [hand[2]] + [hand[3]] + [hand[5]]) #2
	permutsl.append([hand[0]] + [hand[1]] + [hand[2]] + [hand[3]] + [hand[6]]) #3
	permutsl.append([hand[0]] + [hand[1]] + [hand[2]] + [hand[4]] + [hand[5]]) #4
	permutsl.append([hand[0]] + [hand[1]] + [hand[2]] + [hand[4]] + [hand[6]]) #5
	permutsl.append([hand[0]] + [hand[1]] + [hand[2]] + [hand[5]] + [hand[6]]) #6
	permutsl.append([hand[0]] + [hand[1]] + [hand[3]] + [hand[4]] + [hand[5]]) #7
	permutsl.append([hand[0]] + [hand[1]] + [hand[3]] + [hand[4]] + [hand[6]]) #8
	permutsl.append([hand[0]] + [hand[1]] + [hand[3]] + [hand[5]] + [hand[6]]) #9
	permutsl.append([hand[0]] + [hand[1]] + [hand[4]] + [hand[5]] + [hand[6]]) #10
	permutsl.append([hand[0]] + [hand[2]] + [hand[3]] + [hand[4]] + [hand[5]]) #11
	permutsl.append([hand[0]] + [hand[2]] + [hand[3]] + [hand[4]] + [hand[6]]) #12
	permutsl.append([hand[0]] + [hand[2]] + [hand[3]] + [hand[5]] + [hand[6]]) #13
	permutsl.append([hand[0]] + [hand[2]] + [hand[4]] + [hand[5]] + [hand[6]]) #14
	permutsl.append([hand[0]] + [hand[3]] + [hand[4]] + [hand[5]] + [hand[6]]) #15
	permutsl.append([hand[1]] + [hand[2]] + [hand[3]] + [hand[4]] + [hand[5]]) #16
	permutsl.append([hand[1]] + [hand[2]] + [hand[3]] + [hand[4]] + [hand[6]]) #17
	permutsl.append([hand[1]] + [hand[2]] + [hand[3]] + [hand[5]] + [hand[6]]) #18
	permutsl.append([hand[1]] + [hand[2]] + [hand[4]] + [hand[5]] + [hand[6]]) #19
	permutsl.append([hand[1]] + [hand[3]] + [hand[4]] + [hand[5]] + [hand[6]]) #20
	permutsl.append([hand[2]] + [hand[3]] + [hand[4]] + [hand[5]] + [hand[6]]) #21

	return permutsl

#Takes list of 6-element 'hand-strength' lists
#and returns the index of the strongest hand.
#Should only be used in combination with other functions
def adjudicate(hands):

	index = 0
	multiplier = 100	
	search = True
	
	while search:

		#Start with empty array; clear the array for subsequent loops
		array = []
		
		#Populate array with the 1st value of each 'hand-strength' list. 
		#The first value will be the int designating the hand hierarchy
		#The multiplier is used to magnify the hierarchy code so that
		#it outweighs any subsequent values when we take running sum.
		for i in hands:
			array.append(i[index])
			i[index] = i[index]*multiplier
		
		#Set the multiplier to 1 so that the subsequent elements in the list 
		#are not magnified. (Only want to magnify the hierarchy code.)
		multiplier = 1

		#Test whether there is a unique max.  If so, stop and declare index 
		#of strongest hand
		array_max = max(array)
		if array.count(array_max) == 1:
			position = array.index(array_max)
			search = False

		#Test whether we have exhausted the list, in which case multiple hands
		#are tied.  If so, stop and declare the index of the 1st tied best hand
		elif index + 1 == len(hands[0]):
			position = array.index(array_max)
			search = False
		#Note: This is valid for adjudicating among permutations for a given player,
		#but NOT for determining a winning hand across players (in that case, should be a tie)
		#Need to build in this functionality!

		#If both tests fail, increment the index to compare the next element 
		#(card). Instead of comparing the next element per se, we will compare 
		#the cumulative running sum of elements evaluated so far. The purpose 
		#of this is to take into account the hierarchy & preceding cards, 
		#rather than comparing each card on its own
		else:
			index += 1
			for i in hands:
				i[index] += i[index-1]

	return position

#Takes list of 7 cards (hole cards + community cards)
#and returns the hand that should be played (best hand)
def hand_to_play(seven_cards):
	
	#Generate list of all 21 possible 5-card hands
	permuts_list = permuts(seven_cards)

	#Convert each 5-card hand into 'hand-strength' code
	hand_strength_list = []
	for hand in permuts_list:
		hand_strength_list.append(hand_strength(hand))

	#Generate index of the hand to play
	index = adjudicate(hand_strength_list)

	#Return best hand
	return permuts_list[index]

#Takes multiple 5-card hands and returns the best hand.
#Note that the argument is a list of lists of 2-tuples
def declare_winner(all_hands):
	
	#Convert each hand to 'hand-strength' code
	hand_strength_list = []
	for hand in all_hands:
		hand_strength_list.append(hand_strength(hand))

	#Generate index of the hand to play
	index = adjudicate(hand_strength_list)

	#Return best hand
	return all_hands[index]

	#Need to write this so that it permits ties...

def declare_winner_dict(all_hands):

	#Convert each hand to 'hand-strength' code and pull out players into list
	hand_strength_list = []
	players_list = []
	for hand in all_hands:
		players_list.append(hand)
		hand_strength_list.append(hand_strength(all_hands[hand]))

	#Generate index of the best hand
	index = adjudicate(hand_strength_list)

	#Return winning player
	return players_list[index]
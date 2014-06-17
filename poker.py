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

class Card(object):
	lookup = {
	11 : 'Jack',
	12 : 'Queen',
	13 : 'King',
	14 : 'Ace',
	'S' : 'Spades',
	'D' : 'Diamonds',
	'H' : 'Hearts',
	'C' : 'Clubs'
	}

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.card = (rank, suit)
	def __str__(self):
		return ('|' + str(self.lookup.get(self.rank, self.rank)) + 
				' of ' + self.lookup.get(self.suit, self.suit) + '|')

class Deck(object): 
	def __init__(self):
		#Generate deck of 52 cards
		ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
		suits = ['S', 'H', 'C', 'D']
		self.deck = []
		for r in ranks:
				for s in suits:
					self.deck.append(Card(r, s))

		#Shuffle deck
		np.random.shuffle(self.deck)

class Player(object):
	def __init__(self, name, bankroll=1000):
		self.name = name
		self.bankroll = bankroll

	def join(self, table):
		table.add_players(self)

	def leave(self, table):
		table.remove_players(self)

	def bet(self, game, amount):
		if amount <= self.bankroll:
			game.round += amount
			self.bankroll -= amount
		else: 'Not enough money.'

	def action(self, game):
		#If there's a blind or previous bet, options are: call, raise, fold.

		#If there's no blind or previous bet, options are: check, bet.

	#Want to build in functionality that enforces 1-to-many
	#relationship between table and player.

class Table(object):
	def __init__(self, small_blind=1, big_blind=2, n_seats=10):
		self.small_blind = small_blind
		self.big_blind = big_blind
		
		self.n_seats = n_seats
		
		#Build empty dict representing emtpy table
		#Keys = seats (1-n), Value = players (unoccupied = Nonetype)
		self.seats = {}
		for seat in range(1, n_seats + 1):
			self.seats[seat] = None

		self.seats_occupied = []
		self.seats_open = [x for x in self.seats]
		self.next_open = min(self.seats_open)

		self.n_seats_occupied = 0

		#List of players
		self.players = [self.seats[x] for x in self.seats if self.seats[x] != None]

		self.dealer_seat = 0

	def add_players(self, *players):
			for player in players:

				#If the table is not fully occupied...
				if self.n_seats_occupied < self.n_seats:

					#Seat the player at the next open seat
					self.seats[self.next_open] = player

					#Reset list of occupied seats
					self.seats_occupied = [x for x in self.seats if self.seats[x] != None]

					#Reset list of open seats
					self.seats_open = [x for x in self.seats if self.seats[x] == None]

					#Determine next open seat, for next new player
					self.next_open = min(self.seats_open)
					
					#Increment seats_occupied
					self.n_seats_occupied += 1

				else:
					print 'Sorry, there is no more room at the table.'

	def remove_players(self, *names):
		for name in names:
			for seat in self.seats:
				if self.seats[seat] == name:
					
					#Remove player by setting his/her seat to None
					self.seats[seat] = None

					#Reset list of occupied seats
					self.seats_occupied = [x for x in self.seats if self.seats[x] != None]

					#Reset list of open seats
					self.seats_open = [x for x in self.seats if self.seats[x] == None]

					#Determine next open seat, for next new player
					self.next_open = min(self.seats_open)
					
					#Decrement seats_occupied
					self.n_seats_occupied +- 1
	

class Game(object):

	name = 'No Limit Texas Hold Em'

	def __init__(self, table):

		#A game will be specific to a table.  Must pass table argument to begin

		#Create list of players in the game
		self.players = [table.seats[x] for x in table.seats if table.seats[x] != None]

		#Assign dealer based on next occupied seat
		
		self.dealer_assigned = False
		self.i = 1
		
		#Loop until dealer is assigned
		while self.dealer_assigned == False:
			
			#If when you increment by one there is another seat at the table...
			if table.dealer_seat + self.i < table.n_seats:
				
				#then if there is a player in that seat
				if table.seats[table.dealer_seat + self.i] != None:
					
					#Make that the dealer seat
					table.dealer_seat += self.i

					#And declare the dealer the player sitting in that seat
					self.dealer = table.seats[table.dealer_seat]

					self.dealer_assigned = True

				#if there is not a player in that seat, check the next seat
				else:
					self.i += 1

			#If when you increment by one there is NOT another seat at the table...
			else:

				#Start back at the first seat
				table.dealer_seat = 1

				#if there is a player in that seat
				if table.seats[table.dealer_seat] != None:
					
					#Declare the dealer the player sitting in that seat
					self.dealer = table.seats[table.dealer_seat]

					self.dealer_assigned = True

				else:

					#Reset the incrementer, now that you're at the beginning again
					self.i = 1

		#Establish indexes for dealer, small blind, big blind, first action
		#These indexes pertain to the players list
		
		#Dealer index
		self.d = self.players.index(self.dealer)

		#Small blind index
		if self.d + 1 < len(self.players):
			self.s = self.d + 1
		else:
			self.s = 0

		#Big blind index
		if self.s + 1 < len(self.players):
			self.b = self.s + 1
		else:
			self.b = 0

		#Action index
		if self.b + 1 < len(self.players):
			self.a = self.b + 1
		else:
			self.a = 0

		#Action sequence
		self.action_sequence = []

		#First element is action index
		self.action_sequence.append(self.a)

		#Build out subsequent elements of action sequence list
		while len(self.action_sequence) < len(self.players):
			if self.a + 1 < len(self.players):
				self.a += 1
				self.action_sequence.append(self.a)
			else:
				self.a = 0
				self.action_sequence.append(self.a)

		#$$$
		self.round = 0
		self.pot = 0

		#Small blind places blind
		self.players[self.s].bet(self, table.small_blind)

		#Big blind places blind
		self.players[self.b].bet(self, table.big_blind)

		#Update pot
		self.pot = self.round

		#Each game begins with a new, shuffled deck
		self.deck = Deck().deck

		#Cards will be dealt according to deck_index;
		#Each card dealt will increment deck_index by 1
		self.deck_index = 0

		#Game will represent players' cards as dict:
		#key = player, value = hole cards
		self.hole_cards = {}

		self.flop = []
		self.turn = []
		self.river = []
		
		#Community will be the concatenation of flop + turn + river 
		self.community = []

		#All cards accessible by each player
		self.hands = {}

		#Best 5-card hand for each player
		self.best_hands = {}

		print 'New game! \n'

	def betting(self):
		
		for i in self.action_sequence:
			print 'Action to: '
			print self.players[self.i]
			
			#Send action to player
			self.players[i].action(self)

	def deal(self):	
		#1st time function is called:  Deal pocket cards
		if self.hole_cards == {}:
			print 'Dealing pocket cards... \n'
			
			#Deal first card by creating keys (players) in hole_cards dict	
			for player in self.players:
				self.hole_cards[player] = [self.deck[self.deck_index]]
				self.deck_index += 1

			#Deal second card by appending to keys (players)
			for player in self.hole_cards:
				self.hole_cards[player].append(self.deck[self.deck_index])
				self.deck_index += 1

			#Create 'hands' dict representing all cards available to each player
			#(Can just copy hole_cards since hand is empty)
			self.hands = copy.deepcopy(self.hole_cards)

			#Initiate round of betting
			self.betting()
			return
		
		#2nd time function is called:  Deal flop
		elif self.flop == []:
			print 'Dealing flop...'
			while len(self.flop) < 3:
				self.flop.append(self.deck[self.deck_index])
				self.deck_index += 1

			#Add flop to community
			self.community += self.flop

			#Print flop
			for card in self.flop:
				print card,
			print '\n'

			#Add flop to players' hands
			for hand in self.hands:
				self.hands[hand] += self.flop
			return

		#3rd time function is called:  Deal turn
		elif self.turn == []:
			print 'Dealing turn...'
			self.turn.append(self.deck[self.deck_index])
			self.deck_index += 1

			#Add turn to community
			self.community += self.turn

			#Print turn
			for card in self.community:
				print card,
			print '\n'

			#Add turn to players' hands
			for hand in self.hands:
				self.hands[hand] += self.turn
			return

		#4th time function is called:  Deal river
		elif self.river == []:
			self.now_dealing = 'river'
			print 'Dealing river...'
			self.river.append(self.deck[self.deck_index])
			self.deck_index += 1

			#Add river to community
			self.community += self.river

			#Print river
			for card in self.community:
				print card,
			print '\n'

			#Add river to players' hands
			for hand in self.hands:
				self.hands[hand] += self.river

			#Now that a full board exists, calculate best hand for each player
			for x in self.hands:
				self.best_hands[x] = hand_to_play(self.hands[x])
			return

		#After all cards have been dealt...
		else:
			print 'All cards have been dealt.'

	def fold(self, player):
		#remove player from self.players, self.hands, self.best_hands

	def reveal_hole(self, player):
		for i in self.hole_cards[player]:
			print i,
		return

	def reveal_all(self): #Need to refactor this so it works w new setup
		for i in self.hole_cards:
			print i.name + ': ',
			for j in self.hole_cards[i]:
				print j,
			print '\n'

	def reveal_full_hands(self):
		for i in self.hands:
			print i.name + ': ',
			for j in self.hands[i]:
				print j,
			print '\n'

	def show_hands(self):
		for i in self.best_hands:
			print i.name + ': '
			for j in self.best_hands[i]:
				print j
			print '\n'

	def declare_winner(self):
		player_list = []
		hand_list = []
		for i in self.best_hands:
			player_list.append(i.name)
			hand_list.append(self.best_hands[i])
		winning_hand = declare_winner(hand_list)
		winning_player = player_list[hand_list.index(winning_hand)]
		print winning_player
		for card in winning_hand:
			print card,
		#winning_player = player_list[winning_hand_index]
		#winning_hand = hand_list[winning_hand_index]
		#print winning_player, winning_hand

	def probs(self, n=1000):

		#This function currently creates new player instances for each Monte Carlo
		#iteration.  Should test whether this slows the function down / see if there's
		#a better way to do the MC simulation.

		#Determine how many cards need to be dealt
		deal_count = len(self.hands[self.hands.keys()[len(self.hands)-1]])

		#Freeze current deck and create copy
		deck = self.deck[self.deck_index:52]

		#Begin iterative loop (ie Monte Carlo simulation)...
		winner_list = []

		i = 0

		while i < n:

			#Reset current hands
			current_hands = copy.deepcopy(self.hands)

			#Reset and shuffle deck...
			deck = self.deck[self.deck_index:52]
			np.random.shuffle(deck)

			deck_index = 0

			#Reset cards to deal
			cards_to_deal = 7 - deal_count

			#Deal cards
			while cards_to_deal > 0:
				for hand in current_hands:
					current_hands[hand].append((deck[deck_index]))
					deck_index += 1
				cards_to_deal -= 1

			#Calculate best hand for each player
			best_hands_iter = {}
			for x in current_hands:
					best_hands_iter[x] = hand_to_play(current_hands[x])

			#Declare winner for iteration
			winner = declare_winner_dict(best_hands_iter)

			#Append winner to winner list
			winner_list.append(winner.name)

			#Next iter...
			i += 1
		
		#Create list of unique player names
		unique_players = []
		for player in self.players:
			unique_players.append(player.name)

		#Create dict of probabilities
		prob_dict = {}
		for player in unique_players:
			prob_dict[player] = float(winner_list.count(player)) / n

		print prob_dict


















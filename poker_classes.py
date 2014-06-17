'''NO OPTION FOR ACTION WHEN EVERYONE CALLS.'''

import numpy as np
import copy
import random
import math
import itertools
import poker_functions as pf

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
		self.decision = None
		self.already_bet = 0

	def __str__(self):
		return self.name

	def join(self, table):
		table.add_players(self)

	def leave(self, table):
		table.remove_players(self)

	def action(self, game):
		#Place small blind, if appropriate
		if game.pot == 0:
			self.bet(game, game.small_blind)
			print self,
			print 'has placed the small blind.'
			return

		#Place big blind, if appropriate
		if game.pot == game.small_blind:
			self.bet(game, game.big_blind)
			print self,
			print 'has placed the big blind.'
			return

		#Amount owed is the full bet size minus what has already been bet
		self.amount_owed = game.total_to_play - self.already_bet

		if self.amount_owed > 0:
			game.bet_required = True
		else:
			game.bet_required = False

		if self.decision == 'f':
			pass
		
		else:
			print '\nAction to: {0}.'.format(self.name),
			
			#If there's a blind or previous bet, options are: call, raise, fold.
			if game.bet_required == True:
				print '${0} to call.'.format(self.amount_owed)
				self.decision = raw_input('Enter c to call.  Enter r to raise.  Enter f to fold.\n')
				#Need to create validation for these commands

			#If there's no blind or previous bet, options are: check, bet.
			else:
				self.decision = raw_input('Enter b to bet.  Enter h to check.\n') 

			#Excecute action based on decision
			if self.decision == 'c':
				self.call(game)
		
			elif self.decision == 'b':
				self.bet(game, int(raw_input('Enter amount: ')))
		
			elif self.decision == 'r':
				self.rais(game, int(raw_input('Enter amount: ')))

			elif self.decision == 'h':
				self.check(game)

			elif self.decision == 'f':
				self.fold(game)
			else:
				print 'Error.'
				self.action(game)

	#Action functions
	def call(self, game):
		#Call must be smaller than bankroll
		if self.amount_owed <= self.bankroll:
			game.round += self.amount_owed
			game.pot += self.amount_owed
			self.bankroll -= self.amount_owed
			self.already_bet += self.amount_owed

			print self,
			print 'has called ${0}.'.format(self.amount_owed)
			print 'Pot is ${0}.'.format(game.pot)

		else:
			print 'Not enough money.'
			#Add in functionality for side pots later

	def bet(self, game, amount):
		#Bet must be smaller than bankroll
		if amount <= self.bankroll:

			#Bet must be greater or equal to minimum bet
			if amount >= game.min_bet:
		
				#Place bet
				game.round += amount #game.round may be an obsolete variable...
				game.pot += amount
				self.bankroll -= amount
				self.already_bet += amount
				if amount > game.min_bet:
					game.min_bet = amount

				#After the blinds have been placed, print betting activity
				if game.pot > game.small_blind + game.big_blind:
					print self,
					print 'has bet ${0}.'.format(amount)
					print 'Pot is ${0}.'.format(game.pot)

				#Reset iters_left to length of action list
				game.iters_left = len(game.action_list)

			else:
				print 'Bet must be at least: ' + str(game.total_to_play)
				self.action(game)
		else:
			print 'Not enough money'
			#Add in functionality for side pots later

	def rais(self, game, amount):
		#Bet must be smaller than bankroll
		if amount + self.amount_owed <= self.bankroll:

			#Raise must be greater or equal to bet size
			if amount >= game.min_bet:
		
				#Place bet
				game.round += (self.amount_owed + amount)
				game.pot += (self.amount_owed + amount)
				self.bankroll -= (self.amount_owed + amount)
				self.already_bet += (self.amount_owed + amount)
				if amount > game.min_bet:
					game.min_bet = amount

				print '\n'
				print self,
				print 'has raised ${0} over ${1}.'.format(amount, self.amount_owed)
				print 'Pot is ${0}.'.format(game.pot)

				#Reset iters_left to length of action list
				game.iters_left = len(game.action_list)

			else:
				print 'Bet must be at least: ' + str(game.min_bet)
				self.action(game)
		else:
			print 'Not enough money'
			#Add in functionality for side pots later

	def fold(self, game):
		#Remove player from game.players list
		game.players.remove(self)

		#Remove player from hole_cards dict
		game.hole_cards.pop(self, None)

		#Remove player from hands dict
		game.hands.pop(self, None)

	def check(self, game):
		pass		

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

		self.dealer = None

	def assign_dealer(self):
		#If there is no dealer assigned (ie, table has just begun)
		if self.dealer == None:

			#Assign dealer based on first occupied seat
			self.dealer = self.seats[self.seats_occupied[0]]

		else:

			#Otherwise, shift dealer button to the next occupied seat
			if self.players.index(self.dealer) + 1 < len(self.players):
				self.dealer = self.players[self.players.index(self.dealer) + 1]
			else:
				self.dealer = self.players[0]

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

					#Reset list of players
					self.players = [self.seats[x] for x in self.seats if self.seats[x] != None]

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

					#Reset list of players
					self.players = [self.seats[x] for x in self.seats if self.seats[x] != None]

					#Determine next open seat, for next new player
					self.next_open = min(self.seats_open)
					
					#Decrement seats_occupied
					self.n_seats_occupied +- 1
	
class Game(object):

	name = 'No Limit Texas Hold Em'

	def __init__(self, table):
		print 'New game! \n'

		#A game will be specific to a table.  Must pass table argument to begin

		#Create list of players in the game
		self.players = [table.seats[x] for x in table.seats if table.seats[x] != None]

		#Declare small blind and big blind as class attributes
		#Purpose is to access in class functions without passing the table
		self.small_blind = table.small_blind
		self.big_blind = table.big_blind

		#Assign dealer
		table.assign_dealer()
		self.dealer = table.dealer

		#Establish indexes for dealer, small blind, big blind, first action
		#These indexes point to the players list
		
		#Dealer index
		self.d = self.players.index(self.dealer)

		#Anounce the dealer
		print self.players[self.d], 
		print 'is the dealer.'

		#Small blind index
		if self.d + 1 < len(self.players):
			self.s = self.d + 1
		else:
			self.s = 0

		#Create list of players in order of action
		self.action_list = []
		self.action_list.append(self.players[self.s])

		while len(self.action_list) < len(self.players):
			if self.s + 1 < len(self.players):
				self.s += 1
				self.action_list.append(self.players[self.s])
			else:
				self.s = 0
				self.action_list.append(self.players[self.s])

		'Set conditions for betting'

		#Boolean specifying whether player must bet to remain in game
		#In the first round of betting, this will be True, since players
		#have to bet the big blind
		#self.bet_required = True

		#Minimum bet size starts at 0 and then becomes big blind after bb is placed
		#(The reason it starts at 0 is bet function requires bet to be > than bet size
		#and small blind would fail that condition if bet size were set to big blind)
		self.min_bet = 0

		self.total_to_play = self.big_blind

		self.round = 0
		self.pot = 0

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

		#Best 5-card hand for each player
		self.best_hands = {}

	def betting(self):
		#Cycle through action list
		self.iters_left = len(self.action_list)

		for player in itertools.cycle(self.action_list):
			if self.iters_left == 0:
				break
			else:
				#Send action to player
				player.action(self)

				#Update total_to_play to be max that has been committed by any given player
				if player.already_bet > self.total_to_play:
					self.total_to_play = player.already_bet

				#Decrement iters left
				self.iters_left -= 1

		#Remove folded players from action list
		for player in self.action_list:
			if player not in self.players:
				self.action_list.remove(player)

		#If we are left with only one player, meaning everyone 
		#else folded, declare that player the winner, and run the end of game function
		if len(self.players) == 1:
			self.winner = self.players[0]
			self.end_game()

		#No bet required to start next round of betting
		self.bet_required = False

		#Reset minimum bet
		self.min_bet = self.big_blind

		#Reset total_to_play
		self.total_to_play = 0

		#Reset already_bet for each player
		for player in self.players:
			player.already_bet = 0

	def end_game(self):
		#This function will only be run under two conditions:
		#1) All players fold, leaving a winner;
		#2) All cards are dealt and winner is declared

		#Declare winner
		print '\nThe winner is: ',
		print self.winner

		#Award the pot to the winner
		self.winner.bankroll += self.pot
		print '{0} has won ${1}.'.format(self.winner, self.pot)

		#Option to initiate new game
		self.play_again = raw_input('Play again? (Y/N)')

		if self.play_again == 'Y':
			self.new_game()

		'''INSTRUCTIONS FOR INITIATING NEW GAME'''

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
			self.hands = self.hole_cards.copy()

			#For now, we'll show everyone's hands
			self.reveal_all()

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

			#Initiate round of betting
			self.betting()

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

			#Initiate round of betting
			self.betting()

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
				self.best_hands[x] = pf.hand_to_play(self.hands[x])

			#Initiate final round of betting
			self.betting()

			#Declare a winner
			self.winner = self.declare_winner()

			#End game
			self.end_game()

			return

		#After all cards have been dealt...
		else:
			print 'All cards have been dealt.'

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
				print j
			print '\n'

	def show_hands(self):
		for i in self.best_hands:
			print i.name + ': '
			for j in self.best_hands[i]:
				print j

	def declare_winner(self):
		player_list = []
		hand_list = []
		for i in self.best_hands:
			player_list.append(i)
			hand_list.append(self.best_hands[i])
		winning_hand = pf.declare_winner(hand_list)
		winning_player = player_list[hand_list.index(winning_hand)]
		return winning_player

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
					best_hands_iter[x] = pf.hand_to_play(current_hands[x])

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
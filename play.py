'''Play out a simple game...'''

from poker_classes import *

#Create players
ben = Player('Ben')
jeremiah = Player('Jeremiah')
fish = Player('Fish')
chris_moneymaker = Player('Chris Moneymaker')

#Start new table
mytable = Table()
mytable.add_players(ben, jeremiah, fish, chris_moneymaker)

#Start new game
newgame = Game(mytable)

#Deal pocket cards
newgame.deal()

#Deal flop
newgame.deal()

#Deal turn
newgame.deal()

#Deal river
newgame.deal()

#Show hands
newgame.show_hands()

#Declare winnernew
print 'The winner is...'
newgame.declare_winner()

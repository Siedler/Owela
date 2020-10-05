from players.first_bot import *
from players.distribute_bot import *
from players.greedy_bot import *
from players.random_bot import *
from players.high_bot import *
from players.max_in_one_field_bot import *
from players.real_player import *
from game import *

game = Game()
player1 = RealPlayer()
player2 = GreedyBot()
print(game.play(player1.select_move, player2.select_move))

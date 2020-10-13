from players.player import *

class MiniMaxNode():
    def __init__(self, game, player, max_depth, depth):
        self.game = game
        self.player = player
        self.max_depth = max_depth
        self.depth = depth
        self.depth_remaining = max_depth-depth
        self.possible_moves = []
        self.value = None
        self.move = None

        self.calc_value()

    def calc_value(self):

        # If the game is finished means that the previous player played
        # a move that resulted in an end configuration.
        # Is the depth even means that the opponent did the last move
        # is the depth uneven means that the MiniMaxBot made the last
        # move
        if self.game.game_finished():
            factor = 1 if self.depth % 2 != 0 else -1
            self.value = 1000*factor
            return

        if self.depth_remaining > 0:
            moves_to_play = self.game.possible_moves(self.player)

            for move in moves_to_play:
                new_game = self.game.copy()

                new_game.move(self.player, move)

                self.possible_moves.append(MiniMaxNode(new_game, 1-self.player, self.max_depth, self.depth+1))

                if  ((self.value == None) or
                    ((self.depth % 2 == 0) and self.possible_moves[-1].value > self.value) or # if current player is MiniMaxBot look for high
                    ((self.depth % 2 != 0) and self.possible_moves[-1].value < self.value)):   # else look for low
                    self.value = self.possible_moves[-1].value
                    self.move = move
        else:
            me = self.player if self.depth % 2 == 0 else 1-self.player
            opponent = 1-me
            self.value = self.game.stone_count(me) - self.game.stone_count(opponent)


class MiniMaxBot(Player):

    def __init__(self, depth=5):
        self.depth = depth

    def select_move(self, game, player) -> int:
        pos = self.has_direct_winning_move(game, player)
        if pos != None:
            return pos

        mini_max = MiniMaxNode(game, player, self.depth, 0)
        return mini_max.move

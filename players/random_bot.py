from players.player import *
import random

class RandomBot(Player):
    def select_move(self, game, player) -> int:
        """
        Playes random moves.

        This bot is usable as a messurment on how good a bot performs.
        """
        pos = self.has_direct_winning_move(game, player)
        if pos is not None:
            return pos

        return random.choice(game.possible_moves(player))

from players.player import *

class DistributeBot(Player):
    def select_move(self, game, player) -> int:
        """
        This bot tries to distribute it's stones onto as many fields as possible
        """

        return self.find_highest_value_move(game, player, lambda game: game.used_fields_count(player))

from players.player import *

class MaxInOneFieldBot(Player):
    def select_move(self, game, player) -> int:
        """
        Tries to coolect as many stones in one field as possible.
        """

        return self.find_highest_value_move(game, player, lambda game: game.max_field_count(player))

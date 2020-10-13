from players.player import *

class GreedyBot(Player):
    def select_move(self, game, player) -> int:
        """
        Picks the move that results in the highest number of stones.
        """
        return self.find_highest_value_move(game, player, lambda game: game.stone_count(player))

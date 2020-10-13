from players.player import *

class HighBot(Player):
    def select_move(self, game, player) -> int:
        """
        Playes the field with the highest number of stones.
        """
        pos = self.has_direct_winning_move(game, player)
        if pos is not None:
            return pos

        return max(((game.state[player][pos], pos) for pos in game.possible_moves(player)))[1]

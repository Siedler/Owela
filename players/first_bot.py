from players.player import *

class FirstBot(Player):
    def select_move(self, game, player) -> int:
        """
        If the bot has winning move: play it. Else play the first possible move
        """
        pos = self.has_direct_winning_move(game, player)
        if pos is not None:
            return pos

        own_state = game.state[player]
        return game.possible_moves(player)[0]

class Player():
    def has_direct_winning_move(self, game, player):
        """
        Calculates if a player has a move that would be a direct winning move.

        For this all possible moves are played and checked
        (Very inefficent if you are also playing every possible move for the
        selection of the moves)
        """
        own_state = game.state[player]
        for pos in game.possible_moves(player):
            game_copy = game.copy()
            game_copy.move(player, pos)
            if game_copy.player_has_won(player):
                return pos
        return None

    def find_highest_value_move(self, game, player, compute_value):
        """
        This function is used to abstract the selection of a highest value move.
        Given is the game (state), the current player and a function to determine
        the best possible move (according to it's definition).
        """
        best_move = -1
        highest_value = None

        for pos in game.possible_moves(player):
            game_copy = game.copy()
            game_copy.move(player, pos)

            # A move that results in a win is directly chosen as the highest value move
            if game_copy.player_has_won(player):
                return pos

            value = compute_value(game_copy)
            if highest_value is None or value > highest_value:
                highest_value = value
                best_move = pos

        return best_move

    # Abstract method
    def select_move(self, game, player) -> int:
        pass

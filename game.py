from textwrap import dedent
import time
import random

max_field_count = -1

class Game:
    def __init__(self):
        self.state = [
            [2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 0, 0, 0, 0, 0]]

    def copy(self):
        copied_game = Game()
        copied_game.state[0] = self.state[0][:]
        copied_game.state[1] = self.state[1][:]
        return copied_game

    def play(self, player1, player2):
        """
        Simulates an owella game for two given players

        Given as inputs are two functions that determin the behaviour of the
        player/bot.
        These functions need to work out the correct move according the game
        state and selected player (both are given as inputs).
        """
        players = [player1, player2]
        current_player = 0

        # print(self)
        current_round = 1
        while not self.game_finished():
                player = players[current_player]
                start_position = player(self, current_player)
                self.move(current_player, start_position)
                current_player = 1 - current_player

                current_round += 1

        # Return which player has won the game
        if self.player_has_won(0):
            return 0
        else:
            return 1

    def game_finished(self):
        return self.player_has_won(0) or self.player_has_won(1)

    def move(self, player, position):
        """
        Calculates the resulting board according to the current game state,
        player and position to be played
        """

        # Catch the case that the player tries to make a move with an empty field
        if self.state[player][position] <= 0:
            raise Exception("invalid")

        other_player = 1 - player
        my_state = self.state[player]
        other_state = self.state[other_player]

        # While the player is still alowed to make moves
        while True:
            if self.player_has_won(player):
                break

            amount = my_state[position] # amount of stones in that field
            my_state[position] = 0      # set the number of stones to 0 in field

            # Add one stone to each following field
            for i in range(1, amount + 1):
                my_state[(position + i) % 16] += 1
            new_position = (position + amount) % 16

            # If the last field already got a stone
            if my_state[new_position] > 1:
                # If the filed was in the front row: steal stones of opponent
                if new_position >= 8:
                    steal_position_1 = new_position - 8
                    steal_position_2 = 15 - steal_position_1
                    stolen = other_state[steal_position_1] + other_state[steal_position_2]
                    other_state[steal_position_1] = 0
                    other_state[steal_position_2] = 0
                    my_state[new_position] += stolen

                # Continue move from new starting position
                position = new_position
            else:
                break

    def move_recursive(self, player, position):
        """
        Recursive implementation of the described move function.

        Not in use anymore because of recursion-depth-problems
        """
        if self.state[player][position] <= 0:
            raise Exception("invalid")

        other_player = 1 - player
        my_state = self.state[player]
        other_state = self.state[other_player]

        amount = my_state[position]
        my_state[position] = 0

        for i in range(1, amount + 1):
            my_state[(position + i) % 16] += 1
        new_position = (position + amount) % 16

        if my_state[new_position] > 1:
            if new_position >= 8:
                steal_position_1 = new_position - 8
                steal_position_2 = 15 - steal_position_1
                stolen = other_state[steal_position_1] + other_state[steal_position_2]
                other_state[steal_position_1] = 0
                other_state[steal_position_2] = 0
                my_state[new_position] += stolen

            self.move_recursive(player, new_position)

    def max_field_count(self, player):
        """
        Calculate the filed with maximum amount of stones.

        If I remember correctly this was a support function to approximate
        the possible maximum number of stones in one field.
        """
        global max_field_count

        n = max(self.state[player])

        if max_field_count < n:
            max_field_count = n
        return n

    def stone_count(self, player):
        return sum(self.state[player])

    def player_has_won(self, player):
        return self.stone_count(1 - player) <= 1

    def used_fields_count(self, player):
        return len([i for i in range(16) if self.state[player][i] > 0])

    def __repr__(self):
        """
        Represent the current state of the board.
        """
        return dedent(f"""\
            State: {list(reversed(self.state[0][:8]))}
                   {self.state[0][8:]}
                   -----------------------------------------
                   {list(reversed(self.state[1][8:]))}
                   {self.state[1][:8]}\
        """)

    def print_player_perspective(self, player):
        """
        Represent the current state of the board according to the given player
        """
        print(dedent(f"""\
            {list(reversed(self.state[1-player][:8]))}
            {self.state[1-player][8:]}
            -----------------------------------------
            {list(reversed(self.state[player][8:]))}
            {self.state[player][:8]}\
        """))

    def __hash__(self):
        return hash((tuple(self.state[0]), tuple(self.state[1])))

    def __eq__(self, other):
        return self.state == other.state

    def possible_moves(self, player):
        """
        Returns a list of all possible moves a player can make
        """
        return [i for i in range(16) if self.state[player][i] > 0]

def has_direct_winning_move(game, player):
    """
    Calculates if a player has a move that would be a direct winning move.
    """
    own_state = game.state[player]
    for pos in game.possible_moves(player):
        game_copy = game.copy()
        game_copy.move(player, pos)
        if game_copy.player_has_won(player):
            return pos
    return None

def first_bot(game, player) -> int:
    """
    If the bot has winning move: play it. Else play the first possible move
    """
    pos = has_direct_winning_move(game, player)
    if pos is not None:
        return pos

    own_state = game.state[player]
    return game.possible_moves(player)[0]

def find_highest_value_move(game, player, compute_value):
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

        value = compute_value(game_copy)
        if highest_value is None or value > highest_value:
            highest_value = value
            best_move = pos

    return best_move

def distribute_bot(game, player):
    """
    This bot tries to distribute it's stones onto as many fields as possible
    """
    pos = has_direct_winning_move(game, player)
    if pos is not None:
        return pos

    return find_highest_value_move(game, player, lambda game: game.used_fields_count(player))

def greedy_bot(game, player) -> int:
    """
    Picks the move that results in the highest number of stones.
    """
    return find_highest_value_move(game, player, lambda game: game.stone_count(player))

def rand_bot(game, player) -> int:
    """
    Playes random moves.

    This bot is usable as a messurment on how good a bot performs.
    """
    pos = has_direct_winning_move(game, player)
    if pos is not None:
        return pos

    own_state = game.state[player]
    hasStones = []
    for pos in game.possible_moves(player):
        hasStones.append(pos)
    return random.choice(hasStones)

def high_bot(game, player):
    """
    Playes the filed with the highest number of stones.
    """
    pos = has_direct_winning_move(game, player)
    if pos is not None:
        return pos

    return max(((game.state[player][pos], pos) for pos in game.possible_moves(player)))[1]

def max_in_one_field_bot(game, player):
    """
    Tries to coolect as many stones in one field as possible.
    """
    pos = has_direct_winning_move(game, player)
    if pos is not None:
        return pos

    return find_highest_value_move(game, player, lambda game: game.max_field_count(player))


def real_player(game, player):
    """
    Give the opportunity to play the game as a real player.
    """
    print()
    print(f"Player {player} turn")
    game.print_player_perspective(player)

    move = -1
    while(move==-1):
        entered_move = input ("Enter move: ")

        if(int(entered_move) in game.possible_moves(player)):
            move = int(entered_move)
        else:
            print("Entered an invalid move")

    print()
    return move

def trackGames(number_of_games, player1, player2):
    """
    Track how n games between two bots/player work
    """
    winner = [0,0]

    for i in range(number_of_games):
        game = Game()
        winner[game.play(player1, player2)] += 1

    print(winner)
random.seed(1)
trackGames(1000, rand_bot, greedy_bot)

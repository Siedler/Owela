from textwrap import dedent
import time
import random

class Game:
    def __init__(self):
        self.state = [
            [2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 0, 0, 0, 0]]

    def copy(self):
        copied_game = Game()
        copied_game.state[0] = self.state[0][:]
        copied_game.state[1] = self.state[1][:]
        return copied_game

    def bot_play(self, bot1, bot2):
        bots = [bot1, bot2]
        current_player = 0

        # print(self)
        current_round = 1
        while not self.game_finished():
                bot = bots[current_player]
                start_position = bot(self, current_player)
                self.move(current_player, start_position)
                current_player = 1 - current_player

                # print(f"Round {current_round}:")
                # print(self)
                current_round += 1

        if self.player_has_won(0):
            return 0
        else:
            return 1

    def game_finished(self):
        return self.player_has_won(0) or self.player_has_won(1)

    def move(self, player, position):
        if self.state[player][position] <= 0:
            raise Exception("invalid")
        # print(position)

        other_player = 1 - player
        my_state = self.state[player]
        other_state = self.state[other_player]

        while True:
            if self.player_has_won(player):
                break

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

                position = new_position
            else:
                break

    def move_recursive(self, player, position):
        if self.state[player][position] <= 0:
            raise Exception("invalid")
        # print(position)

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

    def stone_count(self, player):
        return sum(self.state[player])

    def player_has_won(self, player):
        return self.stone_count(1 - player) <= 1

    def used_fields_count(self, player):
        return len([i for i in range(16) if self.state[player][i] > 0])

    def __repr__(self):
        return dedent(f"""\
            State: {list(reversed(self.state[0][:8]))}
                   {self.state[0][8:]}
                   -----------------------------------------
                   {list(reversed(self.state[1][8:]))}
                   {self.state[1][:8]}\
        """)

    def __hash__(self):
        return hash((tuple(self.state[0]), tuple(self.state[1])))

    def __eq__(self, other):
        return self.state == other.state

    def possible_moves(self, player):
        return [i for i in range(16) if self.state[player][i] > 0]

def has_direct_winning_move(game, player):
    own_state = game.state[player]
    for pos in game.possible_moves(player):
        game_copy = game.copy()
        game_copy.move(player, pos)
        if game_copy.player_has_won(player):
            return pos
    return None

def first_bot(game, player) -> int:
    if (pos := has_direct_winning_move(game, player)) is not None:
        return pos

    own_state = game.state[player]
    for pos in game.possible_moves(player):
        return pos

def find_highest_value_move(game, player, compute_value):
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
    if (pos := has_direct_winning_move(game, player)) is not None:
        return pos

    return find_highest_value_move(game, player, lambda game: game.used_fields_count(player))

def greedy_bot(game, player) -> int:
    return find_highest_value_move(game, player, lambda game: game.stone_count(player))

def rand_bot(game, player) -> int:
    if (pos := has_direct_winning_move(game, player)) is not None:
        return pos

    own_state = game.state[player]
    hasStones = []
    for pos in game.possible_moves(player):
        hasStones.append(pos)
    return random.choice(hasStones)

def high_bot(game, player):
    if (pos := has_direct_winning_move(game, player)) is not None:
        return pos

    return max(((game.state[player][pos], pos) for pos in game.possible_moves(player)))[1]

def trackGames():
    winner = [0,0]

    for i in range(1000):
        game = Game()
        winner[game.bot_play(rand_bot, rand_bot)] += 1

    print(winner)
random.seed(2)
trackGames()

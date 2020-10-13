from players.player import *

import uuid

import os.path
from os import path

import json

class EvalBoardBot(Player):
    def __init__(self, eval_board):
        self.id = uuid.uuid4()
        self.eval_board = eval_board
        self.wins = 0

    def won_game(self):
        self.wins += 1

    def reset_wins(self):
        self.wins = 0

    def calc_eval_board_value(self, game, player):
        sum = 0
        for i in range(2):
            for j in range(16):
                sum += game.state[player][j] * self.eval_board[i][j]

        return sum

    def select_move(self, game, player):
        return self.find_highest_value_move(game, player, lambda game: self.calc_eval_board_value(game, player))

    def load(self, sub_dir, number):
        if not path.exists(f'generations/{sub_dir}/'):
            raise IOError()

        with open(f'generations/{sub_dir}/{number}.json', 'r', encoding='utf8') as file:
            json_data = json.load(file)

        self.id = uuid.UUID(json_data['id'])
        self.eval_board = json_data['eval_board']
        self.wins = 0

    def save(self, sub_dir, number):
        if(not path.exists(f'generations/{sub_dir}/')):
            os.makedirs(f'generations/{sub_dir}/')

        individual = {
            'id': self.id.hex,
            'eval_board': self.eval_board,
            'wins': self.wins,
        }

        with open(f'generations/{sub_dir}/{number}.json', "w+", encoding='utf8') as write_file:
            json.dump(individual, write_file)

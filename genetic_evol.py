from game import *

import os.path
from datetime import datetime
from os import path
import json
import uuid
import copy
import matplotlib.pyplot as plt

class Individual:
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

    def eval_board_bot(self, game, player):
        return find_highest_value_move(game, player, lambda game: self.calc_eval_board_value(game, player))

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
            os.mkdir(f'generations/{sub_dir}/')

        individual = {
            'id': self.id.hex,
            'eval_board': self.eval_board,
            'wins': self.wins,
        }

        with open(f'generations/{sub_dir}/{number}.json', "w+", encoding='utf8') as write_file:
            json.dump(individual, write_file)

generation_size = 100
survivour_rate = 0.30

num_of_games_per_player = 1

init_value_min = -1
init_value_max = 1

mutation_min = -0.1
mutation_max = 0.1

individuals = []

def save_generation(generation_num):
    i = 0
    for individual in individuals:
        individual.save(f'{generation_num}_gen', f'{i}')

        i += 1

def rand_eval_board():
    eval_board = []

    for i in range(2):
        board = []
        for i in range(16):
            board.append(random.uniform(init_value_min, init_value_max))
        eval_board.append(board)

    return eval_board

def init_first_gen():
    for _ in range(generation_size):
        eval_board = rand_eval_board()

        individuals.append(Individual(rand_eval_board()))

def mutate(eval_board):
    for i in range(2):
        for j in range(16):
            mutation_value = random.uniform(mutation_min, mutation_max)
            eval_board[i][j] += mutation_value

    return eval_board

def evolve():
    global individuals

    if len(individuals) == 0:
        init_first_gen()
    else:
        survivour_num = int(round(generation_size*survivour_rate))
        to_fill_up = generation_size-survivour_num

        individuals = individuals[:survivour_num]

        for individual in individuals:
            individual.reset_wins()

        for i in range(to_fill_up):
            rand_individual_index = random.randint(0, survivour_num-1)
            rand_individual_eval_board = copy.deepcopy(individuals[rand_individual_index].eval_board)

            individuals.append(Individual(mutate(rand_individual_eval_board)))

def evolution(num_of_gen):
    global individuals

    for generation in range(num_of_gen):
        print(f'Calculate generation {generation}')
        start = datetime.now()
        evolve()

        # turnement of all players
        for i in range(generation_size):
            for j in range(i+1, generation_size):
                trackedGames = trackGamesRandStart(num_of_games_per_player, individuals[i].eval_board_bot, individuals[j].eval_board_bot)

                if(trackedGames[0] > trackedGames[1]):
                    individuals[i].won_game()
                else:
                    individuals[j].won_game()

        # Sort individuals according to their win rate inside this generation
        individuals = sorted(individuals, key=lambda individual: individual.wins, reverse=True)

        save_generation(generation)

        end = datetime.now()
        difference = end - start
        print(f'Time passed: {difference.seconds} seconds')
        print()

#evolution(60)
bestG60 = Individual([])
bestG60.load('59_gen', '0')

print(trackGames(1, bestG60.eval_board_bot, greedy_bot))

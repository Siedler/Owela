from players.player import *

class RealPlayer(Player):
    def select_move(self, game, player) -> int:
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

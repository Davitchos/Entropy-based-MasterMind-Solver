from master_mind import MasterMind, TextVisualizer
import simulation
import numpy as np

class PvP_Engine:
    def __init__(self):
        pass

    def next_guess(self, turn, last_result, positions, colors):
        secret = input("Guess: enter 4 numbers separated by spaces: ")
        secret_arr = list(map(int, secret.split()))
        return np.array(secret_arr)


secret = input("Enter 4 numbers separated by spaces: ")
secret_arr = list(map(int, secret.split()))
game = MasterMind(np.array(secret_arr))
simulation.play_with_visualizer(game=game, guesser=PvP_Engine(), max_turns=6, visualizer=TextVisualizer(game.positions, game.colors))


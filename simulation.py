import numpy as np
from master_mind import MasterMind, TextVisualizer

class RandomGuesser:
    def next_guess(self, turn, last_result, positions, colors):
        return np.random.randint(0, colors, size=positions)

def play_with_visualizer(game: MasterMind, guesser, visualizer: TextVisualizer, max_turns=6):
    last_result = None
    for turn in range(1, max_turns + 1):
        guess = guesser.next_guess(turn, last_result, game.positions, game.colors)
        result = game.eval(guess)
        visualizer.show_turn(turn, guess, result)
        if result["black"] == game.positions:
            visualizer.finish(True, game.secret)
            return True, turn, guess
        last_result = result
    visualizer.finish(False, game.secret)
    return False, max_turns, guess

def play(game: MasterMind, guesser, max_turns=6):
    last_result = None
    for turn in range(1, max_turns + 1):
        guess = guesser.next_guess(turn, last_result, game.positions, game.colors)
        result = game.eval(guess)
        if result["black"] == game.positions:
            return True, turn, guess
        last_result = result
    return False, max_turns, guess

def all_codes(positions=4, colors=6, dtype=np.uint8):
    base = np.arange(colors, dtype=dtype)
    grids = np.meshgrid(*([base] * positions), indexing='ij')
    return np.stack(grids, axis=-1).reshape(-1, positions)

#np.random.seed(42)
#game = MasterMind(secret=np.random())
#solver = RandomGuesser()
#viz = TextVisualizer(positions=game.positions, colors=game.colors)
#res, _, _ = play_with_visualizer(game, solver, viz, max_turns=6)
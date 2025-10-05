import importlib
import simulation
from master_mind import MasterMind
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed

importlib.reload(simulation)

codes = simulation.all_codes(positions=4, colors=6)

def benchmark_solver(solver_class, n_jobs=-1):
    def _solve(secret):
        solver = solver_class()  # fresh solver for each secret
        game = MasterMind(secret=secret)
        _, turn, _ = simulation.play(game=game, guesser=solver, max_turns=1000)
        return turn

    turns = Parallel(n_jobs=n_jobs)(
        delayed(_solve)(secret) for secret in tqdm(codes, desc="Benchmarking", unit="game")
    )

    return {
        "# mean turns to guess secret": round(np.average(turns), 2),
        "# maximum turns to guess secret": int(np.max(turns)),
        "# losses (> 6 guesses)": int(np.sum(np.array(turns) > 6))
    }
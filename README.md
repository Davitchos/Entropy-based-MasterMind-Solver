# MasterMind — Entropy Solver

Short project showing how to beat the classic **Mastermind** game with ideas from **information theory**, **constraint pruning**, and a bit of **parallel benchmarking**.  
Implements random guessing, pruning based on feedback, and an **entropy-driven solver** that always wins in ≤6 moves.

---

## Mathematical & programming techniques

- **Combinatorics:** size of code space $c^p$, counting feedback pairs.  
- **Information theory:** Shannon entropy $H=-\sum p\log_2 p$ to rank guesses by expected information gain.  
- **Constraint propagation:** update candidate set from black/white peg feedback.  
- **Symmetry reduction:** color/position permutations to reduce search space.  
- **Vectorization:** NumPy meshgrid to enumerate all codes.  
- **Parallelization:** `n_jobs` for full-space benchmarks.  
- **Visualization:** matplotlib plots for feedback probability & information content.  

---

## Contents

- **Game setup:** formal definition of Mastermind, feedback function $F(\text{secret},\text{guess})$.  
- **Naive random solver:** baseline success probability $\approx 0.46\%$.  
- **Evaluation metrics:** mean, max, loss count across all $6^4=1296$ codes.  
- **Pruning solver:** eliminates inconsistent candidates after each guess.  
- **Information-theoretic solver:** picks guesses with maximal expected entropy; guarantees win ≤6 moves.  
- **Symmetry & optimization:** reduce equivalent starting guesses to 15 isomorph classes to speed up entropy search.  
- **Benchmarking:** exhaustive evaluation with optional parallel execution.  
- **Visualization:** distributions of feedback, information content bars, entropy ranking of guesses.

---

## Benchmark summary (6 colors, 4 positions, 6 tries)

| Solver                  | Mean turns | Max turns | Losses (>6) |
|-------------------------|------------|-----------|-------------|
| RandomGuesser           | ~696       | 1000      | 1289        |
| Pruning (simple)        | ~4.65      | 7         | 12          |
| Pruning + Entropy       | ~4.41      | **6**     | **0**       |

---

## Quick use

```python
import numpy as np
from master_mind import MasterMind, TextVisualizer
import simulation

class RandomGuesser:
    def next_guess(self, turn, last_result, positions, colors):
        return np.random.randint(0, colors, size=positions)

game = MasterMind(secret=np.array([0,0,0,0]))
viz  = TextVisualizer(positions=game.positions, colors=game.colors)
solver = RandomGuesser()
simulation.play_with_visualizer(game, solver, viz, max_turns=6)
```
---
## License & status
This notebook is still work in progress (open questions on theoretical lower bounds remain).

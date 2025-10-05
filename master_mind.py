import numpy as np
from collections import Counter

# ==========================================
# Matrix Layout
#
#              C O L O R S
#          ┌─────┬─────┬─────┬─────┐
# Position │ Red │Blue │ ... │  m  │
# ─────────┼─────┼─────┼─────┼─────┤
#    P1    │  0  │  1  │  0  │  0  │
#    P2    │     │ ... │     │     │
#    ...   │     │     │ ... │     │
#    n     │     │     │     │ ... │
#          └─────┴─────┴─────┴─────┘
#
# Rows = Positions (P1, P2, …)
# Cols = Colors (Red, Blue, Green, …)
# Each cell = some value (e.g., cost, assignment, flag, etc.)
# ==========================================

class MasterMind:
    def __init__(self, secret, positions = 4, colors = 6):
        self.positions = positions
        self.colors = colors
        if self.is_valid_secret(secret):
            self.secret = secret
        else:
            raise Exception("Invalid secret!")
                
    def is_valid_secret(self, secret):
        cond_pos = np.all(secret >= 0)

        # check all entries are integers
        cond_int = np.all(np.equal(np.mod(secret, 1), 0))   # works even if v is float dtype

        # check all entries are < x
        cond_lt = np.all(secret < self.colors)
        if len(secret) != self.positions or not cond_pos or not cond_int or not cond_lt:
            return False
        return True

    def play(self, guesser, max_turns=6):
        last_result = None
        for turn in range(1, max_turns+1):
            guess = guesser.next_guess(turn, last_result, self.positions, self.colors)
            result = self.eval(guess)
            if result["black"] == self.positions:
                return True, turn, guess
            last_result = result
        return False, max_turns, guess

    def play_manually(self):
        while True:
            guess = self.guess()
            eval = self.eval(guess)

    def guess(self):
        guess = np.zeros(self.positions, dtype=int)
        for index, val in enumerate(guess):
            color_guess = int(input(f"Color at position {index + 1}:")) 
            if color_guess < 0 or color_guess >= self.colors:
                raise Exception("Invalid color option")
            guess[index] = color_guess
        return guess        

    def eval(self, guess):
        blacks = np.sum(self.secret == guess)
        whites = 0
        for c in range(self.colors):
            whites += min(np.sum(self.secret == c), np.sum(guess == c))
        whites -= blacks
        return {"black": int(blacks), "white": int(whites)}

#game = MasterMind(np.array([1, 2, 1, 3]))
#game.play_manually()

class TextVisualizer:
    def __init__(self, positions, colors, force_ascii=False):
        self.positions = positions
        self.colors = colors
        self.force_ascii = force_ascii

        # Nice distinct emojis (extend if you want)
        self.emoji_palette = ["🔴","🟢","🔵","🟡","🟣","🟠","🟤","⚫","⚪","🟧","🟦","🟨","🟩","🟥","🟪"]

        # Precompute symbol map 0..colors-1
        self.syms = [self._symbol_for(i) for i in range(colors)]

        print("\n=== MasterMind ===")
        print(f"Positions: {positions}, Colors: {colors}")
        print("-" * (14 + 3*positions))

    # Excel-style letter codes: A..Z, AA..AZ, BA.. etc.
    def _letter_code(self, idx):
        # idx: 0 -> 'A', 25 -> 'Z', 26 -> 'AA', 27 -> 'AB', ...
        s = []
        n = idx + 1
        while n > 0:
            n, rem = divmod(n - 1, 26)
            s.append(chr(ord('A') + rem))
        return "".join(reversed(s))

    def _symbol_for(self, i):
        if not self.force_ascii and i < len(self.emoji_palette):
            return self.emoji_palette[i]
        # fall back to letters after emojis or if force_ascii=True
        letter_idx = i if self.force_ascii else (i - len(self.emoji_palette))
        return self._letter_code(letter_idx)

    def fmt_guess(self, guess):
        return " ".join(self.syms[int(x)] for x in guess)
    
    def fmt_feedback(self, res):
        return "○"*res["black"] + "●"*res["white"]

    def show_turn(self, turn, guess, res):
        print(f"Turn {turn:>2}: {self.fmt_guess(guess)}  | (Black: {res["black"]}, White: {res["white"]}) {self.fmt_feedback(res)}")

    def finish(self, win, secret):
        print("-" * (14 + 3*self.positions))
        print(f"Secret: {self.fmt_guess(secret)}  ->  {'WIN 🎉' if win else 'LOSS ❌'}\n")
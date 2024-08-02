#!/usr/bin/env python3

from racer.constants import framerate
from racer.game_state import GameState
import tqdm
game_state = GameState()

for i in tqdm.trange(0, 100):
    game_state.update(1 / framerate)
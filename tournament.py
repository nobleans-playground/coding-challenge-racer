#!/usr/bin/env python3
from argparse import ArgumentParser

import tqdm

from racer.constants import framerate
from racer.game_state import GameState
from racer.track import Track
from racer.tracks import track1


def main():
    game_state = single_game()

    for bot, car_info in game_state.bots.items():
        print(f'{bot.name} reached round {car_info.round} waypoint {car_info.next_waypoint} with {car_info.cpu:.2f} '
              f'seconds of CPU time ({car_info.cpu * 1000 / game_state.frames:.2f} ms CPU/f)')


def single_game():
    game_state = GameState(Track(track1))
    for _ in tqdm.trange(0, 500):
        game_state.update(1 / framerate)

        for bot, car_info in game_state.bots.items():
            if car_info.round >= 1:
                return game_state

    return game_state


if __name__ == '__main__':
    parser = ArgumentParser(description='Run a tournament of the coding challenge racer')
    args = parser.parse_args()

    try:
        main(**vars(args))
    except KeyboardInterrupt:
        pass

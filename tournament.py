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
    rounds = 3
    min_frames = 6000
    frames_after_finish = 50000

    game_state = GameState(Track(track1))
    finishing = False
    for _ in tqdm.trange(0, min_frames):
        game_state.update(1 / framerate)

        for bot, car_info in game_state.bots.items():
            if car_info.round >= rounds:
                finishing = True
                break
        if finishing:
            break

    for _ in tqdm.trange(0, frames_after_finish):
        game_state.update(1 / framerate)

    finish_index = rounds * len(game_state.track.lines) - 1
    for bot, car_info in game_state.bots.items():
        if finish_index < len(car_info.waypoint_timing):
            finish_time = car_info.waypoint_timing[finish_index]
            print(f'{bot.name} finished in {finish_time:.2f} seconds')
        else:
            print(f'{bot.name} did not finish')

    return game_state


if __name__ == '__main__':
    parser = ArgumentParser(description='Run a tournament of the coding challenge racer')
    args = parser.parse_args()

    try:
        main(**vars(args))
    except KeyboardInterrupt:
        pass

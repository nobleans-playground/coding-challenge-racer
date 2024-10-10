#!/usr/bin/env python3
import itertools
from argparse import ArgumentParser

import pygame
import tqdm

from racer.constants import framerate
from racer.game_state import GameState
from racer.track import Track
from racer.tracks import track1


def get_laps(car_info):
    return car_info.round + (car_info.next_waypoint / len(car_info.track.lines))


def main():
    pygame.init()
    game_state = single_game()

    results = [(b, c, get_laps(c)) for b, c in game_state.bots.items()]
    track_length = sum((v1 - v0).length() for v0, v1 in
                       itertools.pairwise(game_state.track.lines + [game_state.track.lines[0]]))

    print("Bot                  | Contributor      |   Laps | Speed (px/s) | CPU (s) | CPU/t (ms)")
    print("---------------------|------------------|--------|--------------|---------|-----------")
    format_str = "{:20} | {:16} | {:6.2f} | {:12.2f} | {:7.2f} | {:10.2f}"

    for bot, car_info, laps in sorted(results, key=lambda r: r[2], reverse=True):
        speed = (laps * track_length) / (game_state.frames / framerate)
        cpu_per_tick = car_info.cpu * 1000 / game_state.frames
        print(format_str.format(bot.name, bot.contributor, laps, speed, car_info.cpu, cpu_per_tick))


def single_game():
    rounds = 3
    min_frames = 6000
    frames_after_finish = 25_000

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

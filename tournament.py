#!/usr/bin/env python3
import csv
import os
from argparse import ArgumentParser
from datetime import datetime, UTC
from itertools import pairwise
from tempfile import gettempdir

import pandas
import pygame
import tqdm

from racer.constants import framerate
from racer.game_state import GameState
from racer.track import Track
from racer.tracks import all_tracks

rounds = 3


def get_laps(car_info):
    return car_info.round + (car_info.next_waypoint / len(car_info.track.lines))


def main(track):
    pygame.init()

    track = Track(next(t for t in all_tracks if t.name == track))

    # write to a temporary file so that we have partial scores in case of a crash
    filename = f'racer_{datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")}'
    with open(os.path.join(gettempdir(), filename), 'w+') as f:
        print(f'writing game results to {f.name}')
        writer = csv.DictWriter(f, fieldnames=['Name', 'Contributor', 'Finish time', 'Frames', 'CPU', 'Track'])

        rows = single_game(track)

        writer.writeheader()
        writer.writerows(rows)

        f.seek(0)
        df = pandas.read_csv(f)

        track = next(Track(t) for t in all_tracks if t.name == df['Track'][0])
        track_length = sum((v1 - v0).length() for v0, v1 in pairwise(track.lines + [track.lines[0]]))

        df['CPU/t'] = df['CPU'] / df['Frames'] * 1000
        df['Speed'] = track_length * rounds / df['Finish time']

        # Reorder columns
        df = df[['Name', 'Contributor', 'Finish time', 'Speed', 'CPU', 'CPU/t', 'Track']]

        df.sort_values(by='Finish time', inplace=True)
        print()
        print(df.to_string(formatters={'Finish time': '{:.3f}'.format, 'Speed': '{:.2f}'.format, 'CPU': '{:.1f}'.format,
                                       'CPU/t': '{:.1f}'.format}, index=False))


def single_game(track):
    min_frames = 6000
    frames_after_finish = 25_000

    game_state = GameState(track)
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
    rows = []
    for bot, car_info in game_state.bots.items():
        row = {
            'Name': bot.name,
            'Contributor': bot.contributor,
            'CPU': car_info.cpu,
            'Frames': game_state.frames,
            'Track': game_state.track.name,
        }

        if finish_index < len(car_info.waypoint_timing):
            finish_time = car_info.waypoint_timing[finish_index]
            row['Finish time'] = finish_time
        else:
            row['Finish time'] = None
        rows.append(row)
    return rows


if __name__ == '__main__':
    parser = ArgumentParser(description='Run a tournament of the coding challenge racer')
    parser.add_argument('track', choices=[t.name for t in all_tracks], help='The track to run the tournament on')
    args = parser.parse_args()

    try:
        main(**vars(args))
    except KeyboardInterrupt:
        pass

#!/usr/bin/env python3
import asyncio

import pygame

from racer.window import App


def main():
    pygame.init()
    app = App()
    print('Starting the main loop')
    asyncio.run(app.mainloop())
    print('Main loop finished')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()

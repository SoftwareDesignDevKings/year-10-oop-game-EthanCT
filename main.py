import os
import sys

# suppress libpng iCCP warnings before pygame loads anything
# these come from the PNG assets having a slightly malformed colour profile
# and are completely harmless - redirecting the file descriptor at the OS level
# catches warnings that originate inside C libraries, which Python's sys.stderr swap misses
devnull_fd   = os.open(os.devnull, os.O_WRONLY)
old_stderr   = os.dup(2)
os.dup2(devnull_fd, 2)

import pygame
import random
import math
from game import Game
from constants import *


# helper functions go here when needed


# TODO: Write Player Class


# TODO: Write Enemy Class


# TODO: Write Fireball Class


# TODO: Write Coin Class


# TODO: Write Game Class


def main():
    game = Game()
    game.run()

    # restore stderr so any real errors after the game closes are still visible
    os.dup2(old_stderr, 2)
    os.close(old_stderr)
    os.close(devnull_fd)

if __name__ == "__main__":
    main()
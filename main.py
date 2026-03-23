import os
import sys
import pygame
import random
import math
from game import Game
from constants import *




# suppress libpng iCCP warnings
devnull_fd   = os.open(os.devnull, os.O_WRONLY)
old_stderr   = os.dup(2)
os.dup2(devnull_fd, 2)

def main():
    game = Game()
    game.run()


    os.dup2(old_stderr, 2)
    os.close(old_stderr)
    os.close(devnull_fd)

if __name__ == "__main__":
    main()
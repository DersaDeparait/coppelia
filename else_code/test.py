import pygame
from pygame import time
import random
import math
import os


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 30)

    pygame.init()
    display = pygame.display.set_mode((1500, 1000))
    display.fill((0, 128, 255))
    run = True
    clock = time.Clock()



    while(run):
        display.fill((0, 180, 200))
        #pygame.draw.line(display, dot[i].color, dot[i].get_pos_start(), dot[i].get_pos_end(), 2)
        #pygame.draw.circle(display, (4, 5, 5), dot[i].goal, 8)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == '__main__':
   main()
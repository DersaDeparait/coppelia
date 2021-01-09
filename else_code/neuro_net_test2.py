import pygame
from pygame import time
import random
import math
import os

class Dot:
    def __init__(self, x = 0, y = 0, cXX = 0, cXY = 0, cYX = 0, cYY = 0, cXW = 0, cYW = 0):
        self.goal = [500, 500]
        if x == 0 and y == 0:
            self.pos = [random.randrange(0, 1000), random.randrange(0, 1000)]
            while(abs(self.pos[0] - self.goal[0]) < 200 and abs(self.pos[1] - self.goal[1]) < 200):
                self.pos = [random.randrange(0, 1000), random.randrange(0, 1000)]
        else: self.pos = [x, y]
        self.pos_last = [self.pos[0], self.pos[1]]

        self.cXX = cXX
        self.cXY = cXY
        self.cYX = cYX
        self.cYY = cYY
        self.cXW = cXW
        self.cYW = cYW

        self.move = [0, 0]

        self.result = 0
        self.random_coef = 0.02
    def find_move(self):
        self.move[0] = (self.pos[0] - self.goal[0]) * self.cXX + (self.pos[1] - self.goal[1]) * self.cXY + self.cXW
        self.move[1] = (self.pos[0] - self.goal[0]) * self.cYX + (self.pos[1] - self.goal[1]) * self.cYY + self.cYW
    def get_pos(self): return (int(self.pos[0]), int(self.pos[1]))
    def get_pos_last(self): return (int(self.pos_last[0]), int(self.pos_last[1]))
    def update(self):
        self.find_move()
        dx = (self.goal[0] - self.pos[0])
        dy = (self.goal[1] - self.pos[1])
        dxm = (self.goal[0] - self.pos[0] - self.move[0])
        dym = (self.goal[1] - self.pos[1] - self.move[1])
        self.result = - math.sqrt(dxm * dxm + dym * dym)
        self.pos_last = [self.pos[0], self.pos[1]]
        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]
    def get_cXX(self): return self.cXX + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cXY(self): return self.cXY + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cYX(self): return self.cYX + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cYY(self): return self.cYY + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cXW(self): return self.cXW + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cYW(self): return self.cYW + self.random_coef * random.randrange(-1000, 1000) / 1000.


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 30)

    pygame.init()
    display = pygame.display.set_mode((1000, 1000))
    display.fill((0, 128, 255))
    run = True
    clock = time.Clock()

    number = 100
    dot = []
    for i in range(number):
        dot.append(Dot())
    counter = 1

    while(run):


        counter += 1
        if counter < 6:
            if counter % 2 == 0:
                best = 0
                best2 = 1
                for i in range(2, number):
                    if dot[i].result > dot[best].result:
                        best = i
                    elif dot[i].result > dot[best2].result:
                        best2 = i
                dot_best = dot[best]
                dot_second = dot[best]
                for i in range(0, number):
                    dot[i] = Dot(0,0, dot_best.get_cXX() + random.uniform(0,1) * (dot_best.get_cXX() - dot_second.get_cXX()),
                                 dot_best.get_cXY() + random.uniform(0,1) * (dot_best.get_cXY() - dot_second.get_cXY()),
                                 dot_best.get_cYX() + random.uniform(0,1) * (dot_best.get_cYX() - dot_second.get_cYX()),
                                 dot_best.get_cYY() + random.uniform(0,1) * (dot_best.get_cYY() - dot_second.get_cYY()),
                                 dot_best.get_cXW() + random.uniform(0,1) * (dot_best.get_cXW() - dot_second.get_cXW()),
                                 dot_best.get_cYW() + random.uniform(0,1) * (dot_best.get_cYW() - dot_second.get_cYW()))
            else:
                for i in range(number): dot[i].update()
            pygame.display.set_caption(str(counter))
        else:
            if counter % 100 == 0:
                best = 0
                for i in range(1, number):
                    if dot[i].result > dot[best].result:
                        best = i
                    dot[0] = dot[best]
                for i in range(1, number):
                    dot[i] = Dot(0,0,dot[0].get_cXX(), dot[0].get_cXY(), dot[0].get_cYX(), dot[0].get_cYY(), dot[0].get_cXW(), dot[0].get_cYW())
            else:
                for i in range(number): dot[i].update()
            pygame.display.set_caption(" XX: " + str(dot[0].cXX)
                                       + " XY: " + str(dot[0].cXY)
                                       + " YX: " + str(dot[0].cYX)
                                       + " YY: " + str(dot[0].cYY)
                                       + " XW: " + str(dot[0].cXW)
                                       + " YW: " + str(dot[0].cYW)
                                       )

        display.fill((0, 180, 200))
        for i in range(number):
            pygame.draw.line(display, (255, 255, 255), dot[i].get_pos(), dot[i].get_pos_last(), 2)
            pygame.draw.circle(display, (255, 255, 255), dot[i].get_pos(), 4)
            pygame.draw.circle(display, (4, 5, 5), dot[i].goal, 7)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()

if __name__ == '__main__':
   main()
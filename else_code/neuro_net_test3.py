import pygame
from pygame import time
import random
import math
import os

class Dot:
    def __init__(self, x = 0, y = 0, csX = 0, csY = 0, ceX = 0, ceY = 0, cwX = 0, cwY = 0, cX = 0, cY = 0, cW = 0):
        self.goal = [500, 500]
        if x == 0 and y == 0:
            self.pos_start = [random.randrange(0, 1000), random.randrange(0, 1000)]
            while(abs(self.pos_start[0] - self.goal[0]) < 200 and abs(self.pos_start[1] - self.goal[1]) < 200):
                self.pos_start = [random.randrange(0, 1000), random.randrange(0, 1000)]
        else: self.pos_start = [x, y]
        self.angle = random.randrange(0, 2 * 3140)/1000.
        self.distance = 20
        self.pos_end = [self.pos_start[0] + self.distance * math.sin(self.angle),
                        self.pos_start[1] + self.distance * math.cos(self.angle)]

        self.csX = csX
        self.csY = csY
        self.ceX = ceX
        self.ceY = ceY
        self.cwX = cwX
        self.cwY = cwY

        self.cX = cX
        self.cY = cY
        self.cW = cW


        self.result = 0
        self.random_coef = 0.01
    def find_move(self):
        self.angle_X = self.pos_start[0] * self.csX + self.pos_end[0] * self.ceX + self.cwX
        self.angle_Y = self.pos_start[1] * self.csY + self.pos_end[1] * self.ceY + self.cwY

        self.angle = self.angle_X * self.cX + self.angle_Y * self.cY + self.cW
    def update(self):
        self.find_move()

        self.pos_end2 = self.pos_end
        self.pos_end = [self.pos_start[0] + self.distance * math.sin(self.angle),
                        self.pos_start[1] + self.distance * math.cos(self.angle)]
        self.pos_start, self.pos_end = self.pos_end, self.pos_start

        dxs = (self.goal[0] - self.pos_start[0])
        dys = (self.goal[1] - self.pos_start[1])
        dxe = (self.goal[0] - self.pos_end[0])
        dye = (self.goal[1] - self.pos_end[1])
        dxe2 = (self.goal[0] - self.pos_end2[0])
        dye2 = (self.goal[1] - self.pos_end2[1])

        self.result = (math.sqrt(dxe2 * dxe2 + dye2 * dye2) - math.sqrt(dxe * dxe + dye * dye)) \
                      + (math.sqrt(dxe * dxe + dye * dye) - math.sqrt(dxs * dxs + dys * dys)) \
                      - math.sqrt(dxs * dxs + dys * dys)


    def get_pos_start(self): return (int(self.pos_start[0]), int(self.pos_start[1]))
    def get_pos_end(self): return (int(self.pos_end[0]), int(self.pos_end[1]))
    def get_csX(self): return self.csX + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_csY(self): return self.csY + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_ceX(self): return self.ceX + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_ceY(self): return self.ceY + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cwX(self): return self.cwX + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cwY(self): return self.cwY + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cX(self): return self.cX + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cY(self): return self.cY + self.random_coef * random.randrange(-1000, 1000) / 1000.
    def get_cW(self): return self.cW + self.random_coef * random.randrange(-1000, 1000) / 1000.


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 30)

    pygame.init()
    display = pygame.display.set_mode((1500, 1000))
    display.fill((0, 128, 255))
    run = True
    clock = time.Clock()

    number = 500
    dot = []
    for i in range(number):
        dot.append(Dot())
    counter = 1

    while(run):


        counter += 1
        if counter < 1000:
            if counter % 3 == 0:
                best = 0
                best2 = 0
                for i in range(2, number):
                    if dot[i].result > dot[best].result:
                        best = i
                    elif dot[i].result > dot[best2].result:
                        best2 = i
                dot_best = dot[best]
                dot_second = dot[best2]
                for i in range(0, number):
                    dot[i] = Dot(0, 0,
                                 csX = dot_best.get_csX() + random.uniform(0, 1) * (dot_best.get_csX() - dot_second.get_csX()),
                                 csY = dot_best.get_csY() + random.uniform(0, 1) * (dot_best.get_csY() - dot_second.get_csY()),
                                 ceX = dot_best.get_ceX() + random.uniform(0, 1) * (dot_best.get_ceX() - dot_second.get_ceX()),
                                 ceY = dot_best.get_ceY() + random.uniform(0, 1) * (dot_best.get_ceY() - dot_second.get_ceY()),
                                 cwX = dot_best.get_cwX() + random.uniform(0, 1) * (dot_best.get_cwX() - dot_second.get_cwX()),
                                 cwY = dot_best.get_cwY() + random.uniform(0, 1) * (dot_best.get_cwY() - dot_second.get_cwY()),
                                 cX = dot_best.get_cX() + random.uniform(0, 1) * (dot_best.get_cX() - dot_second.get_cX()),
                                 cY = dot_best.get_cY() + random.uniform(0, 1) * (dot_best.get_cY() - dot_second.get_cY()),
                                 cW = dot_best.get_cW() + random.uniform(0, 1) * (dot_best.get_cW() - dot_second.get_cW()))
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
                    dot[i] = Dot(0, 0, csX=dot[0].get_csX(), csY=dot[0].get_csY(), ceX=dot[0].get_ceX(),
                                 ceY=dot[0].get_ceY(), cwX=dot[0].get_cwX(), cwY=dot[0].get_cwY(), cX=dot[0].get_cX(),
                                 cY=dot[0].get_cY(), cW=dot[0].get_cW())
            else:
                for i in range(number): dot[i].update()
            pygame.display.set_caption(" csX: " + str(dot[0].csX)
                                       + " csY: " + str(dot[0].csY)
                                       + " ceX: " + str(dot[0].ceX)
                                       + " ceY: " + str(dot[0].ceY)
                                       + " cwX: " + str(dot[0].cwX)
                                       + " cWY: " + str(dot[0].cwY)

                                       + " cX: " + str(dot[0].cX)
                                       + " cY: " + str(dot[0].cY)
                                       + " cW: " + str(dot[0].cW)
                                       )

        display.fill((0, 180, 200))
        for i in range(number):
            pygame.draw.line(display, (255, 255, 255), dot[i].get_pos_start(), dot[i].get_pos_end(), 2)
            pygame.draw.circle(display, (255, 255, 255), dot[i].get_pos_start(), 4)
            pygame.draw.circle(display, (4, 5, 5), dot[i].goal, 8)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()

if __name__ == '__main__':
   main()
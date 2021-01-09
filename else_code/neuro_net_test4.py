import pygame
from pygame import time
import random
import math
import os

class Dot:
    def __init__(self, x = 0., y = 0., csX = 0., csY = 0., ceX = 0., ceY = 0., cwX = 0., cwY = 0., cX = 0., cY = 0., cW = 0., random_coef = 0.01, color = [255, 255, 255]):
        self.goal = [500, 500]
        self.set_position(x, y)
        self.set_axon_koef(csX, csY, ceX, ceY, cwX, cwY, cX, cY, cW)
        #self.set_axon_koef()
        self.result = 0
        self.random_coef = random_coef
        self.chaild_coef = 0

        self.counter = 0
        self.dead = False
        self.success = False

        self.color = color
    def set_position(self, x = 0., y = 0.):
        if x == 0 and y == 0:
            self.pos_start = [random.randrange(0, 1000), random.randrange(0, 1000)]
            while(abs(self.pos_start[0] - self.goal[0]) < 200 and abs(self.pos_start[1] - self.goal[1]) < 200):
                self.pos_start = [random.randrange(0, 1000), random.randrange(0, 1000)]
        else: self.pos_start = [x, y]
        self.angle = random.randrange(0, 2 * 3140)/1000.
        self.distance = 20
        self.lifetime = 36
        self.pos_end = [self.pos_start[0] + self.distance * math.sin(self.angle),
                        self.pos_start[1] + self.distance * math.cos(self.angle)]
    def set_axon_koef(self, csX = None, csY = None, ceX = None, ceY = None,
                            cwX = None, cwY = None, cX = None, cY = None, cW = None):
        self.c_random_koef = 5
        if (csX == None) : self.csX = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.csX = csX
        if (csY == None) : self.csY = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.csY = csY
        if (ceX == None) : self.ceX = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.ceX = ceX
        if (ceY == None) : self.ceY = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.ceY = ceY

        if (cwX == None) : self.cwX = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.cwX = cwX
        if (cwY == None) : self.cwY = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.cwY = cwY

        if (cX == None) : self.cX = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.cX = cX
        if (cY == None) : self.cY = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.cY = cY
        if (cW == None) : self.cW = random.randrange(-self.c_random_koef, self.c_random_koef)
        else: self.cW = cW

    def update(self):
        self.find_move()
        self.move()
        self.find_result()
        self.find_dead()
        self.find_success()
    def find_move(self):
        # self.angle_X = self.pos_start[0] * self.csX + self.pos_end[0] * self.ceX + self.cwX
        # self.angle_Y = self.pos_start[1] * self.csY + self.pos_end[1] * self.ceY + self.cwY

        # self.angel = self.angle_X * self.cX + self.angle_Y * self.cY + self.cW
        self.angle = (math.atan2(self.pos_start[1] - self.pos_end[1], self.pos_start[0] - self.pos_end[0]) + self.cwX) * self.cX \
                      +(math.atan2(self.goal[1] - self.pos_start[1], self.goal[0] - self.pos_start[0]) + self.cwY) * self.cY + self.cW
    def move(self):
        self.pos_end2 = self.pos_end
        self.pos_end = [self.pos_start[0] + self.distance * math.sin(self.angle),
                        self.pos_start[1] + self.distance * math.cos(self.angle)]
        self.pos_start, self.pos_end = self.pos_end, self.pos_start
    def find_result(self):
        dxs = (self.goal[0] - self.pos_start[0])
        dys = (self.goal[1] - self.pos_start[1])
        dxe = (self.goal[0] - self.pos_end[0])
        dye = (self.goal[1] - self.pos_end[1])
        dxe2 = (self.goal[0] - self.pos_end2[0])
        dye2 = (self.goal[1] - self.pos_end2[1])

        #self.result = #(math.sqrt(dxe2 * dxe2 + dye2 * dye2) - math.sqrt(dxe * dxe + dye * dye)) \
                      #+ (math.sqrt(dxe * dxe + dye * dye) - math.sqrt(dxs * dxs + dys * dys)) \
        self.result = - math.sqrt(dxs * dxs + dys * dys)
    def find_dead(self):
        #if (abs(self.pos_start[0] - self.goal[0]) > 200 or abs(self.pos_start[1] - self.goal[1]) > 200):
        self.counter += 1
        if (self.lifetime - self.counter) * self.distance < \
                math.sqrt((self.pos_start[0] - self.goal[0]) * (self.pos_start[0] - self.goal[0]) +
                                         (self.pos_start[1] - self.goal[1])*(self.pos_start[1] - self.goal[1])):
            self.dead = True
    def find_success(self):
        if (abs(self.pos_start[0] - self.goal[0]) <= 7 and abs(self.pos_start[1] - self.goal[1]) <= 7):
            self.success = True
            self.random_coef = math.sqrt((self.pos_start[0] - self.goal[0])*(self.pos_start[0] - self.goal[0]) +
                                         (self.pos_start[1] - self.goal[1])*(self.pos_start[1] - self.goal[1])) ** 2 * 0.005 + 0.005
            self.chaild_coef =  10 / (math.sqrt((self.pos_start[0] - self.goal[0])*(self.pos_start[0] - self.goal[0]) +
                                           (self.pos_start[1] - self.goal[1])*(self.pos_start[1] - self.goal[1])) + 5)


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

    number = 1000
    dot = []
    for i in range(number):
        dot.append(Dot())
        dot[i].set_axon_koef()
    counter = 1
    csX, csY, ceX, ceY, cwX, cwY, cX, cY, cW = 0., 0., 0., 0.,0., 0.,0., 0.,0.

    while(run):

        counter += 1
        success = 0
        parents = []
        for i in range(len(dot) - 1, -1, -1):
            dot[i].update()
            if dot[i].success:
                parents.append(dot[i])
                if dot[i].random_coef <= 0.01:
                    success += 1
                del dot[i]
                continue
            if dot[i].dead:
                del dot[i]

        if len(dot) == 0: # Якщо всі вимруть то появляться нові жертви
            for i in range(number):
                dot.append(Dot())
                dot[i].set_axon_koef()

        for i in range(len(parents)):
            for j in range(int(5000 / len(dot) * parents[i].chaild_coef + 2) - 1):
                dot.append(Dot(0, 0, csX = parents[i].get_csX(), csY = parents[i].get_csY(), ceX = parents[i].get_ceX(),
                               ceY = parents[i].get_ceY(), cwX = parents[i].get_cwX(), cwY = parents[i].get_cwY(),
                               cX = parents[i].get_cX(), cY = parents[i].get_cY(), cW = parents[i].get_cW(),
                               random_coef = parents[i].random_coef))
            parents[i].set_position()
            parents[i].color[2] = max(0, parents[i].color[2] - 1)

        for j in range(int(5000 / len(dot) + 2) +1):
            dot_random = Dot()
            dot_random.set_axon_koef()
            dot_random.color = [0,0,0]
            dot.append(dot_random)


        if (len(parents) > 0):
            csX = parents[0].get_csX()
            csY = parents[0].get_csY()
            ceX = parents[0].get_ceX()
            ceY = parents[0].get_ceY()
            cwX = parents[0].get_cwX()
            cwY = parents[0].get_cwY()
            cX = parents[0].get_cX()
            cY = parents[0].get_cY()
            cW = parents[0].get_cW()
        pygame.display.set_caption("counter: " + str(counter) + " осіб: " + str(success) + "/" + str(len(dot)) +
                                   " csX: %+1.3f" % csX +
                                   " csY: %+1.3f" % csY +
                                   " ceX: %+1.3f" % ceX +
                                   " ceY: %+1.3f" % ceY +
                                   " cwX: %+1.3f" % cwX +
                                   " cwY: %+1.3f" % cwY +
                                   " cX: %+1.3f" % cX +
                                   " cY: %+1.3f" % cY +
                                   " cW: %+1.3f" % cW
                                   )


        display.fill((0, 180, 200))
        for i in range(len(dot)):
            pygame.draw.line(display, dot[i].color, dot[i].get_pos_start(), dot[i].get_pos_end(), 2)
            pygame.draw.circle(display, dot[i].color, dot[i].get_pos_start(), 4)
            pygame.draw.circle(display, (4, 5, 5), dot[i].goal, 8)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == '__main__':
   main()
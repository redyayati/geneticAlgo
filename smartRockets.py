import pygame as pg 
from pygame.math import Vector2
import numpy as np
import random
import pygame.gfxdraw

pg.init()
width = 800
height = 700
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock() 
running  = True

lifespan = 250 
count = 0 
target = Vector2(width/2, 100)
base_font = pg.font.SysFont('consolas', 12)
textColor = (150,150,150)
maxForce = .5
rectX = 200
rectY = 400
rectW = 400
rectH = 20

class Population():
    def __init__ (self, rockets):
        self.popsize = 200
        if rockets : self.rockets = rockets
        else : 
            self.rockets = []
            for i in range(self.popsize) :
                self.rockets.append(Rocket(None)) 
        self.matingPool = []
        self.maxfitness = 1
        self.reached = False 
    def run(self): 
        for rocket in self.rockets : 
            rocket.update()
            rocket.draw()
            if rocket.distance < 10 : self.reached = True
    def run1(self) : 
        for rocket in self.rockets  :
            rocket.draw()
    def evaluate(self):
        maxFit = 1
        for rocket in self.rockets : 
            rocket.calcFitness()
            if rocket.fitness > maxFit : maxFit = rocket.fitness
        for rocket in self.rockets : rocket.fitness /= maxFit
        self.maxfitness = maxFit
        self.matingPool = []
        for rocket in self.rockets : 
            n = int(rocket.fitness * 100)
            for i in range(n) : self.matingPool.append(rocket)
    def selection(self) : 
        newRockets = []
        for rocket in self.rockets : 
            parentA = random.choice(self.matingPool).dna
            parentB = random.choice(self.matingPool).dna
            child = parentA.crossover(parentB)
            child.mutation()
            newRockets.append(Rocket(child))
        self.rockets = newRockets
    def test(self) : 
        pass


class Rocket(): 
    completed = False
    crashed = False
    distance = 0 
    theta = 0
    fitness = 0
    def __init__ (self,dna):
        if dna : self.dna = dna
        else : self.dna = DNA(None)
        self.pos = Vector2(400,600)
        self.vel = Vector2()
        self.acc = Vector2(0.01,0)
    def applyForce(self,force): 
        self.acc += force
    def calcFitness(self) : 
        d = target.distance_to(self.pos)
        self.fitness = width/2 - d
        if self.completed : self.fitness *= 10
        if self.crashed : self.fitness = 1
    def update(self) : 
        self.applyForce(self.dna.gene[count])

        d = self.pos.distance_to(target)
        self.distance = d
        if d < 10 : 
            self.completed = True
            # self.pos = target.copy()
            self.theta = self.thetaprevious
        if self.pos.x > rectX and self.pos.x < rectX + rectW and self.pos.y > rectY and self.pos.y < rectY + rectH :
            self.crashed = True 
            self.theta = self.thetaprevious
        if self.pos.x < 0 or self.pos.x > width or self.pos.y < 0 or self.pos.y > height : 
            self.crashed = True 
            self.theta = self.thetaprevious
        if not self.completed and not self.crashed : 
            self.pos1 = Vector2(self.pos.x,self.pos.y)
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0
            self.theta = Vector2(0,50).angle_to(self.pos - self.pos1) * np.pi/180
            self.thetaprevious = self.theta
    def draw(self) :
        l = 10
        x1,y1 = self.pos.x+(5*l/4)*np.cos(self.theta + np.pi/2), self.pos.y+(5*l/4)*np.sin(self.theta + np.pi/2)
        x2,y2 = self.pos.x+l*np.cos(self.theta + np.pi/2-(3.5*np.pi/4)), self.pos.y+l*np.sin(self.theta + np.pi/2-(3.5*np.pi/4))
        x3,y3 = self.pos.x+l*np.cos(self.theta + np.pi/2+(3.5*np.pi/4)), self.pos.y+l*np.sin(self.theta + np.pi/2+(3.5*np.pi/4))
        # pg.draw.polygon(screen, ("gray"),((x1,y1), (x2,y2),(x3,y3)), 1)
        pygame.gfxdraw.filled_polygon(screen, ((x1,y1), (x2,y2),(x3,y3)), (200,100,50,120))
    def drawL(self):
        pygame.gfxdraw.line(screen,int(self.pos1.x),int(self.pos1.y),int(self.pos.x),int(self.pos.y),(200,100,50,60))
class DNA(): 
    def __init__(self,gene) :
        if gene : self.gene = gene 
        else :
            self.gene = []
            for i in range(lifespan) : 
                randVec = Vector2(random.uniform(-1,1), random.uniform(-1,1))
                randVec.scale_to_length(maxForce)
                self.gene.append(randVec)
    def crossover(self,partner) :
        newGene = [0 for i in range(lifespan)]
        midpoint = random.randint(0,lifespan) 
        for i in range(lifespan) : 
            if i > midpoint : newGene[i] = self.gene[i]
            else : newGene[i] = partner.gene[i]
        return DNA(newGene)
    def mutation(self) : 
        for i in range(lifespan) : 
            if random.random() < .01 : 
                self.gene[i] = Vector2(random.uniform(-1,1), random.uniform(-1,1))
                self.gene[i].scale_to_length(maxForce)


myPop = Population(None)


gen = 0 
fitness = 0
pause = False
objCol = [125,125,125]

while running : 
    screen.fill((0,0,0))
    if not pause : 
        myPop.run()
        count += 1
    else : myPop.run1()
    pg.draw.rect(screen, (0,0,0), (0,0,110 ,63))
    text = base_font.render("Frame      " + str(count),True,textColor)
    text2 = base_font.render("Generation "+str(gen),True,textColor)
    text3 = base_font.render("MaxFitness "+str(fitness),True,textColor)
    text4 = base_font.render("Population "+str(myPop.popsize),True,textColor)
    screen.blit(text2,(2,20))
    screen.blit(text3,(2,35))
    screen.blit(text4,(2,50))
    screen.blit(text, (2,5))
    if count == lifespan : 
        # screen.fill((0,0,0))
        myPop.evaluate()
        fitness = int(myPop.maxfitness)
        myPop.selection()
        myPop = Population(myPop.rockets)
        count = 0
        gen += 1
    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_q : 
                running = False 
            if event.key == pg.K_p : 
                pause = False 
            if event.key == pg.K_SPACE : 
                pause = True
            if event.key == pg.K_r : 
                screen.fill(('black'))
                myPop = Population(None)
                fitness = int(myPop.maxfitness)
                objCol = [125,125,125]   
                gen = 0
                count = 0
    if myPop.reached : objCol = [125,225,125]
    # else : objCol = [125,125,125]
    pg.draw.circle(screen,objCol, (int(target.x),int(target.y)),10)
    pg.draw.rect(screen,objCol,(rectX,rectY,rectW,rectH),10)
    pg.display.flip()
    clock.tick(60)
pg.quit()

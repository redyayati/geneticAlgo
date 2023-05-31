import pygame as pg 
import random

def displayStats(maxFit, gen, fit, pop, mut,xVal, yVal) : 
    if searching == True : 
        textMaxfit = base_fontFit.render(maxFit,True,(100,100,100))
    if searching == False : 
        textMaxfit = base_fontFit.render(maxFit,True,(100,100,100))
        textyay = base_font.render("there !",True,(0,0,250))
        screen.blit(textyay, (xVal,300))
    textGen = base_font.render("Total Generations :      " + str(gen),True,textColor)
    textFit = base_font.render("Average fitness :        " + str(fit),True,textColor)
    textPop = base_font.render("Total Population :       " + str(pop),True,textColor)
    textMutn = base_font.render("Mutation Rate :          " + str(mut),True,textColor)
    screen.blit(textMaxfit, (xVal,200))
    screen.blit(textGen, (xVal,yVal))
    screen.blit(textFit, (xVal,yVal + textGap))
    screen.blit(textPop, (xVal,yVal + 2*textGap))
    screen.blit(textMutn, (xVal,yVal + 3*textGap))

def displayPop(population, xVal) : 
    line = 0
    for pop in population : 
        text = base_fontpop.render(pop.getPhrase(), True, textColor2)
        yVal = 20+ line*textGap2
        if yVal < height : screen.blit(text, (xVal,yVal))
        elif yVal >= height : 
            nextYval = yVal - height + 20
            if nextYval < height : screen.blit(text, (xVal+200,nextYval))
            if nextYval >= height : pass
        line += 1

class DNA(): 
    def __init__(self, target, mutationRate) : 
        self.gene = []
        self.mutationRate = mutationRate
        self.target = target
        for i in range(len(target)) : 
            c = chr(random.randint(32,128))
            self.gene.append(c)
    def fitness(self) : 
        score = 0 
        for i in range(len(self.target)) : 
            if self.target[i] == self.gene[i] : score += 1 
        self.fit = score / len(self.target)
        # return fit
    def crossover(self, partner) : 
        midpoint = random.randint(0,len(self.target))
        child = DNA(self.target,self.mutationRate)
        for i in range(len(self.target)) : 
            if i < midpoint : child.gene[i] = self.gene[i]
            else : child.gene[i] = partner.gene[i]
        return child
    def mutate(self) : 
        for i in range(len(self.gene)) : 
            if random.random() < self.mutationRate : 
                self.gene[i] = chr(random.randint(32,128))
    def getPhrase(self) : 
        self.myString = ""
        for ele in self.gene : self.myString += ele
        return self.myString



pg.init()
width = 900
height = 800

screen = pg.display.set_mode((width, height))

clock = pg.time.Clock() 
running  = True

base_font = pg.font.SysFont('consolas', 20)
base_fontFit = pg.font.SysFont('consolas', 40)
base_fontpop = pg.font.SysFont('consolas', 12)
textColor = (150,150,150)
textColor2 = (150,150,200)
textGap = 25
textGap2 = 13

genVal = 0 
fitVal = 50
popVal = 500
mutationRate = 0.01

phrase = "failure is not fatal"

population = []

for i in range(popVal) : 
    p = DNA(phrase, mutationRate)
    population.append(p)

maxFit = population[0]
searching = True

while running : 
    screen.fill((255,255,255))
    if searching : 
        matingpool = []
        avgFitness = 0
        for pop in population : 
            pop.fitness()
            avgFitness += pop.fit
            if pop.fit > maxFit.fit : maxFit = pop
        fittestString = maxFit.getPhrase()
        if fittestString == phrase : 
            searching = False
        avgFitness = round(avgFitness / popVal , 2)

        for pop in population : 
            n = int(pop.fit * 100)
            for i in range(n) : 
                matingpool.append(pop)
            
        for i in range(len(population)) : 
            poollength = len(matingpool) - 1
            parentA = matingpool[random.randint(0,poollength)]
            parentB = matingpool[random.randint(0,poollength)]
            child  = parentA.crossover(parentB)
            child.mutate()
            population[i] = child
        genVal += 1

    displayPop(population, 450)
    displayStats(fittestString,genVal,avgFitness,popVal,mutationRate,30,500)
    
    
    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
    pg.display.flip()
    # clock.tick(60)
pg.quit()

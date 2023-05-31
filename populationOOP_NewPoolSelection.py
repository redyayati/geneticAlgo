# Using new pool selection method (this method does not require any lengthy mating pool array) : 
# step 1 : choose random number between 0 and population length 
# step 2 : choose a random number again. If it is less that the fitness of that object then, pick it,
#          otherwise reject it and repeat from step one 

import pygame as pg 
import random

class DNA(): 
    def __init__(self, length) : 
        self.gene = []
        self.length = length
        for i in range(length) : 
            c = chr(random.randint(32,128))
            self.gene.append(c)
    def fitness(self,targetp) : 
        score = 0 
        for i in range(len(targetp)) : 
            if targetp[i] == self.gene[i] : score += 1 
        self.fit = score / len(targetp) + .01  # adding 0.01 just to give positive number during picking for mating 
        # self.fit = score / len(targetp)   # without the "+ .01"

    def crossover(self, partner) : 
        midpoint = random.randint(0,self.length)
        child = DNA(self.length)
        for i in range(self.length) : 
            if i < midpoint : child.gene[i] = self.gene[i]
            else : child.gene[i] = partner.gene[i]
        return child
    def mutate(self, mutationRate) : 
        for i in range(len(self.gene)) : 
            if random.random() < mutationRate : 
                self.gene[i] = chr(random.randint(32,128))
    def getPhrase(self) : 
        self.myString = ""
        for ele in self.gene : self.myString += ele
        return self.myString

class Population() : 
    def __init__(self, targetp,mutationRate, popmax) : 
        self.target = targetp
        self.mutationRate = mutationRate
        self.popmax = popmax
        self.generation = 0
        self.found = False
        self.population = []
        for i in range(popmax) : 
            self.population.append(DNA(len(targetp)))
        self.matingPool = []
        self.xVal = []
        self.maxfitness = 0
    def calcFitness(self) : 
        self.avgFitness = 0
        for pop in self.population : 
            pop.fitness(self.target)
            self.avgFitness += pop.fit
        self.avgFitness = round(self.avgFitness/self.popmax,2)
    def acceptReject(self) : 
        while True :  
            partner = random.choice(self.population)
            r = random.uniform(0,self.maxfitness)
            if r < partner.fit : 
                return partner 
    def generate(self) : 
        # calculate maximum fitness : 
        self.maxfitness = 0 
        for pop in self.population : 
            if pop.fit > self.maxfitness : 
                self.maxfitness = pop.fit
                self.fittestDNA = pop

        # Refill the population with children formed by mating 
        self.xVal = [] # this is for coordinate values for logging values on screen 
        newPopulation = []
        for i in range(len(self.population)) : 
            parentA = self.acceptReject()
            parentB = self.acceptReject()
            child  = parentA.crossover(parentB)
            child.mutate(self.mutationRate)
            newPopulation.append(child)
            self.xVal.append(random.randint(450-20, 450+20)) # this is for coordinate values for logging values on screen 
        self.population = newPopulation
        self.generation +=1
    def evaluate(self):
        if self.target == self.fittestDNA.getPhrase() : self.found = True
    def displayInfo(self) : 
        self.displayPop()
        self.displayStats(30,500)
    def displayStats(self,xVal, yVal) : 
        if searching == True : 
            textMaxfit = base_fontFit.render(self.fittestDNA.getPhrase(),True,(100,100,100))
            textBest = base_font.render("Best so far...",True,textColor)
            screen.blit(textBest, (xVal, 150))
        if searching == False : 
            textMaxfit = base_fontFit.render(self.fittestDNA.getPhrase(),True,(100,100,100))
            textyay = base_font.render("there !",True,"blue")
            screen.blit(textyay, (xVal,150))
        textGen = base_font.render("Total Generations :      " + str(self.generation),True,textColor)
        textFit = base_font.render("Average fitness :        " + str(round(self.avgFitness*100))+"%",True,textColor)
        textPop = base_font.render("Total Population :       " + str(self.popmax),True,textColor)
        textMutn = base_font.render("Mutation Rate :          " + str(self.mutationRate*100) + "%",True,textColor)
        screen.blit(textMaxfit, (xVal,200))
        screen.blit(textGen, (xVal,yVal))
        screen.blit(textFit, (xVal,yVal + textGap))
        screen.blit(textPop, (xVal,yVal + 2*textGap))
        screen.blit(textMutn, (xVal,yVal + 3*textGap))
    def displayPop(self) : 
        line = 0
        for i in range(len(self.population)) : 
            text = base_fontpop.render(self.population[i].getPhrase(), True, textColor2)
            yVal = 20+ line*textGap2
            if yVal < height : screen.blit(text, (self.xVal[i],yVal))
            elif yVal >= height : 
                nextYval = yVal - height + 20
                if nextYval < height : screen.blit(text, (self.xVal[i]+200,nextYval))
                if nextYval >= height : pass
            line += 1


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
textColor2 = (150,150,250)
textGap = 25
textGap2 = 13

popVal = 500
mutationRate = 0.01
phrase = "Its cold Outside !"

searching = True

myPopulation = Population(phrase, mutationRate, popVal)

while running : 
    screen.fill((255,255,255))
    if searching : 
        myPopulation.calcFitness()
        myPopulation.generate()
        myPopulation.evaluate()
        if myPopulation.found : searching = False
    myPopulation.displayInfo()
    
    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
    pg.display.flip()
    # clock.tick(60) 
pg.quit()

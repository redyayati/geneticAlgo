

import random

class obj:
    def __init__(self,name) : 
        self.name = name
        self.score = 0
        self.prob = 0
        self.cummulative = 0
        self.histogram = 0 
    def __repr__(self): 
        # return f"{self.name},{self.score},          ,{round(self.prob,3), round(self.cummulative,3)}"
        return f"{self.name},  ,{self.score}"


names  = ["mango" , "blueberry", "cherry", "melon", "apple","banana", "cheekoo", "Leechi"]
score = [25,3,1,7,1, 8,10,15]

objects = [0 for _ in range(len(names))]
for i in range(len(objects)) : 
    objects[i] = obj(names[i])
    objects[i].score = score[i]

sum = 0 
for i in range(len(objects)) : 
    sum += objects[i].score
for i in range(len(objects)) : 
    objects[i].prob = objects[i].score / sum
    
cum = 0 
for i in range(len(objects)) : 
    cum += objects[i].prob
    objects[i].cummulative = cum 
print(sum)
for object in objects : 
    print(object)
print("")


def pickOne(list) : 
    index = 0 
    r = random.random()
    while r > 0 : 
        r = r - list[index].prob
        index += 1 
    index -= 1 
    return list[index]

count = 0 
while count < 1000 : 
    p  = pickOne(objects)
    p.histogram += 1
    count +=1
for object in objects : 
    print(object.name, object.histogram)
    

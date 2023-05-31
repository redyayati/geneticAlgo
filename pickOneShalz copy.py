# Reference to Shalz method of pool selection 

import random

class obj:
    def __init__(self,name) : 
        self.name = name
        self.score = 0
        self.prob = 0
        self.prob2 = 0
        self.cummulative = 0
        self.histogram = 0 
    def __repr__(self): 
        return f"{self.name},{self.score},{round(self.prob,3), round(self.prob2,2),round(self.cummulative,3)}"
        # return f"{self.name},  ,{self.score}"


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

for i in range(len(objects)) : 
    p = objects[i].prob
    objects[i].prob2 =  (p**2)

cum = 0 

for i in range(len(objects)) : 
    cum = cum + objects[i].prob2
    objects[i].cummulative = cum 
 

print(sum)
# for object in objects : 
#     print(object)
print("")

found = []

count = 0
while count < 10000 : 
    search = True
    r = random.uniform(0,cum) 
    for i in range(len(objects)) : 
        if r > objects[i].cummulative : pass
        else : 
            if search : 
                objects[i].histogram += 1
                search = False
    count += 1

for object in objects : 
    print(object.name , "  ", object.histogram)


# def pickOne(objects) : 
#     r = random.random() 
#     print(r)
#     for i in range(len(objects)) : 
#         if r > objects[i].cummulative : pass
#         else : 
#             return objects[i]

# print(pickOne(objects))




import math
from heapq import heapify, heappush, heappop

#open text files to access data
coordinates = open("Coordinates.txt", "r")
adjacencies = open("Adjacencies.txt", "r")

#create empty dictionary for Coordinates
coorDict = {}
#create empty dictionary for Adjacencies
adjDict = {}
#create empty dictionary for dead ends
deadEndDict = {}
#create has been visited dictionary
beenDict = {}
#Create a priority Q in the way of a max heap as we are paying
#attention to the order that we are visiting cities
memory = []
heapify(memory)

#create dictionary for Coordinates
for x in coordinates:
    x = x.strip("\n")
    data = x.split(" ")
    location = data[1] + ',' + data[2]
    coorDict[data[0]]= location

#create dictionary for Adjacencies
for y in adjacencies:
    y = y.strip("\n")
    data = y.split(" ")
    j = data[0]
    del data[0]
    adjDict[j] = data  

#Distance between points
def Distance(a, b):
    distance = (math.sqrt((float(b[0])-float(a[0]))**2 + (float(b[1])-float(a[1]))**2))
    return distance

#find the lowest distance, either x and y coordinates
def xY(a,b):
    xCoor = abs(float(b[1])-float(a[1]))
    yCoor = abs(float(b[0])-float(a[0]))
    if xCoor < yCoor:
        return xCoor
    else:
        return yCoor

#Decode info for two points and finding distance
def Locations(a, b):
    choice = coorDict[a]
    choice = choice.split(",")
    goal = coorDict[b]
    goal = goal.split(",")
    return Distance(choice,goal)

#decode info to find the best individual movement
def Exact(a,b):
    choice = coorDict[a]
    choice = choice.split(",")
    goal = coorDict[b]
    goal = goal.split(",")
    return xY(choice,goal)
    

#main traverse function
def traverse (a,b):
    #declare start and end and counter for traversal
    start = a
    end = b
    count = 1

    print(start)
    
    #calculate proximity of start
    close = Locations(start, end)
    #set current position to start
    position = start
    #push current position and proximity to max heap
    heappush(memory, (-1*count ,[close, position]))
    count += 1
    beenDict[position] = ' '
    

    #while still not at the end
    while position != end:
        #have we moved bool being established/reset
        moved = False
        
        #get all the current adjancenies for the current position
        current = adjDict[position]
        lowest = 100

        #go through all adjancent cities to determine which one is closer
        for x in range (0,len(current)):
                       
            #if the proximity of this city is closer than the current position and hasn't been
            #marked as a dead end and a city we haven't visited
            if Locations(current[x], end) < close and current[x] not in deadEndDict and current[x] not in beenDict:
                #say we have a potential move
                moved = True
                #update the new position and proximity to this city
                position = current[x]
                close = Locations(current[x], end)
            
        #only the best city will stay after evaluating those cities
        #then add the new city to the has been visited Dict and push it onto memory
        if moved == True:        
            beenDict[position] = ' '
            heappush(memory, (-1*count ,[close, position]))
            count += 1  
            #print(memory)
        
        #if we haven't moved and we're not at start and there is only one adj city (aka previous city) we've hit a dead end    
        if moved == False and len(current) < 2 and position != start:
            
            #add this city to dead endlist and reset memory
            deadEndDict[position] = " "         
            
            #Hold the city aside to find it's parent   
            temp = memory[0]
            heappop(memory)

            #grab the parents info
            position = memory[0][1][1]
            close = memory[0][1][0]
            #push the dead end back on
            heappush(memory, (temp))
            #make the parent the next step for backtracking
            heappush(memory, (-1*count ,[close, position]))            
            count += 1

            #set moved to true
            moved = True

        #if we haven't moved and the only moves are away
        elif moved == False :
            #create comparison point 
            final = 100
            currProx = close
            #iterate through adjacent cities
            for x in range (0,len(current)):
            
                #if the city is not a dead end and one that we haven't been to yet
                if current[x] not in deadEndDict and current[x] not in beenDict:
                    #testing variables for position and proximity
                    pos = current[x]
                    clo = Locations(current[x], end)
                    #look for the next node that provides the least increase in distance from target
                    #when no direct path is available
                    if clo - currProx < final:
                        
                        #set the final comparison/position/proximity
                        final = abs(currProx - clo)
                        position = pos
                        close = clo
                        moved = True
                        
            #if we could move now add it to memory
            if moved == True:
                beenDict[position] = ' '
                heappush(memory, (-1*count ,[close, position]))
                count += 1 
            #If no other prefered method is available just choose the city closeset
            #with no restrictions other than not a known deadend
            #attempted a late adjustment to prefer movements based on a x or y movement being closer
            #But not quite sure on how to mae it work
            else:
                lowest = 100
                for x in range (0,len(current)):                
                    if current[x] not in deadEndDict and Exact(current[x],end) < lowest:

                        position = current[x]
                        close = Locations(current[x], end)
                        heappush(memory, (-1*count ,[close, position]))
                        count += 1
        print (position)
        #print(memory)
        
f = False
s = False
#driver code
while f == False:
    first = input("What city are you in now?: ")
    if first in coorDict:
        f = True
    else: 
        print("Incorrect city, try again")
while s == False:
    second = input("\nWhat city do you want to go to?:  ")
    if second in coorDict:
        s = True
    else: 
        print("Incorrect city, try again")
print("\nYour path will be:")
traverse(first,second)


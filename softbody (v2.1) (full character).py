import math
import random
from graphics import *
import keyboard

x=[]
y=[]
vx=[]
vy=[]
ay = 0
order = []
explode = False
pop = False
zoom = 10 # how zoomed out is the blob from the page (required because exponentials must be within the preset range)
snodes = 40 # amount of nodes that make up the circle (at the start)
nodes = snodes # node value that changes if the blob pops
radius = 200 # this stops shaking at the start if it is at the correct figure (maybe you want a shaky start)
screenwidth = 600
screenheight = 600
#wantdis = 0
middlex = 0
middley = 0
gravity = 0.2
touch = [0,0,0,0]

canvas = GraphWin("blob", screenwidth, screenheight, autoflush = False)
canvas.setBackground (color_rgb(255, 255, 255))
canvas.setCoords(-screenwidth/2,-screenheight/2,screenwidth/2,screenheight/2)

def make(middlex, middley):
    for i in range (len(x)):
        x.pop(0)
        y.pop(0)
        vx.pop(0)
        vy.pop(0)
    for i in range (nodes): # make the nodes
        x.append (math.cos(math.radians(i*(360/nodes)))*radius+middlex)
        y.append (math.sin(math.radians(i*(360/nodes)))*radius+middley)
        #x.append (random.uniform(-radius, radius))
        #y.append (random.uniform(-radius, radius))
        vx.append (0)
        vy.append (-55)

def update_soft(nodes, firmness, bounciness, randomness):
    global ay
    global gravity
    wantdis = 0#10000/nodes**2 # change based on nodes
    #global wantdis
    sc2 = firmness / 15 / nodes # change based on the sc1
    sc1 = firmness / nodes # should be constant
    ay *= 0.98
    for i in range (nodes):
        vx[i] *= 0.997
        vy[i] *= 0.997
        for o in range (nodes):
            if o != i:
                extx = x[i] - x[o]
                exty = y[i] - y[o]
                mag = (math.sqrt(extx**2+exty**2)) # mag = magnitude (distance)
                if mag == 0:
                    mag = 0.001
                mag = 1/mag
                extx /= mag
                exty /= mag
                vx[i] += sc1*extx*mag**2
                vy[i] += sc1*exty*mag**2




        if i == 0:
            extx = x[i] - x[nodes-1]
            exty = y[i] - y[nodes-1]
        else:
            extx = x[i] - x[i-1]
            exty = y[i] - y[i-1]
        mag = wantdis-(math.sqrt(extx**2+exty**2))
        if mag == 0:
            mag = 0.001
        extx /= mag
        exty /= mag
        vx[i] += sc2*extx*mag**2
        vy[i] += sc2*exty*mag**2
        
        if i == nodes-1:
            extx = x[i] - x[0]
            exty = y[i] - y[0]
        else:
            extx = x[i] - x[i+1]
            exty = y[i] - y[i+1]
        mag = wantdis-(math.sqrt(extx**2+exty**2))
        if mag == 0:
            mag = 0.001
        extx /= mag
        exty /= mag
        vx[i] += sc2*extx*mag**2
        vy[i] += sc2*exty*mag**2
            

        if y[i] > -screenheight/2*zoom*0.99: # do not let gravity effect the node if it is against the floor
            vy[i] -= gravity # gravity
            vy[i] += ay
            #print (y[i])
        vx[i] += random.uniform(-randomness,randomness) # randomness to undo the collapse when squashed to the floor
        vy[i] += random.uniform(-randomness,randomness)

    for o in range(4):
        touch[o] = False
    for i in range (nodes):
        x[i] += vx[i] # move the velocity vector
        y[i] += vy[i]
        if x[i] < -screenwidth/2*zoom: # do not exceed boundaries
            x[i] = -screenwidth/2*zoom
            vx[i] *= -bounciness
            touch[0] = True
        elif x[i] > screenwidth/2*zoom:
            x[i] = screenwidth/2*zoom
            vx[i] *= -bounciness
            touch[1] = True
        if y[i] < -screenheight/2*zoom:
            y[i] = -screenheight/2*zoom
            vy[i] *= -bounciness
            touch[2] = True
        elif y[i] > screenheight/2*zoom:
            y[i] = screenheight/2*zoom
            vy[i] *= -bounciness
            touch[3] = True
    #print (min(y), screenheight/-2*zoom)
            
def draw(eye_bad, eye_shrink): # 1/eyebad = fraction points used for the eyes
    points = []
    e1points = []
    e2points = []
    width = (max(x)-min(x))/zoom
    for i in range (nodes):
        if i % eye_bad == 0:
            e1points.append(Point(((((x[i]-middlex)/zoom)/eye_shrink)+(middlex/zoom)-width/5), (((y[i]-middley)/zoom)/eye_shrink)+(middley/zoom)))
            e2points.append(Point(((((x[i]-middlex)/zoom)/eye_shrink)+(middlex/zoom)+width/5), (((y[i]-middley)/zoom)/eye_shrink)+(middley/zoom)))
        points.append (Point(x[i]/zoom, y[i]/zoom))
    blob = Polygon(points)
    blob.setFill("blue3")
    blob.draw(canvas)
    eye1 = Polygon(e1points)
    eye1.setFill("white")
    eye1.draw(canvas)
    eye2 = Polygon(e2points)
    eye2.setFill("white")
    eye2.draw(canvas)
    #circle = Circle(Point((sum(x)/len(x))/zoom,(sum(y)/len(y))/zoom), 3)
    #circle.draw(canvas)

def rearrange(): # this is a function to return the correct order of drawing required for no overlaps
    global order # the function is not used due to bugs and the circle can be built in the correct shape initialy
    global middlex
    global middley
    angle = []
    order = []
    middlex = (sum(x)/len(x))
    middley = (sum(y)/len(y))
    for i in range (nodes):
        angle.append(math.degrees(math.atan2(y[i]-middley,x[i]-middlex)))
    for i in range (nodes):
        order.append(angle.index(min(angle)))
        angle[angle.index(min(angle))] = 999

def refresh():
    canvas.update()
    for item in canvas.items[:]:
        item.undraw()

def move(speed, jumpspeed):
    #global wantdis
    global ay
    if keyboard.is_pressed("w") and touch[2]:
        p = 0
        for i in range (nodes): # all the points gain a velocity in the direction
            if round(abs(y[i]- (-screenheight/2*zoom)))==0: # for each point touching the floor the jump power increases
                p = p+1
        if p > nodes/3:
            p = nodes/3
        for i in range (nodes):
            if p/nodes*2 > ay:
                ay = p/nodes*jumpspeed
    if keyboard.is_pressed("a") and touch[2]: # must be touching floor too
        for i in range (nodes):
            vx[i] -= speed
    if keyboard.is_pressed("s") and touch[2]:
        for i in range (nodes):
            vy[i] -= speed
    if keyboard.is_pressed("d") and touch[2]:
        for i in range (nodes):
            vx[i] += speed
    #if keyboard.is_pressed("+"): # option to change the size while running (not reccomended)
     #   wantdis += 0
    #if keyboard.is_pressed("-"):
     #   wantdis -= 0
    if keyboard.is_pressed("r"):
        pop = True

def broke():
    if touch[0] and touch[1]  and touch[2] and touch[3]:
        return (True)
    else:
        return (False)

def movepop():
    global gravity
    for i in range (nodes):
        vy[i] -= gravity*0.5
        vx[i] *= 0.999
        vy[i] *= 0.999
        x[i] +=vx[i]
        y[i] +=vy[i]
        size[i] -= 0.02
        if size[i] < 0:
            size[i] = 0

def drawpop():
    points = []
    for i in range (nodes):
        points.append (Point(x[i]/zoom, y[i]/zoom))
        if size[i] > 0:
            blob = Circle(points[i], size[i])
            blob.setFill("blue3")
            blob.draw(canvas)

def makepop(amount, power):
    global middlex
    global middley
    global nodes
    avx = (sum(vx)/len(vx))/2
    avy = (sum(vy)/len(vy))/2
    for i in range (amount):
        x.append(random.uniform(min(x),max(x)))
        y.append(random.uniform(min(y),max(y)))
        vx.append(random.uniform(-power,power)+avx)
        vy.append(random.uniform(-power,power)+avy)
        size.append(random.randint(3,8))
    for i in range (nodes):
        x.pop(0)
        y.pop(0)
        vx.pop(0)
        vy.pop(0)
    nodes = amount

def remove():
    global snodes
    global nodes
    for i in range (nodes):
        x.pop(0)
        y.pop(0)
        vx.pop(0)
        vy.pop(0)
        size.append(0)
    nodes = snodes

def checkpop():
    if math.sqrt((sum(vx)/len(vx))**2+(sum(vy)/len(vy))**2) > 60: # if the speed is really quick
        return (True)
    elif keyboard.is_pressed("r"): # user chooses to restart
        return (True)
    elif touch[0] and touch[1]  and touch[2] and touch[3]: # accidental explosion
        return (True)
    else:
        return (False)
    
while True:
    make(middlex,middley)
    pop = False
    while pop == False:
        move(0.15,3)
        update_soft(nodes, 4, 0.1, 0.003)
        #^^^^^^^^^^^^^ firmness should not exceed 5 (risk of explosion) and shouldnt be less than 1 (risk of collapse)
        #^^^^^^^^^^^^^ bounciness should not exceed 0.5 (risk of explosion) it is used to reduce the chance of collapse when hitting ground
        #^^^^^^^^^^^^^ randomness can create a nice ripple effect but can cause the blob to move on its own so is best kept low, it is also requred for recovery after a complete collapse
        rearrange()
        #time.sleep(0.1)
        draw(5,3.5)
        refresh()
        pop = checkpop()
        #print (math.sqrt((sum(vx)/len(vx))**2+(sum(vy)/len(vy))**2))
        
    if pop == True: # if the player dies
        size = []
        makepop(30, 2)
        while max(size) > 0: # until all particles shrink to nothing
            movepop()
            drawpop()
            refresh()
        remove()
    
    

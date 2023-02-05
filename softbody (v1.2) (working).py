import math
import random
from graphics import *
import keyboard

x=[]
y=[]
vx=[]
vy=[]
order = []
zoom = 2
nodes = 40 # amount of nodes that make up the circle
radius = 100
screenwidth = 600
screenheight = 600
middlex = 0
middley = 0
for i in range (nodes):
    x.append (math.cos(math.radians(i*(360/nodes)))*radius)
    y.append (math.sin(math.radians(i*(360/nodes)))*radius)
    #x.append (random.uniform(-radius, radius))
    #y.append (random.uniform(-radius, radius))
    vx.append (0)
    vy.append (0)

canvas = GraphWin("blob", screenwidth, screenheight, autoflush = False)
canvas.setBackground (color_rgb(255, 255, 255))
canvas.setCoords(-screenwidth/2,-screenheight/2,screenwidth/2,screenheight/2)
def update_soft(radius, nodes, sc1):
    global middlex
    global middley
    wantdis = 0#10000/nodes**2 # change based on nodes
    sc2 = sc1 / 15 / nodes # change based on the sc1
    sc1 = sc1 / nodes # should be constant
    #print (wantdis)
    for i in range (nodes):
        vx[i] *= 0.995
        vy[i] *= 0.995
        for o in range (nodes):
            if o != i:
                extx = x[i] - x[o]
                exty = y[i] - y[o]
                mag = (math.sqrt(extx**2+exty**2))
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
            

        if y[i] > -screenheight/2*zoom:
            vy[i] = vy[i]-0.1
            print (y[i])
        vx[i] += random.uniform(-0.001,0.001)
        vy[i] += random.uniform(-0.001,0.001)


    for i in range (nodes):
        x[i] += vx[i]
        y[i] += vy[i]
        if x[i] < -screenwidth/2*zoom:
            x[i] = -screenwidth/2*zoom
            vx[i] = 0
        elif x[i] > screenwidth/2*zoom:
            x[i] = screenwidth/2*zoom
            vx[i] = 0
        if y[i] < -screenheight/2*zoom:
            y[i] = -screenheight/2*zoom
            vy[i] = 0
        elif y[i] > screenheight/2*zoom:
            y[i] = screenheight/2*zoom
            vy[i] = 0

def draw(radius):
    points = []
    for i in range (nodes):
        points.append (Point(x[i]/zoom, y[i]/zoom))
    blob = Polygon(points)
    blob.setFill("blue3")
    blob.draw(canvas)
    circle = Circle(Point((sum(x)/len(x))/zoom,(sum(y)/len(y))/zoom), 3)
    circle.draw(canvas)

def rearrange():
    global order
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

def move():
    if keyboard.is_pressed("w"):
        for i in range (nodes):
            vy[i] += 0.3
    if keyboard.is_pressed("a"):
        for i in range (nodes):
            vx[i] -= 0.3
    if keyboard.is_pressed("s"):
        for i in range (nodes):
            vy[i] -= 0.3
    if keyboard.is_pressed("d"):
        for i in range (nodes):
            vx[i] += 0.3

while True:
    move()
    update_soft(radius,nodes, 3)
    rearrange()
    #time.sleep(0.1)
    draw(radius)
    refresh()
    
    

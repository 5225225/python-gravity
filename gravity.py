import math
import sys
import time
import random

from PIL import Image

FPS = 60

class point:
    def __init__(self, x, y, velocity_x = 0, velocity_y = 0, mass=1.0):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

def distance(p1, p2):
    x = abs(p1.x - p2.x)
    y = abs(p1.y - p2.y)

    return math.sqrt(x**2 + y**2)

def direction(p1, p2):
    d = distance(p1, p2)
    x = (p2.x - p1.x)
    y = (p2.y - p1.y)
    try:
        newx = x / (x + y)
        newy = y / (x + y)
    except ZeroDivisionError:
        return (0, 0)

    assert abs(1.0 - (newx + newy)) < .00000000001
    # It can't be perfectly accurate, but close enough is good.

    return (x, y)

def calcforce(obj1, obj2):
    r = distance(obj1, obj2)
    if r == 0:
        r = 0.001
    m1 = obj1.mass
    m2 = obj2.mass
    g = 0.002

    f = g * ((m1 * m2) / (r))
    
    return f

def step(points):
    newpoints = points[:]
    # Make a copy of points, as the original values are needed

    for index, obj1 in enumerate(points):
        for obj2 in points:
            if obj1 != obj2:
                f = calcforce(obj1, obj2)
                xdir, ydir = direction(obj1, obj2)
                newpoints[index].velocity_x += (f * xdir) / obj1.mass / FPS
                newpoints[index].velocity_y += (f * ydir) / obj1.mass / FPS

    for obj in newpoints:
        obj.x += obj.velocity_x
        obj.y += obj.velocity_y

    return newpoints
                    

simple = [
    point(23.5, 35.3, velocity_y=1.7),
    point(25.1, 45.1, mass=500),
]


many_bodies = []

for _ in range(50):
    x = random.randint(200,1700)
    y = random.randint(200,900)
    many_bodies.append(point(x, y))


points = many_bodies

ticks = 0
starttime = time.time()
calctime = 0
beginframe = time.time()

toclear = []

while True:
    calctime = time.time() - beginframe
#    if not(calctime > 1/FPS):
#        time.sleep((1/FPS) - calctime)

    beginframe = time.time()
    points = step(points)
    ticks += 1

    img = Image.new("RGB", (1920, 1080))
    px = img.load()

    for item in points:
        px[item.x, item.y] = (255,255,255)

    img.save("gravity-{:05d}.png".format(ticks))

    print("ticks: {}".format(ticks))

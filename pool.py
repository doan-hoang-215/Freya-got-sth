import pygame
import random
import numpy 
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('POOL')

back = pygame.image.load('back.jpg')

mouse_pos = pygame.mouse.get_pos()

ENVIRONMENT = [20, 0, 0]

FPS = 72

class Boid:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('boid_idle.png').convert_alpha()
        self.frame = 4
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 48
        self.height = 48
        self.size = 1
        self.center = self.pos + (24, 24)
        self.old = 0
        self.sick = random.choice([0.01, 0.1, 1])

Boids = [Boid(numpy.array([random.randint(200, 1100), random.randint(100, 500)], dtype = numpy.float64), 
              numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64)) for _ in range(15)]
           
class Turtle:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('turtle_idle.png').convert_alpha()
        self.frame = 6
        self.hungry = 100
        self.health = 200
        self.vision = 100
        self.width = 48
        self.height = 48
        self.size = 2
        self.center = self.pos + (48, 48)
        self.old = 0
        self.sick = random.choice([0.01, 0.1, 1])
    
Turtles = [Turtle(numpy.array([random.randint(200, 1100), random.randint(100, 500)], dtype = numpy.float64), 
                  numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64))]
Turtle_foods = []

class Shark:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('shark_idle.png').convert_alpha()
        self.frame = 8
        self.hungry = 100
        self.health = 200
        self.vision = 100
        self.width = 32
        self.height = 32
        self.size = 3
        self.v = 1
        self.center = self.pos + (48, 48)
        self.old = 3
        self.sick = random.choice([0.01, 0.1, 1])

Sharks = [Shark(numpy.array([random.randint(200, 1100), random.randint(100, 500)], dtype = numpy.float64), 
              numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64))]
target = [Boids[0]]
       
class Weed:
    def __init__(self, pos):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.image = random.choice([pygame.image.load('weed0.png').convert_alpha(),
                                   pygame.image.load('weed1.png').convert_alpha(),
                                   pygame.image.load('weed2.png').convert_alpha(),
                                   pygame.image.load('weed3.png').convert_alpha(),
                                   pygame.image.load('weed4.png').convert_alpha(),
                                   pygame.image.load('weed5.png').convert_alpha(),
                                   pygame.image.load('weed6.png').convert_alpha(),
                                   pygame.image.load('weed7.png').convert_alpha()])
        self.frame = 12
        self.health = 200
        self.width = 16
        self.height = 32
        self.size = 3
        self.old = 0
        self.center = self.pos + (24, 48)
    
Weeds = [Weed(numpy.array([random.randint(0, WIDTH - 50), random.randint(HEIGHT + 4, HEIGHT + 10)], dtype = numpy.float64))]

class Squid:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('squid_idle.png').convert_alpha()
        self.frame = 4
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 32 
        self.height = 16
        self.size = 2
        self.center = self.pos + (32, 16)
        self.old = 0
        self.sick = random.choice([0.01, 0.1, 1])
        
Squids = [Squid(numpy.array([random.randint(200, 1100), random.randint(100, 500)], dtype = numpy.float64), 
              numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64))]

class Crab:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('crab_idle.png').convert_alpha()
        self.frame = 4
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 32
        self.height = 9
        self.size = 2
        self.center = self.pos + (32, 4)
        self.change = 500
        self.old = 0
        self.sick = random.choice([0.01, 0.1, 1])
        
Crabs = [Crab(numpy.array([random.randint(200, 1100), 680], dtype = numpy.float64), 
              numpy.array([random.choice([-1, 1]), 0], dtype = numpy.float64))]

class Bubble:
    def __init__(self, pos):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.image = pygame.image.load('bubble.png').convert_alpha()
        self.frame = 10
        self.width = 8
        self.height = 8
        self.size = 2
        self.center = self.pos + (8, 8)
        self.visible = False

class Coral():
    def __init__(self, pos):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.image = random.choice([pygame.image.load('coral0_idle.png').convert_alpha(),
                                    pygame.image.load('coral1_idle.png').convert_alpha(),
                                    pygame.image.load('coral2_idle.png').convert_alpha()])
        if self.image == pygame.image.load('coral0_idle.png').convert_alpha():
            self.bb = True
        else:
            self.bb = False
        self.frame = 4
        self.width = 32
        self.height = 32
        self.size = 1
        self.center = self.pos + (16, 16)
        self.visible = False

Corals = []
for i in range(0, 7):
    for j in range(14, 19):
        Corals.append(Coral(numpy.array([i * 35 + (j % 2 * 16) + random.randrange(0, 15), j * 35 + random.randrange(0, 15)], dtype = numpy.float64)))
num_coral = 0
        
class Nemo:
    def __init__(self, pos, vel, coral_target=None):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('nemo_idle.png').convert_alpha()
        self.frame = 8
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 32
        self.height = 16
        self.size = 1
        self.old = 3
        self.sick = random.choice([0.01, 0.1, 1])
        self.center = self.pos + (16, 8)
        self.coral_target = coral_target
        self.in_coral = False 
        
Nemos = []

class Jellyfish:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('jellyfish_idle.png').convert_alpha()
        self.frame = 4
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 32
        self.height = 16
        self.size = 1
        self.center = self.pos + (16, 8)
        self.old = 3
        self.sick = random.choice([0.01, 0.1, 1])

Jellyfishs = []

class Angle:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('anglerfish_idle.png').convert_alpha()
        self.frame = 6
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 48
        self.height = 48
        self.size = 1
        self.center = self.pos + (24, 24)
        self.old = 0
        self.sick = random.choice([0.01, 0.1, 1])

Angles = [Angle(numpy.array([random.randint(200, 1100), random.randint(500, 650)], dtype = numpy.float64), 
              numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64))]

class Octu:
    def __init__(self, pos, vel):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.vel = numpy.array(vel, dtype = numpy.float64)
        self.image = pygame.image.load('octopus_idle.png').convert_alpha()
        self.frame = 6
        self.hungry = 100
        self.health = 100
        self.vision = 100
        self.width = 48
        self.height = 48
        self.size = 1
        self.center = self.pos + (24, 24)
        self.old = 0
        self.sick = random.choice([0.01, 0.1, 1])

Octus = [Octu(numpy.array([random.randint(1000, 1150), random.randint(50, 650)], dtype = numpy.float64), 
              numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64))]

class Shell:
    def __init__(self, pos):
        self.pos = numpy.array(pos, dtype = numpy.float64)
        self.image = random.choice([pygame.image.load('shell0_idle.png').convert_alpha(), 
                                    pygame.image.load('shell1_idle.png').convert_alpha(),
                                    pygame.image.load('shell2_idle.png').convert_alpha(),
                                    pygame.image.load('shell3_idle.png').convert_alpha(),
                                    pygame.image.load('shell4_idle.png').convert_alpha(),
                                    pygame.image.load('shell5_idle.png').convert_alpha(),
                                    pygame.image.load('shell6_idle.png').convert_alpha(), 
                                    pygame.image.load('shell7_idle.png').convert_alpha(),
                                    pygame.image.load('shell8_idle.png').convert_alpha(),
                                    pygame.image.load('shell9_idle.png').convert_alpha(),
                                    pygame.image.load('shell10_idle.png').convert_alpha(),
                                    pygame.image.load('shell11_idle.png').convert_alpha(),
                                    pygame.image.load('shell12_idle.png').convert_alpha(), 
                                    pygame.image.load('shell13_idle.png').convert_alpha(),
                                    pygame.image.load('shell14_idle.png').convert_alpha(),
                                    pygame.image.load('shell15_idle.png').convert_alpha(),
                                    pygame.image.load('shell16_idle.png').convert_alpha(),
                                    pygame.image.load('shell17_idle.png').convert_alpha(),
                                    pygame.image.load('shell18_idle.png').convert_alpha(), 
                                    pygame.image.load('shell19_idle.png').convert_alpha(),
                                    pygame.image.load('shell20_idle.png').convert_alpha(),
                                    pygame.image.load('shell21_idle.png').convert_alpha(),
                                    pygame.image.load('shell22_idle.png').convert_alpha(),
                                    pygame.image.load('shell23_idle.png').convert_alpha(),
                                    pygame.image.load('shell24_idle.png').convert_alpha(),
                                    pygame.image.load('shell25_idle.png').convert_alpha(), 
                                    pygame.image.load('shell26_idle.png').convert_alpha(),
                                    pygame.image.load('shell27_idle.png').convert_alpha(),
                                    pygame.image.load('shell28_idle.png').convert_alpha(),
                                    pygame.image.load('shell29_idle.png').convert_alpha()])
        self.width = 16
        self.height = 16
        self.size = 2
        self.angle = random.randint(0, 360)
        self.center = self.pos + (16, 16)

Shells = []

def get_frame(sheet, frame, width, height):
    rect = pygame.Rect(frame * width, 0, width, height)
    return sheet.subsurface(rect)
def born():
    for boid1 in Boids:
        near = 0
        for boid2 in Boids:
            distance = numpy.linalg.norm(boid2.center - boid1.center)
            if distance <= boid1.vision and boid2 is not boid1:
                near += 1
        if near > 0 and random.randint(0, 10) == 3:
            new_pos = boid1.pos + numpy.random.rand(2) * 10  
            new_vel = numpy.array([random.uniform(-1, 1), random.uniform(-1, 1)]) * random.random()
            if boid1.old >= 3:
                Boids.append(Boid(new_pos, new_vel))
def rotation(x, time):
    image = get_frame(x.image, time // (FPS // x.frame), x.width, x.height)
    angle = math.degrees(math.atan2(-x.vel[1], x.vel[0]))
    tmp = image
    if x.vel[0] < 0:
        tmp = pygame.transform.flip(image, False, True)
    if x.old == 0:
        rotated_image = pygame.transform.rotozoom(tmp, angle, x.size / 2)
    elif x.old == 1:
        rotated_image = pygame.transform.rotozoom(tmp, angle, x.size / 1.8)
    elif x.old == 2:
        rotated_image = pygame.transform.rotozoom(tmp, angle, x.size / 1.6)
    elif x.old == 3:
        rotated_image = pygame.transform.rotozoom(tmp, angle, x.size / 1.4)
    elif x.old == 4:
        rotated_image = pygame.transform.rotozoom(tmp, angle, x.size / 1.2)
    else:
        rotated_image = pygame.transform.rotozoom(tmp, angle, x.size)
    WIN.blit(rotated_image, x.pos)

def cohesion(x):
    center = numpy.array([0.0, 0.0], dtype = numpy.float64)
    num_cen = 0
    for boid in Boids:
        if numpy.linalg.norm(boid.center - x.center) <= x.vision * 0.95 and boid is not x:
            num_cen += 1
            center += boid.center
    if num_cen > 0:
        center = center / num_cen
        direction = center - x.center
        x.vel += direction / numpy.linalg.norm(direction) * 0.05
def separation(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7 and boid is not x:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - turtle.center) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for angle in Angles:
        distance = numpy.linalg.norm(angle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - angle.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        if numpy.linalg.norm(total) > 0:
            x.vel += total / numpy.linalg.norm(total) * 0.1  
def alignment(x):
    sum_vel = numpy.array([0.0, 0.0])
    num = 0
    for boid in Boids:
        if numpy.linalg.norm(boid.center - x.center) <= x.vision and boid is not x:
            num += 1
            sum_vel += boid.vel
    if num > 0:
        avg_vel = sum_vel / num
        norm = numpy.linalg.norm(avg_vel)
        if norm > 0: 
            avg_vel = avg_vel / norm
            x.vel += avg_vel * 0.05

def tur_move(x):
    max_distance = 1000000
    for turtle_food in Turtle_foods:
        if max_distance > numpy.linalg.norm(turtle_food - x.center):
            if turtle_food[1] < 600:
                max_distance = numpy.linalg.norm(turtle_food - x.center)
                near = turtle_food

    for turtle_food in Turtle_foods:
        if numpy.linalg.norm(turtle_food - x.center) <= 15:
            Turtle_foods.remove(turtle_food)
            x.hungry += random.choice([25, 30, 35])
            if x.hungry > 100:
                x.hungry = 100

    if max_distance != 1000000:
        direction = near - x.center
        if x.hungry < 80:
            x.vel += direction / numpy.linalg.norm(direction)

  
    norm_vel = numpy.linalg.norm(x.vel)
    if norm_vel > 0:
        x.vel = x.vel / (norm_vel * 0.7)
def shark_move(x, y):
    if x.hungry < 50:
        y.image = pygame.image.load('boid_be_hunted.png').convert_alpha()
        x.v = 2
        direction = y.center - (x.center)
        x.vel += direction / numpy.linalg.norm(direction) * 0.2 
        if numpy.linalg.norm(y.center - x.center) < 50:
            x.hungry += 50
            if len(Boids) > 0:
                Boids.remove(Boids[0])
            if len(Boids) > 0:
                target.append(Boids[0])
            if len(target) > 0:
                target.remove(target[0])
    else:
        x.image = pygame.image.load('shark_idle.png').convert_alpha()
        x.v = 1
    norm_vel = numpy.linalg.norm(x.vel)
    if norm_vel > 0:
        x.vel = x.vel / norm_vel
def angle_hunt(x, y):
    direction = x.center - y.center
    y.vel += direction / numpy.linalg.norm(direction)
  
    norm_vel = numpy.linalg.norm(y.vel)
    if norm_vel > 0:
        y.vel = y.vel / (norm_vel * 0.7)

    if numpy.linalg.norm(x.center - y.center) <= 30:
        Boids.remove(y)
        x.hungry += random.choice([25, 30, 35])
        if x.hungry > 100:
            x.hungry = 100

def separation_squid(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7 and turtle:
            num_vec += 1
            total += (x.center - turtle.center) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7 and squid is not x:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for angle in Angles:
        distance = numpy.linalg.norm(angle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - angle.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.01 
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = (x.vel / numpy.linalg.norm(x.vel)) 
    x.pos += x.vel * 0.9
def separation_turtle(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7 and turtle is not x:
            num_vec += 1
            total += (x.center - turtle.center) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for angle in Angles:
        distance = numpy.linalg.norm(angle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - angle.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.01
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = (x.vel / numpy.linalg.norm(x.vel)) 
    x.pos += x.vel
def separation_shark(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.pos - turtle.pos) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7 and shark is not x:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for angle in Angles:
        distance = numpy.linalg.norm(angle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - angle.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.01
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = (x.vel / numpy.linalg.norm(x.vel)) 
def separation_nemo(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - turtle.center) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and nemo is not x:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for angle in Angles:
        distance = numpy.linalg.norm(angle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - angle.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.05
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = x.vel / numpy.linalg.norm(x.vel)
    x.pos += x.vel * 0.9
def separation_angle(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7 and turtle:
            num_vec += 1
            total += (x.center - turtle.center) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for angle in Angles:
        distance = numpy.linalg.norm(angle.center - x.center)
        if distance <= x.vision * 0.7 and angle is not x:
            num_vec += 1
            total += (x.center - angle.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.01 
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = (x.vel / numpy.linalg.norm(x.vel)) 
    x.pos += x.vel * 0.9
def separation_jelly(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.pos - turtle.pos) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for jelly in Jellyfishs:
        distance = numpy.linalg.norm(jelly.center - x.center)
        if distance <= x.vision * 0.7 and jelly is not x:
            num_vec += 1
            total += (x.center - jelly.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.01
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = (x.vel / numpy.linalg.norm(x.vel)) 
def separation_octu(x):
    total = numpy.array([0.0, 0.0])
    num_vec = 0
    for boid in Boids:
        distance = numpy.linalg.norm(boid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - boid.center) / distance
    for turtle in Turtles:
        distance = numpy.linalg.norm(turtle.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.pos - turtle.pos) / distance
    for shark in Sharks:
        distance = numpy.linalg.norm(shark.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - shark.center) / distance
    for squid in Squids:
        distance = numpy.linalg.norm(squid.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - squid.center) / distance
    for crab in Crabs:
        distance = numpy.linalg.norm(crab.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - crab.center) / distance
    for nemo in Nemos:
        distance = numpy.linalg.norm(nemo.center - x.center)
        if distance <= x.vision * 0.7 and not nemo.in_coral:
            num_vec += 1
            total += (x.center - nemo.center) / distance
    for jelly in Jellyfishs:
        distance = numpy.linalg.norm(jelly.center - x.center)
        if distance <= x.vision * 0.7:
            num_vec += 1
            total += (x.center - jelly.center) / distance
    for octu in Octus:
        distance = numpy.linalg.norm(octu.center - x.center)
        if distance <= x.vision * 0.7 and octu is not x:
            num_vec += 1
            total += (x.center - octu.center) / distance
    if num_vec > 0:
        total = total / num_vec
        x.vel += total / numpy.linalg.norm(total) * 0.01
    if numpy.linalg.norm(x.vel) > 1:
        x.vel = (x.vel / numpy.linalg.norm(x.vel)) 

def keep_within_bounds(x):
    if x.pos[0] <= 0:
        x.pos[0] = 10
        x.vel[0] = abs(x.vel[0]) 
    elif x.pos[0] + (x.width * x.size) >= WIDTH:
        x.pos[0] = WIDTH - (x.width * x.size)
        x.vel[0] = -abs(x.vel[0]) 

    if x.pos[1] <= 0:
        x.pos[1] = 0
        x.vel[1] = abs(x.vel[1]) 
    elif x.pos[1] + (x.height * x.size) >= HEIGHT:
        x.pos[1] = HEIGHT - (x.height * x.size)
        x.vel[1] = -abs(x.vel[1])
def keep_within_jelly(x):
    if x.pos[0] <= 0:
        x.pos[0] = 10
        x.vel[0] = abs(x.vel[0]) 
    elif x.pos[0] + (x.width * x.size) >= WIDTH:
        x.pos[0] = WIDTH - (x.width * x.size)
        x.vel[0] = -abs(x.vel[0]) 

    if x.pos[1] <= 0:
        x.pos[1] = 0
        x.vel[1] = abs(x.vel[1]) 
    elif x.pos[1] + (x.height * x.size) >= 200:
        x.pos[1] = 200 - (x.height * x.size)
        x.vel[1] = -abs(x.vel[1])
    x.pos += x.vel
def keep_within_angle(x):
    if x.pos[0] <= 0:
        x.pos[0] = 10
        x.vel[0] = abs(x.vel[0]) 
    elif x.pos[0] + (x.width * x.size) >= WIDTH:
        x.pos[0] = WIDTH - (x.width * x.size)
        x.vel[0] = -abs(x.vel[0]) 

    if x.pos[1] <= 500:
        x.pos[1] = 500
        x.vel[1] = abs(x.vel[1]) 
    elif x.pos[1] + (x.height * x.size) >= HEIGHT:
        x.pos[1] = HEIGHT - (x.height * x.size)
        x.vel[1] = -abs(x.vel[1])
    x.pos += x.vel
def keep_within_octu(x):
    if x.pos[0] <= 1000:
        x.pos[0] = 1000
        x.vel[0] = abs(x.vel[0]) 
    elif x.pos[0] + (x.width * x.size) >= WIDTH:
        x.pos[0] = WIDTH - (x.width * x.size)
        x.vel[0] = -abs(x.vel[0]) 

    if x.pos[1] <= 10:
        x.pos[1] = 10
        x.vel[1] = abs(x.vel[1]) 
    elif x.pos[1] + (x.height * x.size) >= HEIGHT:
        x.pos[1] = HEIGHT - (x.height * x.size)
        x.vel[1] = -abs(x.vel[1])
    x.pos += x.vel

def check_if_in_coral(nemo):
    coral = nemo.coral_target
    distance_to_coral = numpy.linalg.norm(coral.center - nemo.center)
    
    if distance_to_coral < 150:  
        nemo.in_coral = True
    else:
        nemo.in_coral = False
def spawn_nemo():
    available_corals = [coral for coral in Corals if coral.visible]  
    
    if available_corals: 
        coral_target = random.choice(available_corals) 
        new_nemo = Nemo(numpy.array([random.randint(50, 300), random.randint(400, 650)], dtype = numpy.float64),
                        numpy.array([random.randint(-1, 1) * random.random(), random.randint(-1, 1) * random.random()], dtype = numpy.float64),
                        coral_target=coral_target) 
        
        Nemos.append(new_nemo)
        available_corals.remove(coral_target)
def stay_near_assigned_coral(nemo):
    min_distance = 150 
    
    if nemo.coral_target: 
        coral = nemo.coral_target
        distance = numpy.linalg.norm(coral.center - nemo.center)
        
        if distance > min_distance:
            direction_to_coral = coral.center - nemo.center
            direction_to_coral = direction_to_coral / numpy.linalg.norm(direction_to_coral)
            nemo.vel += direction_to_coral * 0.05
def escape_to_coral(nemo):
    danger_distance = 150 
    nearest_coral = None
    min_dist_to_coral = float('inf')
    
    for coral in Corals:
        if coral.visible:
            dist_to_coral = numpy.linalg.norm(coral.center - nemo.center)
            if dist_to_coral < min_dist_to_coral:
                min_dist_to_coral = dist_to_coral
                nearest_coral = coral
    
    danger_nearby = False
    for turtle in Turtles:
        if numpy.linalg.norm(turtle.center - nemo.center) < danger_distance:
            danger_nearby = True
            break
    for boid in Boids:
        if numpy.linalg.norm(boid.center - nemo.center) < danger_distance:
            danger_nearby = True
            break
    for shark in Sharks:
        if numpy.linalg.norm(shark.center - nemo.center) < danger_distance:
            danger_nearby = True
            break
    for squid in Squids:
        if numpy.linalg.norm(squid.center - nemo.center) < danger_distance:
            danger_nearby = True
            break
    for angle in Angles:
        if numpy.linalg.norm(angle.center - nemo.center) < danger_distance:
            danger_nearby = True
            break
    
    if danger_nearby and nearest_coral:
        direction_to_coral = nearest_coral.center - nemo.center
        direction_to_coral = direction_to_coral / numpy.linalg.norm(direction_to_coral)
        nemo.vel += direction_to_coral * 0.1

def Weeding(time):
    if 20 < ENVIRONMENT[0] < 30:
        if len(Weeds) < 30:
            if random.randrange(0, 1000) == 1:
                Weeds.append(Weed(numpy.array([random.randint(0, WIDTH - 50), random.randint(HEIGHT + 4, HEIGHT + 10)], dtype = numpy.float64)))
    for weed in Weeds:
        if ENVIRONMENT[0] < 10:
            weed.health -= 1
        image = get_frame(weed.image, time // (FPS // weed.frame), weed.width, weed.height)
        rotated_image = pygame.transform.rotozoom(image, 0, weed.size)
        if weed.old < weed.height * weed.size:
            weed.old += 0.1
        WIN.blit(rotated_image, weed.pos - (0, weed.old))
        if weed.health < 0:
            Weeds.remove(weed)
def Coral_reef(time):
    global num_coral
    
    if 20 < ENVIRONMENT[0] < 30:
        if random.randrange(0, 1000) == 1:
            if num_coral < 16:
                coral = random.choice(Corals)
                coral.visible = True
                num_coral += 1
                if num_coral == 3 or num_coral == 5 or num_coral == 7:
                    spawn_nemo()
                    
    for coral in Corals:
        if coral.visible == True:
            image = get_frame(coral.image, time // (FPS // coral.frame), coral.width, coral.height)
            rotated_image = pygame.transform.rotozoom(image, 0, coral.size)
            WIN.blit(rotated_image, coral.pos)
            if ENVIRONMENT[0] < 10 or ENVIRONMENT[0] > 35:
                coral.visible = False
                num_coral -= 1 
        
        if coral.visible == True and numpy.array_equal(pygame.surfarray.pixels3d(coral.image), pygame.surfarray.pixels3d(pygame.image.load('coral0_idle.png').convert_alpha())):
            if 0 <= time <= 59:
                Bubbles = Bubble(numpy.array(coral.pos + (4, -4), dtype = numpy.float64))
                image = get_frame(Bubbles.image, time // (FPS // Bubbles.frame), Bubbles.width, Bubbles.height)
                rotated_image = pygame.transform.rotozoom(image, 0, Bubbles.size)
                WIN.blit(rotated_image, Bubbles.pos - (0, time))

def population_density():
    if ENVIRONMENT[2] > 25:
            choise1, choise2, choise3, choise = None, None, None, None
            if len(Boids) > 5:
                choise1 = random.choice(Boids)
            if len(Turtles) > 5:
                choise2 = random.choice(Turtles)
            if len(Crabs) > 3:
                choise3 = random.choice(Crabs)
            if choise1 != None or choise2 != None or choise3 != None:
                while choise == None:
                    choise = random.choice([choise1, choise2, choise3])
                choise.health -= 10
def age(x):
    for self in x:
        self.old += 1
def heal(x):
    if x.hungry > 95:
        x.health += 1
        if x.health > 100:
            x.health = 100
def infor(hour, days, temp, ENVI):
    font = pygame.font.SysFont('sans', 20)
    time = font.render('Hour : ' + str(hour), True, 'black')
    time_day = font.render('Day : ' + str(days), True, 'black')
    en0 = font.render('Temperature : ' + str(round(temp)), True, 'black')
    en1 = font.render('Pollution : ' + str(ENVI[1]), True, 'black')
    en2 = font.render('Density : ' + str(ENVI[2]), True, 'black')
    if hour // 16 == 0:
        dn1 = font.render('DAY', True, 'red')
        dn2 = font.render('NIGHT', True, 'black')
    else:
        dn1 = font.render('DAY', True, 'black')
        dn2 = font.render('NIGHT', True, 'red')
    transparent_surface = pygame.Surface((1200, 600), pygame.SRCALPHA)
    alpha_value = 200
    color_with_alpha = (255, 255, 255, alpha_value)
    pygame.draw.rect(transparent_surface, color_with_alpha, pygame.Rect(100, 100, 1000, 500))
    WIN.blit(transparent_surface, (0, 0))
    WIN.blit(time, (200, 150))
    WIN.blit(time_day, (200, 220))
    WIN.blit(en0, (200, 290))
    WIN.blit(en1, (200, 360))
    WIN.blit(en2, (200, 430))
    WIN.blit(dn1, (200, 500))
    WIN.blit(dn2, (250, 500))
def shell():
    for s in Shells:
        rotated_image = pygame.transform.rotozoom(s.image, s.angle, s.size)
        WIN.blit(rotated_image, s.pos)

def main():
    run = True
    clock = pygame.time.Clock()
    time = 0
    hour = 0
    days = 0
    day_temp = 5
    inf_win = False
    count_food = 30
    spawn_nemo()

    while run:
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(FPS)
        if count_food > 0:
            count_food -= 1
        time += 1
        temp = ENVIRONMENT[0] + day_temp - (len(Weeds) // 5) + (len(Turtle_foods) // 5)
        if len(Boids) > 0:
            target = [Boids[0]]
        if len(Boids) < 5:
            if random.randint(0, 120) == 1:
                born()
        else:
            if random.randint(0, 1200) == 1:
                born()
        ENVIRONMENT[1] = len(Turtle_foods)
        ENVIRONMENT[2] = len(Boids) + len(Sharks) + len(Turtles) + len(Squids) + len(Crabs) + len(Nemos) + len(Jellyfishs)
        population_density()
        
        WIN.blit(back, (0, 0))
        
        if time >= FPS:
            time = 0
            hour += 1
            if hour // 14 < 1:
                day_temp = 5
                if temp > 26:
                    if random.randint(0, 10) == 1:
                        Jellyfishs.append(Jellyfish(numpy.array([random.randint(0, 1200), random.randint(10, 200)], dtype = numpy.float64),
                                                    numpy.array([random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], dtype = numpy.float64)))
            else:
                day_temp = -5
            if 23 < hour:
                hour = 0   
                days += 1 
                age(Boids)
                age(Turtles)
                age(Squids)
                age(Sharks)
                age(Octus)
                age(Angles)
                age(Crabs)
                if len(Shells) < 10:
                    Shells.append(Shell(numpy.array(random.choice([[random.randint(10, 100), random.randint(50, 650)], 
                                                                  [random.randint(1000, 1150), random.randint(50, 650)]]), dtype = numpy.float64)))
                if len(Turtles) == 0:
                    Turtles.append(Turtle(numpy.array([Squids[0].pos[0] + 10, Squids[0].pos[1] + 10], dtype = numpy.float64), 
                                          numpy.array([random.randint(-1, 1) * random.random(), random.randint(-1, 1) * random.random()], dtype = numpy.float64)))
            ENVIRONMENT[0] = ENVIRONMENT[0] + random.uniform(-0.2, 0.2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if count_food == 0:
                        Turtle_foods.append(mouse_pos)
                        count_food = 30
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if inf_win == True:
                        inf_win = False
                    else:
                        inf_win = True
        
        shell()
        
        for jelly in Jellyfishs:
            if temp < 22:
                jelly.health -= jelly.sick
            if jelly.health < 0:
                Jellyfishs.remove(jelly)
                pass
            elif jelly.health < 20:
                jelly.image = pygame.image.load('jellyfish_death.png')
            else:
                jelly.image = pygame.image.load('jellyfish_idle.png')
            separation_jelly(jelly)
            keep_within_jelly(jelly)
            rotation(jelly, time)
            jelly.center = jelly.pos + (16, 8)
        
        for nemo in Nemos:
            check_if_in_coral(nemo)
            if temp < 10 or temp > 40:
                nemo.health -= nemo.sick
            if nemo.health < 0:
                Nemos.remove(nemo)
                break
            separation_nemo(nemo)
            stay_near_assigned_coral(nemo)
            escape_to_coral(nemo)
            keep_within_bounds(nemo)
            rotation(nemo, time)
            nemo.center = nemo.pos + (16, 8)
        
        Coral_reef(time)
            
        for boid in Boids:
            if temp < 10 or temp > 40:
                boid.health -= boid.sick
            if ENVIRONMENT[1] > 20:
                boid.health -= boid.sick
            if boid.health <= 0 or boid.hungry <= 0:
                Boids.remove(boid)
                break
            cohesion(boid)
            alignment(boid)
            separation(boid)
            norm = numpy.linalg.norm(boid.vel)
            if norm > 0:
                boid.vel = boid.vel / norm
            boid.pos += boid.vel
            keep_within_bounds(boid)
            rotation(boid, time)
            boid.center = boid.pos + (24, 24)
            
        for turtle in Turtles:
            if temp < 10 or temp > 40:
                turtle.health -= turtle.sick
            turtle.hungry -= random.choice([0.01, 0.02, 0.03, 0.04, 0.05])
            heal(turtle)
            if turtle.health < 0:
                Turtles.remove(turtle)
                break
            tur_move(turtle)
            separation_turtle(turtle)
            keep_within_bounds(turtle)
            rotation(turtle, time)
            if turtle.hungry <= 0:
                Turtles.remove(turtle)
            elif turtle.hungry == 100:
                if turtle.old > 3:
                    Turtles.append(Turtle(numpy.array([turtle.pos[0] + 10, turtle.pos[1] + 10], dtype = numpy.float64), 
                                          numpy.array([random.randint(-1, 1) * random.random(), random.randint(-1, 1) * random.random()], dtype = numpy.float64)))
            if 0 < turtle.hungry < 15 or 0 < turtle.health < 15:
                turtle.image = pygame.image.load('turtle_death.png').convert_alpha()
            else:
                turtle.image = pygame.image.load('turtle_idle.png').convert_alpha()
            turtle.center = turtle.pos + (48, 48)
                
        for squid in Squids:
            if temp < 10 or temp > 40:
                squid.health -= squid.sick
            if squid.health < 0:
                Squids.remove(squid)
                break
            separation_squid(squid)
            keep_within_bounds(squid)
            rotation(squid, time)
            if squid.hungry <= 0:
                Squids.remove(squid)
                break
            squid.center = squid.pos + (32, 16)
            if random.randint(0, 600) == 1:
                Turtle_foods.append(squid.center)
        
        for octu in Octus:
            if temp < 10 or temp > 40:
                octu.health -= octu.sick
            if octu.health < 0:
                Octus.remove(octu)
                break
            if octu.hungry > 20:
                octu.hungry -= 0.01
                separation_octu(octu)
                keep_within_octu(octu)
                rotation(octu, time)
            else:
                octu.image = pygame.image.load('octopus_hunt.png')
                for boid in Boids:
                    if numpy.linalg.norm(boid.center - octu.center) < 48:
                        octu.hungry += 80
                        Boids.remove(boid)
                        octu.image = pygame.image.load('octopus_idle.png')
                        break
                rotation(octu, time)
            if octu.hungry <= 0:
                Octus.remove(octu)
                break
            octu.center = octu.pos + (24, 24)
                
        for shark in Sharks:
            if temp < 10 or temp > 40:
                shark.health -= shark.sick
            shark.hungry -= 0.01 * (len(Boids) // 5)
            heal(shark)
            if shark.hungry < 50:
                if len(target) > 0:
                    if shark.hungry < 10:
                        shark.image = pygame.image.load('shark_attack_death.png').convert_alpha()
                    else:
                        shark.image = pygame.image.load('shark_attack.png').convert_alpha()
                    separation_shark(shark)
                    shark_move(shark, target[0])
                else:
                    shark.image = pygame.image.load('shark_death.png').convert_alpha()
            else:
                shark_move(shark, shark)
                separation_shark(shark)    
            keep_within_bounds(shark) 
            shark.pos += shark.vel * shark.v
            rotation(shark, time)
            shark.center = shark.pos + (48, 48)
            if shark.hungry <= 0:
                Sharks.remove(shark)
                break
            if shark.health < 0:
                Sharks.remove(shark)
                break
            
        if ENVIRONMENT[1] > 15:
                if random.randint(0, 200) == 1:
                    if len(Crabs) < 5:
                        Crabs.append(Crab(numpy.array([random.randint(200, 1100), 680], dtype = numpy.float64), 
                                          numpy.array([random.choice([-1, 1]), 0], dtype = numpy.float64)))        
        for crab in Crabs:
            if temp < 10 or temp > 40:
                crab.health -= crab.sick
            if ENVIRONMENT[1] > 27:
                crab.health -= crab.sick
            crab.hungry -= 0.01
            heal(crab)
            for food in Turtle_foods:
                if numpy.linalg.norm(crab.center - food) <= crab.width / 2:
                    crab.hungry += 20
                    Turtle_foods.remove(food)
                    if crab.hungry > 100:
                        crab.hungry = 100
            rotation(crab, time)
            if day_temp == 5:
                if crab.pos[0] <= 0:
                    crab.pos[0] = 10
                    crab.vel[0] = abs(crab.vel[0]) 
                elif crab.pos[0] + (crab.width * crab.size) >= WIDTH:
                    crab.pos[0] = WIDTH - (crab.width * crab.size)
                    crab.vel[0] = -abs(crab.vel[0])
                if round(crab.pos[0]) == crab.change:
                    crab.vel[0] = -crab.vel[0]
                    crab.change = random.randint(100, 1000)
                crab.pos += crab.vel
                crab.center = crab.pos + (32, 4)
            if crab.health < 0:
                Crabs.remove(crab)
                break
            if crab.hungry < 0:
                Crabs.remove(crab)
                break  
            
        for angle in Angles:
            if temp < 5 or temp > 45:
                angle.health -= angle.sick
            if angle.health < 0:
                Angles.remove(angle)
                break
            if angle.hungry < 70:
                if day_temp == -5:
                    if len(Boids) > 2:
                        angle_hunt(angle, Boids[0])
                else:
                    separation_angle(angle)
                    keep_within_angle(angle)
            else:
                angle.hungry -= 0.01
                separation_angle(angle)
                keep_within_angle(angle)
            rotation(angle, time)
            if angle.hungry <= 0:
                Angles.remove(angle)
                break
            angle.center = angle.pos + (24, 24)
             
        Weeding(time)
        
        for i, turtle_food in enumerate(Turtle_foods):
            tmp = list(turtle_food)
            if tmp[1] < 680:
                tmp[1] += 0.5  
            Turtle_foods[i] = tuple(tmp) 
            pygame.draw.circle(WIN, 'brown', Turtle_foods[i], 5)
        
        if day_temp == -5:
            transparent_surface = pygame.Surface((1200, 700), pygame.SRCALPHA)
            alpha_value = 150
            color_with_alpha = (0, 0, 0, alpha_value)
            dele = (0, 0, 0, 0)
            pygame.draw.rect(transparent_surface, color_with_alpha, pygame.Rect(0, 0, 1200, 700))
            for angle in Angles:
                pygame.draw.circle(transparent_surface, dele, angle.center, 50)
            WIN.blit(transparent_surface, (0, 0))
        
        if inf_win:
            infor(hour, days, temp, ENVIRONMENT)
            
        pygame.display.update()
       
if __name__ == '__main__':
    main()
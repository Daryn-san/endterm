import pygame
import time
import random
from enum import Enum

pygame.init()
width = 800
height = 650
screen = pygame.display.set_mode((width, height))
wallImage=pygame.image.load('brick.png')
wall_range=50
font = pygame.font.SysFont('Arial', 40) 

pygame.mixer.music.load('megalovania.mp3')
pygame.mixer.music.play()

shotSound=pygame.mixer.Sound('shot.wav')
explosionSound=pygame.mixer.Sound('explosion.wav')

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:
    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN,d_pull=pygame.K_RETURN):
        self.x = x
        self.y = y
        self.life = 3
        self.speed = speed
        self.color = color
        self.width = 35
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}
        self.KEYPULL=d_pull
    def draw(self):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color, 
                         (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))
        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (
            self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)
    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        if self.y < 50:
            self.y = 600
        if self.y > 600:
            self.y = 50
        if self.x < 50:
            self.x = 750
        if self.x > 750:
            self.x = 50
        self.draw()

FPS = 30
clock = pygame.time.Clock()

class Shot:
    def __init__(self,x=0,y=0,color=(0,0,0),direction=Direction.LEFT,speed=12):
        self.x=x
        self.y=y
        self.color=color
        self.speed=speed
        self.direction=direction
        self.status=True
        self.distance=0
        self.radius = 5
        self.width = 10
    
    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.distance+=1
        if self.distance>(2*width):
            self.status=False
        self.draw()

    def draw(self):
        if self.status:
            pygame.draw.circle(screen, (255, 255, 255),
                         (self.x, self.y), self.radius)
    
def give_coordinates(tank):
    if tank.direction == Direction.RIGHT:
        x=tank.x + tank.width + int(tank.width / 2)
        y=tank.y + int(tank.width / 2)

    if tank.direction == Direction.LEFT:
        x=tank.x - int(tank.width / 2)
        y=tank.y + int(tank.width / 2)

    if tank.direction == Direction.UP:
        x=tank.x + int(tank.width / 2)
        y=tank.y - int(tank.width / 2)

    if tank.direction == Direction.DOWN:
        x=tank.x + int(tank.width / 2)
        y=tank.y + tank.width + int(tank.width / 2)

    p=Shot(x,y,tank.color,tank.direction)
    shot.append(p)

def collision():
    for tank in tanks:
        if (tank.x<wall_range):
            tank.x+=tank.speed
        elif tank.x>width-wall_range:
            tank.x-=tank.speed
        if (tank.y<wall_range):
            tank.y+=tank.speed
        elif tank.y>height-wall_range:
            tank.y-=tank.speed
    
    for p in shot:
        for tank in tanks:
            if (tank.x+tank.width+p.radius > p.x > tank.x - p.radius ) and ((tank.y+tank.width + p.radius > p.y > tank.y - p.radius)) and p.status==True:
                explosionSound.play()
                p.color=(0,0,0)
                tank.life -=1
                p.status=False
                
                tank.x=random.randint(50,width-70)
                tank.y=random.randint(50,height-70)

def life():
    life1=tanks[1].life
    life2=tanks[0].life
    res = font.render(str(life1), True, (255, 123, 100))
    res1 = font.render(str(life2), True, (100, 230, 40))
    screen.blit(res, (80,60))
    screen.blit(res1, (720,60))
    
def fill_edges():
    for i in range(width//wall_range):
        screen.blit(wallImage,(wall_range*i,0))
        screen.blit(wallImage,(wall_range*i,height-wall_range-10))

    for i in range(height//wall_range):
        screen.blit(wallImage,(0,i*wall_range))
        screen.blit(wallImage,(width-wall_range-10,i*wall_range))

mainloop = True
tank1 = Tank(300, 300, 7, (240, 240, 0))
tank2 = Tank(100, 100, 7, (200, 0, 200), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s,pygame.K_SPACE)

shot1=Shot()
shot2=Shot()

tanks = [tank1, tank2]
shot = [shot1, shot2]

while mainloop:
    mill = clock.tick(FPS)
    
    screen.fill((0, 0, 0))
    fill_edges()
    life()
    tank1.move()
    tank2.move()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                quit()
            pressed = pygame.key.get_pressed()
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])

                if event.key in tank.KEY.keys():
                    tank.move()
                
                if pressed[tank.KEYPULL]:
                    shotSound.play()
                    give_coordinates(tank)
    if tank1.life == 0 or tank2.life == 0:
    
        mainloop = False
                        

    collision()
    for p in shot:
        p.move()
    
    for tank in tanks:
        tank.draw() 
    fill_edges()
    pygame.display.flip()

pygame.quit()
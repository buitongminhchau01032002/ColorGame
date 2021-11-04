import pygame, sys, random
from pygame.locals import *
from math import sqrt


WINDOWWIDTH = 600 # Chiều dài cửa sổ
WINDOWHEIGHT = 600 # Chiều cao cửa sổ
CIRCLE_PLAYER_RADIUS = 10
ADD_CIRCLE_TIME = 1
EXIST_TIME = 80

CIRCLE_COLOR_RADIUS = 40
EXIST_CIRCLE_COLOR_TIME = 80
ADD_CIRCLECOLOR_TIME = 50

COLORLIST = ((255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 255), (255, 0, 191))

pygame.init()

### Xác định FPS ###
FPS = 120
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Circle Game')

MAINSURF = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), SRCALPHA)

def getColor(colorStart, colorEnd, alpha):
    # start + (end - start)*alpha
    return ( int(colorStart[0] + (colorEnd[0]-colorStart[0])*alpha) , int(colorStart[1] + (colorEnd[1]-colorStart[1])*alpha) , int(colorStart[2] + (colorEnd[2]-colorStart[2])*alpha))

class CirclePlayer():
    def __init__(self, x, y, colorStart, colorEnd):
        self.x = x
        self.y = y
        self.colorStart = colorStart
        self.colorEnd = colorEnd
        self.currentTime = 0
        self.existTime = EXIST_TIME
        self.radius = CIRCLE_PLAYER_RADIUS
        self.speedX = random.random()*random.choice([-1, 1])/3
        self.speedY = random.random()*random.choice([-1, 1])/3

    def draw(self):
        range_r = ((2*self.currentTime-self.existTime)/self.existTime)
        range_r += 0.25
        if range_r < 0:
            range_r *= -1
        range_r /= 2
        range_r = 1 - range_r # 0.5 -> 1 -> 0.5
        r = int(self.radius*range_r)

        range_a = ((2*self.currentTime-self.existTime)/self.existTime)
        range_a = (range_a+0.6)/1.6
        if range_a < 0:
            range_a *= -1
        range_a = 1-range_a # 0.75 -> 1 -> 0
        a = int(255*range_a)

        range_color = 1 - (self.existTime-self.currentTime)/self.existTime # 0 -> 1
        pygame.draw.circle(MAINSURF, (*getColor(self.colorStart, self.colorEnd, range_color), a), (self.x, self.y), r)

    def update(self):
        self.currentTime += 1
        self.x += self.speedX
        self.y += self.speedY

    def isExist(self):
        if (self.currentTime > self.existTime):
            return False
        return True

class Player():
    def __init__(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.currentTime = 0
        self.addCircleTime = ADD_CIRCLE_TIME
        self.listCircle = []
        self.colorStart = random.choice(COLORLIST)
        self.colorEnd = random.choice(COLORLIST)

    def draw(self):
        for circle in self.listCircle:
            circle.draw()
        

    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.currentTime += 1
        for circle in self.listCircle:
            circle.update()
        if (self.currentTime > self.addCircleTime):
            self.listCircle.append(CirclePlayer(self.x, self.y, self.colorStart, self.colorEnd))
            self.currentTime = 0
        if (len(self.listCircle) > 0 and not self.listCircle[0].isExist()):
            self.listCircle.pop(0)

class CircleOfCircleColor():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.currentTime = 0
        self.existTime = EXIST_TIME*2.5
        self.radius = CIRCLE_PLAYER_RADIUS*1.2
        self.speedX = random.random()*random.choice([-1, 1])/2.5
        self.speedY = random.random()*random.choice([-1, 1])/2.5
        self.explored = False

    def draw(self):
        range_r = ((2*self.currentTime-self.existTime)/self.existTime)
        range_r += 0.25
        if range_r < 0:
            range_r *= -1
        range_r /= 2
        range_r = 1 - range_r # 0.5 -> 1 -> 0.5
        r = int(self.radius*range_r)

        range_a = ((2*self.currentTime-self.existTime)/self.existTime)
        range_a = (range_a+0.6)/1.6
        if range_a < 0:
            range_a *= -1
        range_a = 1-range_a # 0.75 -> 1 -> 0
        a = int(255*range_a)

        pygame.draw.circle(MAINSURF, (*self.color, a), (self.x, self.y), r)

    def update(self, explored):
        self.currentTime += 1
        if self.explored == False:
            if explored:
                self.explored = explored
                self.speedX *= 4
                self.speedY *= 4

        self.x += self.speedX
        self.y += self.speedY

    def isExist(self):
        if (self.currentTime > self.existTime):
            return False
        return True


class CircleColor():
    def __init__(self, x, y, color, timeLife, player, score):
        self.x = x
        self.y = y
        self.color = color
        self.radius = CIRCLE_COLOR_RADIUS
        self.currentTime = 0
        self.addCircleTime = ADD_CIRCLE_TIME*3
        self.listCircle = []
        self.explored = False
        self.timeLife = timeLife

    def draw(self):
        for circle in self.listCircle:
            circle.draw()
    def update(self):
        for circle in self.listCircle:
            circle.update(self.explored)
        if not self.explored:
            if self.timeLife > 0:
                self.currentTime += 1
                self.timeLife -= 1
                if (self.currentTime > self.addCircleTime):
                    self.listCircle.append(CircleOfCircleColor(self.x, self.y, self.color))
                    self.currentTime = 0
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            if sqrt((self.x-mouseX)**2 + (self.y-mouseY)**2) < self.radius:
                self.explored = True
                player.colorEnd = player.colorStart
                player.colorStart = self.color
                score.value += 1


        if (len(self.listCircle) > 0 and not self.listCircle[0].isExist()):
            self.listCircle.pop(0)


    def isExist(self):
        if (self.timeLife <= 0 or self.explored) and len(self.listCircle) == 0:
            return False
        return True

class CircleColors():
    def __init__(self, player, score):
        self.ls = []
        self.addTime = ADD_CIRCLECOLOR_TIME
        self.currentTime = 0
        self.timeLife = EXIST_CIRCLE_COLOR_TIME
        self.isGameOver = False

    def draw(self):
        for circle in self.ls:
            circle.draw()

    def update(self):
        self.addTime -= 0.002
        self.timeLife -= 0.01

        if (self.addTime < 20):
            self.addTime = 20

        if (self.timeLife < 5):
            self.timeLife = 5

        for circle in self.ls:
            circle.update()
        self.currentTime += 1
        if (self.currentTime > self.addTime):
            x = random.randint(50, WINDOWWIDTH-50)
            y = random.randint(50, WINDOWHEIGHT-50)
            self.ls.append(CircleColor(x, y, random.choice(COLORLIST), self.timeLife, player, score))
            self.currentTime = 0

        for circle in self.ls:
            if not circle.isExist() and not circle.explored:
                self.isGameOver = True
        if (len(self.ls) > 0 and not self.ls[0].isExist()):
            self.ls.pop(0)

class Score():
    def __init__(self):
        self.value = 0
    def draw(self):
        font = pygame.font.SysFont('Calibri', 50)
        textSurface = font.render(str(self.value), True, (225, 225, 225, 200))
        MAINSURF.blit(textSurface, (int(WINDOWWIDTH/2 - textSurface.get_width()/2), 10))

while True:
    player = Player()
    score = Score()
    circleColors = CircleColors(player, score)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((0, 0, 0))
        MAINSURF.fill((0, 0, 0))

        

        circleColors.draw()
        circleColors.update()
        
        player.draw()
        player.update()
        score.draw()
        DISPLAYSURF.blit(MAINSURF, (0, 0))

        if (circleColors.isGameOver):
            break
        pygame.display.update()
        fpsClock.tick(FPS)

    font1 = pygame.font.SysFont('Calibri', 30)
    textSurface1 = font1.render("Click to replay", True, (225, 225, 225, 200))
    
    font2 = pygame.font.SysFont('Calibri', 80)
    textSurface2 = font2.render("GAME OVER", True, (225, 225, 225, 200))

    replay = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                replay = True

        if replay:
            break

        DISPLAYSURF.fill((0, 0, 0))
        MAINSURF.fill((0, 0, 0))

        score.draw()

        circleColors.draw()
        
        player.draw()
        MAINSURF.blit(textSurface1, (int(WINDOWWIDTH/2 - textSurface1.get_width()/2), WINDOWHEIGHT/2+100))
        MAINSURF.blit(textSurface2, (int(WINDOWWIDTH/2 - textSurface2.get_width()/2), WINDOWHEIGHT/2-80))
        DISPLAYSURF.blit(MAINSURF, (0, 0))
        pygame.display.update()
        fpsClock.tick(FPS)


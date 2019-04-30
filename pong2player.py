import pygame, time, random

pygame.init()

display_width = 1100
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Poncc')

clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red=(255,0,0)
yellow=(200,200,0)

choice = [True, False]

class segment():
    def __init__(self,x, y, width, height, color, speed = 10,left=False, right=False, up=False, down=False):
        self.color = color
        self.x = x
        self.startx = x
        self.x_old = 0
        self.y = y
        self.starty = y
        self.y_old = 0
        self.target = 0
        self.width = width
        self.height = height
        self.left = left
        self.up = up
        self.down = down
        self.right = right
        self.speed = speed
        self.start_speed = speed
        self.rivalHit = False
        self.playerHit = False
        self.score = 0
    
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])

    def move(self):
        if self.up and not (self.y < 0):
            self.y -= self.speed
        if self.down and not (self.y + self.height > display_height):
            self.y += self.speed
        if self.left:
            self.x -= self.speed
        if self.right:
            self.x += self.speed


def display_text(msg, size, color, x, y):
    font = pygame.font.SysFont('verdana', size)
    text = font.render(msg, True, color)
    gameDisplay.blit(text, [x,y])

def score(who):
    if who == 1:
        player.score += 1
    else:
        rival.score += 1
    gameLoop()

def gameLoop():
    ball.x = ball.startx 
    ball.y = ball.starty 
    player.x = player.startx 
    player.y = player.starty
    rival.x = rival.startx
    rival.y = rival.starty 
    ball.y_change = 5

    ball.up = False
    ball.down = choice[random.randint(0,1)]
    if not ball.down:
        ball.up = True
    ball.right = True 
    ball.left = False

    ball.speed = 10
    rival.speed = 10

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_UP:
                    rival.down = False
                    rival.up = True
                if event.key == pygame.K_DOWN:
                    rival.up = False
                    rival.down = True
                if event.key == pygame.K_w:
                    player.down = False
                    player.up = True
                if event.key == pygame.K_s:
                    player.up = False
                    player.down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rival.up = False
                if event.key == pygame.K_DOWN:
                    rival.down = False
                if event.key == pygame.K_w:
                    player.up = False
                if event.key == pygame.K_s:
                    player.down = False

        #Ball movement
        if ball.y < 0:
            ball.up = False
            ball.down = True

        if ball.y+ball.height > display_height:
            ball.down = False
            ball.up = True

        if ball.x < 0:
            ball.left = False
            ball.right = True
            score(0)
        if ball.x > display_width:
            ball.left = True
            ball.right = False
            score(1)

        ball.x_old = ball.x
        ball.y_old = ball.y

        ball.hit()
        ball.ball_movement()

        #Player movement
        player.move()        

        #Rival movement

        rival.move()
        gameDisplay.fill(black)
        player.draw()
        rival.draw()
        ball.draw()
        display_text(str(player.score),100, white, 50, 0)
        display_text(str(rival.score), 100, white, 700 ,0)
        display_text(str(ball.speed), 25, red, 100, 0)
        display_text(str(rival.speed), 25, blue, 150, 0)
        pygame.display.update()
        clock.tick(60)

player = segment(40,display_height/4, 20, 120, blue)
rival = segment(display_width-60, display_height/4, 20, 120,red, speed = 20)
ball = segment(display_width/2-50, display_height/2-50, 20, 20,yellow,speed =50, right = True)

def hit():
    if ball.x == rival.x:
        if (ball.y > rival.y and ball.y < rival.y + rival.height) or (ball.y+ball.height > rival.y and ball.y + ball.height < rival.y + rival.height): 
            ball.rivalHit = True

    if ball.x == player.x+player.width:
        if (ball.y > player.y and ball.y < player.y + player.height) or (ball.y+ball.height > player.y and ball.y + ball.height < player.y + player.height):
            ball.playerHit = True

def ball_movement():
    if ball.rivalHit:
        ball.right = False
        ball.left = True
        ball.diff = abs(ball.y - (rival.y+rival.height/2))
        ball.y_change = ball.diff/6

        if ball.y < rival.y + rival.height/2:
            ball.down = False
            ball.up = True
        else:
            ball.up = False
            ball.down = True

        ball.rivalHit = False

    if ball.playerHit:
        ball.left = False
        ball.right = True
        ball.diff = abs(ball.y - (player.y + player.height/2))
        ball.y_change = ball.diff/6

        if ball.y < player.y + player.height/2:
            ball.down = False
            ball.up = True
        else:
            ball.up = False
            ball.down = True

        ball.playerHit = False
    
    if ball.right:
        ball.left = False
        ball.x += ball.speed
    if ball.left:
        ball.right = False
        ball.x -= ball.speed
    

    if ball.up:
        ball.down = False
        ball.y -= ball.y_change
    if ball.down:
        ball.up = False
        ball.y += ball.y_change

ball.y_change = 5
ball.hit = hit
ball.ball_movement = ball_movement

gameLoop()

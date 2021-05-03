#very beginning -what do we need to get started
import pygame
import random

pygame.init()


#define some simple variables to use later
FPS = 60

screen_width = 600
screen_height = 800

score = 0
lives = 3
retries = 3
difficulty = 0
level = 1
pause = True

BRICKS_PER_ROW = 10
NUM_ROWS = 5
BLANK_ROWS = 2


#define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (232, 92, 180)
BLUE = (92, 116, 232)
PURPLE = (181, 58, 209)
RED = (255, 0, 0)
LIGHTPURPLE = (216, 148, 255)
DARKPURPLE = (116, 33, 163)
LIGHTPINK = (255, 143, 242)
BABYBLUE = (143, 171, 255)


#define some simple functions
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))

screen_rect = screen.get_rect()


#define how to put text on screen
def draw_text(surface, text, pos=(0, 0), color=DARKPURPLE, font_size=20, anchor="topleft"):
    arial = pygame.font.match_font("arial")
    font = pygame.font.Font(arial, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, anchor, pos)
    surface.blit(text_surface, text_rect)


#BALL start
class Ball(pygame.sprite.Sprite):
    #ball initializes itself
    def __init__(self):
        super().__init__()
        ball_image = pygame.image.load("pika.png").convert_alpha()
        self.image = pygame.transform.scale(ball_image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset()

    #ball updates itself
    def update(self):
        #bounces off of walls
        if self.rect.right >= screen_rect.right:
            self.x_speed = -5
        if self.rect.left <= screen_rect.left:
            self.x_speed = 5
        if self.rect.top <= screen_rect.top:
            self.y_speed = 5
        if self.rect.bottom >= screen_rect.bottom:
            self.y_speed = -5
            self.lost = True
            
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
    
    #ball resets itself
    def reset(self):
        self.rect.center = screen_rect.center
        #self.x_speed = 5
        self.y_speed = 5
        self.x_speed = random.choice((5, -5))
        self.lost = False

#BALL end


#PADDLE start
class Paddle(pygame.sprite.Sprite):
    #paddle exists
    def __init__(self):
        super().__init__()
        paddle_image = pygame.image.load("paddle.png").convert_alpha()
        self.image = pygame.transform.scale(paddle_image, (100, 15))
        self.rect = self.image.get_rect()
        self.rect.center = screen_rect.center
        self.rect.bottom = screen_rect.bottom - 10
    
    #therefore it is
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if self.rect.right >= screen_rect.right:
            self.rect.right = screen_rect.right
        if self.rect.left <= screen_rect.left:
            self.rect.left = screen_rect.left
            
#PADDLE end

#BRICK class start
class Brick(pygame.sprite.Sprite):
    #brick exists, not by itself though
    def __init__(self, row, col):
        super().__init__()
        brick_image = pygame.image.load("brick.png").convert_alpha()
        
        #calculate size of bricks
        brick_width = round(screen_rect.width / BRICKS_PER_ROW)
        orig_size = brick_image.get_rect()
        scale_factor = (brick_width / orig_size.width)
        brick_height = round(orig_size.height * scale_factor)
        new_size = (brick_width, brick_height)
        
        self.image = pygame.transform.scale(brick_image, new_size)
        self.rect = self.image.get_rect()
        
        #position the bricks
        row += BLANK_ROWS
        self.rect.x = col * brick_width
        self.rect.y = row * brick_height
        
        
#BRICK class end



#define sprites group
all_sprites = pygame.sprite.Group()

#add sprites to group
ball = Ball()
all_sprites.add(ball)

paddle = Paddle()
all_sprites.add(paddle)

#define bricks group
bricks = pygame.sprite.Group()

#determine how many bricks to draw
for row in range(0, NUM_ROWS):
    for col in range(0, BRICKS_PER_ROW):
        brick = Brick(row, col)
        #add bricks group to all sprites group
        all_sprites.add(brick)
        #add each brick to bricks group
        bricks.add(brick)



#the GAME LOOP - this section is where the ACTION is
running = True
while running:  
    #time passes each loop
    clock.tick(FPS)

    #make the window close-able
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #check if any retries remaining
    #if no retries then GAME OVER
    if retries == 0:
        screen.fill(RED)
        draw_text(screen, "GAME OVER", screen_rect.center, font_size=60, anchor="center")
    
    #if not game over then move on    
    else:
        #check if paused 
        if pause:
            screen.fill(BABYBLUE)
            draw_text(screen, "PAUSED", screen_rect.center, font_size=60, anchor="center")
            #during pause set score text to show retries
            score_text = f"{retries} attempts remaining - press X to START"
            #draw_text(screen, f"{retries} attempts remaining - press X to START", screen_rect.bottom, font_size=20, anchor="bottom")
            keys = pygame.key.get_pressed()
            #watch out for x key pressed
            if keys[pygame.K_x]:
                #then unpause
                pause=False
        
        #if not paused then move on
        else:
            #update and move on
            all_sprites.update()
            #change score text during active game
            score_text = f"Score: {score} / Lives: {lives} / Difficulty: {difficulty}"    
    
    #check for paddle / ball collision
    if pygame.sprite.collide_rect(ball, paddle):
        ball.y_speed = -5
        if ball.rect.centerx < paddle.rect.centerx:
            ball.x_speed = -5
        else:
            ball.x_speed = 5
        
    #Reduce lives if ball is lost
    if ball.lost:
        lives -= 1
        #check if lives are zero
        if lives == 0:
            pause = True
            #then reset lives
            lives = 3
            #then subtract retries
            retries -= 1
        #reset the ball after calculations
        ball.reset()
    
    #check for brick collision
    collided_brick = pygame.sprite.spritecollideany(ball,bricks)
    if collided_brick:
        score +=1
        collided_brick.kill()
        ball.y_speed *= -1
    
    #draw everything on the internal screen
    all_sprites.draw(screen)
    
    draw_text(screen, score_text, (8, 8))
    
    #flip the display so human eyes can see
    pygame.display.flip()
    
    #fill the screen every loop to start fresh to make it look animated
    screen.fill(BLACK)

#end of GAME LOOP section

#bye
pygame.quit()
#bye

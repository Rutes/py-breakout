#very beginning -what even are we doing
import pygame
import random

pygame.init()


#define some constant values
FPS = 60

BLACK = (0, 0, 0)
PINK = (232, 92,180)
BLUE = (92, 116,232)
PURPLE = (181, 58,209)
RED = (255, 0, 0)
LIGHTPURPLE = (216, 148, 255)
DARKPURPLE = (116, 33, 163)
LIGHTPINK = (255, 143, 242)
BABYBLUE = (143, 171, 255)

BRICKS_PER_ROW = 10
NUM_ROWS = 5
BLANK_ROWS = 2

screen = pygame.display.set_mode((600, 800))
screen_rect = screen.get_rect()

clock = pygame.time.Clock()

lives = 10
score = 0


#BALL start
class Ball(pygame.sprite.Sprite):
    #ball initializes itself
    def __init__(self):
        super().__init__()
#        self.image = pygame.Surface((20, 20))
#        self.image.fill(RED)
        ball_image = pygame.image.load("pika.png").convert_alpha()
        self.image = pygame.transform.scale(ball_image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset()

    #ball updates itself
    def update(self):
        if self.rect.right >= screen_rect.right:
            self.x_speed = -5
        if self.rect.left <= screen_rect.left:
            self.x_speed = 5
        if self.rect.top <= screen_rect.top:
            self.y_speed = 5
        if self.rect.bottom >= screen_rect.bottom:
            #self.y_speed = -5
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
    def __init__(self):
        super().__init__()
#        self.image = pygame.Surface((100, 15))
#        self.image.fill(BLUE)
        paddle_image = pygame.image.load("paddle.png").convert_alpha()
        self.image = pygame.transform.scale(paddle_image, (100, 15))
        self.rect = self.image.get_rect()
        self.rect.center = screen_rect.center
        self.rect.bottom = screen_rect.bottom - 10
    
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
    def __init__(self, row, col):
        super().__init__()
        brick_image = pygame.image.load("brick.png").convert_alpha()
        
        #calculate new size of bricks
        brick_width = round(screen_rect.width / BRICKS_PER_ROW)
        orig_size = brick_image.get_rect()
        scale_factor = (brick_width / orig_size.width)
        brick_height = round(orig_size.height * scale_factor)
        new_size = (brick_width, brick_height)
        
        #self.image = brick_image
        self.image = pygame.transform.scale(brick_image, new_size)
        self.rect = self.image.get_rect()
        
        #position the brick
        self.rect.x = col * brick_width
        self.rect.y = row * brick_height
        
        
#BRICK class end


#define how to put text on screen
def draw_text(surface, text, pos=(0, 0), color=BABYBLUE, font_size=20, anchor="topleft"):
    arial = pygame.font.match_font("arial")
    font = pygame.font.Font(arial, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, anchor, pos)
    surface.blit(text_surface, text_rect)
#what is a blit?


#group all the things

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()



ball = Ball()
all_sprites.add(ball)

paddle = Paddle()
all_sprites.add(paddle)



for row in range(0, NUM_ROWS):
    for col in range(0, BRICKS_PER_ROW):
        brick = Brick(row, col)
        all_sprites.add(brick)
        bricks.add(brick)




#this section is where the ACTION is - the game LOOP
running = True
while running:  
    clock.tick(FPS)

    #make the window close-able
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update so we know whats up
    all_sprites.update()
    
    #check for paddle / ball collision
    if pygame.sprite.collide_rect(ball, paddle):
        ball.y_speed = -5
        
    #Reset ball if lost
    if ball.lost:
        lives -= 1
        ball.reset()
    
    #check for collision
    collided_brick = pygame.sprite.spritecollideany(ball,bricks)
    if collided_brick:
        score +=1
        collided_brick.kill()
        ball.y_speed *= -1
    
    #draw everything
    all_sprites.draw(screen)
    
    score_text = f"Score: {score} / Lives: {lives}"
    draw_text(screen, score_text, (8, 8))
    
    pygame.display.flip()
    
    #fill the screen every loop to start fresh
    screen.fill(BLACK)

#end of ACTION section

#bye
pygame.quit()
#bye
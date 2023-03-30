import pygame, random

pygame.init()


### setting up
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Pong!')

FPS = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont('agencyfb', 20)
winning_score = 1


### music
pygame.mixer.music.load('pong_tetris_soundtrack.ogg')
pygame.mixer.music.play(-1)


### colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)


### DRAWING SHAPES & BUTTONS : paddles
paddle_width = 10
paddle_height = 150

class Paddle:
    color = white
    paddle_speed = 7

    def __init__(self, x, y, screen_width, screen_height):
        self.x = self.default_x = x
        self.y = self.default_y = y
        self.width = screen_width
        self.height = screen_height
    
    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def moveUp(self):
        self.y -= self.paddle_speed
        if self.y <= 0:
            self.y = 0
          
    def moveDown(self):
        self.y += self.paddle_speed
        if self.y + self.height >= screen_height:
            self.y = screen_height - self.height

    def reset(self):
        self.x = self.default_x
        self.y = self.default_y

    def scoring(self, text, score, x, y, color):
        text = font.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)


### DRAWING SHAPES & SPRITES : ball
ball_radius = 10

class Ball:
    color = white
    ball_speed = 7

    def __init__(self, x, y, radius):
        self.x = self.default_x = x
        self.y = self.default_y = y
        self.radius = radius
        self.x_speed = self.ball_speed * random.choice((-1,1))  #
        self.y_speed = self.ball_speed * random.choice((-1,1))  #

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def border(self):
        if self.y <= 0 or self.y + self.radius >= screen_height:
            self.y_speed *= -1

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.border()
    
    def reset(self):
        self.x = self.default_x
        self.y = self.default_y
        self.x_speed *= random.choice((-1,1))
        self.y_speed *= random.choice((-1,1))
    
    def hit(self):
        self.x_speed *= -1
        self.y_speed *= 1


### DISPLAYING OBJECTS ON SCREEN
def display(screen, left_paddle, right_paddle, ball):
    screen.fill(black)

    left_paddle.display(screen)
    right_paddle.display(screen)
    ball.display(screen)
    
    pygame.draw.aaline(screen, white, (screen_width/2, 0), (screen_width/2, screen_height))

    pygame.display.update()


### RESPONDING TO EVENT : ball & paddle collide
def collision(ball, left_paddle, right_paddle):
    if ball.x_speed < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x <= left_paddle.x + left_paddle.width:
                ball.hit()

                half_paddle = left_paddle.y + left_paddle.height / 2
                y_diff = half_paddle - ball.y
                reduction = (left_paddle.height / 2) / ball.ball_speed
                y_speed = y_diff / reduction
                ball.y_speed = -1 * y_speed

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.hit()
                
                half_paddle = right_paddle.y + right_paddle.height / 2
                y_diff = half_paddle - ball.y
                reduction = (right_paddle.height / 2) / ball.ball_speed
                y_speed = y_diff / reduction
                ball.y_speed = -1 * y_speed


### RESPONDING TO USER INPUT : animate paddle
def paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.moveUp()
    if keys[pygame.K_s]:
        left_paddle.moveDown()
    
    if keys[pygame.K_p]:
        right_paddle.moveUp()
    if keys[pygame.K_l]:
        right_paddle.moveDown()


def main():
    left_paddle = Paddle(10, screen_height/2 - paddle_height/2, paddle_width, paddle_height)
    right_paddle = Paddle(screen_width-(10+paddle_width), screen_height/2 - paddle_height/2, paddle_width, paddle_height)
    ball = Ball(screen_width // 2, screen_height // 2, ball_radius)

    left_score = 0
    right_score = 0

    running = True
    while running:
        display(screen, left_paddle, right_paddle, ball)

        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()

        elif ball.x > screen_width:
            left_score += 1
            ball.reset()

        left_paddle.scoring("left : ", left_score, 100, 20, green)
        right_paddle.scoring("right : ", right_score, screen_width-100, 20, green)

        pygame.display.update()
        clock.tick(FPS)

    # quit loop
    pygame.quit()


if __name__ == '__main__':
    main()

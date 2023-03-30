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


### colors
black = (0, 0, 0)
green = (0, 255, 0)


### display objects
def display(screen, left_paddle, right_paddle, ball):
    screen.fill(black)

    left_paddle.display(screen)
    right_paddle.display(screen)
    ball.display(screen)
    
    pygame.draw.aaline(screen, white, (screen_width/2, 0), (screen_width/2, screen_height))

    pygame.display.update()


### ball & paddle collide
def collision(ball, left_paddle, right_paddle):
    if ball.x_speed < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x <= left_paddle.x + left_paddle.width:
                ball.x_speed *= -1

                half_paddle = left_paddle.y + left_paddle.height / 2
                y_diff = half_paddle - ball.y
                reduction = (left_paddle.height / 2) / ball.ball_speed
                y_speed = y_diff / reduction
                ball.y_speed = -1 * y_speed

                # count = 0
                # while count < 1: 
                # pygame.mixer.Sound.play(ball_hit)
                # pygame.mixer.Sound.stop()
                #     count += 1
                # pygame.mixer.Sound.pause(ball_hit)

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_speed *= -1
                
                half_paddle = right_paddle.y + right_paddle.height / 2
                y_diff = half_paddle - ball.y
                reduction = (right_paddle.height / 2) / ball.ball_speed
                y_speed = y_diff / reduction
                ball.y_speed = -1 * y_speed

                # count = 0
                # while count < 1: 
                # pygame.mixer.Sound.play(ball_hit)
                # pygame.mixer.Sound.stop()
                #     count += 1
                # pygame.mixer.Sound.stop(ball_hit)


### animate paddle
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
            # add time delay before start again
            # time.delay(1)
        elif ball.x > screen_width:
            left_score += 1
            ball.reset()
            # add time delay before start again
            # time.delay(1)

        left_paddle.scoring("left : ", left_score, 100, 20, green)
        right_paddle.scoring("right : ", right_score, screen_width-100, 20, green)

        pygame.display.update()
        clock.tick(FPS)

    # quit loop
    pygame.quit()


if __name__ == '__main__':
    main()

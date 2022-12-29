import pygame
from pygame.locals import *
from sys import exit

pygame.init()

all_sprites = pygame.sprite.Group()
all_bricks_sprites = pygame.sprite.Group()
brick_width = 30
brick_height = 10


def main():
    # colors
    blue = (0, 180, 250)
    light_gray = (180, 180, 180)
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (135, 135, 135)
    yellow = (197, 199, 37)
    green = (0, 127, 33)
    orange = (183, 119, 0)
    red = (162, 8, 0)

    # width and height of screen
    screen_width = 505
    screen_height = 700

    # screen size
    size = (screen_width, screen_height)
    player_x = 245
    player_y = 600

    # create the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Breakout")

    # variables
    score_max = 448
    score_1 = 0
    brick_color = 0
    game_clock = pygame.time.Clock()
    fps = 30
    life_max = 0
    life = 3
    combo = 0
    ball_x = 250
    ball_y = 450
    ball_dx = 5
    ball_dy = 5
    ball_width = 10
    ball_height = 10
    bricks = []

    # score text
    score_font = pygame.font.Font('PressStart2P.ttf', 32)
    score_text = score_font.render('000', True, white, black)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (260, 80)

    life_font = pygame.font.Font('PressStart2P.ttf', 32)
    life_text = life_font.render('000', True, red, black)
    life_text_rect = life_text.get_rect()
    life_text_rect.center = (80, 80)

    game_over_font = pygame.font.Font('PressStart2P.ttf', 32)
    game_over_text = game_over_font.render('GAME OVER', True, white, black)
    game_over_text_rect = score_text.get_rect()
    game_over_text_rect.center = (150, 500)

    # victory text
    victory_font = pygame.font.Font('PressStart2P.ttf', 32)
    victory_text = victory_font.render('VICTORY', True, white, black)
    victory_text_rect = victory_text.get_rect()
    victory_text_rect.center = (250, 350)

    restart_font = pygame.font.Font('PressStart2P.ttf', 12)
    restart_text = restart_font.render('Press R to restart or ESC to finish', True, white, black)
    restart_text_rect = restart_text.get_rect()
    restart_text_rect.center = (250, 530)

    # class brick
    class Brick(pygame.sprite.Sprite):
        def __init__(self, color, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y
            self.width = 30
            self.height = 10
            self.color = color

        def render(self):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    for coord_y in range(180, 286, 15):
        if 180 <= coord_y <= 195:
            brick_color = red
        elif 210 <= coord_y <= 225:
            brick_color = orange
        elif 240 <= coord_y <= 255:
            brick_color = green
        elif coord_y > 255:
            brick_color = yellow
        for coord_x in range(10, 466, 35):
            brick = Brick(brick_color, coord_x, coord_y)
            bricks.append(brick)

    brick_sound = pygame.mixer.Sound('sounds_brick.wav')
    paddle_sound = pygame.mixer.Sound('sounds_paddle.wav')
    wall_sound = pygame.mixer.Sound('sounds_wall.wav')

    # create the game loop
    game_loop = True
    while game_loop:
        game_clock.tick(fps)
        screen.fill(black)
        # player position(cord.x, cord.y, width, height)
        player_position = (player_x, player_y, 30, 10)
        # player
        pygame.draw.rect(screen, blue, player_position)
        # ball
        ball = (ball_x, ball_y, ball_width, ball_height)
        pygame.draw.rect(screen, light_gray, ball)
        # exit of game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        if score_1 < score_max:
            # player movement
            if pygame.key.get_pressed()[K_a]:
                player_x -= 10
            if player_x <= 10:
                player_x = 10
            if pygame.key.get_pressed()[K_d]:
                player_x += 10
            if player_x >= 465:
                player_x = 465

            # ball collision with the walls
            if ball_y >= 700:
                ball_x = 250
                ball_y = 450
                ball_dy *= -1
                ball_dx *= -1
                life -= 1
                combo = 0
                ball_dx = 5
                ball_dy = -5
            if life == life_max:
                ball_x = 250
                ball_y = 450
                ball_dy *= 0
                ball_dx *= 0
                screen.blit(game_over_text, game_over_text_rect)
                screen.blit(restart_text, restart_text_rect)
                if pygame.key.get_pressed()[K_r]:
                    screen.fill(black)
                    main()
                if pygame.key.get_pressed()[K_ESCAPE]:
                    break

            if ball_y <= 10:
                ball_dy *= -1
                wall_sound.play()
            if ball_x >= 495:
                ball_dx *= -1
                wall_sound.play()
            if ball_x <= 10:
                ball_dx *= -1
                wall_sound.play()
            # score render
            score_text = score_font.render(str(score_1), True, white, black)
            screen.blit(score_text, score_text_rect)
            life_text = life_font.render(str(life), True, red, black)
            screen.blit(life_text, life_text_rect)

            # ball collision with the paddle player
            if player_y <= ball_y + 10 <= player_y + 10 and player_x <= ball_x <= player_x + 30:
                if ball_dy > 0:
                    ball_dy *= -1
                paddle_sound.play()

            # ball collision with the bricks
            for brick in bricks:
                if (brick.x <= ball_x <= brick.x + brick.width) or (
                        brick.x <= ball_x + ball_width <= brick.x + brick.width):
                    if (brick.y <= ball_y <= brick.y + brick.height) or (
                            brick.y <= ball_y + ball_height <= brick.y + brick.height):
                        bricks.remove(brick)
                        ball_dy *= -1
                        if brick.color == yellow:
                            score_1 += 1
                        elif brick.color == green:
                            score_1 += 3
                        elif brick.color == orange:
                            score_1 += 5
                        elif brick_color == red:
                            score_1 += 7
                        brick_sound.play()
                        combo += 1
                        if combo == 4:
                            ball_dy *= 1.2
                            ball_dx *= 1.2
                        if combo == 20 and (brick.color == orange or brick.color == red):
                            ball_dy *= 1.2
                            ball_dx *= 1.2
            # ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            for brick in bricks:
                brick.render()

        # pygame.draw.rect(screen, color, pygame.Rect(10, 20, 30, 10))
        # creating the walls (cord.x, cord.y, width, height)
        # wall upper
        pygame.draw.rect(screen, gray, pygame.Rect(0, 0, 495, 20))

        # wall left
        pygame.draw.rect(screen, gray, pygame.Rect(0, 0, 10, 595))
        pygame.draw.rect(screen, red, pygame.Rect(0, 177, 10, 31))
        pygame.draw.rect(screen, orange, pygame.Rect(0, 207, 10, 31))
        pygame.draw.rect(screen, green, pygame.Rect(0, 238, 10, 31))
        pygame.draw.rect(screen, yellow, pygame.Rect(0, 268, 10, 31))
        pygame.draw.rect(screen, blue, pygame.Rect(0, 595, 10, 20))
        pygame.draw.rect(screen, gray, pygame.Rect(0, 615, 10, 700))
        # wall right
        pygame.draw.rect(screen, gray, pygame.Rect(495, 0, 10, 595))
        pygame.draw.rect(screen, red, pygame.Rect(495, 177, 10, 31))
        pygame.draw.rect(screen, orange, pygame.Rect(495, 207, 10, 31))
        pygame.draw.rect(screen, green, pygame.Rect(495, 238, 10, 31))
        pygame.draw.rect(screen, yellow, pygame.Rect(495, 268, 10, 31))
        pygame.draw.rect(screen, blue, pygame.Rect(495, 595, 10, 20))
        pygame.draw.rect(screen, gray, pygame.Rect(495, 615, 10, 700))
        pygame.display.update()


main()

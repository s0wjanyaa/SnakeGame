import pygame
import random

pygame.init()

width = 600
height = 480
block_size = 20

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
header_color = (50, 50, 50)
button_color = (0, 0, 128)  

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

try:
    game_over_font = pygame.font.Font("PressStart2P-Regular.ttf", 48)  
except pygame.error:
    print("PressStart2P font not found. Using default font for Game Over.")
    game_over_font = pygame.font.Font(None, 48)

default_font = pygame.font.Font(None, 36)  
button_font = pygame.font.Font(None, 24)  


def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, (block[0], block[1], block_size, block_size))

def draw_food(food):
    pygame.draw.rect(screen, red, (food[0], food[1], block_size, block_size))

def generate_food(snake_list):
    while True:
        food_x = random.randrange(0, width // block_size) * block_size
        food_y = random.randrange(40 // block_size, (height - 40) // block_size) * block_size 
        food = (food_x, food_y)
        if food not in snake_list:
            return food

def game_over(final_score, high_score):
    global running, snake_list, snake_direction, food, score

    play_again_text = button_font.render("Play Again", True, white)
    quit_text = button_font.render("Quit", True, white)

    play_again_rect = play_again_text.get_rect()  
    quit_rect = quit_text.get_rect()

    play_again_x = width // 2 - play_again_rect.width // 2 
    quit_x = width // 2 - quit_rect.width // 2

    play_again_y = height // 2 + 60 + (40 - play_again_rect.height) // 2  
    quit_y = height // 2 + 110 + (40 - quit_rect.height) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if pygame.Rect(play_again_x, play_again_y, play_again_rect.width, play_again_rect.height).colliderect(pygame.Rect(mouse_x, mouse_y, 1, 1)):
                    snake_list = [(width // 2, height // 2 - 40)]
                    snake_direction = "RIGHT"
                    food = generate_food(snake_list)
                    score = 0
                    return True

                if pygame.Rect(quit_x, quit_y, quit_rect.width, quit_rect.height).colliderect(pygame.Rect(mouse_x, mouse_y, 1, 1)):
                    running = False
                    pygame.quit()
                    quit()

        screen.fill(black)

        game_over_text = game_over_font.render("Game Over!", True, red)  
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 80))
        screen.blit(game_over_text, game_over_rect)

        score_text = default_font.render(f"Score: {final_score}", True, white)  
        score_rect = score_text.get_rect(center=(width // 4, height // 2 - 20))
        screen.blit(score_text, score_rect)

        high_score_text = default_font.render(f"High Score: {high_score}", True, white)  
        high_score_rect = high_score_text.get_rect(center=(3 * width // 4, height // 2 - 20))
        screen.blit(high_score_text, high_score_rect)

        pygame.draw.rect(screen, button_color, (width // 2 - 70, height // 2 + 60, 140, 40), 0)  
        pygame.draw.rect(screen, button_color, (width // 2 - 70, height // 2 + 110, 140, 40), 0)  

        screen.blit(play_again_text, (play_again_x, play_again_y)) 
        screen.blit(quit_text, (quit_x, quit_y))  

        pygame.display.flip()
        clock.tick(10)


running = True
while running:
    snake_list = [(width // 2, height // 2 - 40)]
    snake_direction = "RIGHT"
    food = generate_food(snake_list)
    score = 0

    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"

        head_x = snake_list[0][0]
        head_y = snake_list[0][1]

        if snake_direction == "RIGHT":
            new_head = (head_x + block_size, head_y)
        elif snake_direction == "LEFT":
            new_head = (head_x - block_size, head_y)
        elif snake_direction == "UP":
            new_head = (head_x, head_y - block_size)
        elif snake_direction == "DOWN":
            new_head = (head_x, head_y + block_size)

        snake_list.insert(0, new_head)

        if snake_list[0] == food:
            food = generate_food(snake_list)
            score += 1
        else:
            snake_list.pop()

        if not (0 <= snake_list[0][0] < width and 40 <= snake_list[0][1] < height):
            running = False
        for i in range(1, len(snake_list)):
            if snake_list[i] == snake_list[0]:
                running = False

        if not running:
            if game_over(score, high_score):
                running = True
                break
            else:
                break

        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))

        screen.fill(black)

        pygame.draw.rect(screen, header_color, (0, 0, width, 40))

        score_text = default_font.render(f"Score: {score}", True, white)  
        screen.blit(score_text, (10, 10))

        high_score_text = default_font.render(f"High Score: {high_score}", True, white)  
        screen.blit(high_score_text, (width - 180, 10))

        draw_snake(snake_list)
        draw_food(food)

        pygame.display.flip()
        clock.tick(10)

pygame.quit()
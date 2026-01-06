# dodging game using tutorial by keith galli

import pygame
import random

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
player_size = 50
player_pos = [width / 2, height / 2 - player_size]
player_color = (13, 120, 255)
bg_color = (175, 231, 250)
enemy_size = 50
enemy_color = (45, 222, 10)
enemy_pos = [random.randint(0, width - enemy_size), 0]
enemy_list = [enemy_pos]
clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont("monospace", 35)

def set_level(score, speed):
    #global speed
    if score < 10:
        speed = 8
    elif score < 20:
        speed = 10
    elif score < 30:
        speed = 12
    else: 
        speed = 15
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        pygame.draw.rect(screen, enemy_color, (enemy[0], enemy[1], enemy_size, enemy_size))

def detect_collisions(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    
    # check for collisions
    if (e_x >= p_x and e_x < (p_x + player_size)) or (e_x <= p_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
        return False

def update_enemy_pos(enemy_list):
    global score
    # update position of enemy
    for index, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += speed
        else:
            score += 1
            enemy_list.pop(index)

def check_collision(enemy_list, player_pos):
    for enemy in enemy_list:
        if detect_collisions(player_pos, enemy):
            return True
    return False

    # alternative code, check if it works
    # p_x = player_pos[0]
    # p_y = player_pos[1]
    # for enemy in enemy_list:    
    #     e_x = enemy[0]
    #     e_y = enemy[1]
    #     if (e_x >= p_x and e_x < (p_x + player_size)) or (e_x <= p_x and p_x < (e_x + enemy_size)):
    #         if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
    #             return True
    #         return False

def main ():
    global speed, death_count
    death_count = 0
    speed = 8
    run = True
    enemy_list = []
    player_pos = [width / 2, height / 2 - player_size]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            # move player right and left to avoid collisions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_pos[0] -= player_size
                elif event.key == pygame.K_RIGHT:
                    player_pos[0] += player_size

        screen.fill((bg_color))
        drop_enemies(enemy_list)
        update_enemy_pos(enemy_list)
        speed = set_level(score, speed)
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (width-200, height-40))
        speed_text = font.render("Speed: " + str(speed), True, (0, 0, 0))
        screen.blit(speed_text, (width-760, height-40))
        if check_collision(enemy_list, player_pos):
            death_count += 1
            menu(death_count)
        draw_enemies(enemy_list)
        pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))
        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global score
    run = True
    start_pos = [100, 400]
    direction = 1

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                score = 0
                main()
        screen.fill((bg_color))
        if death_count == 0:
            text = font.render("Press any key to start", True, player_color)
            screen.blit(text, (180, height//2))
        elif death_count > 0:
            text = font.render("Press any key to restart", True, player_color)
            screen.blit(text, (160, height//2))
            score_text = font.render("Score: " + str(score), True, player_color)
            screen.blit(score_text, (300, height//2 + 50))
        
        pygame.draw.rect(screen, player_color, (start_pos[0], start_pos[1], player_size, player_size))
        start_pos[0] += 5 * direction
        if start_pos[0] <= 100:
            direction = 1
        elif start_pos[0] >= 700:
            direction = -1
        pygame.display.update()
        

menu(death_count=0)
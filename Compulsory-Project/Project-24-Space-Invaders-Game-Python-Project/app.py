import pygame
import random
import sys

pygame.init()
pygame.mixer.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


try:
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    game_over_sound = pygame.mixer.Sound("game_over.wav")
except:
    shoot_sound = pygame.mixer.Sound(buffer=bytearray(100))
    explosion_sound = pygame.mixer.Sound(buffer=bytearray(100))
    game_over_sound = pygame.mixer.Sound(buffer=bytearray(100))

player_width = 50
player_height = 30
player_x = width // 2 - player_width // 2
player_y = height - player_height - 20
player_speed = 7
player_lives = 3

enemy_width = 40
enemy_height = 40
enemy_speed = 2
enemies = []
enemy_spawn_rate = 30  
enemy_spawn_timer = 0

bullet_width = 5
bullet_height = 15
bullets = []
bullet_speed = 10
bullet_cooldown = 0
bullet_cooldown_max = 15  

score = 0
game_over = False
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

powerups = []
powerup_types = ["extra_life", "fast_shoot", "slow_enemies"]
powerup_spawn_chance = 0.01  

def spawn_enemy():
    enemy_x = random.randint(0, width - enemy_width)
    enemy_y = random.randint(-100, -40)
    enemies.append([enemy_x, enemy_y, enemy_width, enemy_height])

def draw_player(x, y):
    pygame.draw.rect(screen, green, (x, y, player_width, player_height))
    pygame.draw.polygon(screen, white, [
        (x + player_width//2, y),
        (x, y + player_height),
        (x + player_width, y + player_height)
    ])

def draw_enemy(x, y, w, h):
    pygame.draw.rect(screen, red, (x, y, w, h))
    pygame.draw.circle(screen, white, (x + w//3, y + h//3), 5)
    pygame.draw.circle(screen, white, (x + 2*w//3, y + h//3), 5)

def draw_powerup(x, y, powerup_type):
    if powerup_type == "extra_life":
        color = green
    elif powerup_type == "fast_shoot":
        color = blue
    else:  
        color = white
    
    pygame.draw.rect(screen, color, (x, y, 20, 20))
    pygame.draw.rect(screen, black, (x, y, 20, 20), 1)

def show_game_over():
    screen.fill(black)
    game_over_text = font.render("GAME OVER", True, red)
    score_text = font.render(f"Final Score: {score}", True, white)
    restart_text = font.render("Press R to Restart or Q to Quit", True, white)
    
    screen.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//2 - 50))
    screen.blit(score_text, (width//2 - score_text.get_width()//2, height//2))
    screen.blit(restart_text, (width//2 - restart_text.get_width()//2, height//2 + 50))
    
    pygame.display.flip()

def reset_game():
    global player_x, player_y, player_lives, enemies, bullets, score, game_over
    player_x = width // 2 - player_width // 2
    player_y = height - player_height - 20
    player_lives = 3
    enemies = []
    bullets = []
    score = 0
    game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and game_over:
                running = False
            if event.key == pygame.K_r and game_over:
                reset_game()
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and bullet_cooldown == 0:
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
            shoot_sound.play()
            bullet_cooldown = bullet_cooldown_max
        
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_rate:
            spawn_enemy()
            enemy_spawn_timer = 0
            enemy_spawn_rate = max(10, 30 - score // 10)
        
        if random.random() < powerup_spawn_chance:
            powerup_x = random.randint(0, width - 20)
            powerup_y = 0
            powerup_type = random.choice(powerup_types)
            powerups.append([powerup_x, powerup_y, powerup_type])
        
        if bullet_cooldown > 0:
            bullet_cooldown -= 1
        
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            
            if enemy[1] > height:
                enemies.remove(enemy)
                player_lives -= 1
                if player_lives <= 0:
                    game_over = True
                    game_over_sound.play()
            
            for bullet in bullets[:]:
                if (enemy[0] < bullet[0] < enemy[0] + enemy[2] and
                    enemy[1] < bullet[1] < enemy[1] + enemy[3]):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    explosion_sound.play()
                    break
            
            if (player_x < enemy[0] + enemy[2] and player_x + player_width > enemy[0] and
                player_y < enemy[1] + enemy[3] and player_y + player_height > enemy[1]):
                enemies.remove(enemy)
                player_lives -= 1
                explosion_sound.play()
                if player_lives <= 0:
                    game_over = True
                    game_over_sound.play()
        
        for powerup in powerups[:]:
            powerup[1] += 3  
            
            if powerup[1] > height:
                powerups.remove(powerup)
                continue
            
            if (player_x < powerup[0] + 20 and player_x + player_width > powerup[0] and
                player_y < powerup[1] + 20 and player_y + player_height > powerup[1]):
                powerup_type = powerup[2]
                if powerup_type == "extra_life":
                    player_lives += 1
                elif powerup_type == "fast_shoot":
                    bullet_cooldown_max = max(5, bullet_cooldown_max - 3)
                elif powerup_type == "slow_enemies":
                    enemy_speed = max(1, enemy_speed - 0.5)
                powerups.remove(powerup)
    
    screen.fill(black)
    
    for _ in range(5): 
        star_x = random.randint(0, width)
        star_y = random.randint(0, height)
        pygame.draw.circle(screen, white, (star_x, star_y), 1)
    
    if not game_over:
        draw_player(player_x, player_y)
        
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1], enemy[2], enemy[3])
        
        for bullet in bullets:
            pygame.draw.rect(screen, white, (bullet[0], bullet[1], bullet_width, bullet_height))
        
        for powerup in powerups:
            draw_powerup(powerup[0], powerup[1], powerup[2])
        
        lives_text = font.render(f"Lives: {player_lives}", True, white)
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (10, 50))
    else:
        show_game_over()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
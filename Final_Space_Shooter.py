import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('First Game')
TURQUOISE = (64,224,208)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (235, 107, 52)
BORDER = pygame.Rect(WIDTH/2-5 , 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT =pygame.font.SysFont(' comicsans', 80)



FPS = 60
VEL = 5
BULLETS_VEL = 10
MAX_BULLETS = 7


first_hit = pygame.USEREVENT + 1
second_hit = pygame.USEREVENT + 2

SHIP_WIDTH, SHIP_HEIGHT = 55, 40
FIRST_SHIP_IMAGE =  pygame.image.load('C:\\Users\geo86\\OneDrive\\Desktop\\Portfolio\\Python\\Space_Shooter_Game\\ship1.png')
FIRST_SHIP = pygame.transform.rotate(pygame.transform.scale(FIRST_SHIP_IMAGE,(SHIP_WIDTH, SHIP_HEIGHT)),270)
SECOND_SHIP_IMAGE =  pygame.image.load('C:\\Users\geo86\\OneDrive\\Desktop\\Portfolio\\Python\\Space_Shooter_Game\\ship2.png')
SECOND_SHIP = pygame.transform.rotate(pygame.transform.scale(SECOND_SHIP_IMAGE,(SHIP_WIDTH, SHIP_HEIGHT)),90)
SPACE = pygame.transform.scale(pygame.image.load('C:\\Users\\geo86\\OneDrive\\Desktop\\Portfolio\\Python\\Space_Shooter_Game\\space.jpg'),(WIDTH,HEIGHT))
##SECOND_SHIP =  pygame.image.load(os.path.join('First', 'ship2'))
                    

def FiRST_SHIP_Keys(keys_pressed, first):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and first.x - VEL > 0: #left
             first.x -= VEL
        if keys_pressed[pygame.K_d] and first.x + VEL + first.width / 1.55 < BORDER.x: #right
             first.x += VEL
        if keys_pressed[pygame.K_w] and first.y - VEL > 0: #up
             first.y -= VEL
        if keys_pressed[pygame.K_s] and first.y + VEL + first.height < HEIGHT - 12: #down
             first.y += VEL

def SECOND_SHIP_Keys(keys_pressed, second):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and second.x + VEL - second.width // 3 > BORDER.x: #left
             second.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and second.x + VEL + second.width// 1.3 < WIDTH: #right
             second.x += VEL
        if keys_pressed[pygame.K_UP]and second.y - VEL > 0: #up
             second.y -= VEL
        if keys_pressed[pygame.K_DOWN] and second.y + VEL + second.height < HEIGHT - 10: #down
             second.y += VEL

def handle_bullets(first_bullets, second_bullets, first, second):
     for bullet in first_bullets:
          bullet.x += BULLETS_VEL
          if second.colliderect(bullet):
               pygame.event.post(pygame.event.Event(second_hit))
               first_bullets.remove(bullet)
          elif bullet.x > WIDTH:
               first_bullets.remove(bullet)

     for bullet in second_bullets:
          bullet.x -= BULLETS_VEL
          if first.colliderect(bullet):
               pygame.event.post(pygame.event.Event(first_hit))
               second_bullets.remove(bullet)
          elif bullet.x < 0:
               second_bullets.remove(bullet)
     


def draw_window(first, second, first_bullets, second_bullets, first_health, second_health):
        WIN.blit(SPACE,(0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)

        first_health_text = HEALTH_FONT.render("Health: " + str(first_health), 1, WHITE)
        second_health_text = HEALTH_FONT.render("Health: " + str(second_health), 1, WHITE)
        WIN.blit(first_health_text, (10, 10))
        WIN.blit(second_health_text, (WIDTH - second_health_text.get_width() - 10, 10))

        WIN.blit(FIRST_SHIP,(first.x, first.y))
        WIN.blit(SECOND_SHIP,(second.x, second.y))

        for bullet in first_bullets:
             pygame.draw.rect(WIN,RED, bullet)

        for bullet in second_bullets:
             pygame.draw.rect(WIN,GREEN, bullet)

        pygame.display.update()

def draw_winner(text):
     draw_text = WINNER_FONT.render(text, 1, WHITE)
     WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
     pygame.display.update()
     pygame.time.delay(5000)

def main():
    first = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    second = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)

    first_bullets = []
    second_bullets = []
    first_health = 10
    second_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
          
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LALT and len(first_bullets) < MAX_BULLETS:
                      bullet = pygame.Rect(first.x + first.width, first.y + first.height // 2 - 2, 10, 5)
                      first_bullets.append(bullet)
                      

                 if event.key == pygame.K_RALT and len(second_bullets) < MAX_BULLETS:
                      bullet = pygame.Rect(second.x, second.y + second.height // 2 + 2, 10, 5)
                      second_bullets.append(bullet)

            if event.type == first_hit:
                    first_health -= 1              

            if event.type == second_hit:
                    second_health-=1
                    
        winner_text = ""  
        if first_health <= 0:
             winner_text ='Second Player Wins!!!'
        if second_health <= 0:
             winner_text = 'First Player Wins!!!'
        if winner_text != "":
             draw_winner(winner_text) # We have a winner
             break
                     

        keys_pressed = pygame.key.get_pressed()
        FiRST_SHIP_Keys(keys_pressed, first)
        SECOND_SHIP_Keys( keys_pressed, second)

        handle_bullets(first_bullets, second_bullets, first, second)
             

        draw_window(first, second , first_bullets, second_bullets, first_health, second_health)


    main()

if __name__ == "__main__":
    main()
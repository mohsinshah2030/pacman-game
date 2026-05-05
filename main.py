import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 660
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
RED = (255,0,0)

maze = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROWS = len(maze)
COLS = len(maze[0])

def reset_game():
    return 1,1,(0,0),18,8,0,3,"start"

pac_x, pac_y, direction, ghost_x, ghost_y, score, lives, game_state = reset_game()

food = [(c,r) for r in range(ROWS) for c in range(COLS) if maze[r][c]==0]

def draw_maze():
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLUE, (c*CELL, r*CELL, CELL, CELL))

def draw_food():
    for f in food:
        pygame.draw.circle(screen, WHITE, (f[0]*CELL+15, f[1]*CELL+15), 4)

def draw_pacman():
    pygame.draw.circle(screen, YELLOW, (pac_x*CELL+15, pac_y*CELL+15), 13)

def draw_ghost():
    pygame.draw.circle(screen, RED, (ghost_x*CELL+15, ghost_y*CELL+15), 13)

def move_ghost():
    global ghost_x, ghost_y
    moves = [(0,1),(0,-1),(1,0),(-1,0)]
    valid = []
    for dx,dy in moves:
        nx, ny = ghost_x+dx, ghost_y+dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx]==0:
            valid.append((nx,ny))
    if valid:
        ghost_x, ghost_y = random.choice(valid)

def draw_ui():
    txt = font.render(f"Score: {score}   Lives: {lives}", True, WHITE)
    screen.blit(txt, (10, HEIGHT-40))

def draw_start():
    screen.fill(BLACK)
    screen.blit(font.render("Press SPACE to Start", True, WHITE),(180,300))

def draw_game_over():
    screen.fill(BLACK)
    screen.blit(font.render("GAME OVER", True, RED),(240,250))
    screen.blit(font.render("Press R to Restart", True, WHITE),(200,300))

def main():
    global pac_x, pac_y, direction, score, lives, game_state, food, ghost_x, ghost_y

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "start":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = "play"

            elif game_state == "over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    pac_x, pac_y, direction, ghost_x, ghost_y, score, lives, game_state = reset_game()
                    food = [(c,r) for r in range(ROWS) for c in range(COLS) if maze[r][c]==0]

        keys = pygame.key.get_pressed()

        if game_state == "play":
            if keys[pygame.K_LEFT]: direction = (-1,0)
            if keys[pygame.K_RIGHT]: direction = (1,0)
            if keys[pygame.K_UP]: direction = (0,-1)
            if keys[pygame.K_DOWN]: direction = (0,1)

            if direction != (0,0):
                nx = pac_x + direction[0]
                ny = pac_y + direction[1]

                if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
                    pac_x, pac_y = nx, ny

            if (pac_x, pac_y) in food:
                food.remove((pac_x, pac_y))
                score += 10

            move_ghost()

            if pac_x == ghost_x and pac_y == ghost_y:
                lives -= 1
                pac_x, pac_y = 1,1
                if lives == 0:
                    game_state = "over"

            draw_maze()
            draw_food()
            draw_pacman()
            draw_ghost()
            draw_ui()

        elif game_state == "start":
            draw_start()

        elif game_state == "over":
            draw_game_over()

        pygame.display.update()
        clock.tick(8)

if __name__ == "__main__":
    main()
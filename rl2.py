import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600  # Set to a larger window
CELL_SIZE = WIDTH // 10  # Adjust for 10x10 grid
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Maze Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Maze size and walls
ROWS, COLS = 10, 10
maze = np.ones((ROWS, COLS))  # 1 = wall, 0 = path
directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Directions for DFS

# Generate maze using Depth-First Search (DFS)
def generate_maze(x, y):
    maze[x, y] = 0
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx, ny] == 1:
            maze[x + dx // 2, y + dy // 2] = 0
            generate_maze(nx, ny)

generate_maze(0, 0)

# Initialize agent
agent_x, agent_y = 0, 0

# Function to draw the maze on the screen
def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if maze[i, j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (200, 200, 200), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to draw the agent
def draw_agent():
    pygame.draw.rect(screen, RED, (agent_y * CELL_SIZE, agent_x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw the maze and agent
    draw_maze()
    draw_agent()
    
    pygame.display.flip()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and agent_x > 0 and maze[agent_x - 1, agent_y] == 0:
                agent_x -= 1
            elif event.key == pygame.K_DOWN and agent_x < ROWS - 1 and maze[agent_x + 1, agent_y] == 0:
                agent_x += 1
            elif event.key == pygame.K_LEFT and agent_y > 0 and maze[agent_x, agent_y - 1] == 0:
                agent_y -= 1
            elif event.key == pygame.K_RIGHT and agent_y < COLS - 1 and maze[agent_x, agent_y + 1] == 0:
                agent_y += 1
    
    clock.tick(10)  # Controls the speed of the agent movement

pygame.quit()

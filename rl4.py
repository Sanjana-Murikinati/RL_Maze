import pygame
import numpy as np
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Maze Game")
clock = pygame.time.Clock()

# Colors
BLACK = (20, 20, 20)  # Thin maze walls
WHITE = (255, 255, 255)  # Paths
BLUE = (0, 0, 255)  # Start position
BORDER_COLOR = (100, 100, 100)  # Maze border
ORANGE = (255, 165, 0)  # Winning text color

# Maze size and walls
ROWS, COLS = 10, 10
maze = np.ones((ROWS, COLS))  # 1 = wall, 0 = path
directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Directions for DFS

# Maze generation using Depth-First Search
def generate_maze(x, y):
    maze[x, y] = 0
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx, ny] == 1:
            maze[x + dx // 2, y + dy // 2] = 0
            generate_maze(nx, ny)

generate_maze(0, 0)

# Load images
cat_image = pygame.image.load('cat.png')
cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))

rat_image = pygame.image.load('rat.png')
rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

# Function to get a random goal position (not on a wall)
def get_random_goal():
    while True:
        goal_x = random.randint(0, ROWS - 1)
        goal_y = random.randint(0, COLS - 1)
        if maze[goal_x, goal_y] == 0:  # Ensure it's a path
            return goal_x, goal_y

# Initialize agent (cat) and goal (rat)
agent_x, agent_y = 0, 0
goal_x, goal_y = get_random_goal()

# Function to draw the maze with a border
def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if maze[i, j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BORDER_COLOR, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)  # Thin border

# Function to draw start and goal
def draw_start_goal():
    pygame.draw.rect(screen, BLUE, (0, 0, CELL_SIZE, CELL_SIZE))  # Start position
    screen.blit(rat_image, (goal_y * CELL_SIZE, goal_x * CELL_SIZE))  # Corrected rat position

# Function to display "YOU WON!" text
def display_win_message():
    font = pygame.font.Font(None, 80)
    text = font.render("YOU WON!", True, ORANGE)  # Changed text color to orange
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(2)  # Pause for 2 seconds

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw maze, start, goal
    draw_maze()
    draw_start_goal()

    # Draw the cat (agent)
    screen.blit(cat_image, (agent_y * CELL_SIZE, agent_x * CELL_SIZE))

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

    # Check if the agent has reached the goal
    if agent_x == goal_x and agent_y == goal_y:
        display_win_message()  # Show "YOU WON!" on screen
        agent_x, agent_y = 0, 0  # Reset cat to start
        goal_x, goal_y = get_random_goal()  # Move rat to a new random position

    clock.tick(30)  # Controls game speed

pygame.quit()

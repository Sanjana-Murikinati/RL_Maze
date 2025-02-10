import pygame
import numpy as np
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Maze Game")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)  # Maze walls and border
WHITE = (255, 255, 255)  # Paths
BLUE = (0, 0, 255)  # Start position
ORANGE = (255, 165, 0)  # Winning text color

# Function to generate a maze using Depth-First Search
def generate_maze(maze, x, y, directions):
    maze[x, y] = 0
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 1:
            maze[x + dx // 2, y + dy // 2] = 0
            generate_maze(maze, nx, ny, directions)

# Function to get a random goal position (not on a wall)
def get_random_goal(maze):
    while True:
        goal_x = random.randint(0, maze.shape[0] - 1)
        goal_y = random.randint(0, maze.shape[1] - 1)
        if maze[goal_x, goal_y] == 0:  # Ensure it's a path
            return goal_x, goal_y

# Function to draw the maze with a border
def draw_maze(maze, cell_size):
    # Draw borders
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 10))  # Top border
    pygame.draw.rect(screen, BLACK, (0, 0, 10, HEIGHT))  # Left border
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 10, WIDTH, 10))  # Bottom border
    pygame.draw.rect(screen, BLACK, (WIDTH - 10, 0, 10, HEIGHT))  # Right border
    
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size))

# Function to draw start and goal
def draw_start_goal(cell_size, goal_x, goal_y, rat_image):
    pygame.draw.rect(screen, BLUE, (0, 0, cell_size, cell_size))  # Start position
    screen.blit(rat_image, (goal_y * cell_size, goal_x * cell_size))  # Corrected rat position

# Function to display "YOU WON!" and "NEXT LEVEL!!!" text
def display_win_message():
    font = pygame.font.Font(None, 80)
    text1 = font.render("YOU WON!", True, ORANGE)
    text2 = font.render("NEXT LEVEL!!!", True, ORANGE)
    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    pygame.display.flip()
    time.sleep(2)  # Pause for 2 seconds

# Load images
cat_image = pygame.image.load('cat.png')
rat_image = pygame.image.load('rat.png')

# Main game loop
level = 1
running = True
while running:
    # Increase the number of boxes and difficulty with each level
    ROWS, COLS = 10 + level * 2, 10 + level * 2
    CELL_SIZE = WIDTH // COLS
    maze = np.ones((ROWS, COLS))  # 1 = wall, 0 = path
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Directions for DFS

    generate_maze(maze, 0, 0, directions)

    cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))
    rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

    agent_x, agent_y = 0, 0
    goal_x, goal_y = get_random_goal(maze)

    level_complete = False
    while not level_complete:
        screen.fill(WHITE)

        # Draw maze, start, goal
        draw_maze(maze, CELL_SIZE)
        draw_start_goal(CELL_SIZE, goal_x, goal_y, rat_image)

        # Draw the cat (agent)
        screen.blit(cat_image, (agent_y * CELL_SIZE, agent_x * CELL_SIZE))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                level_complete = True
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
            display_win_message()  # Show "YOU WON!" and "NEXT LEVEL!!!" on screen
            level_complete = True

    level += 1  # Increase level

pygame.quit()
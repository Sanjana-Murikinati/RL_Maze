import pygame
import numpy as np
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600  # Larger window
CELL_SIZE = WIDTH // 10  # Adjust to fit 10x10 grid
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Maze Game")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)  # Black for maze walls
RED = (255, 0, 0)  # Red for the agent (cat)
BLUE = (0, 0, 255)  # Blue for start
WHITE = (255, 255, 255)  # White for paths

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

# Initialize agent (cat)
agent_x, agent_y = 0, 0

# Function to pick a random goal position (excluding walls)
def get_random_goal():
    while True:
        goal_x = random.randint(0, ROWS-1)
        goal_y = random.randint(0, COLS-1)
        if maze[goal_x, goal_y] == 0 and (goal_x != agent_x or goal_y != agent_y):
            return goal_x, goal_y

goal_x, goal_y = get_random_goal()  # Set initial goal position

# Load images for the agent (cat) and goal (rat)
cat_image = pygame.image.load('cat.png')  # Replace with your actual cat image path
cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))

rat_image = pygame.image.load('rat.png')  # Replace with your actual rat image path
rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

# Function to display a "You Won!" message and restart game
def show_win_message():
    root = tk.Tk()
    root.withdraw()  # Hide main Tkinter window
    messagebox.showinfo("Game Over", "Congratulations! You won the game!")
    root.destroy()

# Function to draw the maze
def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if maze[i, j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to draw Start and Goal
def draw_start_goal():
    pygame.draw.rect(screen, BLUE, (0 * CELL_SIZE, 0 * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Start position
    screen.blit(rat_image, (goal_y * CELL_SIZE, goal_x * CELL_SIZE))  # Place rat at goal

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
        show_win_message()  # Display win message
        goal_x, goal_y = get_random_goal()  # Set new random goal

    clock.tick(30)  # Controls game speed

pygame.quit()

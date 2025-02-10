import pygame
import numpy as np
import random
import time
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Screen settings with padding
WIDTH, HEIGHT = 800, 700
PADDING = 20  # Add padding around the maze
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Maze Game")
clock = pygame.time.Clock()

# Game Constants
ANIMATION_SPEED = 10  # Default animation speed
MIN_DISTANCE_TO_GOAL = 5  # Minimum distance between start and goal
MAX_STEPS = 1000  # Maximum steps per level
INITIAL_MAZE_SIZE = 10  # Starting maze size

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# RL Parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
INITIAL_EPSILON = 0.1
EPSILON_DECAY = 0.95
MIN_EPSILON = 0.01

class QLearningAgent:
    def __init__(self, actions, learning_rate=LEARNING_RATE, discount_factor=DISCOUNT_FACTOR, epsilon=INITIAL_EPSILON):
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.actions = actions
        self.total_reward = 0
        
    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(range(len(self.actions)))
        return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error
        self.total_reward += reward

def calculate_cell_size(rows, cols):
    available_width = WIDTH - (2 * PADDING)
    available_height = HEIGHT - 150 - (2 * PADDING)  # 150 for score panel
    return min(available_width // cols, available_height // rows)

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def check_path_exists(maze, start, goal):
    visited = set()
    queue = [start]
    visited.add(start)
    
    while queue:
        current = queue.pop(0)
        if current == goal:
            return True
            
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)
            
            if (0 <= next_x < maze.shape[0] and 
                0 <= next_y < maze.shape[1] and 
                maze[next_x, next_y] == 0 and 
                next_pos not in visited):
                queue.append(next_pos)
                visited.add(next_pos)
    
    return False

def get_random_goal(maze, start_pos):
    max_attempts = 100
    attempts = 0
    while attempts < max_attempts:
        goal_x = random.randint(0, maze.shape[0] - 1)
        goal_y = random.randint(0, maze.shape[1] - 1)
        
        if (maze[goal_x, goal_y] == 0 and 
            manhattan_distance((goal_x, goal_y), start_pos) >= MIN_DISTANCE_TO_GOAL):
            if check_path_exists(maze, start_pos, (goal_x, goal_y)):
                return goal_x, goal_y
        attempts += 1
    
    # If no suitable goal found, use the furthest reachable point
    return find_furthest_reachable_point(maze, start_pos)

def find_furthest_reachable_point(maze, start):
    visited = set()
    queue = [(start, 0)]
    visited.add(start)
    furthest_point = start
    max_distance = 0
    
    while queue:
        current, dist = queue.pop(0)
        if dist > max_distance:
            max_distance = dist
            furthest_point = current
            
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)
            
            if (0 <= next_x < maze.shape[0] and 
                0 <= next_y < maze.shape[1] and 
                maze[next_x, next_y] == 0 and 
                next_pos not in visited):
                queue.append((next_pos, dist + 1))
                visited.add(next_pos)
    
    return furthest_point

def generate_maze(maze, x, y, directions):
    maze[x, y] = 0
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 1:
            maze[x + dx // 2, y + dy // 2] = 0
            generate_maze(maze, nx, ny, directions)

def draw_maze(maze, cell_size):
    # Calculate maze offset to center it
    maze_width = maze.shape[1] * cell_size
    maze_height = maze.shape[0] * cell_size
    offset_x = (WIDTH - maze_width) // 2
    offset_y = (HEIGHT - 150 - maze_height) // 2  # Consider score panel

    # Draw border
    border_rect = pygame.Rect(offset_x - 2, offset_y - 2, 
                            maze_width + 4, maze_height + 4)
    pygame.draw.rect(screen, BLACK, border_rect)
    
    # Draw maze cells
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            x = offset_x + j * cell_size
            y = offset_y + i * cell_size
            if maze[i, j] == 1:
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))

def draw_ball(x, y, cell_size, color, maze_shape):
    # Calculate maze offset
    maze_width = maze_shape[1] * cell_size
    maze_height = maze_shape[0] * cell_size
    offset_x = (WIDTH - maze_width) // 2
    offset_y = (HEIGHT - 150 - maze_height) // 2

    radius = int(cell_size * 0.4)
    center_x = offset_x + int(y * cell_size + cell_size // 2)
    center_y = offset_y + int(x * cell_size + cell_size // 2)
    
    # Draw main ball
    pygame.draw.circle(screen, color, (center_x, center_y), radius)
    
    # Add shine effect
    shine_radius = int(radius * 0.3)
    shine_offset = int(radius * 0.2)
    pygame.draw.circle(screen, WHITE, 
                      (center_x - shine_offset, center_y - shine_offset), 
                      shine_radius)

def draw_score_info(level, score, steps, epsilon):
    font = pygame.font.Font(None, 36)
    
    # Draw score panel background
    pygame.draw.rect(screen, BLACK, (0, HEIGHT-100, WIDTH, 100))
    
    # Display information
    level_text = font.render(f"Level: {level}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    steps_text = font.render(f"Steps: {steps}", True, WHITE)
    epsilon_text = font.render(f"Exploration Rate: {epsilon:.2f}", True, WHITE)
    
    screen.blit(level_text, (20, HEIGHT-90))
    screen.blit(score_text, (200, HEIGHT-90))
    screen.blit(steps_text, (400, HEIGHT-90))
    screen.blit(epsilon_text, (20, HEIGHT-50))

def draw_speed_control():
    font = pygame.font.Font(None, 24)
    text = font.render("Speed Control: Left/Right Arrow", True, WHITE)
    screen.blit(text, (WIDTH - 250, HEIGHT - 30))

def display_win_message(score):
    font = pygame.font.Font(None, 80)
    text1 = font.render("Level Complete!", True, ORANGE)
    text2 = font.render(f"Score: {score}", True, ORANGE)
    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    pygame.display.flip()
    time.sleep(2)

def main():
    level = 1
    total_score = 0
    running = True
    animation_delay = ANIMATION_SPEED

    # Initialize RL agent
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    agent = QLearningAgent(actions)

    while running:
        ROWS, COLS = INITIAL_MAZE_SIZE + level * 2, INITIAL_MAZE_SIZE + level * 2
        CELL_SIZE = calculate_cell_size(ROWS, COLS)
        maze = np.ones((ROWS, COLS))
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        generate_maze(maze, 0, 0, directions)

        agent_x, agent_y = 0, 0
        goal_x, goal_y = get_random_goal(maze, (agent_x, agent_y))
        steps = 0
        episode_reward = 0

        level_complete = False
        while not level_complete and steps < MAX_STEPS:
            screen.fill(WHITE)
            draw_maze(maze, CELL_SIZE)
            draw_ball(goal_x, goal_y, CELL_SIZE, GOLD, maze.shape)
            draw_ball(agent_x, agent_y, CELL_SIZE, BLUE, maze.shape)
            draw_score_info(level, total_score + episode_reward, steps, agent.epsilon)
            draw_speed_control()
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    level_complete = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        animation_delay = min(50, animation_delay + 5)
                    elif event.key == pygame.K_RIGHT:
                        animation_delay = max(1, animation_delay - 5)

            if not running:
                break

            current_state = (agent_x, agent_y)
            action = agent.get_action(current_state)
            
            dx, dy = actions[action]
            new_x, new_y = agent_x + dx, agent_y + dy
            
            if (0 <= new_x < ROWS and 
                0 <= new_y < COLS and 
                maze[new_x, new_y] == 0):
                agent_x, agent_y = new_x, new_y
                
                if (agent_x, agent_y) == (goal_x, goal_y):
                    reward = 100
                    level_complete = True
                else:
                    reward = -1
            else:
                reward = -5
                
            next_state = (agent_x, agent_y)
            agent.learn(current_state, action, reward, next_state)
            episode_reward += reward
            steps += 1

            pygame.time.wait(animation_delay)

            if level_complete:
                total_score += episode_reward
                display_win_message(total_score)
                level += 1
                agent.epsilon = max(MIN_EPSILON, agent.epsilon * EPSILON_DECAY)

    pygame.quit()

if __name__ == "__main__":
    main()
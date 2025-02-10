import numpy
print(numpy.__version__)
import numpy as np
import random

# Define the maze size (4x4 grid)
maze_size = (4, 4)
goal_state = (3, 3)  # The target position

# Define actions (0: Up, 1: Down, 2: Left, 3: Right)
actions = {
    0: (-1, 0),  # Move Up
    1: (1, 0),   # Move Down
    2: (0, -1),  # Move Left
    3: (0, 1)    # Move Right
}

print("Maze environment initialized successfully!")
import numpy as np
import random

# Define the maze size (4x4 grid)
maze_size = (4, 4)
goal_state = (3, 3)  # The target position

# Define actions (0: Up, 1: Down, 2: Left, 3: Right)
actions = {
    0: (-1, 0),  # Move Up
    1: (1, 0),   # Move Down
    2: (0, -1),  # Move Left
    3: (0, 1)    # Move Right
}
# Initialize Q-table (state_size x actions)
q_table = np.zeros((maze_size[0], maze_size[1], 4))  # 4 actions (up, down, left, right)
# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 1.0  # Start with full exploration
exploration_decay = 0.99
min_exploration = 0.01
episodes = 500  # Number of training episodes
# Training loop
for episode in range(episodes):
    state = (0, 0)  # Start at top-left corner
    done = False

    while not done:
        # Choose action (explore or exploit)
        if random.uniform(0, 1) < exploration_rate:
            action = random.choice(list(actions.keys()))  # Explore randomly
        else:
            action = np.argmax(q_table[state[0], state[1]])  # Exploit best known action

        # Take action and move to new state
        new_state = (state[0] + actions[action][0], state[1] + actions[action][1])

        # Ensure agent stays within the maze boundaries
        new_state = (max(0, min(maze_size[0] - 1, new_state[0])),
                     max(0, min(maze_size[1] - 1, new_state[1])))

        # Reward system
        if new_state == goal_state:
            reward = 100  # Large reward for reaching the goal
            done = True
        else:
            reward = -1  # Small penalty for each step

        # Q-learning update rule
        old_value = q_table[state[0], state[1], action]
        next_max = np.max(q_table[new_state[0], new_state[1]])
        q_table[state[0], state[1], action] = old_value + learning_rate * (reward + discount_factor * next_max - old_value)

        # Move to the new state
        state = new_state

    # Decay exploration rate
    exploration_rate = max(min_exploration, exploration_rate * exploration_decay)

# Print trained Q-table
print("Trained Q-Table:")
print(q_table)
def test_agent():
    state = (0, 0)
    path = [state]

    while state != goal_state:
        action = np.argmax(q_table[state[0], state[1]])  # Choose best action
        new_state = (state[0] + actions[action][0], state[1] + actions[action][1])
        new_state = (max(0, min(maze_size[0] - 1, new_state[0])),
                     max(0, min(maze_size[1] - 1, new_state[1])))
        path.append(new_state)
        state = new_state

    return path

# Run test
optimal_path = test_agent()
print("Optimal Path:", optimal_path)
def print_maze(path):
    maze = np.full(maze_size, ' ')
    
    for position in path:
        maze[position] = '*'
    
    maze[goal_state] = 'G'  # Mark the goal
    maze[0, 0] = 'S'  # Mark the start
    
    for row in maze:
        print(" ".join(row))

print("\nAgent's Path in the Maze:")
print_maze(optimal_path)
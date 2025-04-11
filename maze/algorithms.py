from .state import MazeState, Path, MazeGeneratorFactory, AXIAL_DIRECTIONS
from .logger import LoggerGroup, StateLogger, StepLogger, PathLogger


class Algorithm:
    def run(self) -> None: ...


class RightHandRule(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def run(self) -> None:
        self.maze.logger.newPhase("RightHandRule")
        pos = (1, 1)
        currentDir = 0
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)
        self.path.add(pos)

        while pos != end:
            newDir = (currentDir + 1) % 4
            newPos = (
                pos[0] + RightHandRule.directions[newDir][0],
                pos[1] + RightHandRule.directions[newDir][1],
            )

            if self.maze[newPos] == 0:
                pos = newPos
                currentDir = newDir
                self.path.add(pos)
            else:
                newPos = (
                    pos[0] + RightHandRule.directions[currentDir][0],
                    pos[1] + RightHandRule.directions[currentDir][1],
                )
                if self.maze[newPos] == 0:
                    pos = newPos
                    self.path.add(pos)
                else:
                    currentDir = (currentDir - 1) % 4
            self.maze.logger.endStep(self.maze)


class Tremaux(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)
        # Dictionary to store the number of times each cell is visited.
        # Keys are positions (x, y) and values are counts.
        self.marks = {}

    def run(self) -> None:
        self.maze.logger.newPhase("Tremaux")

        # Starting at the entrance (for example, (1,1)) and setting the exit.
        pos = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)
        self.path.add(pos)
        # Mark the start cell as visited once.
        self.marks[pos] = 1

        while pos != end:
            # Gather valid adjacent positions.
            candidates = []
            for d in AXIAL_DIRECTIONS:
                newPos = (pos[0] + d[0], pos[1] + d[1])
                if self.maze[newPos] == 0:  # check if it is a passage
                    # Get current mark count; unvisited cells have 0.
                    count = self.marks.get(newPos, 0)
                    # We only consider cells visited less than 2 times.
                    if count < 2:
                        candidates.append((count, newPos))

            if candidates:
                # Choose candidate with the lowest mark count (i.e. prefer unvisited)
                candidates.sort(key=lambda x: x[0])
                chosen = candidates[0][1]
                # Increase the mark for the chosen cell.
                self.marks[chosen] = self.marks.get(chosen, 0) + 1
                pos = chosen
                self.path.add(pos)
            else:
                self.path.remove()
                # Backtrack to the previous position.
                pos = self.path.path[-1]

            self.maze.logger.endStep(self.maze)


class BreadthFirst(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def run(self) -> None:
        self.maze.logger.newPhase("BreadthFirst")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Initialize the queue for the BFS and mark the start as visited.
        queue = [start]
        visited = {start: True}

        # Add the starting position to the path.
        self.path.add(start)

        found = False
        # Process the queue until it's empty or the end is found.
        while queue and not found:
            current = queue.pop(0)
            if current == end:
                found = True
                break

            # Explore all neighboring positions.
            for d in BreadthFirst.directions:
                new_pos = (current[0] + d[0], current[1] + d[1])
                # Check if the new position is within maze bounds and is accessible.
                if self.maze[new_pos] == 0 and new_pos not in visited:
                    visited[new_pos] = True
                    queue.append(new_pos)
                    # Add the new position to the path as it is visited.
                    self.path.add(new_pos)

            # Log the state after each step.
            self.maze.logger.endStep(self.maze)


class DepthFirst(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def run(self) -> None:
        self.maze.logger.newPhase("DepthFirst")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Initialize the stack for DFS and mark the start as visited.
        stack = [start]
        visited = {start: True}

        # Add the starting position to the path.
        self.path.add(start)

        while stack:
            current = stack.pop()
            if current == end:
                break

            # Track whether a valid move was found.
            found_move = False

            # Explore all neighboring positions.
            for d in DepthFirst.directions:
                new_pos = (current[0] + d[0], current[1] + d[1])
                # Check if the new position is within maze bounds and is accessible.
                if self.maze[new_pos] == 0 and new_pos not in visited:
                    visited[new_pos] = True
                    stack.append(current)  # Push the current position back for backtracking.
                    stack.append(new_pos)  # Push the new position to explore next.
                    self.path.add(new_pos)  # Add the new position to the path.
                    found_move = True
                    break  # Move to the next position immediately after finding a valid move.

            # If no valid move was found, backtrack by removing the current position from the path.
            if not found_move:
                self.path.remove()

            # Log the state after each step.
            self.maze.logger.endStep(self.maze)


import heapq

class AStar(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def heuristic(self, pos, end):
        # Use Manhattan distance as the heuristic
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    def run(self) -> None:
        self.maze.logger.newPhase("AStar")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Priority queue for A* (min-heap)
        open_set = []
        heapq.heappush(open_set, (0, start))  # (priority, position)

        # Dictionaries to store the cost and path
        g_score = {start: 0}  # Cost from start to the current position
        came_from = {}  # To reconstruct the path

        visited = set()

        # Add the starting position to the path
        self.path.add(start)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            # If we reach the end, stop
            if current == end:
                self.path.add(current)
                break

            # Explore all neighboring positions
            for d in AStar.directions:
                neighbor = (current[0] + d[0], current[1] + d[1])

                # Check if the neighbor is within maze bounds and is accessible
                if self.maze[neighbor] != 0 or neighbor in visited:
                    continue

                # Calculate tentative g_score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update g_score and priority
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

                    # Add the neighbor to the path as it is visited
                    self.path.add(neighbor)

            # Log the state after each step
            self.maze.logger.endStep(self.maze)


class Dijkstra(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def run(self) -> None:
        self.maze.logger.newPhase("Dijkstra")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Priority queue for Dijkstra (min-heap)
        open_set = []
        heapq.heappush(open_set, (0, start))  # (cost, position)

        # Dictionaries to store the cost and path
        g_score = {start: 0}  # Cost from start to the current position
        came_from = {}  # To reconstruct the path

        visited = set()

        # Add the starting position to the path
        self.path.add(start)

        while open_set:
            current_cost, current = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            # If we reach the end, reconstruct the path
            if current == end:
                while current in came_from:
                    self.path.add(current)
                    current = came_from[current]
                self.path.add(start)  # Add the start position
                self.path.path.reverse()  # Reverse the path to start-to-end order
                break

            # Explore all neighboring positions
            for d in Dijkstra.directions:
                neighbor = (current[0] + d[0], current[1] + d[1])

                # Check if the neighbor is within maze bounds and is accessible
                if self.maze[neighbor] != 0 or neighbor in visited:
                    continue

                # Calculate tentative g_score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update g_score and priority
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score, neighbor))
                    came_from[neighbor] = current

                    # Add the neighbor to the path as it is visited
                    self.path.add(neighbor)

            # Log the state after each step
            self.maze.logger.endStep(self.maze)


class RecursiveBacktracking(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)
        self.visited = set()

    def run(self) -> None:
        self.maze.logger.newPhase("RecursiveBacktracking")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Start the recursive backtracking process
        self._backtrack(start, end)

    def _backtrack(self, current, end) -> bool:
        # Add the current position to the path and mark it as visited
        self.path.add(current)
        self.visited.add(current)

        # If we reach the end, return True
        if current == end:
            return True

        # Explore all neighboring positions
        for d in RecursiveBacktracking.directions:
            neighbor = (current[0] + d[0], current[1] + d[1])

            # Check if the neighbor is within maze bounds, accessible, and not visited
            if self.maze[neighbor] == 0 and neighbor not in self.visited:
                # Recursively explore the neighbor
                if self._backtrack(neighbor, end):
                    return True

        # If no valid path is found, backtrack by removing the current position from the path
                self.path.remove()
                return False        
            self.maze.logger.endStep(self.maze)  # Log the step after adding the position

        self.maze.logger.endStep(self.maze)  # Log the step after backtracking


class GreedyBestFirstSearch(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def heuristic(self, pos, end):
        # Use Manhattan distance as the heuristic
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    def run(self) -> None:
        self.maze.logger.newPhase("GreedyBestFirstSearch")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Priority queue for Greedy Best-First Search (min-heap)
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, end), start))  # (priority, position)

        visited = set()

        # Add the starting position to the path
        self.path.add(start)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            # If we reach the end, stop
            if current == end:
                self.path.add(current)
                break

            # Explore all neighboring positions
            for d in GreedyBestFirstSearch.directions:
                neighbor = (current[0] + d[0], current[1] + d[1])

                # Check if the neighbor is within maze bounds and is accessible
                if self.maze[neighbor] != 0 or neighbor in visited:
                    continue

                # Add the neighbor to the priority queue
                heapq.heappush(open_set, (self.heuristic(neighbor, end), neighbor))

                # Add the neighbor to the path as it is visited
                self.path.add(neighbor)

            # Log the state after each step
            self.maze.logger.endStep(self.maze)


import random

class GaussianWalkers(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze, num_walkers=5) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)
        self.num_walkers = num_walkers  # Number of walkers
        self.walkers = []  # List of walker positions
        self.visited = set()

    def run(self) -> None:
        self.maze.logger.newPhase("GaussianWalkers")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Initialize walkers at the starting position
        self.walkers = [start] * self.num_walkers
        self.visited.add(start)
        self.path.add(start)

        while True:
            for i in range(len(self.walkers)):
                current = self.walkers[i]

                # If any walker reaches the end, stop
                if current == end:
                    self.path.add(current)
                    return

                # Generate a list of valid moves
                valid_moves = []
                for d in GaussianWalkers.directions:
                    neighbor = (current[0] + d[0], current[1] + d[1])
                    if self.maze[neighbor] == 0 and neighbor not in self.visited:
                        valid_moves.append(neighbor)

                # If there are valid moves, choose one randomly
                if valid_moves:
                    next_move = random.choice(valid_moves)
                    self.walkers[i] = next_move
                    self.visited.add(next_move)
                    self.path.add(next_move)

                # Log the state after each walker moves
                self.maze.logger.endStep(self.maze)


import numpy as np

class QLearning(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def __init__(self, _maze, *, alpha=0.1, gamma=0.9, epsilon=0.1, episodes=1000) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.episodes = episodes  # Number of episodes for training
        self.q_table = {}  # Q-Table to store state-action values

    def run(self) -> None:
        self.maze.logger.newPhase("QLearning")

        # Define starting and ending positions
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Train the Q-Learning agent
        for episode in range(self.episodes):
            state = start
            self.path.clear()
            self.path.add(state)

            while state != end:
                # Choose an action using epsilon-greedy policy
                action = self._choose_action(state)

                # Take the action and observe the next state and reward
                next_state = (state[0] + QLearning.directions[action][0],
                              state[1] + QLearning.directions[action][1])

                # Check if the next_state is within maze bounds
                if not (0 <= next_state[0] < self.maze.height and 0 <= next_state[1] < self.maze.width):
                    continue  # Skip invalid states

                reward = self._get_reward(next_state, end)

                # Update the Q-Table
                self._update_q_table(state, action, reward, next_state)

                # Move to the next state
                state = next_state
                self.path.add(state)

                # Log the state after each step
                self.maze.logger.endStep(self.maze)

                # If the agent reaches the end, break
                if state == end:
                    break

        # After training, use the learned policy to solve the maze
        self._solve(start, end)

    def _choose_action(self, state):
        # Epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 3)  # Explore: choose a random action
        else:
            # Exploit: choose the action with the highest Q-value
            return np.argmax([self.q_table.get((state, a), 0) for a in range(4)])

    def _get_reward(self, state, end):
        # Check if the state is within maze bounds
        if not (0 <= state[0] < self.maze.height and 0 <= state[1] < self.maze.width):
            return -100  # Penalize for trying to access out-of-bounds cells

        # Reward function: +100 for reaching the end, -1 for every other step
        if state == end:
            return 100
        elif self.maze[state] == 1:  # Penalize hitting a wall
            return -100
        else:
            return -1

    def _update_q_table(self, state, action, reward, next_state):
        # Update Q-Table using the Q-Learning formula
        max_next_q = max([
            self.q_table.get((next_state, a), 0)
            for a in range(4)
            if 0 <= next_state[0] < self.maze.height and 0 <= next_state[1] < self.maze.width
        ])
        current_q = self.q_table.get((state, action), 0)
        self.q_table[(state, action)] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

    def _solve(self, start, end):
        # Use the learned policy to solve the maze
        state = start
        self.path.clear()
        self.path.add(state)

        while state != end:
            # Choose the best action based on the Q-Table
            action = np.argmax([self.q_table.get((state, a), 0) for a in range(4)])
            state = (state[0] + QLearning.directions[action][0],
                     state[1] + QLearning.directions[action][1])
            self.path.add(state)

            # Log the state after each step
            self.maze.logger.endStep(self.maze)
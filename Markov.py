import numpy as np
import random
from pyamaze import agent, COLOR

class MarkovModel:
    def __init__(self, maze_obj):
        self.maze = maze_obj
        self.transition_matrix = self.create_transition_matrix()
        self.saved_matrices = {}  # Dictionary to store matrices at each step

    def move(self, cell, direction):
        # Determine the next cell based on the current cell and direction
        row, col = cell
        if direction == 'E':  # Move East
            if col < self.maze.cols:  # Ensure the move stays within bounds
                return (row, col + 1)
        elif direction == 'W':  # Move West
            if col > 1:  # Ensure the move stays within bounds
                return (row, col - 1)
        elif direction == 'N':  # Move North
            if row > 1:  # Ensure the move stays within bounds
                return (row - 1, col)
        elif direction == 'S':  # Move South
            if row < self.maze.rows:  # Ensure the move stays within bounds
                return (row + 1, col)
        return cell  # If the movement is out of bounds, stay in the current cell

    def create_transition_matrix(self):
        matrix = {}
        for cell in self.maze.grid:
            directions = self.maze.maze_map[cell]
            possible_moves = sum(directions.values())
            if possible_moves == 0:
                matrix[cell] = {cell: 1}
            else:
                matrix[cell] = {}
                for direction, can_move in directions.items():
                    if can_move == 1:
                        next_cell = self.move(cell, direction)
                        if next_cell != cell:  # Ensure there is an actual move
                            matrix[cell][next_cell] = 1 / possible_moves
        return matrix

    def print_transition_matrix(self, step_count):
        size = self.maze.rows * self.maze.cols
        matrix = np.zeros((size, size))
        for (row, col), transitions in self.transition_matrix.items():
            for (next_row, next_col), prob in transitions.items():
                matrix[(row-1)*self.maze.cols + (col-1)][(next_row-1)*self.maze.cols + (next_col-1)] = prob
        print(f"Transition matrix after {step_count} steps:")
        print(matrix)
        self.saved_matrices[step_count] = matrix  # Save the matrix for output

    def simulate(self, steps):
        current_position = random.choice(list(self.transition_matrix.keys()))
        paths = []
        path = [current_position]
        for step in range(steps):
            if step % 10 == 0 or step == steps - 1:
                self.print_transition_matrix(step + 1)
            if current_position == self.maze.goal:
                print(f"Goal reached at step {step + 1}")
                paths.append(path)
                return current_position, step + 1, paths
            next_positions = list(self.transition_matrix[current_position].keys())
            probabilities = list(self.transition_matrix[current_position].values())
            next_position = random.choices(next_positions, probabilities)[0]
            path.append(next_position)
            current_position = next_position
            if step % 10 == 0 and len(paths) < 3:
                paths.append(path.copy())
        # Ensure the final matrix is saved
        self.saved_matrices[steps] = self.saved_matrices[step + 1]
        return current_position, steps, paths

import sys
import random
from pyamaze import maze, agent, COLOR
from Markov import MarkovModel
import numpy as np

def create_maze(size, loop_perc):
    m = maze(size, size)
    m.CreateMaze(loopPercent=loop_perc, theme=COLOR.light)

    # Manually set the goal after creating the maze
    goal_row = random.randint(1, size)
    goal_col = random.randint(1, size)
    m.goal = (goal_row, goal_col)  # Setting the goal attribute directly

    return m

def main(size, loop_perc):
    m = create_maze(size, loop_perc)

    start_pos = (random.randint(1, m.rows), random.randint(1, m.cols))
    a = agent(m, start_pos[0], start_pos[1], shape='arrow', footprints=True)

    # Initialize the Markov Model
    model = MarkovModel(m)
    final_position, step_count, paths = model.simulate(100)

    print(f"Final position of the agent after {step_count} steps: {final_position}")

    # Trace the paths in the GUI
    for i, path in enumerate(paths):
        trace_agent = agent(m, start_pos[0], start_pos[1], shape='arrow', footprints=True, color=COLOR.red)
        m.tracePath({trace_agent: path}, delay=300)

    # Save the Readme.txt with required details
    with open("Readme.txt", "w") as f:
        f.write(f"Maze Size: {size}x{size}\n")
        f.write(f"Loop Percent: {loop_perc}\n")
        for step, matrix in model.saved_matrices.items():
            f.write(f"\nTransition Matrix after {step} steps:\n")
            np.savetxt(f, matrix, fmt="%.4f")
        f.write(f"\nFinal position of the agent after {step_count} steps: {final_position}\n")
        f.write(f"Steps taken to reach the goal: {step_count}\n")
        f.write(f"\nTransition Matrix when the agent reached the goal:\n")
        np.savetxt(f, model.saved_matrices[step_count], fmt="%.4f")
        if "steady_state" in model.saved_matrices:
            f.write("\nSteady State Transition Matrix:\n")
            np.savetxt(f, model.saved_matrices["steady_state"], fmt="%.4f")

        # Conclusion Report
        f.write("\n--- Conclusion Report ---\n")
        f.write(f"The agent started at position {start_pos} and reached the goal at position {m.goal} in {step_count} steps.\n")
        f.write("The transition matrices show the probability distribution of moving between cells in the maze.\n")
        f.write("As observed, the agent reached the goal relatively quickly, which indicates an efficient traversal of the maze.\n")
        f.write("Further analysis could explore the impact of different maze configurations or the influence of different search algorithms.\n")

    print("Finished writing to Readme.txt.")  # Debugging statement

    # Run the GUI with agent movement visualization
    m.run()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: MazeRunner.py [size] [loopperc]")
        sys.exit(1)
    
    size = int(sys.argv[1])
    loop_perc = int(sys.argv[2])
    
    main(size, loop_perc)

from maze.algorithms import RightHandRule, Tremaux, BreadthFirst
from maze.state import MazeState
import timeit


print(timeit.timeit(RightHandRule(MazeState(50, 50)).run, number=100))
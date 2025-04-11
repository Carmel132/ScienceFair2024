
from maze.algorithms import RightHandRule, Tremaux, BreadthFirst
from maze.state import MazeState, MazeGeneratorFactory
import timeit
import time
import matplotlib.pyplot as plt

def generateMaze(size) -> MazeState:
    return MazeGeneratorFactory(MazeState(size[0], size[1]), time.time()).generate()
def testAlgo(algo, sz, n=30):
    return timeit.timeit(algo(generateMaze((sz,sz))).run, number=n)

xx = [1, 10, 20, 40]
yy1 = [testAlgo(RightHandRule, i) for i in xx]
yy2 = [testAlgo(Tremaux, i) for i in xx]
yy3 = [testAlgo(BreadthFirst, i) for i in xx]
plt.plot(xx, yy1, label="RightHandRule")
plt.plot(xx, yy2, label="Tremaux")
plt.plot(xx, yy3, label="BreadthFirst")
plt.show()

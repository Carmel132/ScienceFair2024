from logger import MazeAction


# Outputs a MazeAction list to a text file
def out(dim: tuple[int, int], log: list[MazeAction], filename="out.txt"):
    with open(filename, "w+") as file:
        file.write("DIM: " + str(dim) + "\n")
        file.write("\n".join(map(repr, log)))


from logger import LoggerGroup, StateLogger, StepLogger
from state import MazeState, MazeGeneratorFactory

s = LoggerGroup(StateLogger(), StepLogger())
m = MazeState(5, 6, _logger=s)
MazeGeneratorFactory(m, 4).generate()
out((5, 6), s.log)

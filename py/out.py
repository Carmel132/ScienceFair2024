from logger import (
    LoggerGroup,
    StateLogger,
    StepLogger,
    PathLogger,
    MazeAction,
    PhaseLogger,
)
from state import MazeState, MazeGeneratorFactory
from algorithms import RightHandRule


# Outputs a MazeAction list to a text file
def out(dim: tuple[int, int], log: list[MazeAction], filename="out.txt"):
    with open(filename, "w+") as file:
        file.write("DIM: " + str(dim) + "\n")
        file.write("\n".join(map(repr, log)))


s = LoggerGroup(PhaseLogger(), StateLogger(), PathLogger(), StepLogger())
m = MazeState(6, 5, _logger=s)
MazeGeneratorFactory(m, 4).generate()
RightHandRule(m).run()

out((m.width, m.height), s.log, "../out.txt")

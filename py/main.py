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

s = LoggerGroup(PhaseLogger(), StateLogger(), PathLogger(), StepLogger())
m = MazeState(6, 5, _logger=s)
MazeGeneratorFactory(m, 4).generate()
RightHandRule(m).run()

print(s.log)

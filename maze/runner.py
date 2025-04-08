from .logger import LoggerGroup, StateLogger, MazeAction
from .state import MazeState, MazeGeneratorFactory


# Runs MazeActions in order on maze
class Runner:
    def __init__(self, _start: MazeState, _log: list[MazeAction]) -> None:
        self.log: list[MazeAction] = _log
        self.idx: int = 0
        self.state: MazeState = _start

    def next(self) -> MazeState:
        if self.idx >= len(self.log):
            return self.state
        self.idx += 1
        self.log[self.idx].run(self.state)
        return self.state

    def back(self) -> MazeState:
        if self.idx <= 0:
            return self.state
        self.idx -= 1
        self.log[self.idx].reverse(self.state)
        return self.state

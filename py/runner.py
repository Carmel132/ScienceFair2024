from logger import LoggerGroup, StateLogger, MazeAction
from state import MazeState, MazeGeneratorFactory


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


s = LoggerGroup(StateLogger())
m = MazeState(5, 5, s)
MazeGeneratorFactory(m, 1).generate()
import os

r = Runner(MazeState(5, 5, s), s.log)
for i in range(100):
    # os.system("cls" if os.name == "nt" else "clear")
    print(r.state)
    inp = input("\ninput: ")
    if inp == "d":
        print("hi")
        r.next()
    else:
        print("hello")
        r.back()

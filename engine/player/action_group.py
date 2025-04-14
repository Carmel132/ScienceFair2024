from maze.state import MazeState
from maze.logger import MazeAction


class ActionPlayer:
    # next action
    def next(self) -> None: ...
    # previous action
    def prev(self) -> None: ...
    # go to start by acting
    def start(self) -> None: ...
    # go to end
    def end(self) -> None: ...
    # returns whether the player is ready to end and allow the playing of the following player
    def isAtEnd(self) -> bool: ...
    # returns element at the current index
    def getCurrent(self) -> object: ...


class MazeActionPlayer(ActionPlayer):
    def __init__(self, _maze: MazeState, *_actions: MazeAction) -> None:
        self.actions = _actions
        self.maze = _maze
        self.idx = 0

    def next(self) -> None:
        if self.idx >= len(self.actions):
            return
        self.actions[self.idx].run(self.maze)
        self.idx += 1

    def prev(self) -> None:
        if self.idx <= 0:
            return
        self.idx -= 1
        self.actions[self.idx].reverse(self.maze)

    def start(self) -> None:
        while self.idx > 0:
            self.prev()

    def end(self) -> None:
        while self.idx < len(self.actions) - 1:
            self.next()

    def isAtEnd(self) -> bool:
        return self.idx >= len(self.actions)

    def getCurrent(self):
        if self.idx >= len(self.actions):
            return self.actions[-1]
        return self.actions[self.idx]


class ActionPlayerGroup(ActionPlayer):
    def __init__(self, *_actionsPlayers: ActionPlayer) -> None:
        self.actionPlayers = _actionsPlayers
        self.idx = 0

    def next(self) -> None:
        if self.idx >= len(self.actionPlayers): return
        if self.actionPlayers[self.idx].isAtEnd():
            self.idx += 1

        self.actionPlayers[self.idx].next()

        if self.actionPlayers[self.idx].isAtEnd():
            self.idx += 1
            return

    def prev(self) -> None:
        if self.idx <= 0:
            return
        self.actionPlayers[self.idx].prev()
        self.idx -= 1

    def start(self) -> None:
        while self.idx > 0:
            self.prev()

    def end(self) -> None:
        while self.idx < len(self.actionPlayers) - 1:
            self.next()

    def isAtEnd(self) -> bool:
        return self.idx >= len(self.actionPlayers)

    def getCurrent(self) -> ActionPlayer:
        if (self.idx >= len(self.actionPlayers)):
            return self.actionPlayers[-1]
        return self.actionPlayers[self.idx]

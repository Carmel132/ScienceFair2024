from engine.player.action_group import ActionPlayer, MazeActionPlayer, ActionPlayerGroup
from maze.logger import MazeAction, PhaseDivider

# Each step will be combined into an [MazeActionGroup]. This array will be divided by phases,
# and each phase will be encapsulated into
# a [MazeActionPlayer]. Lastly, the phases will be combined into one [ActionPlayerGroup]


class PhasePlayer(ActionPlayerGroup):
    def __init__(self, _phase: PhaseDivider, *_actions: ActionPlayerGroup):
        self.phase = _phase
        super().__init__(*_actions)


def logToPhases(log: list[MazeAction]) -> list[tuple[PhaseDivider, list[MazeAction]]]:
    phases: list[tuple[PhaseDivider, list[MazeAction]]] = []
    for action in log:
        if action.TYPE == MazeAction.ActionTypes.PHASEDIVIDER:
            phases.append((action, []))
            continue

        phases[-1][1].append(action)
    return phases

def phasesToSteps(phases: list[tuple[PhaseDivider, list[MazeAction]]]) -> list[tuple[PhaseDivider, list[list[MazeAction]]]]

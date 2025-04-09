from engine.player.action_group import ActionPlayer, MazeActionPlayer, ActionPlayerGroup
from maze.logger import MazeAction, PhaseDivider
from maze.state import MazeState
# Each step will be combined into an [MazeActionGroup]. This array will be divided by phases,
# and each phase will be encapsulated into
# a [MazeActionPlayer]. Lastly, the phases will be combined into one [ActionPlayerGroup]


class PhasePlayer(ActionPlayerGroup):
    def __init__(self, _phase: PhaseDivider, _actions: ActionPlayerGroup):
        self.phase = _phase
        super().__init__(*_actions.actionPlayers)


def _logToPhases(log: list[MazeAction]) -> list[tuple[PhaseDivider, list[MazeAction]]]:
    phases: list[tuple[PhaseDivider, list[MazeAction]]] = []
    for action in log:
        if action.TYPE == MazeAction.ActionTypes.PHASEDIVIDER:
            phases.append((action, []))
            continue

        phases[-1][1].append(action)
    return phases


def _phasesToSteps(
    phases: list[tuple[PhaseDivider, list[MazeAction]]],
) -> list[tuple[PhaseDivider, list[list[MazeAction]]]]:
    ret: list[tuple[PhaseDivider, list[list[MazeAction]]]] = []
    for phase in phases:
        newPhase = (phase[0], [[]])
        for action in phase[1]:
            if action.TYPE == MazeAction.ActionTypes.STEPDIVIDER:
                newPhase[1].append([])
                continue
            newPhase[1][-1].append(action)

        ret.append(newPhase)
    return ret


def _stepsToPlayer(
    maze: MazeState, steps: list[tuple[PhaseDivider, list[list[MazeAction]]]]
) -> ActionPlayerGroup:
    phasePlayers: list[PhasePlayer] = []
    for phase in steps:
        phasePlayers.append(
            PhasePlayer(
                phase[0],
                ActionPlayerGroup(
                    *map(lambda actions: MazeActionPlayer(maze, *actions), phase[1])
                ),
            )
        )
    return ActionPlayerGroup(*phasePlayers)


def generatePhasePlayer(maze: MazeState, log: list[MazeAction]) -> ActionPlayerGroup:
    return _stepsToPlayer(maze, _phasesToSteps(_logToPhases(log)))

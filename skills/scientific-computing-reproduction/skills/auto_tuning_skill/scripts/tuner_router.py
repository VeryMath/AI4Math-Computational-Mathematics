from __future__ import annotations

from skills.auto_tuning_skill.scripts.parameter_space import ParameterSpace


def choose_tuner(space: ParameterSpace) -> str:
    continuous = sum(1 for param in space.parameters.values() if param.kind == "float")
    if len(space.parameters) <= 3 and continuous == 0:
        return "grid_search"
    if len(space.parameters) <= 2 and continuous <= 1:
        return "grid_search"
    return "random_search"

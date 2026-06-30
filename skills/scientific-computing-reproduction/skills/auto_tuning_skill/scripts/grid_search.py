from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from skills.auto_tuning_skill.scripts.parameter_space import load_parameter_space, ParameterSpace


def _values(param) -> list:
    if param.kind in {"categorical", "bool"}:
        return list(param.values if param.values is not None else [False, True])
    lo, hi = param.range
    if param.kind == "int":
        return [int(lo), int(hi)] if int(lo) != int(hi) else [int(lo)]
    return [float(lo), float(hi)] if float(lo) != float(hi) else [float(lo)]


def generate_grid(space: ParameterSpace, max_experiments: int = 50) -> list[dict]:
    names = list(space.parameters)
    products = itertools.product(*[_values(space.parameters[name]) for name in names])
    experiments = []
    for combo in products:
        experiments.append(dict(zip(names, combo)))
        if len(experiments) >= max_experiments:
            break
    return experiments


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--space", required=True)
    parser.add_argument("--max-experiments", type=int, default=50)
    args = parser.parse_args()
    print(json.dumps(generate_grid(load_parameter_space(Path(args.space)), args.max_experiments), indent=2))


if __name__ == "__main__":
    main()

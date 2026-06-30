from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from skills.auto_tuning_skill.scripts.parameter_space import ParameterSpace, load_parameter_space


def _sample(param, rng: random.Random):
    if param.kind == "categorical":
        return rng.choice(param.values)
    if param.kind == "bool":
        return bool(rng.choice(param.values if param.values is not None else [False, True]))
    lo, hi = param.range
    if param.scale == "log":
        value = math.exp(rng.uniform(math.log(float(lo)), math.log(float(hi))))
    else:
        value = rng.uniform(float(lo), float(hi))
    if param.kind == "int":
        return int(round(value))
    return float(value)


def generate_random(space: ParameterSpace, budget: int, random_seed: int = 0) -> list[dict]:
    rng = random.Random(random_seed)
    return [{name: _sample(param, rng) for name, param in space.parameters.items()} for _ in range(budget)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--space", required=True)
    parser.add_argument("--budget", type=int, default=20)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(generate_random(load_parameter_space(Path(args.space)), args.budget, args.random_seed), indent=2))


if __name__ == "__main__":
    main()

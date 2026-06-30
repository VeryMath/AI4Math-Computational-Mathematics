from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Parameter:
    kind: str
    range: list | None = None
    scale: str = "linear"
    values: list | None = None


@dataclass
class ParameterSpace:
    parameters: dict[str, Parameter]


def load_parameter_space(path: Path | str) -> ParameterSpace:
    data = yaml.safe_load(Path(path).read_text())
    params = data.get("parameters") or data.get("tuning", {}).get("parameter_space") or {}
    parsed = {}
    for name, spec in params.items():
        parsed[name] = Parameter(
            kind=spec["type"],
            range=spec.get("range"),
            scale=spec.get("scale", "linear"),
            values=spec.get("values"),
        )
    return ParameterSpace(parsed)


def as_serializable(space: ParameterSpace) -> dict:
    return {"parameters": {name: vars(param) for name, param in space.parameters.items()}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--space", required=True)
    args = parser.parse_args()
    print(json.dumps(as_serializable(load_parameter_space(args.space)), indent=2))


if __name__ == "__main__":
    main()

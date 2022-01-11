from collections import defaultdict
from pathlib import Path
import shlex
from typing import List, Dict, Optional, Union, Tuple

from pydantic import BaseModel, validator, validators, root_validator

from opensafely.core.parse import parse_yaml_file


class Expectations(BaseModel):
    population_size: int = 1000


class Outputs(BaseModel):
    highly_sensitive: Optional[Dict[str, str]]
    moderately_sensitive: Optional[Dict[str, str]]
    minimally_sensitive: Optional[Dict[str, str]]

    @root_validator()
    def at_least_one_output(cls, outputs):
        if not any(outputs.values()):
            raise ValueError(
                f"must specify at least one output of: {', '.join(outputs)}"
            )
        return outputs


class Command(BaseModel):
    run: str  # original string
    name: str
    version: str
    args: str

    class Config:
        # this makes Command hashable, which for some reason due to the
        # parse_run_string works, pydantic requires.
        frozen = True


class Action(BaseModel):
    run: Command
    needs: Optional[List[str]] = []
    outputs: Outputs

    @validator("run", pre=True)
    def parse_run_string(cls, run):
        parsed = {}
        parts = shlex.split(run)
        name, _, version = parts[0].partition(":")
        args = " ".join(parts[1:])
        return Command(
            run=run,
            name=name,
            version=version,
            args=args,
        )


class Pipeline(BaseModel):
    version: Union[str, float]
    expectations: Expectations
    actions: Dict[str, Action]

    @validator("actions")
    def validate_unique_commands(cls, actions):
        seen = defaultdict(list)
        for name, action in actions.items():
            run = action.run
            if run in seen:
                raise ValueError(
                    f"Action {name} has the same 'run' command as other actions: {' ,'.join(seen[run])}"
                )
            seen[run].append(name)
        return actions

    @validator("actions")
    def validate_needs_exist(cls, actions):
        missing = []
        for name, action in actions.items():
            for need in action.needs:
                if need not in actions:
                    missing.append(need)
        if missing:
            raise ValueError(
                f"Action {name} has the same 'run' command as other actions: {' ,'.join(seen[run])}"
            )
        return actions



def load_pipeline(project_yaml):
    try:
        pipeline_data = parse_yaml_file(Path(project_yaml))
    except Exception as exc:
        breakpoint()
        raise

    try:
        return Pipeline(**pipeline_data)
    except Exception:
        raise
 

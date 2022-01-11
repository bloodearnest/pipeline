from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.error import MarkedYAMLError, MarkedYAMLFutureWarning


# We use "safe" to avoid malicious inputs, and "rt" (round-trip) in order to
# have detailed line number information to help generate better error message
# We also use the pure-Python version here as we don't care about speed
# and it gives better error messages (and consistent behaviour
# cross-platform)
PARSER = YAML(typ=["safe", "rt"], pure=True)


class YAMLError(Exception):
    pass


def file_context_filename(exc, filename):
    try:
        exc.context_mark.name = filename
    except AttributeError:
        pass
    try:
        exc.problem_mark.name = filename
    except AttributeError:
        pass


def parse_yaml_file(yaml_data, filename=None):
    try:
        return PARSER.load(yaml_data)
    except Exception as exc:
        # TODO: skip this if debug switched on?
        if hasattr(exc, "note"):
            exc.note = None
        if hasattr(exc, "warn"):
            exc.warn = None
        
        if filename and isinstance(yaml_data, (str, bytes)):
            try:
                exc.context_mark.name = filename
            except AttributeError:
                pass
            try:
                exc.problem_mark.name = filename
            except AttributeError:
                pass

        # wrap in our error
        raise YAMLError(str(exc)) from exc

import subprocess
import re

PROPERTY_RE = re.compile(r'^\s*(\S+)\s*=\s*(\S+)\s*$')


def read_props() -> dict:
    lines = subprocess.getoutput('synclient').splitlines()[1:]
    return {k: float(v) if '.' in v else int(v) for (k, v) in [
        PROPERTY_RE.match(line).groups() for line in lines
    ]}


def write_props(props: dict):
    subprocess.check_call([
        'synclient',
        *[f'{k}={v}' for [k, v] in props.items()],
    ])

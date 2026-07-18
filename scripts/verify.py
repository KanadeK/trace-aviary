from __future__ import annotations

import subprocess
import sys
from os import environ

COMMANDS = [
    [sys.executable, "-m", "ruff", "check", "."],
    [sys.executable, "-m", "mypy", "src"],
    [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "pytest_cov",
        "-q",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
    ],
    [sys.executable, "-m", "build"],
]


def main() -> None:
    environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    for command in COMMANDS:
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()

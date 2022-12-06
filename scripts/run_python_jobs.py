#!/usr/bin/env python3

import subprocess
import tomli
import sys


def output(*line):
    if not line:
        print()
        return
    print("\033[94m" + line[0], *line[1:], "\033[0m")


def get_python_workspaces():
    with open("pyproject.toml", mode="rb") as f:
        pyproject = tomli.load(f)
        return pyproject["tool"]["poetry"]["group"]["workspaces"][
            "dependencies"
        ].items()


def run_task(*args, **kwargs):
    task = subprocess.run(*args, **kwargs)
    if task.returncode:
        sys.exit(1)


def run_poetry_task(workspace_path):
    output("Running poetry check")
    run_task(["poetry", "check"], cwd=workspace_path)
    output("Writing poetry lock file")
    run_task(["poetry", "lock", "--no-update"], cwd=workspace_path)


def run_black_task(workspace_path):
    output("Running black")
    run_task(["black", workspace_path])


def run_isort_task(workspace_path):
    output("Running isort")
    run_task(["isort", workspace_path])


def main():
    for workspace in get_python_workspaces():
        name, spec = workspace
        output("Running jobs for", name)
        path = spec["path"]
        run_poetry_task(path)
        run_isort_task(path)
        run_black_task(path)

    output("Running jobs for root")
    run_poetry_task(".")


if __name__ == "__main__":
    main()

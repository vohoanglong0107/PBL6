#!/usr/bin/env python3

import subprocess
import tomli


def output(*line):
    if not line:
        print()
        return
    print("\033[94m" + line[0], *line[1:], "\033[0m")


def run_poetry_task(workspace_name, workspace_path):
    output("Running poetry jobs for", workspace_name)
    output("Running check")
    subprocess.run(["poetry", "check"], cwd=workspace_path)
    output("Writing lock file")
    subprocess.run(["poetry", "lock", "--no-update"], cwd=workspace_path)


def main():
    with open("pyproject.toml", mode="rb") as f:
        pyproject = tomli.load(f)
        for workspaces in pyproject["tool"]["poetry"]["group"]["workspaces"][
            "dependencies"
        ].items():
            name, spec = workspaces
            path = spec["path"]
            run_poetry_task(name, path)

    run_poetry_task("root", ".")


if __name__ == "__main__":
    main()

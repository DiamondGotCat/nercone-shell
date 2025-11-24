#!/usr/bin/env python3

# -- nercone-shell ---------------------------------------------- #
# __main__.py on Nersh                                            #
# Made by DiamondGotCat, Licensed under MIT License               #
# Copyright (c) 2025 DiamondGotCat                                #
# ---------------------------------------------- DiamondGotCat -- #

import os
import sys
import re
import json
import glob
import shutil
import getpass
import readline
import subprocess
from pathlib import Path
from nercone_modern.color import ModernColor
from importlib.metadata import version, PackageNotFoundError

try:
    VERSION: str = version("nercone-shell")
except PackageNotFoundError:
    VERSION: str = "0.0.0"
ENVIRONMENT: dict = {}
NERSH_AUTORUN: str = os.environ.get("NERSH_AUTORUN", None)
NERSH_PATH = Path(os.environ.get("NERSH_PATH", str(Path(Path("~").expanduser(), ".nercone", "nercone-shell"))))
NERSH_HISTORY_PATH = Path(os.environ.get("NERSH_HISTORY_PATH", str(Path(NERSH_PATH, "history.txt"))))
NERSH_CONFIG: dict = {}
NERSH_CONFIG_PATH = Path(os.environ.get("NERSH_CONFIG_PATH", str(Path(NERSH_PATH, "config.json"))))
NERSH_CONFIG_DEFAULT: dict = {
    "customization": {
        "show_version": True,
        "override_env": {
            "SHELL": f"{shutil.which('nersh')}"
        },
        "autoruns": [
            f"{Path(NERSH_PATH, 'autostart.sh')}"
        ]
    },
    "compatibility": {
        "report_invisible_characters": False
    }
}

class NershCompleter:
    def __init__(self):
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            full_line = readline.get_line_buffer()
            line_to_cursor = full_line[:readline.get_begidx()]
            if not line_to_cursor.strip() and ' ' not in text:
                self.matches = self._complete_command(text)
            else:
                self.matches = self._complete_path(text)

        try:
            return self.matches[state]
        except IndexError:
            return None

    def _complete_command(self, text):
        results = set()

        builtins = ['cd', 'exit']
        for cmd in builtins:
            if cmd.startswith(text):
                results.add(cmd + " ")

        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        for p in path_dirs:
            if not os.path.isdir(p):
                continue
            try:
                for filename in os.listdir(p):
                    if filename.startswith(text):
                        results.add(filename + " ")
            except (PermissionError, OSError):
                continue

        return sorted(list(results))

    def _complete_path(self, text):
        expanded_text = os.path.expanduser(text)

        current_pwd = ENVIRONMENT.get("PWD", os.getcwd())
        
        if os.path.isabs(expanded_text):
            search_pattern = expanded_text + "*"
        else:
            search_pattern = os.path.join(current_pwd, expanded_text + "*")

        glob_matches = glob.glob(search_pattern)

        results = []
        for match in glob_matches:
            if os.path.isdir(match):
                display_match = match + "/"
            else:
                display_match = match + " "

            if not os.path.isabs(expanded_text) and not text.startswith("~"):
                rel_path = os.path.relpath(match, current_pwd)
                if os.path.isdir(match):
                    rel_path += "/"
                else:
                    rel_path += " "
                results.append(rel_path)
            elif text.startswith("~"):
                home = os.path.expanduser("~")
                if match.startswith(home):
                    rel_home = "~" + match[len(home):]
                    if os.path.isdir(match):
                        rel_home += "/"
                    else:
                        rel_home += " "
                    results.append(rel_home)
                else:
                    results.append(display_match)
            else:
                results.append(display_match)

        return sorted(results)

def shorten_path(path: str) -> str:
    path = os.path.abspath(path)
    home = os.path.expanduser('~')
    if path.startswith(home):
        rel = os.path.relpath(path, home)
        if rel == ".":
            return "~"
        parts = rel.split("/")
        prefix = "~"
    else:
        parts = path.strip("/").split("/")
        prefix = "/"
    if len(parts) > 1:
        shortened = [p[0] for p in parts[:-1]]
        shortened.append(parts[-1])
        path_str = "/".join(shortened)
    elif parts:
        path_str = parts[0]
    else:
        path_str = ""
    if prefix == "~":
        return f"~/{path_str}"
    elif prefix == "/":
        return f"/{path_str}"
    return path_str

def show_version():
    print(f"Nersh v{VERSION}")

def reset():
    global ENVIRONMENT, NERSH_CONFIG
    ENVIRONMENT = {"PWD": f"{Path(Path("~").expanduser())}"}
    NERSH_CONFIG = {}
    reload()

def reload():
    global ENVIRONMENT
    load_config()
    pwd = ENVIRONMENT.get("PWD")
    ENVIRONMENT |= os.environ
    ENVIRONMENT |= {"PWD": pwd}
    ENVIRONMENT |= NERSH_CONFIG.get("customization", {}).get("override_env", {})

def load_config() -> dict:
    global NERSH_CONFIG
    NERSH_PATH.mkdir(parents=True, exist_ok=True)
    if not NERSH_CONFIG_PATH.is_file():
        with NERSH_CONFIG_PATH.open("w") as f:
            f.write(json.dumps(NERSH_CONFIG_DEFAULT, indent=4) + "\n")
    with NERSH_CONFIG_PATH.open("r") as f:
        NERSH_CONFIG |= json.loads(f.read())
    for p in NERSH_CONFIG.get("customization", {}).get("autoruns", []):
        if not Path(p).is_file():
            with Path(p).open("w") as f:
                f.write("\n")
    return NERSH_CONFIG

def run_line(command: str) -> int:
    def expand_vars(match):
        key = match.group(1) or match.group(2)
        return ENVIRONMENT.get(key, "")
    if command.strip():
        command = re.sub(r'\$(\w+)|\$\{(\w+)\}', expand_vars, command)
    args = command.strip().split(" ")
    cmd = args[0]
    if cmd == "version":
        show_version()
    elif cmd == "reset":
        reset()
    elif cmd == "reload":
        reload()
    elif cmd == "cd":
        target = " ".join(args[1:])
        if not target:
            ENVIRONMENT["PWD"] = f"{Path("~").expanduser()}"
        target = os.path.expanduser(target)
        target_path = Path(target)
        if not target_path.is_absolute():
            target_path = Path(ENVIRONMENT["PWD"]) / target_path
        try:
            resolved_path = target_path.resolve()
            if resolved_path.is_dir():
                ENVIRONMENT["PWD"] = str(resolved_path)
            elif resolved_path.exists():
                print(f"Not a directory: {target}")
            else:
                print(f"Not exist: {target}")
        except FileNotFoundError:
            print(f"Not exist: {target}")
    elif cmd == "export":
        content = command.strip()[6:].strip()
        if "=" in content:
            key, value = content.split("=", 1)
            if len(value) >= 2 and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")):
                value = value[1:-1]
            ENVIRONMENT[key] = value
        else:
            if not content:
                for k, v in ENVIRONMENT.items():
                    print(f"{k}={v}")
    elif cmd == "source" or cmd == ".":
        if len(args) < 2:
            print(f"{cmd}: filename argument required")
            return 1
        target = args[1]
        target_path = Path(os.path.expanduser(target))
        if not target_path.is_absolute():
            target_path = Path(ENVIRONMENT.get("PWD")) / target_path
        if target_path.is_file():
            try:
                with target_path.open("r") as f:
                    for line in f:
                        if line.strip() and not line.strip().startswith("#"):
                            run_line(line)
            except Exception as e:
                print(f"nersh: {e}")
                return 1
        else:
            print(f"nersh: {target}: No such file")
            return 1
    elif cmd == "exit":
        readline.write_history_file(str(NERSH_HISTORY_PATH))
        try:
            raise SystemExit(int(args[1]))
        except IndexError:
            raise SystemExit(0)
    else:
        process = subprocess.run(command, cwd=ENVIRONMENT.get("PWD", None), env=ENVIRONMENT, shell=True, encoding="utf-8", stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        return process.returncode

def run_script(script: str):
    for line in script.split('\n'):
        run_line(line)

def main() -> int:
    reset()
    completer = NershCompleter()
    readline.set_completer(completer.complete)
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(' \t\n;')
    if NERSH_CONFIG.get("customization", {}).get("show_version", True):
        show_version()
    for p in NERSH_CONFIG.get("customization", {}).get("autoruns", []):
        if Path(p).is_file():
            with Path(p).open("r") as f:
                run_script(f.read())
        elif Path(p).exists():
            print(f"(autorun failed) Not a file: {p}")
        else:
            print(f"(autorun failed) Not exist: {p}")
    if NERSH_AUTORUN:
        run_script(NERSH_AUTORUN)
    if NERSH_HISTORY_PATH.is_file():
        readline.read_history_file(NERSH_HISTORY_PATH)
    RL_PROMPT_START_IGNORE = "\001" if NERSH_CONFIG.get("compatibility", {}).get("report_invisible_characters", False) else ""
    RL_PROMPT_END_IGNORE = "\002" if NERSH_CONFIG.get("compatibility", {}).get("report_invisible_characters", False) else ""
    color_green = f"{RL_PROMPT_START_IGNORE}{ModernColor.color('green')}{RL_PROMPT_END_IGNORE}"
    color_reset = f"{RL_PROMPT_START_IGNORE}{ModernColor.color('reset')}{RL_PROMPT_END_IGNORE}"
    while True:
        try:
            run_line(input(f"{color_green}{getpass.getuser()}{color_reset}@{os.uname()[1].rsplit('.', 1)[0]} {color_green}{shorten_path(ENVIRONMENT.get('PWD', f'{Path('~').expanduser()}'))}{color_reset}> "))
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            break

if __name__ == "__main__":
    main()

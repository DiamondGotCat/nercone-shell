
<img width="1240" alt="Screenshot" src="https://github.com/user-attachments/assets/e4f2ea8d-9ec0-465d-8d49-9bd7763e0283" />

# Nersh (Nercone Shell)
Modern shell for Developers

## Requiments
- CPython 3.9+
- `uv` [PyPI↗︎](https://pypi.org/project/uv/) or `pip3` [PyPI↗︎](https://pypi.org/project/pip/) 
- `nercone-modern` [PyPI↗︎](https://pypi.org/project/nercone-modern/)

## Installation

### using uv (recommended)
```
uv tool install nercone-shell
```

### using pip3

**System Python:**
```
pip3 install nercone-shell --break-system-packages
```

**Venv Python:**
```
pip3 install nercone-shell
```

## Update

### using uv (recommended)
```
uv tool install nercone-shell --upgrade
```

### using pip3

**System Python:**
```
pip3 install nercone-shell --upgrade --break-system-packages
```

**Venv Python:**
```
pip3 install nercone-shell --upgrade
```

## Usage
```
nersh
```

## Configuration
The configuration file is usually located at `~/.nercone/nercone-shell/config.json`.
If the file does not exist when Nersh starts, it will be automatically created.

The following is the default configuration file:
```json
{
    "customization": {
        "show_version": true,
        "accent_color": "blue",
        "override_env": {
            "SHELL": "None"
        },
        "autoruns": [
            "<path to home directory>/.nercone/nercone-shell/autostart.sh"
        ]
    },
    "compatibility": {
        "report_invisible_characters": false
    },
    "experimental": {
        "command_history": false
    }
}
```

### Customization
These settings customize the behavior of Nersh.
- `show_version`: Sets whether to display version information at startup.
- `accent_color`: Accent color used for prompts etc.
- `override_env`: Sets the environment variables you want to set at startup in dictionary format.
- `autoruns`: Sets the shell scripts you want to run at startup in array format.

### Compatibility
These settings allows Nersh to function properly in special environments.
- `report_invisible_characters`: A Boolean value that enables reporting of invisible characters to readline, which is necessary in some environments, such as Linux without a GUI (TUI only).

### Experimental
The Experimental setting is used to enable experimental features.
It enables new features that are incomplete, have many bugs, or have unfixable bugs.
Some features are difficult to completely disable, so they are effectively disabled. (Bugs in external libraries/modules, etc.)

- `command_history` The readline command history feature.
    - It was marked as an experimental feature because there were frequent issues with the layout collapsing when retracing the history.
    - Since cannot to find a way to disable the history feature in the readline module, it is effectively disabled by clearing the history after each input.

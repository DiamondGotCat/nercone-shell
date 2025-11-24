
<img width="1710" alt="Screenshot" src="https://github.com/user-attachments/assets/a717ebd3-c9d4-447c-86a5-7d33eea9c028" />

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
```
{
    "customization": {
        "show_version": true,
        "override_env": {
            "SHELL": "None"
        },
        "autoruns": [
            "<path to home directory>/.nercone/nercone-shell/autostart.sh"
        ]
    },
    "compatibility": {
        "report_invisible_characters": false
    }
}
```

### Customization
These settings customize the behavior of Nersh.
- `show_version`: Sets whether to display version information at startup.
- `override_env`: Sets the environment variables you want to set at startup in dictionary format.
- `autoruns`: Sets the shell scripts you want to run at startup in array format.

### Compatibility
This setting allows Nersh to function properly in special environments.
- `report_invisible_characters`: A Boolean value that enables reporting of invisible characters to readline, which is necessary in some environments, such as Linux without a GUI (TUI only).

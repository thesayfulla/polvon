# Polvon

A terminal UI tool for managing Linux systemd services.

## Features

- Modern terminal interface with color-coded status indicators
- Keyboard-driven navigation and controls
- Search and filter services by name or description
- Start, stop, restart, enable, and disable services
- Toggle between active and all services

## Installation

```bash
pip install polvon
```

Or from source:

```bash
git clone https://github.com/thesayfulla/polvon.git
cd polvon
pip install -e .
```

## Requirements

- Python 3.8 or higher
- Linux with systemd
- Root privileges or sudo access for service management

## Usage

```bash
polvon              # View-only mode
polvon --sudo       # Full service management
polvon --version    # Show version
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Refresh service list |
| `a` | Toggle between all services and active services |
| `/` | Focus search input to filter services |
| `Esc` | Clear search and return to service list |
| `s` | Start selected service |
| `Shift+S` | Stop selected service |
| `Shift+R` | Restart selected service |
| `e` | Enable selected service (start on boot) |
| `d` | Disable selected service (don't start on boot) |
| `v` | View detailed status of selected service |
| `l` | View logs of selected service |
| `↑`/`↓` | Navigate through services |


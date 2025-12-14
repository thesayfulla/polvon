# Polvon

**Polvon** is a modern, interactive Terminal UI (TUI) tool for managing Linux systemd services. Built with Python, it provides a keyboard-driven interface with color-coded status indicators and confirmation dialogs for safe service management.

## Features

- 🎨 **Modern Terminal UI** - Beautiful, color-coded interface using Textual
- ⌨️ **Keyboard-driven** - Navigate and control services efficiently
- 🔒 **Safe Operations** - Confirmation dialogs for critical actions
- 📊 **Real-time Status** - View service states with color indicators
- 📝 **Log Viewing** - Access service logs directly from the interface
- 🔄 **Service Management** - Start, stop, restart, enable, and disable services
- 📋 **Comprehensive Listing** - Toggle between active and all services

## Installation

### From Source

```bash
git clone https://github.com/thesayfulla/polvon.git
cd polvon
pip install -e .
```

### Using pip (when published)

```bash
pip install polvon
```

## Requirements

- Python 3.8 or higher
- Linux with systemd
- Root privileges or sudo access for service management

## Usage

### Basic Usage

```bash
# Run with current user permissions (view-only for most services)
polvon

# Run with sudo for full service management
polvon --sudo

# Show version
polvon --version
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Refresh service list |
| `a` | Toggle between all services and active services |
| `s` | Start selected service |
| `Shift+S` | Stop selected service |
| `Shift+R` | Restart selected service |
| `e` | Enable selected service (start on boot) |
| `d` | Disable selected service (don't start on boot) |
| `v` | View detailed status of selected service |
| `l` | View logs of selected service |
| `↑`/`↓` | Navigate through services |

### Service State Colors

- **Green** - Active (running)
- **Yellow** - Inactive (stopped)
- **Red** - Failed
- **Blue** - Other states (activating, deactivating, etc.)

## Architecture

Polvon is built with a modular structure:

- **`service.py`** - Core service management module with safe systemd interactions
- **`tui.py`** - Terminal UI implementation using Textual framework
- **`main.py`** - CLI entry point and argument parsing

### Key Design Principles

1. **Safety First** - All system calls use subprocess with timeouts and proper error handling
2. **Modular Design** - Clear separation between service logic and UI
3. **User-Friendly** - Confirmation dialogs for destructive operations
4. **Efficient** - Keyboard-driven navigation for power users

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/thesayfulla/polvon.git
cd polvon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Project Structure

```
polvon/
├── polvon/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── service.py       # Service management logic
│   └── tui.py           # Terminal UI implementation
├── tests/               # Test files
├── pyproject.toml       # Project configuration
├── README.md            # This file
└── LICENSE              # MIT License
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual) - Modern TUI framework
- Uses [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting

## Author

**Sayfulla Mirkhalikov**

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub repository](https://github.com/thesayfulla/polvon/issues).

# File Teleporter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://pypi.org/project/PySide6/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/khrehankashmiri/file_teleporter)

**File Teleporter** is a professional desktop GUI application for organizing and teleporting files and folders into predefined destinations. Built with PySide6, it provides an intuitive drag-and-drop interface with configurable tabs, multiple operation modes, and comprehensive history tracking.

![File Teleporter Screenshot](https://via.placeholder.com/800x500?text=File+Teleporter+Screenshot)

## ✨ Features

### Core Functionality
- **📁 Drag & Drop Interface** - Simply drag files or folders onto any tab to teleport them
- **🔄 Multiple Operation Modes** - Choose how files are handled:
  - **Copy & Replace** - Copy files, overwriting existing ones
  - **Copy New Only** - Copy only files that don't exist at destination
  - **Move & Replace** - Move files, overwriting existing ones
  - **Move New Only** - Move only files that don't exist at destination
- **📑 Unlimited Tabs** - Create as many teleport destinations as you need
- **📜 History Tracking** - View detailed history of all file operations per tab
- **💾 Persistent Configuration** - Settings are automatically saved and restored
- **📤 Import/Export** - Share configurations or backup your settings

### User Experience
- **🎨 Platform-Native Styling** - Optimized UI for Windows, macOS, and Linux
- **⚡ Real-time Feedback** - Visual indicators for drag operations and status updates
- **🔒 Safe Operations** - Confirmation dialogs for destructive actions
- **📊 Operation Statistics** - Track successful and failed operations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/khrehankashmiri/file_teleporter.git
cd file_teleporter
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python file_teleporter.py
```

### Alternative: Install as Package
```bash
pip install -e .
file-teleporter
```

## 📖 Usage

### Basic Workflow

1. **Launch the application**
   ```bash
   python file_teleporter.py
   ```

2. **Configure a tab**
   - Click "Set Destination Folder" to choose where files should be teleported
   - Select your preferred operation mode (Copy/Move, Replace/New Only)

3. **Teleport files**
   - Drag and drop files or folders onto the drop zone
   - Watch the status bar for operation results

4. **View history**
   - Click the "History" button to see all operations for that tab
   - Review timestamps, operations, and results

### Advanced Features

#### Managing Tabs
- **Add Tab**: Click "➕ Add Tab" in the toolbar or menu
- **Rename Tab**: Select a tab and click "✏️ Rename"
- **Delete Tab**: Select a tab and click "🗑️ Delete"
- **Reorder Tabs**: Drag tabs to rearrange them

#### Import/Export Configuration
- **Export**: File → Export Configuration → Save as JSON
- **Import**: File → Import Configuration → Choose JSON file
  - Replace all tabs or merge with existing ones

#### Operation Modes Explained

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Copy & Replace** | Copies files, overwrites if exists | Update files in destination |
| **Copy New Only** | Copies only if file doesn't exist | Avoid overwriting existing files |
| **Move & Replace** | Moves files, overwrites if exists | Organize files, replace old versions |
| **Move New Only** | Moves only if file doesn't exist | Organize without overwriting |

## 🛠️ Configuration

Configuration is stored in `config.json` in the application directory:

```json
{
  "tabs": [
    {
      "id": "unique-uuid",
      "name": "Documents",
      "path": "/path/to/destination",
      "operation": "copy_replace",
      "history": [
        {
          "timestamp": "2024-01-15 14:30:22",
          "operation": "copy_replace",
          "source": "/path/to/source/file.txt",
          "destination": "/path/to/destination/file.txt",
          "result": "Success"
        }
      ]
    }
  ]
}
```

## 🖥️ Platform Support

File Teleporter is tested and optimized for:

- **Windows** 10/11
- **macOS** 12+ (Intel and Apple Silicon)
- **Linux** (Ubuntu 20.04+, Fedora, Debian)

Each platform features native-looking UI styling for a seamless experience.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature idea? Please open an issue on [GitHub Issues](https://github.com/khrehankashmiri/file_teleporter/issues).

When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## 📚 Documentation

- [Contributing Guidelines](CONTRIBUTING.md)
- [License](LICENSE)
- [Changelog](CHANGELOG.md)

## 🙏 Acknowledgments

- Built with [PySide6](https://pypi.org/project/PySide6/) (Qt for Python)
- Inspired by the need for simple, efficient file organization tools

## 📧 Contact

- **Author**: khrehankashmiri
- **GitHub**: [@khrehankashmiri](https://github.com/khrehankashmiri)
- **Issues**: [GitHub Issues](https://github.com/khrehankashmiri/file_teleporter/issues)

---

**Made with ❤️ for efficient file management**

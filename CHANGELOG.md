# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with professional open-source structure
- Comprehensive README with badges and documentation
- Contributing guidelines (CONTRIBUTING.md)
- GitHub Actions CI/CD workflow
- Pre-commit hooks configuration
- EditorConfig for consistent formatting
- Requirements.txt for easy dependency installation

### Changed
- Renamed configuration files to standard names (.gitignore, pyproject.toml)
- Updated author email in pyproject.toml
- Rebranded project from "File Router" to "File Teleporter"
- Updated all documentation and code references to new name
- Updated repository URLs to file_teleporter

## [0.1.0] - 2024-01-15

### Added
- Initial release of File Teleporter
- Drag and drop file teleporting interface
- Multiple operation modes (Copy/Move, Replace/New Only)
- Configurable tabs for different destinations
- Per-tab history tracking with timestamps
- Import/Export configuration functionality
- Platform-specific UI styling (Windows, macOS, Linux)
- Persistent configuration storage
- Status bar with real-time feedback
- Confirmation dialogs for destructive actions

### Features
- **Core Functionality**
  - Drag & drop interface for files and folders
  - 4 operation modes per tab
  - Unlimited tab creation
  - History viewer with detailed operation logs
  - Configuration persistence

- **User Interface**
  - Platform-native styling
  - Visual feedback for drag operations
  - Resizable history dialog
  - Intuitive tab management
  - Toolbar with quick actions

- **Configuration**
  - JSON-based configuration
  - Import/Export settings
  - Tab reordering support
  - Operation mode per tab

### Technical
- Built with PySide6 (Qt for Python)
- Python 3.8+ support
- Cross-platform compatibility
- MIT License

---

## Release Notes

### Version 0.1.0
This is the initial release of File Teleporter, a professional desktop application for organizing and teleporting files. The application provides an intuitive drag-and-drop interface with configurable tabs, multiple operation modes, and comprehensive history tracking.

**Key Features:**
- Drag & drop file teleporting
- Multiple operation modes
- Tab-based organization
- History tracking
- Cross-platform support

**Supported Platforms:**
- Windows 10/11
- macOS 12+
- Linux (Ubuntu 20.04+, Fedora, Debian)

---

[Unreleased]: https://github.com/khrehankashmiri/file_teleporter/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/khrehankashmiri/file_teleporter/releases/tag/v0.1.0

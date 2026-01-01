# Contributing to File Teleporter

Thank you for your interest in contributing to File Teleporter! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

* **Clear title** describing the issue
* **Operating system** and version (Windows 11, macOS 14, Ubuntu 22.04, etc.)
* **Python version** (`python --version`)
* **Steps to reproduce** the bug
* **Expected behavior** vs. **actual behavior**
* **Screenshots** if applicable
* **Error messages** from console or dialogs

### Suggesting Features

Feature requests are welcome! Please open an issue with:

* **Clear description** of the feature
* **Use case** – why would this be useful?
* **Proposed implementation** (if you have ideas)
* **Mockups or examples** (optional but helpful)

### Code Contributions

#### Getting Started

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:

```bash
git clone https://github.com/YOUR_USERNAME/file_teleporter.git
cd file_teleporter
```

3. **Create a virtual environment**:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

#### Making Changes

1. **Create a feature branch**:

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** following the code style guidelines below

3. **Test your changes** thoroughly on your platform

4. **Commit your changes**:

```bash
git add .
git commit -m "Add feature: brief description"
```

5. **Push to your fork**:

```bash
git push origin feature/your-feature-name
```

6. **Open a Pull Request** on GitHub

#### Pull Request Guidelines

* **One feature per PR** – keep changes focused
* **Clear description** of what the PR does
* **Reference related issues** (e.g., "Fixes #123")
* **Test on your platform** before submitting
* **Update documentation** if needed (README, comments, etc.)
* **Follow code style** guidelines below

## Code Style Guidelines

### Python Style

* Follow **PEP 8** style guide
* Use **4 spaces** for indentation (no tabs)
* Maximum line length: **88 characters** (Black formatter standard)
* Use **descriptive variable names**
* Add **docstrings** for classes and non-trivial functions

### Code Organization

* Keep functions **focused and small**
* Use **type hints** where appropriate
* Add **comments** for complex logic
* Group related functionality together
* Maintain **consistent naming conventions**

### Qt/PySide6 Conventions

* Use **snake_case** for method names
* Use **CamelCase** for class names
* Connect signals properly and avoid memory leaks
* Use layouts instead of absolute positioning
* Follow platform-specific design guidelines

### Example Code Style

```python
def calculate_destination_path(self, source_path: str, tab_id: str) -> str:
    """
    Calculate the destination path for a file operation.
    
    Args:
        source_path: Path to the source file or folder
        tab_id: Unique identifier for the target tab
        
    Returns:
        Full destination path as a string
        
    Raises:
        ValueError: If tab_id is invalid or destination not set
    """
    tab = self._get_tab_config_by_id(tab_id)
    if not tab or not tab.get("path"):
        raise ValueError(f"Invalid tab or no destination set: {tab_id}")
    
    name = os.path.basename(source_path.rstrip(os.sep))
    return os.path.join(tab["path"], name)
```

## Testing

### Manual Testing

Before submitting a PR, test:

* **All operation modes** (copy/move, replace/new)
* **Tab management** (add, rename, delete, reorder)
* **Import/Export** configuration
* **History viewer**
* **Error handling** (invalid paths, permission errors, etc.)
* **UI responsiveness** and styling

### Platform Testing

If possible, test on:

* **Windows 10/11**
* **macOS** (Intel and/or Apple Silicon)
* **Linux** (Ubuntu, Fedora, or similar)

If you can only test on one platform, mention this in your PR.

## Documentation

### Code Comments

* Add comments for **non-obvious logic**
* Explain **why**, not just **what**
* Keep comments **up to date** with code changes

### README Updates

If your changes affect:

* **Installation** process
* **Usage** instructions
* **Features** or capabilities
* **Configuration** format

Please update the README.md accordingly.

## Commit Message Guidelines

Use clear, descriptive commit messages:

### Format

```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

### Types

* `feat:` – New feature
* `fix:` – Bug fix
* `docs:` – Documentation changes
* `style:` – Code style/formatting (no logic change)
* `refactor:` – Code restructuring (no behavior change)
* `test:` – Adding or updating tests
* `chore:` – Maintenance tasks

### Examples

```
feat: Add file filtering by extension

Users can now filter which files are routed based on file extensions.
Adds a new "Filter" section in each tab with include/exclude patterns.

Closes #42
```

```
fix: Prevent crash when dropping invalid paths

Added validation before processing dropped URLs to handle edge cases
where the path doesn't exist or isn't accessible.

Fixes #56
```

## Questions?

If you have questions about contributing:

* Open a **Discussion** on GitHub
* Check existing **Issues** and **Pull Requests**
* Review the **README** and code comments

Thank you for contributing to File Router! 🎉

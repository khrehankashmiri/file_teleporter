"""
File Router - Professional File Management Application

A desktop GUI tool to route files and folders into predefined destinations
using configurable tabs with multiple operation modes.
"""

import sys
import os
import json
import uuid
import shutil
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QStatusBar,
    QMessageBox,
    QMenuBar,
    QMenu,
    QInputDialog,
    QRadioButton,
    QButtonGroup,
    QToolBar,
    QFrame,
    QDialog,
    QTextEdit,
)
from PySide6.QtGui import QAction

# Operation mode constants
OP_COPY_REPLACE = "copy_replace"
OP_COPY_NEW = "copy_new"
OP_MOVE_REPLACE = "move_replace"
OP_MOVE_NEW = "move_new"


def get_config_path() -> str:
    """
    Return OS-appropriate path for config.json.
    
    Returns:
        str: Full path to the configuration file
    """
    system = platform.system()
    
    if system == "Windows":
        base = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        base_dir = Path(base) / "FileRouter"
    elif system == "Darwin":  # macOS
        base_dir = Path.home() / "Library" / "Application Support" / "FileRouter"
    else:  # Linux and others
        base_dir = Path.home() / ".config" / "file_router"
    
    base_dir.mkdir(parents=True, exist_ok=True)
    return str(base_dir / "config.json")


CONFIG_FILENAME = get_config_path()


def generate_default_config() -> Dict[str, Any]:
    """Generate default configuration with L1–L5 tabs and no paths."""
    return {
        "tabs": [
            {
                "id": str(uuid.uuid4()),
                "name": f"L{i}",
                "path": "",
                "operation": OP_COPY_REPLACE,
                "history": [],
            }
            for i in range(1, 6)
        ]
    }


class ConfigManager:
    """Manages loading and saving of application configuration."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load(self) -> Dict[str, Any]:
        """Load configuration from file or return default config."""
        if not os.path.exists(self.config_path):
            return generate_default_config()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "tabs" not in data or not isinstance(data["tabs"], list):
                return generate_default_config()

            for t in data["tabs"]:
                t.setdefault("id", str(uuid.uuid4()))
                t.setdefault("name", "Unnamed")
                t.setdefault("path", "")

                # Map old operation values to new ones
                op = t.get("operation", OP_COPY_REPLACE)
                if op == "copy":
                    op = OP_COPY_REPLACE
                elif op == "move":
                    op = OP_MOVE_REPLACE
                elif op not in {
                    OP_COPY_REPLACE,
                    OP_COPY_NEW,
                    OP_MOVE_REPLACE,
                    OP_MOVE_NEW,
                }:
                    op = OP_COPY_REPLACE
                t["operation"] = op

                # Ensure history list exists
                t.setdefault("history", [])

            return data
        except Exception as e:
            print(f"Error loading config: {e}")
            return generate_default_config()

    def save(self, data: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")


class HistoryDialog(QDialog):
    """Custom resizable dialog for displaying history with proper visibility."""

    def __init__(self, tab_name: str, history_entries: List[Dict], parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"History - {tab_name}")
        self.resize(800, 600)
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel(f"📜 History for Tab: {tab_name}")
        title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #212529; padding: 5px;"
        )
        layout.addWidget(title)

        # Text area with scrolling
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet(
            """
            QTextEdit {
                background-color: #FFFFFF;
                color: #212529;
                border: 2px solid #DEE2E6;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """
        )

        if not history_entries:
            text_edit.setPlainText("No history entries yet for this tab.")
        else:
            lines = []
            for idx, h in enumerate(history_entries, 1):
                timestamp = h.get("timestamp", "N/A")
                operation = h.get("operation", "N/A")
                source = h.get("source", "N/A")
                destination = h.get("destination", "N/A")
                result = h.get("result", "N/A")

                lines.append(f"{'=' * 80}")
                lines.append(f"Entry #{idx}")
                lines.append(f"{'=' * 80}")
                lines.append(f"⏰ Time:      {timestamp}")
                lines.append(f"⚙️  Operation: {operation}")
                lines.append(f"📂 Source:    {source}")
                lines.append(f"📁 Dest:      {destination}")
                lines.append(f"✅ Result:    {result}")
                lines.append("")

            text_edit.setPlainText("\n".join(lines))

        layout.addWidget(text_edit)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D7;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """
        )
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)


class DropArea(QLabel):
    """Central drop zone, tied to a specific tab (via tab_id)."""

    def __init__(self, main_window: 'MainWindow', tab_id: str, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.tab_id = tab_id
        self.dest_path = ""
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(180)
        self.setWordWrap(True)
        self.setText("📁 Drag files or folders here")

        self.base_style = (
            "QLabel {"
            "  border: 3px dashed #0078d7;"
            "  border-radius: 8px;"
            "  background-color: #f8f9fa;"
            "  color: #212529;"
            "  font-size: 15px;"
            "  font-weight: 500;"
            "  padding: 20px;"
            "}"
        )
        self.highlight_style = (
            "QLabel {"
            "  border: 3px solid #0078d7;"
            "  border-radius: 8px;"
            "  background-color: #cfe2ff;"
            "  color: #084298;"
            "  font-size: 15px;"
            "  font-weight: 600;"
            "  padding: 20px;"
            "}"
        )
        self.disabled_style = (
            "QLabel {"
            "  border: 3px dashed #dee2e6;"
            "  border-radius: 8px;"
            "  background-color: #f8f9fa;"
            "  color: #6c757d;"
            "  font-size: 14px;"
            "  padding: 20px;"
            "}"
        )
        self.update_style()

    def set_destination(self, path: str) -> None:
        """Set the destination path for this drop area."""
        self.dest_path = path or ""
        self.update_style()

    def has_valid_destination(self) -> bool:
        """Check if the destination path is valid."""
        return bool(self.dest_path) and os.path.isdir(self.dest_path)

    def update_style(self, highlight: bool = False) -> None:
        """Update the visual style of the drop area."""
        if not self.has_valid_destination():
            self.setStyleSheet(self.disabled_style)
            if not self.dest_path:
                self.setText(
                    "⚠️ No folder assigned\n\nClick 'Set Destination Folder' above to get started"
                )
            else:
                self.setText(
                    "❌ Destination folder is invalid or missing\n\n"
                    "Please reassign a valid folder"
                )
        else:
            self.setStyleSheet(self.highlight_style if highlight else self.base_style)
            self.setText(
                "✅ Drop files here!"
                if highlight
                else "📁 Drag files or folders here"
            )

    def dragEnterEvent(self, event):
        """Handle drag enter events."""
        if event.mimeData().hasUrls() and self.has_valid_destination():
            event.acceptProposedAction()
            self.update_style(highlight=True)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Handle drag leave events."""
        self.update_style(highlight=False)
        event.accept()

    def dropEvent(self, event):
        """Handle drop events."""
        self.update_style(highlight=False)
        if not self.has_valid_destination():
            event.ignore()
            self.main_window.show_status(
                "Cannot drop: no valid destination folder for this tab.", error=True
            )
            return

        urls = event.mimeData().urls()
        if not urls:
            event.ignore()
            return

        paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        if not paths:
            event.ignore()
            return

        event.acceptProposedAction()
        self.main_window.handle_drop(self.tab_id, paths)


class MainWindow(QMainWindow):
    """Main application window for File Router."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Router - Professional File Management")

        # Free manual resize: just give a reasonable starting size and minimum
        self.resize(1000, 600)
        self.setMinimumSize(800, 500)

        self.config_manager = ConfigManager(CONFIG_FILENAME)
        self.config = self.config_manager.load()

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(True)
        self.setCentralWidget(self.tab_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.tab_ui: Dict[str, Dict] = {}

        self._apply_platform_styles()
        self._build_menu()
        self._build_toolbar()
        self._rebuild_tabs()

        self.show_status("✔ Application ready. Configure your routing tabs to get started.")

    # ---------- Styling ----------

    def _apply_platform_styles(self) -> None:
        """Apply platform-specific styling for Windows, macOS, and Linux."""
        system = platform.system()

        if system == "Windows":
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QMenuBar {
                    background-color: #F3F3F3;
                    color: #212529;
                    border-bottom: 1px solid #E0E0E0;
                    padding: 4px;
                    font-size: 13px;
                }
                QMenuBar::item {
                    padding: 6px 12px;
                    background-color: transparent;
                }
                QMenuBar::item:selected {
                    background-color: #E5E5E5;
                    border-radius: 4px;
                }
                QToolBar {
                    background-color: #F8F9FA;
                    border-bottom: 2px solid #DEE2E6;
                    spacing: 8px;
                    padding: 8px;
                }
                QToolButton {
                    background-color: #FFFFFF;
                    border: 2px solid #0078D7;
                    border-radius: 6px;
                    padding: 8px 16px;
                    color: #0078D7;
                    font-weight: 600;
                    font-size: 13px;
                    min-width: 90px;
                }
                QToolButton:hover {
                    background-color: #0078D7;
                    color: #FFFFFF;
                }
                QToolButton:pressed {
                    background-color: #005A9E;
                }
                QTabWidget::pane {
                    border: 2px solid #DEE2E6;
                    border-radius: 6px;
                    background-color: #FFFFFF;
                    top: -1px;
                }
                QTabBar::tab {
                    background-color: #E9ECEF;
                    color: #495057;
                    border: 2px solid #DEE2E6;
                    border-bottom: none;
                    padding: 10px 20px;
                    margin-right: 2px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                    font-weight: 600;
                    font-size: 13px;
                }
                QTabBar::tab:selected {
                    background-color: #FFFFFF;
                    color: #0078D7;
                    border-bottom: 3px solid #0078D7;
                }
                QTabBar::tab:hover {
                    background-color: #F8F9FA;
                }
                QPushButton {
                    background-color: #0078D7;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: 600;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
                QPushButton:pressed {
                    background-color: #004578;
                }
                QPushButton#secondaryButton {
                    background-color: #FFFFFF;
                    color: #495057;
                    border: 2px solid #ADB5BD;
                }
                QPushButton#secondaryButton:hover {
                    background-color: #F8F9FA;
                    border-color: #6C757D;
                }
                QRadioButton {
                    color: #212529;
                    font-size: 13px;
                    font-weight: 500;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QLabel {
                    color: #212529;
                    font-size: 13px;
                }
                QStatusBar {
                    background-color: #F8F9FA;
                    color: #495057;
                    border-top: 2px solid #DEE2E6;
                    font-size: 12px;
                }
            """
            )

        elif system == "Darwin":  # macOS
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QMenuBar {
                    background-color: transparent;
                    color: #1D1D1F;
                }
                QToolBar {
                    background-color: #F5F5F7;
                    border-bottom: 1px solid #D2D2D7;
                    spacing: 10px;
                    padding: 10px;
                }
                QToolButton {
                    background-color: #007AFF;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 18px;
                    color: #FFFFFF;
                    font-weight: 600;
                    font-size: 13px;
                    min-width: 90px;
                }
                QToolButton:hover {
                    background-color: #0051D5;
                }
                QTabWidget::pane {
                    border: 1px solid #D2D2D7;
                    border-radius: 8px;
                    background-color: #FFFFFF;
                }
                QTabBar::tab {
                    background-color: #F5F5F7;
                    color: #1D1D1F;
                    border: 1px solid #D2D2D7;
                    padding: 10px 22px;
                    margin-right: 4px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    font-size: 13px;
                }
                QTabBar::tab:selected {
                    background-color: #FFFFFF;
                    color: #007AFF;
                    font-weight: 600;
                }
                QPushButton {
                    background-color: #007AFF;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 500;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #0051D5;
                }
                QPushButton#secondaryButton {
                    background-color: #F5F5F7;
                    color: #1D1D1F;
                    border: 1px solid #D2D2D7;
                }
                QRadioButton {
                    color: #1D1D1F;
                    font-size: 13px;
                    spacing: 8px;
                }
                QLabel {
                    color: #1D1D1F;
                    font-size: 13px;
                }
                QStatusBar {
                    background-color: #F5F5F7;
                    color: #86868B;
                    border-top: 1px solid #D2D2D7;
                }
            """
            )

        else:  # Linux
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QMenuBar {
                    background-color: #F6F6F6;
                    color: #2C2C2C;
                    border-bottom: 1px solid #DADADA;
                    padding: 4px;
                }
                QToolBar {
                    background-color: #FAFAFA;
                    border-bottom: 2px solid #E0E0E0;
                    spacing: 8px;
                    padding: 8px;
                }
                QToolButton {
                    background-color: #FFFFFF;
                    border: 2px solid #1976D2;
                    border-radius: 4px;
                    padding: 8px 16px;
                    color: #1976D2;
                    font-weight: 600;
                    font-size: 13px;
                    min-width: 90px;
                }
                QToolButton:hover {
                    background-color: #1976D2;
                    color: #FFFFFF;
                }
                QTabWidget::pane {
                    border: 2px solid #E0E0E0;
                    border-radius: 4px;
                    background-color: #FFFFFF;
                }
                QTabBar::tab {
                    background-color: #F0F0F0;
                    color: #424242;
                    border: 2px solid #E0E0E0;
                    padding: 10px 20px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    font-weight: 600;
                    font-size: 13px;
                }
                QTabBar::tab:selected {
                    background-color: #FFFFFF;
                    color: #1976D2;
                    border-bottom: 3px solid #1976D2;
                }
                QPushButton {
                    background-color: #1976D2;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: 600;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QPushButton#secondaryButton {
                    background-color: #FFFFFF;
                    color: #424242;
                    border: 2px solid #BDBDBD;
                }
                QRadioButton {
                    color: #2C2C2C;
                    font-size: 13px;
                    font-weight: 500;
                    spacing: 8px;
                }
                QLabel {
                    color: #2C2C2C;
                    font-size: 13px;
                }
                QStatusBar {
                    background-color: #FAFAFA;
                    color: #616161;
                    border-top: 2px solid #E0E0E0;
                }
            """
            )

    # ---------- Menu & Toolbar ----------

    def _build_menu(self) -> None:
        """Build the application menu bar."""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File menu
        file_menu = QMenu("📄 File", self)
        menu_bar.addMenu(file_menu)

        import_action = file_menu.addAction("📥 Import Configuration…")
        import_action.triggered.connect(self.import_config)

        export_action = file_menu.addAction("📤 Export Configuration…")
        export_action.triggered.connect(self.export_config)

        file_menu.addSeparator()
        exit_action = file_menu.addAction("🚪 Exit")
        exit_action.triggered.connect(self.close)

        # Tabs menu
        tabs_menu = QMenu("📑 Tabs", self)
        menu_bar.addMenu(tabs_menu)

        add_tab_action = tabs_menu.addAction("➕ Add Tab…")
        add_tab_action.triggered.connect(self.add_tab)

        rename_tab_action = tabs_menu.addAction("✏️ Rename Current Tab…")
        rename_tab_action.triggered.connect(self.rename_current_tab)

        delete_tab_action = tabs_menu.addAction("🗑️ Delete Current Tab…")
        delete_tab_action.triggered.connect(self.delete_current_tab)

        # Help menu
        help_menu = QMenu("❓ Help", self)
        menu_bar.addMenu(help_menu)

        about_action = help_menu.addAction("ℹ️ About")
        about_action.triggered.connect(self.show_about)

    def _build_toolbar(self) -> None:
        """Build the application toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        add_action = QAction("➕ Add Tab", self)
        add_action.triggered.connect(self.add_tab)
        toolbar.addAction(add_action)

        toolbar.addSeparator()

        rename_action = QAction("✏️ Rename", self)
        rename_action.triggered.connect(self.rename_current_tab)
        toolbar.addAction(rename_action)

        delete_action = QAction("🗑️ Delete", self)
        delete_action.triggered.connect(self.delete_current_tab)
        toolbar.addAction(delete_action)

        toolbar.addSeparator()

        import_action = QAction("📥 Import", self)
        import_action.triggered.connect(self.import_config)
        toolbar.addAction(import_action)

        export_action = QAction("📤 Export", self)
        export_action.triggered.connect(self.export_config)
        toolbar.addAction(export_action)

    # ---------- Tab Management ----------

    def _rebuild_tabs(self) -> None:
        """Rebuild all tabs from configuration."""
        self.tab_widget.clear()
        self.tab_ui.clear()
        for tab in self.config["tabs"]:
            self._create_tab(tab)

    def _create_tab(self, tab: Dict[str, Any]) -> int:
        """Create a new tab widget from configuration."""
        page = QWidget()
        page.setProperty("tab_id", tab["id"])

        vbox = QVBoxLayout(page)
        vbox.setSpacing(15)
        vbox.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel(f"📂 Destination for tab: {tab['name']}")
        title_label.setStyleSheet(
            "font-weight: bold; font-size: 15px; color: #212529;"
        )
        vbox.addWidget(title_label)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        vbox.addWidget(line)

        # Path row
        path_row = QHBoxLayout()
        path_label_caption = QLabel("📁 Folder:")
        path_label_caption.setMinimumWidth(70)
        path_label_caption.setStyleSheet("font-weight: 600;")
        path_row.addWidget(path_label_caption)

        path_label = QLabel()
        path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        path_label.setStyleSheet(
            "padding: 5px; background-color: #F8F9FA; border-radius: 4px;"
        )
        path_row.addWidget(path_label, stretch=1)

        assign_btn = QPushButton("Set Destination Folder")
        assign_btn.clicked.connect(lambda _, tid=tab["id"]: self.assign_folder(tid))
        path_row.addWidget(assign_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.clicked.connect(lambda _, tid=tab["id"]: self.clear_folder(tid))
        path_row.addWidget(clear_btn)

        history_btn = QPushButton("History")
        history_btn.setObjectName("secondaryButton")
        history_btn.clicked.connect(lambda _, tid=tab["id"]: self.show_history(tid))
        path_row.addWidget(history_btn)

        vbox.addLayout(path_row)

        # Operation row: 4 modes
        operation_row = QHBoxLayout()
        operation_label = QLabel("⚙️ Operation:")
        operation_label.setMinimumWidth(70)
        operation_label.setStyleSheet("font-weight: 600;")
        operation_row.addWidget(operation_label)

        copy_replace_radio = QRadioButton("Copy (Replace existing)")
        copy_new_radio = QRadioButton("Copy (New only)")
        move_replace_radio = QRadioButton("Move (Replace existing)")
        move_new_radio = QRadioButton("Move (New only)")

        button_group = QButtonGroup(page)
        button_group.addButton(copy_replace_radio)
        button_group.addButton(copy_new_radio)
        button_group.addButton(move_replace_radio)
        button_group.addButton(move_new_radio)

        op = tab.get("operation", OP_COPY_REPLACE)
        if op == OP_COPY_REPLACE:
            copy_replace_radio.setChecked(True)
        elif op == OP_COPY_NEW:
            copy_new_radio.setChecked(True)
        elif op == OP_MOVE_REPLACE:
            move_replace_radio.setChecked(True)
        else:
            move_new_radio.setChecked(True)

        copy_replace_radio.toggled.connect(
            lambda checked, tid=tab["id"]: self.set_operation(
                tid, OP_COPY_REPLACE
            )
            if checked
            else None
        )
        copy_new_radio.toggled.connect(
            lambda checked, tid=tab["id"]: self.set_operation(
                tid, OP_COPY_NEW
            )
            if checked
            else None
        )
        move_replace_radio.toggled.connect(
            lambda checked, tid=tab["id"]: self.set_operation(
                tid, OP_MOVE_REPLACE
            )
            if checked
            else None
        )
        move_new_radio.toggled.connect(
            lambda checked, tid=tab["id"]: self.set_operation(
                tid, OP_MOVE_NEW
            )
            if checked
            else None
        )

        for rb in (
            copy_replace_radio,
            copy_new_radio,
            move_replace_radio,
            move_new_radio,
        ):
            operation_row.addWidget(rb)

        operation_row.addStretch(1)
        vbox.addLayout(operation_row)

        vbox.addSpacing(10)

        # Drop area
        drop_area = DropArea(self, tab["id"])
        vbox.addWidget(drop_area)

        vbox.addStretch(1)

        index = self.tab_widget.addTab(page, tab["name"])

        self.tab_ui[tab["id"]] = {
            "page": page,
            "title_label": title_label,
            "path_label": path_label,
            "drop_area": drop_area,
        }

        self._update_tab_path_ui(tab["id"], tab.get("path", ""))

        return index

    def _get_tab_config_by_id(self, tab_id: str) -> Optional[Dict[str, Any]]:
        """Get tab configuration by ID."""
        for t in self.config["tabs"]:
            if t["id"] == tab_id:
                return t
        return None

    def _update_tab_path_ui(self, tab_id: str, path: str) -> None:
        """Update the UI elements for a tab's path."""
        ui = self.tab_ui.get(tab_id)
        if not ui:
            return

        path_label = ui["path_label"]
        drop_area = ui["drop_area"]

        path = path or ""
        if not path:
            path_label.setText("⚠️ No folder assigned")
            path_label.setStyleSheet(
                "color: #6C757D; padding: 5px; background-color: #F8F9FA; border-radius: 4px;"
            )
        elif not os.path.isdir(path):
            path_label.setText(f"❌ {path}  (invalid)")
            path_label.setStyleSheet(
                "color: #DC3545; padding: 5px; background-color: #F8D7DA; border-radius: 4px;"
            )
        else:
            path_label.setText(f"✅ {path}")
            path_label.setStyleSheet(
                "color: #198754; padding: 5px; background-color: #D1E7DD; border-radius: 4px;"
            )

        drop_area.set_destination(path)

    # ---------- History ----------

    def _add_history_entry(
        self, tab_id: str, operation: str, src: str, dest: str, result: str
    ) -> None:
        """Add a history entry to a tab (with timestamp)."""
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return

        history = tab.setdefault("history", [])
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "source": src,
            "destination": dest,
            "result": result,
        }
        history.append(entry)

        # Keep last 200 entries per tab
        if len(history) > 200:
            history[:] = history[-200:]

        self.config_manager.save(self.config)

    def show_history(self, tab_id: str) -> None:
        """Show history for a tab using custom dialog."""
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return

        history = tab.get("history", [])
        dialog = HistoryDialog(tab["name"], history, self)
        dialog.exec()

    # ---------- Folder & Operation Settings ----------

    def assign_folder(self, tab_id: str) -> None:
        """Assign a destination folder to a tab."""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Destination Folder", os.path.expanduser("~")
        )
        if not folder:
            return

        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return

        tab["path"] = folder
        self._update_tab_path_ui(tab_id, folder)
        self.config_manager.save(self.config)
        self.show_status(f"✔ Assigned folder for tab '{tab['name']}': {folder}")

    def clear_folder(self, tab_id: str) -> None:
        """Clear the destination folder for a tab."""
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return
        tab["path"] = ""
        self._update_tab_path_ui(tab_id, "")
        self.config_manager.save(self.config)
        self.show_status(f"✔ Cleared folder for tab '{tab['name']}'")

    def set_operation(self, tab_id: str, operation: str) -> None:
        """Set the operation mode for a tab."""
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return
        tab["operation"] = operation
        self.config_manager.save(self.config)
        self.show_status(
            f"✔ Set operation for tab '{tab['name']}' to '{operation.upper()}'"
        )

    # ---------- Tab Actions ----------

    def add_tab(self) -> None:
        """Add a new tab."""
        default_name = f"L{len(self.config['tabs']) + 1}"
        name, ok = QInputDialog.getText(
            self, "Add Tab", "Enter tab name:", text=default_name
        )
        if not ok or not name.strip():
            return

        name = name.strip()
        new_tab = {
            "id": str(uuid.uuid4()),
            "name": name,
            "path": "",
            "operation": OP_COPY_REPLACE,
            "history": [],
        }
        self.config["tabs"].append(new_tab)
        self._create_tab(new_tab)
        self.config_manager.save(self.config)
        self.show_status(f"✔ Added tab '{name}'")

    def rename_current_tab(self) -> None:
        """Rename the currently selected tab."""
        index = self.tab_widget.currentIndex()
        if index < 0:
            return

        page = self.tab_widget.widget(index)
        tab_id = page.property("tab_id")
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return

        current_name = tab["name"]
        new_name, ok = QInputDialog.getText(
            self, "Rename Tab", "Enter new tab name:", text=current_name
        )
        if not ok or not new_name.strip():
            return

        new_name = new_name.strip()
        tab["name"] = new_name

        self.tab_widget.setTabText(index, new_name)
        ui = self.tab_ui.get(tab_id)
        if ui:
            ui["title_label"].setText(f"📂 Destination for tab: {new_name}")

        self.config_manager.save(self.config)
        self.show_status(f"✔ Renamed tab to '{new_name}'")

    def delete_current_tab(self) -> None:
        """Delete the currently selected tab."""
        index = self.tab_widget.currentIndex()
        if index < 0:
            return

        page = self.tab_widget.widget(index)
        tab_id = page.property("tab_id")
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            return

        reply = QMessageBox.question(
            self,
            "Delete Tab",
            f"Are you sure you want to delete tab '{tab['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self.config["tabs"] = [t for t in self.config["tabs"] if t["id"] != tab_id]
        self.tab_widget.removeTab(index)
        self.tab_ui.pop(tab_id, None)

        self.config_manager.save(self.config)
        self.show_status(f"✔ Deleted tab '{tab['name']}'")

    # ---------- Drag & Drop / File Operations ----------

    def handle_drop(self, tab_id: str, src_paths: List[str]) -> None:
        """Handle dropped files/folders."""
        tab = self._get_tab_config_by_id(tab_id)
        if not tab:
            self.show_status("❌ Internal error: tab not found.", error=True)
            return

        dest_root = tab.get("path") or ""
        if not dest_root or not os.path.isdir(dest_root):
            self.show_status(
                f"❌ No valid destination folder for tab '{tab['name']}'", error=True
            )
            return

        mode = tab.get("operation", OP_COPY_REPLACE)
        successes = 0
        failures = 0
        failure_messages = []

        for src in src_paths:
            if not os.path.exists(src):
                failures += 1
                msg = f"Source does not exist: {src}"
                failure_messages.append(msg)
                self._add_history_entry(
                    tab_id, mode, src, "", f"failed: {msg}"
                )
                continue

            name = os.path.basename(src.rstrip(os.sep))
            target = os.path.join(dest_root, name)
            exists = os.path.exists(target)

            try:
                # Decide if we should skip existing targets
                if mode in (OP_COPY_NEW, OP_MOVE_NEW) and exists:
                    # skip existing
                    self._add_history_entry(
                        tab_id,
                        mode,
                        src,
                        target,
                        "skipped (target exists, NEW only)",
                    )
                    continue

                # Perform copy / replace
                if os.path.isdir(src):
                    # Replace directory if needed
                    if exists and mode in (OP_COPY_REPLACE, OP_MOVE_REPLACE):
                        shutil.rmtree(target)
                    shutil.copytree(src, target)
                else:
                    # File copy; copy2 overwrites
                    shutil.copy2(src, target)

                # Handle move (delete source)
                if mode in (OP_MOVE_REPLACE, OP_MOVE_NEW):
                    if os.path.isdir(src):
                        shutil.rmtree(src)
                    else:
                        os.remove(src)

                successes += 1
                self._add_history_entry(
                    tab_id, mode, src, target, "success"
                )

            except Exception as e:
                failures += 1
                msg = f"Failed to {mode} '{src}': {e}"
                failure_messages.append(msg)
                self._add_history_entry(
                    tab_id, mode, src, target, f"failed: {e}"
                )

        op_label = {
            OP_COPY_REPLACE: "Copy & Replace",
            OP_COPY_NEW: "Copy New Only",
            OP_MOVE_REPLACE: "Move & Replace",
            OP_MOVE_NEW: "Move New Only",
        }.get(mode, mode)

        if failures == 0:
            self.show_status(
                f"✔ {op_label}: {successes} item(s) to '{dest_root}' for tab '{tab['name']}'"
            )
        else:
            self.show_status(
                f"⚠️ {op_label}: {successes} item(s) OK, {failures} failure(s). See details.",
                error=True,
            )
            QMessageBox.warning(
                self,
                f"{op_label} - Errors",
                "Some items failed:\n\n" + "\n".join(failure_messages),
            )

    # ---------- Import / Export ----------

    def export_config(self) -> None:
        """Export configuration to a JSON file."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            "tabs_config.json",
            "JSON Files (*.json);;All Files (*)",
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            self.show_status(f"✔ Exported configuration to '{filename}'")
        except Exception as e:
            QMessageBox.critical(
                self, "Export Error", f"Failed to export configuration:\n{e}"
            )

    def import_config(self) -> None:
        """Import configuration from a JSON file."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Configuration",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(
                self, "Import Error", f"Failed to read configuration file:\n{e}"
            )
            return

        if "tabs" not in data or not isinstance(data["tabs"], list):
            QMessageBox.critical(
                self,
                "Import Error",
                "Invalid configuration format (no 'tabs' array).",
            )
            return

        for t in data["tabs"]:
            t.setdefault("id", str(uuid.uuid4()))
            t.setdefault("name", "Unnamed")
            t.setdefault("path", "")
            # Normalize operations
            op = t.get("operation", OP_COPY_REPLACE)
            if op == "copy":
                op = OP_COPY_REPLACE
            elif op == "move":
                op = OP_MOVE_REPLACE
            elif op not in {
                OP_COPY_REPLACE,
                OP_COPY_NEW,
                OP_MOVE_REPLACE,
                OP_MOVE_NEW,
            }:
                op = OP_COPY_REPLACE
            t["operation"] = op
            t.setdefault("history", [])

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Import Configuration")
        msg_box.setText(
            "How would you like to apply the imported configuration?\n\n"
            "Yes: Replace existing tabs\n"
            "No: Merge with existing tabs\n"
            "Cancel: Abort"
        )
        msg_box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        choice = msg_box.exec()

        if choice == QMessageBox.Cancel:
            return
        elif choice == QMessageBox.Yes:
            self.config = {"tabs": data["tabs"]}
        elif choice == QMessageBox.No:
            self.config["tabs"].extend(data["tabs"])

        self.config_manager.save(self.config)
        self._rebuild_tabs()
        self.show_status("✔ Imported configuration successfully")

    # ---------- Misc ----------

    def show_status(self, message: str, error: bool = False) -> None:
        """Show a status message."""
        self.status_bar.showMessage(message, 8000)
        if error:
            print("ERROR:", message)

    def show_about(self) -> None:
        """Show the About dialog."""
        QMessageBox.information(
            self,
            "About File Router",
            (
                "📁 File Router - Professional File Management\n\n"
                "A utility to route files and folders into\n"
                "predefined destinations using configurable tabs.\n\n"
                "Features:\n"
                "• 4 operation modes per tab:\n"
                "  - Copy & Replace\n"
                "  - Copy New Only\n"
                "  - Move & Replace\n"
                "  - Move New Only\n"
                "• Per-tab history with date & time\n"
                "• Persistent configuration\n"
                "• Import/Export settings\n"
                "• Drag & drop support\n"
                "• Platform-specific styling (Windows, macOS, Linux)\n\n"
                f"Running on: {platform.system()}\n"
                f"Config location: {CONFIG_FILENAME}"
            ),
        )


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

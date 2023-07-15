from typing import Optional, cast
from PyQt5.QtWidgets import QMainWindow, QListWidget, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QInputDialog, QFileDialog
from projectitem import ProjectItem
from settings import Settings
from editor import Editor
import os


class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.settings: Settings = Settings()

        self.list_widget: QListWidget = QListWidget()
        self.add_to_startup_button: QPushButton = QPushButton("Add to Startup")
        self.delete_from_startup_button: QPushButton = QPushButton("Delete from Startup")
        self.new_project_button: QPushButton = QPushButton("New Project")
        self.edit_entry_script_button: QPushButton = QPushButton("Edit Entry Script")
        self.edit_wrapper_script_button: QPushButton = QPushButton("Edit Wrapper Script")
        self.autostart_status_label: QLabel = QLabel()

        self.editor: Editor = Editor()

        self.list_widget.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.add_to_startup_button.clicked.connect(self.on_add_to_startup_clicked)
        self.delete_from_startup_button.clicked.connect(self.on_delete_from_startup_clicked)
        self.new_project_button.clicked.connect(self.on_new_project_clicked)
        self.edit_entry_script_button.clicked.connect(self.on_edit_entry_script_clicked)
        self.edit_wrapper_script_button.clicked.connect(self.on_edit_wrapper_script_clicked)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget)
        left_layout.addWidget(self.add_to_startup_button)
        left_layout.addWidget(self.delete_from_startup_button)
        left_layout.addWidget(self.new_project_button)
        left_layout.addWidget(self.autostart_status_label)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.edit_entry_script_button)
        right_layout.addWidget(self.edit_wrapper_script_button)

        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        central_widget: QWidget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_projects()

    def load_projects(self) -> None:
        workspace_root: str = self.settings.get_workspace_root()

        for dir_name in os.listdir(workspace_root):
            dir_path: str = os.path.join(workspace_root, dir_name)

            if os.path.isdir(dir_path):
                project_item: ProjectItem = ProjectItem(dir_path)
                self.list_widget.addItem(project_item)

    def on_item_selection_changed(self) -> None:
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            self.editor.clear()
            self.autostart_status_label.clear()
            return

        project_item: ProjectItem = cast(ProjectItem, selected_items[0])
        entry_script_path = project_item.get_entry_script_path()
        if entry_script_path:
            self.editor.open_file(entry_script_path)
        self.update_autostart_status(project_item)

    def on_add_to_startup_clicked(self) -> None:
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            return

        project_item: ProjectItem = cast(ProjectItem, selected_items[0])
        project_item.add_to_startup()
        self.update_autostart_status(project_item)

    def on_delete_from_startup_clicked(self) -> None:
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            return

        project_item: ProjectItem = cast(ProjectItem, selected_items[0])
        project_item.delete_from_startup()
        self.update_autostart_status(project_item)

    def on_new_project_clicked(self) -> None:
        project_name, ok = QInputDialog.getText(self, "New Project", "Project Name:")

        if not ok or not project_name:
            return

        script_language, ok = QInputDialog.getItem(self, "New Project", "Script Language:", ["Python", "Powershell", "Executable"], 0, False)

        if not ok or not script_language:
            return

        project_item: Optional[ProjectItem] = None
        if script_language == "Python":
            interpreter_path: str = QFileDialog.getOpenFileName(self, "Select Python Interpreter", "", "Python Interpreter (*.exe)")[0]

            if not interpreter_path:
                return

            project_item = ProjectItem.create_python_project(self.settings.get_workspace_root(), project_name, interpreter_path)
        elif script_language == "Powershell":
            project_item = ProjectItem.create_powershell_project(self.settings.get_workspace_root(), project_name)
        else:
            executable_path: str = QFileDialog.getOpenFileName(self, "Select Executable", "", "Executable (*.exe)")[0]

            if not executable_path:
                return

            project_item = ProjectItem.create_executable_project(self.settings.get_workspace_root(), project_name, executable_path)

        if project_item is not None:
            self.list_widget.addItem(project_item)

    def on_edit_entry_script_clicked(self) -> None:
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            return

        project_item: ProjectItem = cast(ProjectItem, selected_items[0])
        entry_script_path = project_item.get_entry_script_path()
        if entry_script_path:
            self.editor.open_file(entry_script_path)

    def on_edit_wrapper_script_clicked(self) -> None:
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            return

        project_item: ProjectItem = cast(ProjectItem, selected_items[0])
        self.editor.open_file(project_item.get_wrapper_script_path())

    def update_autostart_status(self, project_item: ProjectItem) -> None:
        if project_item.is_startup_item():
            self.autostart_status_label.setText("This project is added to autostart.")
        else:
            self.autostart_status_label.setText("This project is not added to autostart.")

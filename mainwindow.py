from PyQt5.QtWidgets import QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from projectitem import ProjectItem
from settings import Settings
import os

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = Settings()

        self.list_widget = QListWidget()
        self.text_edit = QTextEdit()
        self.add_to_startup_button = QPushButton("Add to Startup")
        self.delete_from_startup_button = QPushButton("Delete from Startup")
        self.autostart_status_label = QLabel()

        self.list_widget.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.add_to_startup_button.clicked.connect(self.on_add_to_startup_clicked)
        self.delete_from_startup_button.clicked.connect(self.on_delete_from_startup_clicked)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget)
        left_layout.addWidget(self.add_to_startup_button)
        left_layout.addWidget(self.delete_from_startup_button)
        left_layout.addWidget(self.autostart_status_label)

        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_projects()

    def load_projects(self):
        workspace_root = self.settings.get_workspace_root()

        for dir_name in os.listdir(workspace_root):
            dir_path = os.path.join(workspace_root, dir_name)

            if os.path.isdir(dir_path):
                project_item = ProjectItem(dir_path)
                self.list_widget.addItem(project_item)

    def on_item_selection_changed(self):
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            self.text_edit.clear()
            self.autostart_status_label.clear()
            return

        project_item = selected_items[0]
        self.text_edit.setPlainText(project_item.get_script())
        self.update_autostart_status(project_item)

    def on_add_to_startup_clicked(self):
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            return

        project_item = selected_items[0]
        project_item.add_to_startup()
        self.update_autostart_status(project_item)

    def on_delete_from_startup_clicked(self):
        selected_items = self.list_widget.selectedItems()

        if not selected_items:
            return

        project_item = selected_items[0]
        project_item.delete_from_startup()
        self.update_autostart_status(project_item)

    def update_autostart_status(self, project_item):
        if project_item.is_startup_item():
            self.autostart_status_label.setText("This project is added to autostart.")
        else:
            self.autostart_status_label.setText("This project is not added to autostart.")

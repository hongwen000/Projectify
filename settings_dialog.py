from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QWidget
from settings import Settings
from typing import Optional, cast

class SettingsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] =None) -> None:
        super(SettingsDialog, self).__init__(parent)
        self.settings = Settings()

        layout = QVBoxLayout(self)

        self.workspace_dir_label = QLabel("Workspace Directory:", self)
        self.workspace_dir_edit = QLineEdit(self.settings.get_workspace_root(), self)

        self.python_interpreter_label = QLabel("Python Interpreter Path:", self)
        self.python_interpreter_edit = QLineEdit(self.settings.get_python_interpreter(), self)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.workspace_dir_label)
        layout.addWidget(self.workspace_dir_edit)
        layout.addWidget(self.python_interpreter_label)
        layout.addWidget(self.python_interpreter_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def accept(self) -> None:
        self.settings.set_workspace_root(self.workspace_dir_edit.text())
        self.settings.set_python_interpreter(self.python_interpreter_edit.text())
        super(SettingsDialog, self).accept()

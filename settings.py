from PyQt5.QtCore import QSettings
import os

class Settings(QSettings):
    def __init__(self, parent=None):
        super().__init__(parent)

    def get_workspace_root(self):
        return self.value("workspace_root", os.getcwd())

    def set_workspace_root(self, workspace_root):
        self.setValue("workspace_root", workspace_root)

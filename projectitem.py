from PyQt5.QtWidgets import QListWidgetItem
from startupmanager import StartupManager
import os

class ProjectItem(QListWidgetItem):
    def __init__(self, dir_path, parent=None):
        super().__init__(parent)

        self.dir_path = dir_path
        self.startup_manager = StartupManager()

        self.setText(os.path.basename(dir_path))

    def get_script(self):
        script_path = os.path.join(self.dir_path, "script.py")

        if not os.path.isfile(script_path):
            return ""

        with open(script_path, "r") as file:
            return file.read()

    def set_script(self, script):
        script_path = os.path.join(self.dir_path, "script.py")

        with open(script_path, "w") as file:
            file.write(script)

    def add_to_startup(self):
        self.startup_manager.add_to_startup(self.dir_path)

    def is_startup_item(self):
        return self.startup_manager.is_startup_item(self.dir_path)

    def delete_from_startup(self):
        self.startup_manager.delete_from_startup(self.dir_path)

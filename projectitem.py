from PyQt5.QtWidgets import QListWidgetItem
from settings import Settings
import os
import subprocess

class ProjectItem(QListWidgetItem):
    def __init__(self, project_path):
        super().__init__(os.path.basename(project_path))

        self.project_path = project_path
        self.run_script_path = os.path.join(project_path, "run.bat")

        if os.path.exists(os.path.join(project_path, "main.py")):
            self.entry_script_path = os.path.join(project_path, "main.py")
        elif os.path.exists(os.path.join(project_path, "main.ps1")):
            self.entry_script_path = os.path.join(project_path, "main.ps1")
        else:
            self.entry_script_path = None

    @classmethod
    def create_python_project(cls, workspace_root, project_name, interpreter_path):
        project_path = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        entry_script_path = os.path.join(project_path, "main.py")
        with open(entry_script_path, "w") as f:
            f.write("# Python script")

        run_script_path = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\n"{interpreter_path}" "{entry_script_path}"\npause')

        return cls(project_path)

    @classmethod
    def create_powershell_project(cls, workspace_root, project_name):
        project_path = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        entry_script_path = os.path.join(project_path, "main.ps1")
        with open(entry_script_path, "w") as f:
            f.write("# Powershell script")

        run_script_path = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\npowershell -ExecutionPolicy Bypass -File "{entry_script_path}"\npause')

        return cls(project_path)

    @classmethod
    def create_executable_project(cls, workspace_root, project_name, executable_path):
        project_path = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        run_script_path = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\n"{executable_path}"\npause')

        return cls(project_path)

    def get_entry_script(self):
        if self.entry_script_path is None:
            return ""

        with open(self.entry_script_path, "r") as f:
            return f.read()

    def get_wrapper_script(self):
        with open(self.run_script_path, "r") as f:
            return f.read()

    def is_startup_item(self):
        startup_folder = os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        return os.path.exists(os.path.join(startup_folder, f"{self.text()}.bat"))

    def add_to_startup(self):
        startup_folder = os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        subprocess.run(f'copy "{self.run_script_path}" "{startup_folder}\\{self.text()}.bat"', shell=True)

    def delete_from_startup(self):
        startup_folder = os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        subprocess.run(f'del "{startup_folder}\\{self.text()}.bat"', shell=True)

    def get_entry_script_path(self):
        return self.entry_script_path

    def get_wrapper_script_path(self):
        return self.run_script_path
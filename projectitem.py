from PyQt5.QtWidgets import QListWidgetItem
from settings import Settings
import os
import subprocess

class ProjectItem(QListWidgetItem):
    def __init__(self, project_path):
        super().__init__(os.path.basename(project_path))

        self.project_path = project_path
        self.run_script_path = os.path.join(project_path, "run.bat")

    @classmethod
    def create_python_project(cls, workspace_root, project_name, interpreter_path):
        project_path = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        run_script_path = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\n"{interpreter_path}" "{project_path}\\script.py"\npause')

        return cls(project_path)

    @classmethod
    def create_powershell_project(cls, workspace_root, project_name):
        project_path = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        run_script_path = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\npowershell -ExecutionPolicy Bypass -File "{project_path}\\script.ps1"\npause')

        return cls(project_path)

    @classmethod
    def create_executable_project(cls, workspace_root, project_name, executable_path):
        project_path = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        run_script_path = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\n"{executable_path}"\npause')

        return cls(project_path)

    def get_script(self):
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

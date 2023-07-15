from typing import Optional, ClassVar
from PyQt5.QtWidgets import QListWidgetItem
from settings import Settings
import os
import subprocess

class ProjectItem(QListWidgetItem):
    def __init__(self, project_path: str):
        super().__init__(os.path.basename(project_path))
        self.project_path: str = project_path
        self.run_script_path: str = os.path.join(project_path, "run.bat")
        self.entry_script_path: Optional[str]
        if os.path.exists(os.path.join(project_path, "main.py")):
            self.entry_script_path = os.path.join(project_path, "main.py")
        elif os.path.exists(os.path.join(project_path, "main.ps1")):
            self.entry_script_path = os.path.join(project_path, "main.ps1")
        else:
            self.entry_script_path = None

    @classmethod
    def create_python_project(cls, workspace_root: str, project_name: str, interpreter_path: str) -> 'ProjectItem':
        project_path: str = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        entry_script_path: str = os.path.join(project_path, "main.py")
        with open(entry_script_path, "w") as f:
            f.write("# Python script")

        run_script_path: str = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\n"{interpreter_path}" "{entry_script_path}"\npause')

        return cls(project_path)

    @classmethod
    def create_powershell_project(cls, workspace_root: str, project_name: str) -> 'ProjectItem':
        project_path: str = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        entry_script_path: str = os.path.join(project_path, "main.ps1")
        with open(entry_script_path, "w") as f:
            f.write("# Powershell script")

        run_script_path: str = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\npowershell -ExecutionPolicy Bypass -File "{entry_script_path}"\npause')

        return cls(project_path)

    @classmethod
    def create_executable_project(cls, workspace_root: str, project_name: str, executable_path: str) -> 'ProjectItem':
        project_path: str = os.path.join(workspace_root, project_name)
        os.makedirs(project_path, exist_ok=True)

        run_script_path: str = os.path.join(project_path, "run.bat")
        with open(run_script_path, "w") as f:
            f.write(f'@echo off\n"{executable_path}"\npause')

        return cls(project_path)

    def get_entry_script(self) -> str:
        if self.entry_script_path is None:
            return ""

        with open(self.entry_script_path, "r") as f:
            return f.read()

    def get_wrapper_script(self) -> str:
        with open(self.run_script_path, "r") as f:
            return f.read()

    def get_entry_script_path(self) -> Optional[str]:
        return self.entry_script_path

    def get_wrapper_script_path(self) -> str:
        return self.run_script_path

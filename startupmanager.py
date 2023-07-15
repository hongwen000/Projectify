from abc import ABC, abstractmethod
from projectitem import ProjectItem

class StartupManager(ABC):
    @abstractmethod
    def add_to_startup(self, project_item: ProjectItem) -> None:
        pass

    @abstractmethod
    def is_startup_item(self, project_item: ProjectItem) -> bool:
        pass

    @abstractmethod
    def delete_from_startup(self, project_item: ProjectItem) -> None:
        pass

import os
import subprocess
if os.name == 'nt':
    import winreg
    import win32serviceutil

    class RegistryStartupManager(StartupManager):
        def __init__(self):
            self.registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_ALL_ACCESS
            )

        def add_to_startup(self, project_item: ProjectItem):
            winreg.SetValueEx(self.registry_key, project_item.text(), 0, winreg.REG_SZ, project_item.run_script_path)

        def is_startup_item(self, project_item: ProjectItem):
            try:
                winreg.QueryValueEx(self.registry_key, project_item.text())
                return True
            except FileNotFoundError:
                return False

        def delete_from_startup(self, project_item: ProjectItem):
            winreg.DeleteValue(self.registry_key, project_item.text())

    class ServiceStartupManager(StartupManager):
        def __init__(self, service_template_path):
            with open(service_template_path, "r") as file:
                self.service_script_template = file.read()
        
        def add_to_startup(self, project_item: ProjectItem):
            service_name = project_item.text()
            script_path = project_item.get_entry_script_path()

            service_script = self.service_script_template.replace('PLACEHOLDER_SERVICE_NAME', service_name)
            service_script = service_script.replace('PLACEHOLDER_SCRIPT_PATH', script_path)
            service_script_path = os.path.join(project_item.project_path, 'service.py')

            with open(service_script_path, 'w') as f:
                f.write(service_script)

            subprocess.run([f'python "{service_script_path}" install'])

        def is_startup_item(self, project_item: ProjectItem):
            service_name = project_item.text()

            try:
                status_info = win32serviceutil.QueryServiceStatus(service_name)
                return True
            except:
                return False

        def delete_from_startup(self, project_item: ProjectItem):
            service_name = project_item.text()

            if self.is_startup_item(project_item):
                subprocess.run([f'python "{os.path.join(project_item.project_path, "service.py")}" stop'])
                subprocess.run([f'python "{os.path.join(project_item.project_path, "service.py")}" remove'])



import shutil

class FolderStartupManager(StartupManager):
    def __init__(self) -> None:
        self.startup_folder = os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')

    def add_to_startup(self, project_item: ProjectItem) -> None:
        shutil.copy(project_item.run_script_path, os.path.join(self.startup_folder, f"{project_item.text()}.bat"))

    def is_startup_item(self, project_item: ProjectItem) -> bool:
        return os.path.exists(os.path.join(self.startup_folder, f"{project_item.text()}.bat"))

    def delete_from_startup(self, project_item: ProjectItem) -> None:
        os.remove(os.path.join(self.startup_folder, f"{project_item.text()}.bat"))

default_startup_manager = FolderStartupManager
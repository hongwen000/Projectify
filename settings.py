from PyQt5.QtCore import QSettings
from typing import Optional, Any, cast
import os
import sys

class Settings(QSettings):
    def __init__(self, parent: Optional[QSettings]=None) -> None:
        super().__init__(parent)

    def get_workspace_root(self) -> str:
        ret: Any = self.value("workspace_root", os.path.expanduser("~/workspace"))
        str_ret: str = cast(str, ret)
        return str_ret

    def get_python_interpreter(self) -> str:
        ret: Any = self.value("python_interpreter", os.path.expanduser("~/workspace"))
        str_ret: str = cast(str, ret)
        return str_ret

    def set_workspace_root(self, workspace_root: str) -> None:
        self.setValue("workspace_root", workspace_root)

    def set_python_interpreter(self, python_interpreter: str) -> None:
        self.python_interpreter = python_interpreter
        self.setValue("python_interpreter", sys.executable)

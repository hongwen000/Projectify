from PyQt5.QtCore import QSettings
from typing import Optional, Any, cast
import os

class Settings(QSettings):
    def __init__(self, parent: Optional[QSettings]=None) -> None:
        super().__init__(parent)

    def get_workspace_root(self) -> str:
        ret: Any = self.value("workspace_root", os.path.expanduser("~/workspace"))
        str_ret: str = cast(ret, str)
        return str_ret

    def set_workspace_root(self, workspace_root: str) -> None:
        self.setValue("workspace_root", workspace_root)

from PyQt5.QtWidgets import QTextEdit

class ScriptEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

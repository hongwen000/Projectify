from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from typing import Optional

class Editor(QTextEdit):
    def __init__(self, parent: Optional[QTextEdit] = None) -> None:
        super().__init__(parent)

        self.current_file: Optional[QFile] = None

        self.textChanged.connect(self.on_text_changed)

    def open_file(self, file_path: str) -> None:
        self.current_file = QFile(file_path)

        if not self.current_file.open(QIODevice.ReadOnly | QIODevice.Text): # type:ignore
            return

        stream = QTextStream(self.current_file)
        self.setPlainText(stream.readAll())
        self.current_file.close()

    def on_text_changed(self) -> None:
        if self.current_file is None:
            return

        # The QFile instance needs to be opened again after it was closed.
        # We need to re-create the QFile instance here because once a QFile instance is closed, it can't be opened again.
        self.current_file = QFile(self.current_file.fileName())
        if not self.current_file.open(QIODevice.WriteOnly | QIODevice.Text): # type:ignore
            return

        stream = QTextStream(self.current_file)
        stream << self.toPlainText()
        self.current_file.close()

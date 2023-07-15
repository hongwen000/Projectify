from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QFile, QIODevice, QTextStream

class Editor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_file = None

        self.textChanged.connect(self.on_text_changed)

    def open_file(self, file_path):
        self.current_file = QFile(file_path)

        if not self.current_file.open(QIODevice.ReadOnly | QIODevice.Text):
            return

        stream = QTextStream(self.current_file)
        self.setPlainText(stream.readAll())
        self.current_file.close()

    def on_text_changed(self):
        if self.current_file is None:
            return

        if not self.current_file.open(QIODevice.WriteOnly | QIODevice.Text):
            return

        stream = QTextStream(self.current_file)
        stream << self.toPlainText()
        self.current_file.close()

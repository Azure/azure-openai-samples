import datetime
import json

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel
from PySide6.QtGui import QGuiApplication, QTextCursor

from GUI.PlainTextPasteEdit import PlainTextPasteEdit

defult_tool_template = \
"""{
    "type": "function",
    "function": {
        "name": "",
        "description": "",
        "parameters": {
            "type": "object",
            "properties": {
                "args1": {
                    "type": "string",
                    "description": ""
                }
            },
            "required": ["args1"]
        }
    }
}"""

class FunctionEditDialog(QDialog):
    def __init__(self, jsonStr, parent):
        super().__init__(parent)
        self.initUI(jsonStr)
        return
    

    def initUI(self, jsonStr):
        self.setWindowTitle("Edit Functions")
        self.setGeometry(0, 0, 580, 560)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.txt_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Template")
        self.check_json_button = QPushButton("Check Json")
        self.import_button = QPushButton("Open Json")
        self.export_button = QPushButton("Save As Json")
        self.txt_layout.addWidget(self.add_button)
        self.txt_layout.addWidget(self.check_json_button)
        self.txt_layout.addWidget(self.import_button)
        self.txt_layout.addWidget(self.export_button)
        self.add_button.clicked.connect(self.on_insert_template)
        self.check_json_button.clicked.connect(self.on_check_json)
        self.import_button.clicked.connect(self.on_import_function)
        self.export_button.clicked.connect(self.on_export_function)
        layout.addLayout(self.txt_layout)

        self.text_edit = PlainTextPasteEdit()
        self.text_edit.setPlainText(jsonStr)
        layout.addWidget(self.text_edit)

        self.lineNumLabel = QLabel("Current Line Number: 1")
        layout.addWidget(self.lineNumLabel)
        self.text_edit.cursorPositionChanged.connect(self.on_cursor_position_changed)

        self.button_layout = QHBoxLayout()
        layout.addLayout(self.button_layout)

        self.save_button = QPushButton("OK")
        self.save_button.clicked.connect(self.on_save)
       
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)

        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        
        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()
        x = (screenGeometry.width() - self.width()) / 2
        y = ((screenGeometry.height() - self.height()) / 2) - 50
        self.move(int(x), int(y))
        return
    

    def on_cursor_position_changed(self):
        self.lineNumLabel.setText(f"Current Line Number: {self.text_edit.textCursor().blockNumber() + 1}")
        return
    

    def on_insert_template(self):
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        if self.text_edit.toPlainText().strip() == "":
            self.text_edit.insertPlainText('[' + defult_tool_template + ']')
        else:
            self.text_edit.moveCursor(QTextCursor.MoveOperation.Left)
            if self.text_edit.toPlainText().strip() == "[]":
                self.text_edit.insertPlainText(defult_tool_template)
            else:
                self.text_edit.insertPlainText(",\n")
                self.text_edit.insertPlainText(defult_tool_template)
        return
    

    def on_check_json(self):
        try:
            json.loads(self.text_edit.toPlainText())
            QMessageBox.information(self, "Check", "JSON format is correct")
        except Exception as e:
            QMessageBox.critical(self, "Check", f"JSON format error: {str(e)}")
        return
    

    def on_import_function(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Json File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "r") as f:
                self.text_edit.setPlainText(f.read())
        return


    def on_export_function(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As Json", f"tools_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "w") as f:
                f.write(self.text_edit.toPlainText())
        return
    

    def on_save(self):
        self.accept()


    def on_cancel(self):
        self.reject()

import docx2txt
from PyPDF2 import PdfReader
import pandas as pd
import chardet

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QToolButton, QSizePolicy
from PySide6.QtGui import QGuiApplication

from TextPreprocessor import TextPreprocessor
from GUI.PlainTextPasteEdit import PlainTextPasteEdit

class TextInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cleaner = None
        self.setWindowTitle("Document")
        self.setGeometry(0, 0, 480, 500)

        layout = QVBoxLayout()

        data_layout = QHBoxLayout()
        self.import_button = QPushButton("From File")
        self.process_button = QToolButton()
        self.process_button.setText("Process")
        self.process_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.process_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.process_button.addAction("Pre-process")
        self.process_button.addAction("Extract-lemma")
        self.process_button.triggered.connect(self.on_process_text)
        self.import_button.clicked.connect(self.on_import_for_doc)
        data_layout.addWidget(self.process_button)
        data_layout.addWidget(self.import_button)
        layout.addLayout(data_layout)

        self.text_edit = PlainTextPasteEdit()
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        self.reject_button = QPushButton("Cancel")
        self.reject_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.reject_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()
        x = (screenGeometry.width() - self.width()) / 2
        y = ((screenGeometry.height() - self.height()) / 2) - 50
        self.move(int(x), int(y))
        return
    

    def on_process_text(self, action):
        if not self.cleaner:
            self.cleaner = TextPreprocessor()

        text = self.text_edit.textCursor().selectedText()
        if action.text() == "Pre-process":
            text = self.cleaner.process_text_pre(text)
        elif action.text() == "Extract-lemma":
            text = self.cleaner.process_text_en(text)
        
        cursor = self.text_edit.textCursor()
        cursor.removeSelectedText()
        cursor.insertText(text)
        return
    

    def on_import_for_doc(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Open Document", "", "Documents (*.txt *.docx *.pdf *.xlsx)")
        text = ''

        if file_name:
            if file_name.endswith('.txt'):
                with open(file_name, "rb") as file:
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                    if encoding in ['utf-8', 'UTF-8-SIG']:
                        text = raw_data.decode('utf-8')
                    else:
                        text = raw_data.decode(errors='ignore')
            elif file_name.endswith('.docx'):
                text = docx2txt.process(file_name)
            elif file_name.endswith('.pdf'):
                pdf_reader = PdfReader(file_name)
                text = ' '.join([page.extract_text() for page in pdf_reader.pages])
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(file_name)
                text = df.to_string(index=False)

        reply = QMessageBox.question(self, "Process", "Preprocess the text?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if not self.cleaner:
                self.cleaner = TextPreprocessor()
            text = self.cleaner.process_text_pre(text)
            self.text_edit.setPlainText(text)
        else:
            self.text_edit.setPlainText(text)
        return
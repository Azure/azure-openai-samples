import os
import re
import chardet
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QTextCursor

import GUI.Common as comm

class PlainTextPasteEdit(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        return

    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())
        return
    
    def insertImage(self, file_name):
        image_html = f'<img src="{file_name}" alt="image" width="64" height="64"/>'
        self.insertHtml(image_html)
        self.moveCursor(QTextCursor.MoveOperation.End)
        return

    def getImagePaths(self):
        img_tags = re.findall(r'<img .*?src="([^"]*)"', self.toHtml())
        return img_tags
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        super().dragEnterEvent(event)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        return

    def dropEvent(self, event: QDropEvent):
        super().dropEvent(event)
        mime = event.mimeData()
        if mime.hasUrls():
            urls = mime.urls()
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    file_extension = os.path.splitext(file_path)[1].lower()
                    if comm.vision_flag and file_extension in \
                        ['.jfif', '.gif', '.jpeg', '.jpg', '.png', '.bmp', '.pjp', '.apng', '.pjpeg', '.avif']:
                        self.undo()
                        self.insertImage(file_path)
                    elif file_extension == '.txt':
                        with open(file_path, 'rb') as file:
                            raw_data = file.read()
                            result = chardet.detect(raw_data)
                            encoding = result['encoding']
                            if encoding in ['utf-8', 'UTF-8-SIG']:
                                text = raw_data.decode('utf-8')
                            else:
                                text = raw_data.decode(errors='ignore')
                        self.setText(text)
            event.acceptProposedAction()
        return
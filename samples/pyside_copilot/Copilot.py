import os
import sys

from PySide6.QtWidgets import QApplication
from GUI.ChatWindow import ChatWindow

# Set the encoding to UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"

# Create a PyQt6 application instance
app = QApplication(sys.argv)

# Run the application  
if __name__ == "__main__":
    app.setStyle("WindowsVista")
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

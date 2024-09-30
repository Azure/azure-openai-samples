import os
import sys

# Set the encoding to UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"

from PySide6.QtWidgets import QApplication
from GUI.ChatWindow import ChatWindow

# Create a PyQt6 application instance
app = QApplication(sys.argv)
app.setStyle("WindowsVista")

# Run the application  
if __name__ == "__main__":
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

# Main window class  
import os
import sys
import re
import datetime
import markdown
import configparser
import chardet

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMenu, QLineEdit, QDialog, QInputDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextBrowser, QPushButton, QMessageBox, QFileDialog, QSystemTrayIcon, QSplitter
from PySide6.QtGui import QTextCursor, QGuiApplication, QAction, QTextDocument, QPdfWriter, QIcon

from Core import ApiManager

import GUI.Common as comm
from GUI.PlainTextPasteEdit import PlainTextPasteEdit
from GUI.TextInputDialog import TextInputDialog
from GUI.CompletionsDialog import CompletionsDialog
from GUI.FunctionEditDialog import FunctionEditDialog
from GUI.ResponseWorker import ResponseWorker

# Welcome message
welcome_message = "Start chatting!\nTest your assistant by sending queries below."

# exe title
exe_title = "PySide Copilot"

class ChatWindow(QMainWindow):

    def __init__(self):  
        super().__init__()
        """
        Warning:
        It is not safe to get the key directly from the environment variable. 
        Please do not use it in the production environment!!!!!
        """
        api_key = os.getenv("AZURE_OPENAI_KEY")
        if api_key is None:
            api_key, ok = QInputDialog.getText(self, 'Auth', 'azure_ad_token:', QLineEdit.EchoMode.Password)
            if not ok:
                sys.exit()

        self.config = configparser.ConfigParser()
        try:
            with open("config.ini", "rb") as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                text = raw_data.decode(result['encoding'])
                self.config.read_string(text)
        except Exception as e:
            QMessageBox.information(self, "Load Configuration", "Failed to load configuration file!")
            sys.exit()
        
        self.user_role_name = self.config.get('EXE', 'user_role_name', fallback="User")
        self.assistant_role_name = self.config.get('EXE', 'assistant_role_name', fallback="Assistant")
        self.debug_mode = self.config.getboolean('EXE', 'debug_mode', fallback=False)

        comm.vision_flag = self.config.getboolean('Azure', 'vision', fallback=False)

        self.client = ApiManager(api_key)
        self.cfg_prompt_template = None

        # Window settings
        if hasattr(sys, '_MEIPASS'):
            self.icon_path = sys._MEIPASS
        else:
            self.icon_path = os.path.abspath(".")
        self.setWindowIcon(QIcon(os.path.join(self.icon_path, "icon.ico")))
        self.setWindowTitle("{} ({})".format(exe_title, self.client.deployment_name))
        self.setGeometry(0, 0, 480, 640)
        self.__initMenu()
        self.__initTray()

        # Layout and widgets  
        self.mainLayout = QVBoxLayout()
        self.splitter = QSplitter(Qt.Orientation.Vertical)

        self.chat_history = QTextBrowser()
        self.chat_history.setReadOnly(True)
        self.chat_history.setOpenExternalLinks(True)
        self.user_input = PlainTextPasteEdit()
        self.user_input.setMinimumHeight(100)

        self.splitter.addWidget(self.chat_history)
        self.splitter.addWidget(self.user_input)
        self.splitter.setSizes([400, 100]) 
        self.mainLayout.addWidget(self.splitter)

        self.buttonLayout = QHBoxLayout()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.on_send_message)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.on_reset_chat)

        self.buttonLayout.addWidget(self.reset_button)
        self.buttonLayout.addWidget(self.send_button)
        self.mainLayout.addLayout(self.buttonLayout)
  
        self.container = QWidget()  
        self.container.setLayout(self.mainLayout)  
        self.setCentralWidget(self.container)

        self.worker = None

        self.chat_history.append(welcome_message)

        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()
        x = (screenGeometry.width() - self.width()) / 2
        y = ((screenGeometry.height() - self.height()) / 2) - 50
        self.move(int(x), int(y))
        return
    

    def __initMenu(self):
        self.menuBar = self.menuBar()

        self.fileMenu = self.menuBar.addMenu("File")
        self.chatDataMenu = self.fileMenu.addMenu("Chat Json")
        self.exportChatJsonAction = QAction("Save as json", self)
        self.importChatJsonAction = QAction("Open json", self)
        self.chatDataMenu.addAction(self.exportChatJsonAction)
        self.chatDataMenu.addAction(self.importChatJsonAction)
        self.importAction = QAction("Open Document", self)
        self.exportAction = QAction("Save as Document", self)
        
        self.fileMenu.addAction(self.importAction)
        self.fileMenu.addAction(self.exportAction)

        self.exportChatJsonAction.triggered.connect(self.on_data_save_chat)
        self.importChatJsonAction.triggered.connect(self.on_data_import_chat)
        self.importAction.triggered.connect(self.on_data_import_data)
        self.exportAction.triggered.connect(self.on_data_export_pdf)

        self.compsMenu = self.menuBar.addMenu("Completion")
        self.compsAction = QAction("New Completion", self)
        self.compsClearExt = QAction("Clear Data", self)
        self.compsMenu.addAction(self.compsAction)
        self.compsMenu.addAction(self.compsClearExt)
        self.compsAction.triggered.connect(self.on_completions)
        self.compsClearExt.triggered.connect(self.on_completions_clear_ext)

        self.toolsMenu = self.menuBar.addMenu("Tools")
        self.toolsEdit = QAction("Edit Funcs", self)
        self.toolsMenu.addAction(self.toolsEdit)

        self.toolsCallMode = self.toolsMenu.addMenu("Call Mode")
        self.toolsCallAuto = QAction("Auto", self)
        self.toolsCallAuto.setCheckable(True)
        self.toolsCallForce = QAction("Force", self)
        self.toolsCallForce.setCheckable(True)
        self.toolsCallNone = QAction("Disable", self)
        self.toolsCallNone.setCheckable(True)
        self.toolsCallMode.addAction(self.toolsCallAuto)
        
        # TODO: The API is not yet fully developed, so the force call feature is temporarily disabled
        # self.toolsCallMode.addAction(self.toolsCallForce)
        
        self.toolsCallMode.addAction(self.toolsCallNone)
        self.toolsCallAuto.setChecked(True)
        
        self.toolsClear = QAction("Clear Funcs", self)
        self.toolsMenu.addAction(self.toolsClear)
    
        self.toolsEdit.triggered.connect(self.on_tools_edit_function)
        self.toolsClear.triggered.connect(self.on_tools_clear_function)
        
        self.toolsCallAuto.triggered.connect(self.on_tools_call_auto)
        self.toolsCallNone.triggered.connect(self.on_tools_call_none)
        self.toolsCallForce.triggered.connect(self.on_tools_call_force)
    
        self.cfgMenu = self.menuBar.addMenu("Config")
        self.cfgdefault = QAction("Default", self)
        self.cfgdefault.setCheckable(True)
        self.cfgdefault.setChecked(True)
        self.cfgMenu.addAction(self.cfgdefault)
        self.cfgdefault.triggered.connect(self.on_cfg_reset_config)

        self.cfgPromptTemplateMenu = None
        if os.path.exists(os.path.join(os.path.abspath("."), "template")):
            self.cfgPromptTemplateMenu = self.cfgMenu.addMenu("Templates")
            template_path = os.path.join(os.path.abspath("."), "template")
            for file in os.listdir(template_path):
                if file.endswith(".cfg"):
                    action = QAction(file, self)
                    action.setCheckable(True)
                    action.setChecked(False)
                    self.cfgPromptTemplateMenu.addAction(action)
                    action.triggered.connect(lambda checked, file=file: self.on_cfg_load_prompt_template(file))

        self.imgMenu = self.menuBar.addMenu("Vision")
        self.imgMenu.setEnabled(comm.vision_flag)

        self.importImg = QAction("Add Image", self)
        self.imgMenu.addAction(self.importImg)
        self.detailMenu = self.imgMenu.addMenu("Analysis Mode")
        self.detailLow = self.detailMenu.addAction("low")
        self.detailLow.setCheckable(True)
        self.detailLow.setChecked(True)
        self.detailHigh = self.detailMenu.addAction("high")
        self.detailHigh.setCheckable(True)
        self.importImg.triggered.connect(self.on_image_import)
        self.detailLow.triggered.connect(self.on_image_set_detail_low)
        self.detailHigh.triggered.connect(self.on_image_set_detail_high)

        return
    
    
    def __initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(self.icon_path, "icon.ico")))
        tray_menu = QMenu()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)
        return
    

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()
        return


    def closeEvent(self, event):
        if self.debug_mode:
            self.exit_app()
            return

        reply = QMessageBox.question(self, "Exit", "Minimize to tray?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if self.tray_icon.isVisible() and reply == QMessageBox.StandardButton.Yes:
            self.hide()
            event.ignore()
        else:
            self.exit_app()
        return


    def exit_app(self):
        self.tray_icon.hide()
        QApplication.quit()


    def on_cfg_reset_config(self):
        ret = self.client.reset_prompt_to_default()
        if not ret:
            QMessageBox.information(self, "Load Configuration", "Failed to load default configuration!")
            return

        self.cfg_prompt_template = None
        self.cfgdefault.setChecked(True)

        if self.cfgPromptTemplateMenu is not None:
            for action in self.cfgPromptTemplateMenu.actions():
                action.setChecked(False)

        self.setWindowTitle("{} ({})".format(exe_title, self.client.deployment_name))
        comm.vision_flag = self.config.getboolean('Azure', 'vision', fallback=False)
        self.imgMenu.setEnabled(comm.vision_flag)
        return
    

    def on_cfg_load_prompt_template(self, file):
        text = ""
        self.cfg_prompt_template = configparser.ConfigParser()

        try:
            with open(os.path.join(os.path.abspath("."), "template", file), "rb") as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                text = raw_data.decode(result['encoding'])
                self.cfg_prompt_template.read_string(text)
        except Exception as e:
            QMessageBox.information(self, "Load Configuration", f"Failed to load configuration file: {file.name}")
            self.on_cfg_reset_config()
            return
        
        ret = self.client.set_prompt_template(self.cfg_prompt_template)
        if not ret:
            QMessageBox.information(self, "Load Configuration", f"Failed to load configuration file: {file.name}")
            self.on_cfg_reset_config()
            return

        self.cfgdefault.setChecked(False)
        fname = os.path.basename(file.name)
        for action in self.cfgPromptTemplateMenu.actions():
            if action.text() != fname:
                action.setChecked(False)

        self.setWindowTitle("{} ({})".format(exe_title, self.client.deployment_name))
        comm.vision_flag = self.cfg_prompt_template.getboolean('Azure', 'vision', fallback=False)
        self.imgMenu.setEnabled(comm.vision_flag)
        return


    def on_data_import_data(self):
        dialog = TextInputDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = dialog.text_edit.toPlainText().strip().replace("￼", "")
            images = dialog.text_edit.getImagePaths()
            if not text and len(images) == 0:
                QMessageBox.information(self, "Document", "Import failed, text or image is empty!")
                return
            flag = self.client.add_extra_data(text, images)
            if not flag:
                QMessageBox.information(self, "Document", "Import failed, the number of images cannot exceed 10!")
        return
    

    def on_image_import(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Import Image", "", "Images (*.jfif *.gif *.jpeg *.jpg *.png *.bmp *.pjp *.apng *.pjpeg *.avif)")
        if file_name:
            with open(file_name, "rb"):
                self.user_input.insertImage(file_name)
        return
    

    def on_image_set_detail_low(self):
        self.client.set_detail("low")
        self.detailLow.setChecked(True)
        self.detailHigh.setChecked(False)
        return
    

    def on_image_set_detail_high(self):
        self.client.set_detail("high")
        self.detailLow.setChecked(False)
        self.detailHigh.setChecked(True)
        return
        

    def on_data_export_pdf(self):
        document = QTextDocument()
        document.setHtml(self.chat_history.toHtml())
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Export PDF", f"chat_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", "PDF Files (*.pdf)")
        if file_name:
            pdf_writer = QPdfWriter(file_name)
            document.print(pdf_writer)
        return
    

    def on_data_save_chat(self):
        if self.send_button.text() == "Responding...":
            return

        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Chat JSON", f"chat_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(self.client.get_conversion_json())
        return
    

    def on_data_import_chat(self):
        if self.send_button.text() == "Responding...":
            return

        if QMessageBox.question(self, "Restore Chat", "This operation will overwrite the current chat!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return

        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Restore Chat", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                ret, rStr = self.client.set_conversion_json(file.read())
                if ret == False:
                    QMessageBox.information(self, "Restore Chat", f"Error: {rStr}")
                    return
                chat_list = self.client.conversation.copy()
                for chat in chat_list:
                    if chat["role"] == "user":
                        self.update_chat_history(chat["content"], 0)
                    elif chat["role"] == "assistant":
                        self.update_chat_history(chat["content"], 1)
        return
    

    def on_completions(self):
        CompletionsDialog(self).show()
        return
    

    def on_completions_clear_ext(self):
        if QMessageBox.question(self, "Clear", "Are you sure you want to clear the additional data for completion mode?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.client.reset_completions_extra_data()
        return
    

    def on_tools_edit_function(self):
        dialog = FunctionEditDialog(self.client.get_tools(), self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = dialog.text_edit.toPlainText()
            flag, msg = self.client.set_tools(text)
            if not flag:
                QMessageBox.information(self, "Edit Functions", f"Import failed: {msg}")
        return
    

    def on_tools_clear_function(self):
        if QMessageBox.question(self, "Clear Functions", "Are you sure you want to clear the functions?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.client.set_tools("[]")
        return
    

    def on_tools_call_auto(self):
        self.toolsCallAuto.setChecked(True)
        self.toolsCallNone.setChecked(False)
        self.toolsCallForce.setChecked(False)
        self.client.set_tool_choice("auto")
        return
    

    def on_tools_call_none(self):
        self.toolsCallAuto.setChecked(False)
        self.toolsCallNone.setChecked(True)
        self.toolsCallForce.setChecked(False)
        self.client.set_tool_choice("none")
        return
    

    def on_tools_call_force(self):
        return
        

    def on_reset_chat(self):
        if QMessageBox.question(self, "Reset Chat", "Are you sure you want to reset current chat history?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.chat_history.clear()
            self.client.reset_chat()
            self.chat_history.append(welcome_message)
        return


    def on_send_message(self):
        self.send_button.setEnabled(False)
        img_paths = self.user_input.getImagePaths()
        user_message = self.user_input.toPlainText().strip().replace("￼", "")
            
        if user_message or len(img_paths) > 0:
            self.update_chat_history(user_message, 0, img_paths)
            self.user_input.clear()
            if self.debug_mode:
                flag, req = self.client.get_chat_response(user_message, img_paths)
                self.on_update_response((flag, req))
            else:
                self.worker = ResponseWorker(self.client, user_message, img_paths=img_paths)
                self.worker.signal.connect(self.on_update_response)
                self.send_button.setText("Responding...")
                self.send_button.clicked.disconnect()
                self.send_button.clicked.connect(self.on_stop_response)
                self.send_button.setEnabled(True)
                self.worker.start()
                return
        self.send_button.setEnabled(True)
        return
    

    def on_stop_response(self):
        if QMessageBox.question(self, "Stop Response", "Are you sure you want to stop the response?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            if self.worker:
                self.worker.terminate()
                self.worker = None
                self.update_chat_history("Stop response!", 2)
                self.send_button.setText("Send")
                self.send_button.clicked.disconnect()
                self.send_button.clicked.connect(self.on_send_message)
        return


    def on_update_response(self, response):
        if not self.debug_mode:
            self.send_button.setText("Send")
            self.send_button.clicked.disconnect()
            self.send_button.clicked.connect(self.on_send_message)

        flag, req = response
        if flag:
            self.update_chat_history(req, 1)
        else:
            self.update_chat_history(req, 2)
        return
  

    def update_chat_history(self, message, msgType=3, imgPaths=[]):
        if msgType == 0:
            headerText = f'<p style="color: green; margin: 0;"><b>{datetime.datetime.now().strftime(f"[{self.user_role_name}] %Y-%m-%d %H:%M:%S")}</b></p>'
        elif msgType == 1:
            headerText = f'<p style="color: blue; margin: 0;"><b>{datetime.datetime.now().strftime(f"[{self.assistant_role_name}] %Y-%m-%d %H:%M:%S")}</b></p>'
        elif msgType == 2:
            headerText = f'<p style="color: red; margin: 0;"><b>{datetime.datetime.now().strftime("[Error] %Y-%m-%d %H:%M:%S")}</b></p>'
        else:
            headerText = f'<p style="margin: 0;">{datetime.datetime.now().strftime("[Other] %Y-%m-%d %H:%M:%S")}</p>'
        
        headerText = f"<br>{headerText}<p style='margin: 0;'></p>"
        
        message = re.sub(r'```(\w*\n)?(.*?)```', comm.replace_code_block, message, flags=re.DOTALL)
        if msgType == 1:
            message = markdown.markdown(message)

        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)
        self.chat_history.insertHtml(headerText)
        self.chat_history.insertHtml(message)
        if imgPaths:
            self.chat_history.insertHtml(f'<br><p style="color: #FF8C00; margin: 0;"><b>Images:</b></p><br>')
            for imgPath in imgPaths:
                self.chat_history.insertHtml(f'<img src="{imgPath}" alt="image" width="128" height="128" />&nbsp;')
        self.chat_history.moveCursor(QTextCursor.MoveOperation.End)
        return
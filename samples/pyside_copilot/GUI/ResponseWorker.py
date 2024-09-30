from PySide6.QtCore import QThread, Signal

# Response worker class
class ResponseWorker(QThread):
    signal = Signal(object)

    def __init__(self, client, user_message, comps=False, cfg_prompt_template=None, img_paths=[]):
        super().__init__()
        self.client = client
        self.user_message = user_message
        self.comps = comps
        self.prompt_template = cfg_prompt_template
        self.img_paths = img_paths

    def run(self):
        if self.comps:
            flag, req = self.client.get_completions_response(self.user_message, self.prompt_template, img_paths=self.img_paths)
        else:
            flag, req = self.client.get_chat_response(self.user_message, img_paths=self.img_paths)
        self.signal.emit((flag, req))

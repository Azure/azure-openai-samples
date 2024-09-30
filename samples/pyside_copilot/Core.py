from openai import AzureOpenAI
import tiktoken

import io
from PIL import Image
import configparser
import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from mimetypes import guess_type
import chardet
import threading

class ApiManager:

    def __init__(self, api_key: str):
        self.config = configparser.ConfigParser()

        config_txet = ""
        try:
            with open("config.ini", "rb") as file:
                config_txet = file.read()
                result = chardet.detect(config_txet)
                config_txet = config_txet.decode(result['encoding'])
                self.config.read_string(config_txet)
        except Exception as e:
            raise Exception("config.ini file not found")
        
        self.deployment_name = self.config.get('Azure', 'deployment_name', fallback="gpt-35-turbo")
        self.max_hist_msg_count = self.config.getint('Azure', 'max_hist_msg_count', fallback=10)

        self.client = AzureOpenAI(
            api_key= api_key,  
            azure_endpoint = self.config.get('Azure', 'openai_endpoint', fallback="https://api.openai.com"),
            api_version= self.config.get('Azure', 'api_version', fallback="2024-06-01")
        )
        self.token_limit = self.config.getint('Azure', 'token_limit', fallback=4096)

        self.tokeniser = self.config.get('Azure', 'tokeniser', fallback="cl100k_base")
        self.encoding = tiktoken.get_encoding(self.tokeniser)
        self.encoding_thread_flag = self.config.getboolean('EXE', 'encoding_thread_flag', fallback=False)
        self.encoding_obj_lock = threading.Lock()

        self.defult_system_message = {"role": "system", "content": self.config.get('Chat', 'defult_system_message', fallback="You are an Assistant that helps User find information.")}
        self.extra_data_header = {"role": "system", "content": self.config.get('Chat', 'extra_data_header', fallback="The User manually adds data to optimize the chat with the Assistant:")}
        self.conversation = [self.defult_system_message]
        
        self.extra_data_chat = []
        self.extra_data_completions = []
        
        self.tools = []
        self.tool_choice = "auto"
        self.img_detail = "low"

        self.max_tokens = self.config.getint('Chat', 'max_tokens', fallback=800)
        self.temperature = self.config.getfloat('Chat', 'temperature', fallback=0.7)
        self.top_p = self.config.getfloat('Chat', 'top_p', fallback=0.95)
        return
    

    def __num_tokens_from_messages(self, messages: list):
        num_tokens = 0
        num_images = 0
        
        def encode_value(value):
            images = 0
            encoded = 0
            if isinstance(value, str):
                encoded += len(self.encoding.encode(value))
            else:
                for item in value:
                    if item["type"] == "text":
                        encoded += len(self.encoding.encode(item["text"]))
                    elif item["type"] == "image_url":
                        if item["image_url"]["detail"] == "high":
                            blocks = self.__calculate_num_blocks(item["image_url"]["url"])
                            encoded += (170 * blocks + 85)
                        else:
                            encoded += 85
                        images += 1
            return encoded, images

        if self.encoding_thread_flag and (len(messages) >= 5 or len(self.extra_data_chat) != 0 or len(self.extra_data_completions) != 0):
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(encode_value, message[key]) for message in messages for key, value in message.items() if value is not None]
                for future in as_completed(futures):
                    tokens, images = future.result()
                    num_tokens += tokens
                    num_images += images
        else:
            for message in messages:
                for key, value in message.items():
                    if value is not None:
                        tokens, images = encode_value(value)
                        num_tokens += tokens
                        num_images += images
                                
        return num_tokens, num_images


    def __calculate_num_blocks(self, image_url: str):
        image_data = base64.b64decode(image_url.split(',', 1)[1])
        image = Image.open(io.BytesIO(image_data))
        
        max_size = (2048, 2048)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        if image.width < image.height:  
            scale_factor = 768 / image.width
        else:  
            scale_factor = 768 / image.height
            
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        num_blocks_wide = (new_width + 511) // 512
        num_blocks_high = (new_height + 511) // 512
        total_blocks = num_blocks_wide * num_blocks_high
        
        return total_blocks


    def __image_to_base64(self, image_path: str):
        mime_type, _ = guess_type(image_path)
        if mime_type is None:
             mime_type = 'application/octet-stream'

        try:
            with open(image_path, "rb") as image_file:
                base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            return ""
        
        return f"data:{mime_type};base64,{base64_encoded_data}"


    def __add_conversation(self, role: str, content: str, img_paths=[]):
        current_img_num = len(img_paths)
        if current_img_num > 10:
            return 0, False
        
        with self.encoding_obj_lock:
            if current_img_num > 0:
                _, conv_current_images = self.__num_tokens_from_messages(self.conversation) 
                if conv_current_images + current_img_num > 10:
                    return 0, False

            if len(self.conversation) > self.max_hist_msg_count:
                del self.conversation[1]

            if 0 < current_img_num <= 10:
                contentList = [{"type": "text", "text": content}]
                for imgPath in img_paths:
                    contentList.append({"type": "image_url", \
                                        "image_url": \
                                            {
                                             "url": self.__image_to_base64(imgPath), \
                                             "detail": self.img_detail \
                                            }
                                        })
                self.conversation.append({"role": role, "content": contentList})
            else:
                self.conversation.append({"role": role, "content": content})

            conv_history_tokens, _ = self.__num_tokens_from_messages(self.conversation) 
            while conv_history_tokens + self.max_tokens >= self.token_limit:
                del self.conversation[1]
                conv_history_tokens, _ = self.__num_tokens_from_messages(self.conversation)

        return conv_history_tokens, True


    def reset_chat(self):
        self.conversation = [self.defult_system_message]
        self.extra_data_chat.clear()
        return True
    

    def reset_completions_extra_data(self):
        self.extra_data_completions.clear()
        return True
    

    def add_extra_data(self, text: str, img_paths=[]):
        if len(img_paths) > 10:
            return False

        if len(self.extra_data_chat) == 0:
            self.extra_data_chat = [self.extra_data_header]
        if len(self.extra_data_completions) == 0:
            self.extra_data_completions = [self.extra_data_header]

        if 0 < len(img_paths) <= 10:
            contentList = [{"type": "text", "text": text}]
            for imgPath in img_paths:
                contentList.append({"type": "image_url", \
                                    "image_url": \
                                        {
                                         "url": self.__image_to_base64(imgPath), \
                                         "detail": self.img_detail \
                                        }
                                    })
            self.extra_data_chat.append({"role": "system", "content": contentList})
            self.extra_data_completions.append({"role": "system", "content": contentList})
        else:
            self.extra_data_chat.append({"role": "system", "content": text})
            self.extra_data_completions.append({"role": "system", "content": text})
        return True
    

    def set_defult_system_message(self, text: str):
        self.defult_system_message["content"] = text
        self.conversation[0] = self.defult_system_message
        return True
    

    def set_temperature(self, temperature: float):
        self.temperature = temperature
        return True
    

    def set_top_p(self, top_p: float):
        self.top_p = top_p
        return True
    

    def set_deployment_name(self, deployment_name: str):
        self.deployment_name = deployment_name
        return True
    

    def set_detail(self, detail: str):
        if detail not in ["low", "high"]:
            return False
        self.img_detail = detail
        return True
    

    def reset_prompt_to_default(self):
        with self.encoding_obj_lock:
            self.deployment_name = self.config.get('Azure', 'deployment_name', fallback="gpt-35-turbo")
            self.tokeniser = self.config.get('Azure', 'tokeniser', fallback="cl100k_base")
            self.encoding = tiktoken.get_encoding(self.tokeniser)
            self.token_limit = self.config.getint('Azure', 'token_limit', fallback=4096)
            self.defult_system_message = {"role": "system", "content": self.config.get('Chat', 'defult_system_message', fallback="You are an Assistant that helps User find information.")}
            self.conversation[0] = self.defult_system_message
            self.temperature = self.config.getfloat('Chat', 'temperature', fallback=0.7)
            self.top_p = self.config.getfloat('Chat', 'top_p', fallback=0.95)
        return True
    

    def set_prompt_template(self, cfg: configparser.ConfigParser):
        with self.encoding_obj_lock:
            self.deployment_name = cfg.get("Azure", "deployment_name", fallback="gpt-35-turbo")
            self.tokeniser = cfg.get("Azure", "tokeniser", fallback="cl100k_base")
            self.encoding = tiktoken.get_encoding(self.tokeniser)
            self.token_limit = cfg.getint("Azure", "token_limit", fallback=4096)
            self.temperature = cfg.getfloat("Chat", "temperature", fallback=0.5)
            self.top_p = cfg.getfloat("Chat", "top_p", fallback=0.9)
            self.defult_system_message["content"] = cfg.get("Chat", "defult_system_message", fallback="")
            self.conversation[0] = self.defult_system_message
        return True
    

    def set_tools(self, toolsStr: str):
        if toolsStr and toolsStr != "[]":
            try:
                self.tools = json.loads(toolsStr)
            except Exception as e:
                return False, str(e)
        else:
            self.tools.clear()
        return True, ""
    

    def get_tools(self):
        if len(self.tools) == 0:
            return "[]"
        return json.dumps(self.tools, indent=4).encode('utf-8').decode('unicode_escape')
    

    def set_tool_choice(self, flag: str):
        if flag in ["auto", "none"]:
            self.tool_choice = flag
        else:
            self.tool_choice = json.dumps('{"name": "' + flag + '"}')
        return
    

    def get_conversion_json(self):
        return json.dumps(self.conversation)
    

    def set_conversion_json(self, convStr: str):
        try:
            self.conversation = json.loads(convStr)
        except Exception as e:
            return False, str(e)
        return True, ""
    

    def get_chat_response(self, user_message: str, img_paths=[]):
        response_message = ""
        if len(self.extra_data_chat) > 0:
            self.conversation = self.conversation + self.extra_data_chat
            self.extra_data_chat.clear()

        try:
            num_tokens, flag = self.__add_conversation("user", user_message, img_paths)
            if not flag:
                return False, "Too many images (max 10) or prompt is not a string!"

            if len(self.tools) > 0 and self.tool_choice != "none":
                response = self.client.chat.completions.create(\
                    model=self.deployment_name, \
                    messages=self.conversation, \
                    tools=self.tools, \
                    tool_choice=self.tool_choice, \
                    max_tokens=self.max_tokens, \
                    temperature=self.temperature, \
                    top_p=self.top_p)
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                if not tool_calls:
                    return False, str("No tool calls found in response")
                
                tools_conversation = self.conversation.copy()
                tools_conversation.append(response_message)

                for tool_call in tool_calls:
                    tools_conversation.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_call.function.name,
                            "content": tool_call.function.arguments
                        }
                    )
            
                response = self.client.chat.completions.create(\
                model=self.deployment_name, \
                messages=tools_conversation, \
                max_tokens=self.max_tokens, \
                temperature=self.temperature, \
                top_p=self.top_p)

                response_message = response.choices[0].message.content
                self.__add_conversation("assistant", response_message)
                return True, response_message
            
            else:

                response = self.client.chat.completions.create(\
                    model=self.deployment_name, \
                    messages=self.conversation, \
                    max_tokens=self.max_tokens, \
                    temperature=self.temperature, \
                    top_p=self.top_p)
                
                response_message = response.choices[0].message.content
                self.__add_conversation("assistant", response_message)
                return True, response_message
            
        except Exception as e:  
            return False, str(e)
        

    def get_completions_response(self, prompt: str, cfg=None, img_paths=[]):
        if len(img_paths) > 10:
            return False, "Too many images (max 10) or prompt is not a string!"

        comps_max_tokens = self.config.getint('Completions', 'max_tokens', fallback=2048)
        if cfg is not None:
            comps_descriptor = cfg.get('Completions', 'descriptor', fallback="You are an Assistant that helps User complete tasks.")
            comps_temperature = cfg.getfloat('Completions', 'temperature', fallback=1)
            comps_top_p = cfg.getfloat('Completions', 'top_p', fallback=0.50)
        else:
            comps_descriptor = self.config.get('Completions', 'descriptor', fallback="You are an Assistant that helps User complete tasks.")
            comps_temperature = self.config.getfloat('Completions', 'temperature', fallback=1)
            comps_top_p = self.config.getfloat('Completions', 'top_p', fallback=0.50)


        system_message = \
        """
        {descriptor}\n
        Instructions:
        - You have been switched to completion mode (instructGPT), non chat scenarios.
        - User provide a prompt, and the You will completion the task.
        - The user will only provide one prompt, so please try to generate rich and high-quality content.
        - The final completion content uses the language of the prompt content.
        - The user permits a maximum token (max_tokens) return of {max_tokens}.
        """.format(descriptor=comps_descriptor, max_tokens=comps_max_tokens)

        completions = [{"role": "system", "content": system_message}]
        if len(self.extra_data_completions) > 0:
            completions = completions + self.extra_data_completions

        if 0 < len(img_paths) <= 10:
            contentList = [{"type": "text", "text": prompt}]
            for imgPath in img_paths:
                contentList.append({"type": "image_url", \
                                    "image_url": \
                                        {
                                         "url": self.__image_to_base64(imgPath), \
                                         "detail": self.img_detail \
                                        }
                                    })
            completions.append({"role": "user", "content": contentList})
        else:
            completions.append({"role": "user", "content": prompt})

        with self.encoding_obj_lock:
            conv_history_tokens, _ = self.__num_tokens_from_messages(completions)
        if conv_history_tokens + comps_max_tokens >= self.token_limit:
            return False, "The prompt is too long, please provide a shorter prompt!"

        try:
            if len(self.tools) > 0 and self.tool_choice != "none":
                response = self.client.chat.completions.create(\
                    model=self.deployment_name, \
                    messages=completions, \
                    tools=self.tools, \
                    tool_choice=self.tool_choice, \
                    max_tokens=comps_max_tokens, \
                    temperature=comps_temperature, \
                    top_p=comps_top_p, \
                    n=1)
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                if not tool_calls:
                    return False, str("No tool calls found in response")
                
                tools_conversation = completions.copy()
                tools_conversation.append(response_message)

                for tool_call in tool_calls:
                    tools_conversation.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_call.function.name,
                            "content": tool_call.function.arguments
                        }
                    )

                response = self.client.chat.completions.create(\
                model=self.deployment_name, \
                messages=tools_conversation, \
                max_tokens=self.max_tokens, \
                temperature=self.temperature, \
                top_p=self.top_p)

                final_message = response.choices[0].message.content
                return True, final_message
            
            else:

                response = self.client.chat.completions.create(\
                    model=self.deployment_name, \
                    messages=completions, \
                    max_tokens=comps_max_tokens, \
                    temperature=comps_temperature, \
                    top_p=comps_top_p)
                
                response_message = response.choices[0].message.content
                return True, response_message
            
        except Exception as e:  
            return False, str(e)

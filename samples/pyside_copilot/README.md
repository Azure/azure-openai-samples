# PySide Copilot

This is a Chatbot Client implemented using PySide6(LGPL), providing a reference for calling the Azure OpenAI API.

**Features:**
- Basic ChatCompletion functionality. 
- Prompt Demo, which includes a Completion mode implemented using Prompt-Engineering. 
- Local token count check using tiktoke to ensure safety. 
- Demonstration of Vision series Image requests and token count calculation.
- Demonstration of ToolCall related functionalities. 
- Processing of imported documents (docx, pdf, txt) for stopword removal and lemma extraction to improve token efficiency. 
- Flexible switching of parameters such as deployment_name, top_p, system_message, etc. 
- Exporting or restoring chat history to/from JSON. 
- Exporting Chat history and Completion as PDF documents.

**Notes:** 
- The demonstration code loads the api_key from environment variables; encryption is required for actual use! 
- The ToolCall feature currently only provides JSON request implementation and does not demonstrate calling Python code. 
- It has not undergone a complete testing process.

**Directory Structure:** 
- Copilot.py: Program entry point, where the main function is located. (This is actually a habit from my days as a C++ developer...emmmmm) 
- Core.py: Code for calling the Azure OpenAI API, completely separated from the GUI. 
- GUI: Directory for PySide6 GUI related code. 
- template: Directory for Prompt configuration files. 
- TextPreprocessor.py: Code for processing text.
- config.ini: Configuration file, all configurable parameters are in this file.

**Runtime Environment:** 
- Windows 11 Pro 23H2 x64 
- Python 3.11.10 64bit 
- Pyip OpenAI 1.50.0 
- Pyip PySide 6.7.3 
- Other dependencies in requirements.txt
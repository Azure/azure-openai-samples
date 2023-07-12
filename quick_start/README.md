# 프롬프트 엔지니어링 Code를 이용한 실습

There are two ways to authenticate (see Jupyter notebooks):
1. (Recommended) Use the Azure CLI to authenticate to Azure and Azure OpenAI Service
2. Using a token (not needed if using the Azure CLI)

Get the Azure OpenAI Service endpoint (and key) from the Azure portal.

### Workspace environment

Choose one of the following options to set up your environment: Codespaces, Devcontainer or bring your own environment (Anaconda). Building the environment can take a few minutes, so please start early.

#### 1️⃣ Codespaces

> 🌟 Highly recommended: *Best option if you already have a Github account. You can develop on local VSCode or in a browser window.*

* Go to Github repository and click on `Code` button
* Create and edit the `.env` file in the base folder including Azure OpenAI Service endpoint and key before starting any notebooks

#### 2️⃣ Devcontainer

> *Usually a good option if VSCode and Docker Desktop are already installed.*

* Install [Docker](https://www.docker.com/products/docker-desktop)
* Install [Visual Studio Code](https://code.visualstudio.com/)
* Install [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
* Clone this repository
* Open the repository in Visual Studio Code
* Click on the green button in the bottom left corner of the window
* Select `Reopen in Container`
* Wait for the container to be built and started
* Create and edit `.env` file in the base folder including Azure OpenAI Service endpoint and key before starting any notebooks

#### 3️⃣ Bring your own environment

> *If you already have a Python environment with Jupyter Notebook and the Azure CLI installed.*

Make sure you have the requirements installed in your Python environment using `pip install -r requirements.txt`.

-------------------

## Prepare Conda Environment
Use requirements.txt to install necessary packages

## Setup Environmental Variable
After creating Azure OPENAI service, setup 2 environmental variables for 
- OPENAI_API_BASE
- OPENAI_API_KEY
- DEPLOYMENT_NAME = 'text-davinci-003'

Optional - Used for "OpenAI Large Language Model Chain of Thoughts Demo"
- AZURE_COGNITIVE_SEARCH_ENDPOINT
- AZURE_COGNITIVE_SEARCH_KEY
## Run Demo Code
# 프롬프트 엔지니어링 Code를 이용한 실습

## 실습을 위한 개발환경 선택하기
해당 실습을 원활하게 제공하기 위해서 .devcontainer 환경을 제공하고 있습니다. 나의 PC에 Docker나 IDE 설치를 원하지 않는다면, `CodeSpace`를 권장합니다. 
- Local PC에 `Docker`가 설치되어 있다면, VS Code에서 Reopen DevContainer를 실행하여 Docker에 컨테이너 이미지를 생성하면 자동으로 실습 가능한 런타임과 패키지들이 설치되도록 구성되어 있습니다.
- GitHub에서 제공하는 `CodeSpace`를 활용하면, CodeSpace가 제공하는 리모트 VM에 컨테이너가 올라가고, CodeSpace가 제공하는 웹브라우저 용 VS Code를 통해 즉시 개발을 진행할 수 있습니다.

참고: `CodeSpace`는 GitHub 개인 계정에게 월 15GB의 저장공간과 120 시간/core의 VM을 무료로 제공합니다. [자세한 가격 정보 참고는 클릭](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)


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
- DEPLOYMENT_NAME = 'gpt-35-turbo'

Optional - Used for "OpenAI Large Language Model Chain of Thoughts Demo"
- AZURE_COGNITIVE_SEARCH_ENDPOINT
- AZURE_COGNITIVE_SEARCH_KEY
## Run Demo Code
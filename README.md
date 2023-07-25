# GPT 기초, 사용 사례 및 샘플 솔루션 - 한국어 버전
이 리포지토리에는 Azure OpenAI에서 제공하는 GPT(Generative Pre-trained Transformer)를 사용하는 기본 방법을 이해하고 샘플 솔루션을 및 다양한 사용 사례를 통해 이해에 도움이 되는 리소스가 포함되어 있습니다.

## GPT란?
GPT(Generative Pre-trained Transformer)는 OpenAI에서 개발한 LLM(Large Language Model)입니다. 트랜스포머 아키텍처 기반의 딥러닝 모델입니다. 자세한 내용은 [OpenAI](openai.com)를 참조하세요.
간단하게 정리된 문서는 다음을 참고하세요.
- [Azure OpenAI 소개 - 한글 deck](http://azure.studydev.site/openai/aoai_2023_201.pdf)
- [Azure OpenAI 서비스 최신 업데이트 - 한글 deck](http://azure.studydev.site/openai/aoai_2023_sol.pdf)

## 리소스
다음의 순서로 GPT를 학습할 수 있습니다.

- [(누구나) Prompt Engineering - 기초](http://azure.studydev.site/openai/aoai_2023_pe_01.pdf)

- [(누구나) Prompt Engineering - Playground에서 놀기](http://azure.studydev.site/openai/aoai_2023_pe_02.pdf)

- [(개발자) Prompt Engineering - IDE에서 개발](http://azure.studydev.site/openai/aoai_2023_pe_03.pdf)

- [(개발자) Prompt Engineering - Quick Start](./quick_start/): GPT 사용을 빠르게 시작할 수 있는 노트북 모음입니다.

- [Use Cases | Kakao Navi 길찾기 API 통합](./use_cases/kakao_navi/notebooks/kakao_navi.ipynb): GPT의 Function Calling 기능에 실시간 카카오 Navi API를 연동하는 방법을 학습합니다.

----

- [Fundamentals](./fundamentals/): GPT의 기본 사용법을 설명하는 노트북 모음입니다.

- [Use Cases](./use_cases/): 챗봇, 고객 서비스, 콘텐츠 생성 등과 같은 다양한 애플리케이션에서 GPT를 사용하는 방법에 대한 예제를 보여주는 노트북 모음입니다.

- [Sample Solutions](./solution_accelerators/): GPT가 솔루션의 일부인 다양한 산업에 특화된 비즈니스 애플리케이션 맥락에서 질문 답변, 텍스트 요약 및 감정 분석 등과 같은 다양한 NLP 작업을 위한 종단 간 솔루션입니다. *기여가 필요합니다!*

- [Serverless SQL GPT](https://github.com/balakreshnan/Samples2023/blob/main/AzureML/serverlesssqlgpt.md) - Azure Machine Learning을 사용하는 Azure Synapse Analytics Serverless SQL에서 GPT를 사용한 NLP(자연어 처리).

## GPT Version
현재 여기의 샘플은 주로 GPT 3.5를 기반으로 합니다. 일반적으로 gpt-35-turbo 최신 모델을 활용합니다. OpenAI의 모델 정책에 맞추어 Chat Completion API 기반으로 컨텐츠가 수정중에 있습니다. 한국어 토큰 길이에 대한 제약이 있을 경우에는 gpt-35-turbo-16k 모델을 활용하는 것을 추천 드립니다. GPT-4는 가용할 수 있는 자원이 충분히 확보된 시점에 업데이트할 예정입니다.

## 설정하기
이 리포지토리에서 샘플 코드를 사용하려면 Azure 서비스에 대한 주요 정보를 저장하는 .env 파일을 설정하는 것이 좋습니다. 예를 들어 [.env.sample](./.env.sample) 파일을 복사하여 `.env` 파일을 만들고 해당 API KEY 정보를 입력하여 사용합니다.

# 개발환경 선택하기
해당 실습을 원활하게 제공하기 위해서 .devcontainer 환경을 제공하고 있습니다. 나의 PC에 Docker나 IDE 설치를 원하지 않는다면, `CodeSpace`를 권장합니다. 
- Local PC에 `Docker`가 설치되어 있다면, VS Code에서 Reopen DevContainer를 실행하여 Docker에 컨테이너 이미지를 생성하면 자동으로 실습 가능한 런타임과 패키지들이 설치되도록 구성되어 있습니다.
- GitHub에서 제공하는 `CodeSpace`를 활용하면, CodeSpace가 제공하는 리모트 VM에 컨테이너가 올라가고, CodeSpace가 제공하는 웹브라우저 용 VS Code를 통해 즉시 개발을 진행할 수 있습니다.

참고: `CodeSpace`는 GitHub 개인 계정에게 월 15GB의 저장공간과 120 시간/core의 VM을 무료로 제공합니다. [자세한 가격 정보 참고는 클릭](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)

## Contributing
We welcome contributions to this repository. If you have any ideas or suggestions, please feel free to open an issue or submit a pull request.

As technologies changes very fast, we endevour to keep this repository updated as quick as possible. However, this is heavily rely on keen community contributors to make this happen.

## Solution Accelerators
- **Business Process Automation:**
   - https://github.com/Azure/business-process-automation
   
- **Azure Cognitive Search + OpenAI**
   - https://github.com/Azure-Samples/azure-search-openai-demo

- **PowerApp + OpenAI**
   - https://github.com/Azure/azure-openai-samples/tree/main/solution_accelerators/PowerApp
   
- **Azure SQL Datbase + OpenAI**
   - https://github.com/louis-li/SqlGPT

- **ChatGPT + Enterprise data with Azure OpenAI**
   - https://github.com/lordlinus/Enterprise-ChatGPT

- **Azure OpenAI Semantic Search Demo | Document Upload**
   - https://github.com/MaheshSQL/openai-vector-search-demo

- **Redis + OpenAI**
   - https://github.com/louis-li/pdfGPT

## Relevant Repositories
- **OpenAI Cookbook**
   -  https://github.com/openai/openai-cookbook

- **Call center solutions:**
   - https://github.com/jakeatmsft/AzureOpenAIExamples/blob/main/Examples/Speech/Conversation_SSML%20OpenAI.ipynb 
   - https://github.com/amulchapla/AI-Powered-Call-Center-Intelligence 

- **Income Statement Analysis:**
   - https://github.com/jakeatmsft/AzureOpenAIExamples/blob/main/Examples/FormRecognizer/Balance_sheet_analysis.ipynb 

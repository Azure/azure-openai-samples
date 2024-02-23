# OpenAI PowerApp

This application demonstrates the exceptional capabilities of Azure AI Cognitive Services in extracting data from various unstructured file formats. Additionally, it provides insights on how OpenAI can be seamlessly integrated into workflows to develop valuable applications. By utilizing interactive demos and features, users can explore the impressive capabilities of OpenAI's machine learning and natural language processing. The OpenAI large language model (LLM) enables quick comprehension and analysis of unstructured data such as audio files, PDFs, and videos. Leveraging Azure Cognitive Services and the Power Platform, organizations can automate processes for improved handling of inquiries, feedback, and conversations, thus empowering their operations.

<b>This application is built on PowerPlatform and used Azure AI & Open AI http endpoints via PowerAutomate to connect to Azure Services.

App Landing Page: ![image](https://github.com/msavita-cloud/azure-openai-samples/assets/65045244/2ca0f7c8-f900-4785-ada7-77b7345f3748)</b><BR>

<b>PDF Extraction and Ask Questions from extracted text:</b><BR><BR>
![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/04b03163-b18c-47b7-9b3c-1e4e55ca1db8)<BR><BR>
<b>Video Insights Extraction and Ask Questions from extracted text:</b><BR><BR>
![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/85526861-59c6-4bc8-9509-a28487af71c6)

Let's build a Power App to use Azure AI & Open AI to Improve Productivity

<b>What's needed</b><BR>
<b>Azure Open AI</b>

1. Register for Azure Open AI - https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview
2. Once got approved create Azure Open AI resource in Azure portal.
3. Select region as East US
4. At the time of writing this article davinci-003 is only available in East US
5. Create a deployment inside the resource.

Computer Vision (for PDF extraction)
https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision

Speech Service (For Speech Extraction)
https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices

Video Indexer (Extract insights from Video)
https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-get-started

<b>Import PowerApp</b>
1. Download .zip file from repository
2. Import package in PowerApps
https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/export-import-app#importing-a-canvas-app-package

<b>Update all the endPoints in PowerAutomate </b>

  1. Video Indexer - OpenAIVideoToText

  <li>Go to Flow.microsoft.com</li>
<li>Edit <b>OpenAIVideoToText</b></li>
<li>Get accesstoken from Azure Video Indexer at Portal.Azure.com</li>

![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/aea11849-995b-4ca8-baee-555875ed53e7)
Update accesstoken in powerautomate
![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/d8e2d9b1-e429-4f4e-8aa3-a79b63033287)
<BR><BR><BR>
2. Computer Vision - OpenAIPDFExtraction
 <li>Go to Flow.microsoft.com</li>
<li>Edit <b>OpenAIPDFExtraction</b></li>
<li>Get keys and endpoint from computer vision in Portal.Azure.com</li>

![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/9335a201-70e0-45df-8597-d6bbbfd15073)
Update http url and key in powerautomate
![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/200438e3-5426-495c-9a13-aac766fbaaae)

3. Speech - OpenAIAudioToText
 <li>Go to Flow.microsoft.com</li>
<li>Edit <b>OpenAudioToText</b></li>
<li>Get keys and endpoint from Speech in Portal.Azure.com</li>

![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/82c54481-4eaa-4698-b7e3-498fe962e674)
Update http url and key in powerautomate
![image](https://github.com/msavita-cloud/OpenAIPowerApp/assets/65045244/65514fb4-926e-442e-8847-40acd029da78)
  
  4. OpenAI - Openaigeneral, Openaisummarization-Summary

![image](https://github.com/msavita-cloud/azure-openai-samples/assets/65045244/c4def313-c60b-4a57-884e-367102e2c930)

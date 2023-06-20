# OpenAI PowerApp

This application showcases the incredible capabilities of Azure AI Cognitive services in extracting data from diverse unstructured file formats. It also highlights the seamless integration of OpenAI's cutting-edge machine learning and natural language processing technologies, enabling users to unlock powerful insights and drive meaningful outcomes. By leveraging interactive demos and a wide range of features, you can experience firsthand the transformative potential of OpenAI. Rapidly derive valuable insights from unstructured data, including audio files, PDF documents, and videos. Additionally, streamline your operations by creating automated workflows using Azure cognitive services and Power Platform, empowering you to efficiently handle inquiries, feedback, and conversations.

![image](https://github.com/msavita-cloud/azure-openai-samples/assets/65045244/2ca0f7c8-f900-4785-ada7-77b7345f3748)

Let's build a Power App to use Azure AI & Open AI to Improve Productivity

<b>What's needed</b>

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

# Import langchain and azure cognitive search
import langchain
from typing import Dict, List
from pydantic import BaseModel, Extra, root_validator
from langchain.utils import get_from_dict_or_env
from langchain.tools.base import BaseTool

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import azure.search.documents as azs


class AzureCognitiveSearchWrapper(BaseModel):
    """Wrapper for Azure Cognitive Search API.

    In order to set this up, follow instructions at:
    https://levelup.gitconnected.com/api-tutorial-how-to-use-bing-web-search-api-in-python-4165d5592a7e
    """

    azure_cognitive_search_key: str
    azure_cognitive_search_endpoint: str
    index_name: str
    k: int = 3
    api_version: str = "2021-04-30-Preview"
    result_field_list: list = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def _cognitive_search_results(self, search_term: str, count: int) -> List[dict]:
        search_client = SearchClient(endpoint=self.azure_cognitive_search_endpoint,
                            index_name=self.index_name ,
                            api_version=self.api_version,
                            credential=AzureKeyCredential(self.azure_cognitive_search_key))
        results = search_client.search(search_text=search_term, top=count, include_total_count=True)
        # print(next(results)['article'])
        return results
    
    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        azure_cognitive_search_key = get_from_dict_or_env(
            values, "azure_cognitive_search_key", "AZURE_COGNITIVE_SEARCH_KEY"
        )
        values["azure_cognitive_search_key"] = azure_cognitive_search_key

        cognitive_search_url = get_from_dict_or_env(
            values,
            "azure_cognitive_search_endpoint",
            "AZURE_COGNITIVE_SEARCH_ENDPOINT",
        )

        values["azure_cognitive_search_endpoint"] = cognitive_search_url

        index_name = get_from_dict_or_env(
            values,
            "index_name",
            "AZURE_COGNITIVE_SEARCH_INDEX_NAME",
        )

        values["index_name"] = index_name

        api_version = get_from_dict_or_env(
            values,
            "api_version",
            "AZURE_COGNITIVE_SEARCH_API_VERSION",
            "2021-04-30-Preview"
        )

        values["api_version"] = api_version

        return values

    def run(self, query: str) -> str:
        """Run query through Azure Cognitive Search and parse result."""
        response = []
        results = self._cognitive_search_results(query, count=self.k)
        for idx, result in enumerate(results):
            for field in self.result_field_list:
                response.append(f"{field}: " + result[field])
        if len(response) == 0:
            return "No good Azure Cognitive Search Result was found"

        return " ".join(response)

    def results(self, query: str, num_results: int) -> List[Dict]:
        """Run query through Azure Cognitive Search and return metadata.

        Args:
            query: The query to search for.
            num_results: The number of results to return.

        Returns:
            A list of dictionaries with the following keys:
                snippet - The description of the result.
                title - The title of the result.
                link - The link to the result.
        """
        metadata_results = []
        results = self._cognitive_search_results(query, count=num_results)
        if len(results) == 0:
            return [{"Result": "No good Azure Cognitive Search Result was found"}]
        for result in results['value']:
            metadata_result = {
                "id": result["id"],
                "AzureSearch_DocumentKey": result["AzureSearch_DocumentKey"],
                "search.score": result["@search.score"],
            }
            metadata_results.append(metadata_result)

        return metadata_results


class AzureCognitiveSearchRun(BaseTool):
    """Tool that adds the capability to query the Bing search API."""

    name = "Azure Cognitive Search"
    description = (
        "A wrapper around Azure Cognitive Search. "
        "Useful for when you need to answer questions about your knowledge base. "
        "Input should be a search query."
    )
    api_wrapper: AzureCognitiveSearchWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("AzureCognitiveSearchRun does not support async")

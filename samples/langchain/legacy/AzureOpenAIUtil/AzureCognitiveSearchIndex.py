from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.models import Vector  
from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SearchField,  
    SemanticSettings,  
    VectorSearch,  
    VectorSearchAlgorithmConfiguration,  
)

class AzureCognitiveSearchIndex:
    """Create and use an Index in Azure Cogntive Search"""
    _vector_search_name_prefix = "vector-config-"
    _semantic_search_name_prefix = "semantic-config-"

    def _get_vector_search_name(self, index_name):
        return self._vector_search_name_prefix + index_name
    
    def _get_semantic_search_name(self, index_name):
        return self._semantic_search_name_prefix + index_name

    def create_index(self, index_name, title_field, keywords_field):
        from azure.search.documents.models import Vector  
        from azure.search.documents.indexes.models import (  
            SearchIndex,  
            SearchField,  
            SearchFieldDataType,  
            SimpleField,  
            SearchableField,  
            SearchIndex,  
            SemanticConfiguration,  
            PrioritizedFields,  
            SemanticField,  
            SearchField,  
            SemanticSettings,  
            VectorSearch,  
            VectorSearchAlgorithmConfiguration,  
        )  
        
        # Reference Doc:
        # https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.indexes.models.searchfield?view=azure-python
        the_index_fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, 
                            filterable=True, key=True),
            SearchableField(name=title_field, type=SearchFieldDataType.String,
                            searchable=True),
            SearchableField(name="content", type=SearchFieldDataType.String,
                            searchable=True),
            SearchableField(name=keywords_field, type=SearchFieldDataType.String,
                            filterable=True, searchable=True),
            SearchableField(name="metadata", type=SearchFieldDataType.String,
                            filterable=True, searchable=True),
            SearchField(
                        name="content_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True,
                        dimensions=1536, 
                        vector_search_configuration=self._get_vector_search_name(index_name)
            )
        ]
        the_vector_config = VectorSearch(
                                algorithm_configurations=[
                                    VectorSearchAlgorithmConfiguration(
                                        name=self._get_vector_search_name(index_name),
                                        kind="hnsw",
                                        hnsw_parameters={
                                            "m": 4,
                                            "efConstruction": 400,
                                            "metric": "cosine"
                                        }
                                    )
                                ]
                            )
        # Reference Doc:
        # https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request?tabs=portal%2Cportal-query#2---create-a-semantic-configuration
        # https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.indexes.models.semanticconfiguration?view=azure-python-preview
        the_semantic_config = SemanticConfiguration(
                            name=self._get_semantic_search_name(index_name),
                            prioritized_fields=PrioritizedFields(
                                title_field=SemanticField(field_name=title_field),
                                prioritized_keywords_fields=[SemanticField(field_name=keywords_field)],
                                prioritized_content_fields=[SemanticField(field_name="content")]
                            )
                        )
        the_semantic_settings = SemanticSettings(configurations=[the_semantic_config])

        the_search_index = SearchIndex(
                                name=index_name, 
                                fields=the_index_fields, 
                                vector_search=the_vector_config,
                                semantic_settings=the_semantic_settings
                            )
        return the_search_index

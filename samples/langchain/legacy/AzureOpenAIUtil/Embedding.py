import openai
from openai.error import RateLimitError
from time import sleep
import numpy as np
import os, json
from .RedisUtil import RedisUtil
from redis import Redis
from redis.commands.search.query import Query
from redis.commands.search.result import Result
from langchain.docstore.document import Document
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import AzureOpenAI

class DocumentEmbedding:
    def __init__(self, document_embedding_deployment_name, \
                 query_embedding_deployment_name, \
                 summerization_deployment_name, \
                 vector_field_name='vector', \
                 qa_chain_type = 'map_rerank') -> None:
        openai.api_type = "azure"
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE")
        openai.api_version = os.getenv("OPENAI_API_VERSION") #openai api version m
        self.document_embedding_deployment_name = os.getenv("DOCUMENT_MODEL_NAME")
        self.query_embedding_deployment_name =os.getenv("QUERY_MODEL_NAME")
        self.summerization_deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.vector_field_name = vector_field_name
        self.qa_chain_type = qa_chain_type
        self.documents = []
        self.redis=None

    def get_embedding(self, text: str, engine: str, tobytes=True):
        while True:
            try:
                embedding = openai.Embedding().create(input=[text], engine=engine)["data"][0]["embedding"]
                break;
            except RateLimitError:
                sleep(2)
        if tobytes:
            return np.array(embedding).astype(np.float32).tobytes()
        else:
            return embedding
        
    def build_redis_index(self):
        if self.redis is None:
            self.redis = RedisUtil(vector_field_name=self.vector_field_name,number_of_vectors=len(self.documents))
            self.redis.redis_conn.flushall()
            self.redis.create_flat_index()
        self.redis.load_vectors(self.documents)

    def convert_redis_query_result_to_document(self, query_results):
        docs = []
        for r in query_results:
            source = r.document_name + ":"+str(r.page_number)
            docs.append(Document(page_content=r.page_text,lookup_str="", metadata={"source":source}))
        return docs    

    def query(self, query_text:str, topK=5):
        if self.redis is not None:
            query_vector = self.get_embedding(query_text, engine=self.query_embedding_deployment_name)
            #prepare the query
            q = Query(f'*=>[KNN {topK} @{self.vector_field_name} $vec_param AS vector_score]').\
                        sort_by('vector_score').\
                        paging(0,topK).\
                        return_fields('vector_score','document_name','page_number','page_text').\
                        dialect(2)
            params_dict = {"vec_param": query_vector}

            #Execute the query
            query_results = self.redis.redis_conn.ft().search(q, query_params = params_dict)
            print(query_results)
            
            # Convert results to Document type in langchain
            docs = self.convert_redis_query_result_to_document(query_results.docs)
            print(docs)

            # Call qna_source_chain
            chain = load_qa_with_sources_chain(AzureOpenAI(temperature=0, deployment_name=self.summerization_deployment_name), \
                                               chain_type=self.qa_chain_type, \
                                               metadata_keys=['source'], \
                                               return_intermediate_steps=True)
            results = chain({"input_documents": docs, "question": query_text}, return_only_outputs=False)
            #Print similar products found
            # for r in results.docs:
            #     print("Score: ", r.vector_score, " "* 5, "Document Name: ", r.document_name, " "*5, "Page Number: ", r.page_number)
            #     print("  Text: ", r.page_text)
        else:
            results=""
        return results

    def load_documents(self, source_folder: str, use_redis:bool=True, verbose:bool=True):
        tobytes = True if use_redis else False

        for file in os.listdir(source_folder):
            if verbose:
                print('\n\nLoading file:', file)
            with open(os.path.join(source_folder, file)) as f:
                page_content= json.loads(f.read())
            self.documents.extend([{'document_key':page_content['filename'].split('/')[-1] + '-' + str(page['page_number']),\
                                'document_name':page_content['filename'].split('/')[-1],\
                                'file_path':page_content['filename'],\
                                'page_number': page['page_number'],\
                                'page_text': page['page_content'],\
                                self.vector_field_name: self.get_embedding(page['page_content'], \
                                                                           self.document_embedding_deployment_name, \
                                                                           tobytes=tobytes) } \
                                for page in page_content['content'] ])
        if use_redis:
            self.build_redis_index()
    
    def add_document_embedding(self, tobytes=True):
        assert self.documents is not None, 'No documents to process.'
        # for item in self.documents:
        #     item[self.vector_field_name] = self.get_embedding(item['page_text'], tobytes=tobytes) 
        
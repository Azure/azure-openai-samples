from redis import Redis
from redis.commands.search.field import VectorField
from redis.commands.search.field import TextField
from redis.commands.search.field import TagField

import os

class RedisUtil:
    def __init__(self, vector_field_name='vector', \
                 number_of_vectors=10000, \
                vector_dimensions=4096, \
                distance_metric='COSINE') -> None:
        host=os.getenv('REDIS_HOST')
        port=os.getenv('REDIS_PORT')
        username=os.getenv('REDIS_USERNAME')
        password=os.getenv('REDIS_PASSWORD')
        ssl=True if os.getenv('REDIS_SSL').upper() == 'TRUE' else False
        if host=='localhost':
            self.redis_conn = Redis(host = host, port = port)
        else:
            self.redis_conn = Redis(host = host, port = port, username=username, password=password, ssl=ssl)
        self.vector_field_name = vector_field_name
        self.number_of_vectors = number_of_vectors
        self.vector_dimensions = vector_dimensions
        self.distance_metric = distance_metric


    def load_vectors(self, text_metadata):
        p = self.redis_conn.pipeline(transaction=False)
        for page in text_metadata:    
            #hash key
            key="docuemnt:"+page['document_key']
            # HSET
            p.hset(key,mapping=page)
                
        p.execute()

    def create_flat_index (self):
        self.redis_conn.ft().create_index([
            VectorField(self.vector_field_name, "FLAT", \
                        {"TYPE": "FLOAT32", "DIM": self.vector_dimensions, \
                         "DISTANCE_METRIC": self.distance_metric, "INITIAL_CAP": \
                            self.number_of_vectors, "BLOCK_SIZE":self.number_of_vectors }),
            TagField("document_name"),
            TagField("page_number"),
            TextField("page_text")
        ])

    def create_hnsw_index (self, M=40,EF=200):
        self.redis_conn.ft().create_index([
            VectorField(self.vector_field_name, "HNSW", \
                        {"TYPE": "FLOAT32", "DIM": self.vector_dimensions, \
                        "DISTANCE_METRIC": self.distance_metric, \
                        "INITIAL_CAP": self.number_of_vectors, \
                        "M": M, "EF_CONSTRUCTION": EF}),
            TagField("document_name"),
            TagField("page_number"),
            TextField("page_text")    
        ])    

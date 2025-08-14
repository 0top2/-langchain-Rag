from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.storage import RedisStore
from langchain_huggingface import HuggingFaceEmbeddings
from GitHub_Prepared_Rag.Config.config import *

def embedding(modelname = None):
    if embedding_load_remote:
        try:
            return HuggingFaceEmbeddings(
                                        model_name=modelname or embedding_model_name,
                                        encode_kwargs={'normalize_embeddings': True}
            )
        except Exception as e:
            print("远程加载模型失败,正在从本地加载....")
            return HuggingFaceEmbeddings(model_name = embedding_local_path,
                                          encode_kwargs={'normalize_embeddings': True}
            )
    else:
        return HuggingFaceEmbeddings(
            model_name=embedding_local_path,
            encode_kwargs={'normalize_embeddings': True}
        )



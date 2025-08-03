import hashlib

from langchain.retrievers import RePhraseQueryRetriever, EnsembleRetriever
from dotenv import load_dotenv, find_dotenv
import os
import openai
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.retrievers import BM25Retriever
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from transformers import pipeline

from config import redis_url,chunk_size,chunk_overlap,embedding_url
from Utils.change_faiss_index_IVFFLAT import change_faiss_index_IVFFLAT
from Utils.compress_retriever import compress_retriever
from sentence_transformers import SentenceTransformer
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.document_loaders import UnstructuredFileLoader, PyPDFLoader, Docx2txtLoader, TextLoader, \
    UnstructuredExcelLoader, CSVLoader, DirectoryLoader
from langchain_community.storage import RedisStore
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

def doc_process(embedding):
    doc = load_doc()
    chunk = split_doc(doc,embedding)
    return chunk

def load_doc():
    loading_map = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".csv": CSVLoader,
        # 可以继续添加其他文件类型的加载器
    }
    pdf = DirectoryLoader(
        path="Rag_source",
        glob="**/*.pdf",
        loader_cls = PyPDFLoader
    )
    text = DirectoryLoader(
        path="Rag_source",
        glob="**/*.{txt,md}",
        loader_cls = TextLoader
    )
    csv = DirectoryLoader(
        path="Rag_source",
        glob="**/*.csv",
        loader_cls = CSVLoader
    )
    xlsx = DirectoryLoader(
        path="Rag_source",
        glob="**/*.xlsx",
        loader_cls=UnstructuredExcelLoader
    )
    return pdf.load()+text.load()+csv.load()+xlsx.load()

# def upload(file):写到fast里,作为api同时写一个clear的api,清除指定的文件

def split_doc(document,embedding):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,
                                              separators=["\n\n", "\n", "。", ""])
    chunk = splitter.split_documents(document)
    deep_splitter = SemanticChunker(embeddings=embedding)
    result = []
    for doc in chunk:
        for ele in deep_splitter.split_documents([doc]):
            result.append(ele)
    for i,doc in enumerate(result):
            # 生成基于内容和索引的ID
        content_hash = hashlib.sha256(doc.page_content.encode()).hexdigest()[:8]
        doc.metadata["id"] = f"chunk_{i}_{content_hash}"
    return result

def embedding():
    option = input("请问模型是否从网上加载:Y/N")
    model_name = "BAAI/bge-large-en-v1.5"
    if option in ['Y', 'y']:
        try:
            embedding = HuggingFaceEmbeddings(model_name=model_name,
                                          encode_kwargs={
                                              'normalize_embeddings': True
                                          }
                                          )
        except Exception as e:
            print("远程加载模型失败,正在从本地加载....")
            embedding = HuggingFaceEmbeddings(model_name = embedding_url,
                                          encode_kwargs={
                                              'normalize_embeddings': True
                                          }
                                          )
        return embedding
    return HuggingFaceEmbeddings(model_name = embedding_url,
                                          encode_kwargs={
                                              'normalize_embeddings': True
                                          }
                                          )

def llm():
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.base_url = os.environ['OPENAI_API_URL']
    # api = os.environ['HUGGINGFACEHUB_API_TOKEN']
    llm = ChatOpenAI(base_url=openai.base_url,
                     api_key=openai.api_key,
                     model='gpt-3.5-turbo')
    # pipe = pipeline(
    #     "text-generation",
    #     model="google/flan-t5-xl",
    #     max_length=512,
    #     temperature=0.7,
    # )
    # llm = HuggingFacePipeline(pipeline=pipe)
    return llm


def cache_embedding(embedding):
    store = RedisStore(redis_url=redis_url, namespace="vector")
    # embedding = SentenceTransformer("BAAI/bge-large-en-v1.5")
    cache = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=embedding,
        document_embedding_cache=store,
        key_encoder="sha256"
    )
    return cache

def index_change_db(chunk,cache):
    db = FAISS.from_documents(chunk,cache)
    db = change_faiss_index_IVFFLAT(db)
    return db

def query_rewrite_retriever(retriever,llm):
    retrieval_with_llm = RePhraseQueryRetriever.from_llm(
        retriever=retriever,
        llm = llm
    )
    return retrieval_with_llm

def Retriever(retriever,chunk):
    bm25_retriever = BM25Retriever.from_documents(chunk)
    retrievers = EnsembleRetriever(
                        retrievers=[bm25_retriever, retriever],
                        weight = [0.3,0.7]
    )
    return retrievers

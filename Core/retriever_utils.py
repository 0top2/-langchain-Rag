from langchain.retrievers import RePhraseQueryRetriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from GitHub_Prepared_Rag.Utils.change_faiss_index_IVFFLAT import change_faiss_index_IVFFLAT


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
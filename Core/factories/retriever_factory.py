from langchain.retrievers import EnsembleRetriever, RePhraseQueryRetriever, ParentDocumentRetriever
from langchain_community.retrievers import BM25Retriever
from GitHub_Prepared_Rag.Utils.change_faiss_index_IVFFLAT import change_faiss_index_IVFFLAT


class RetrieverFactory:
    @staticmethod
    def create_ensemble_retriever(
            vector_retriever,
            chunks
    ):
        """创建混合检索器（BM25+向量检索）"""
        bm25_retriever = BM25Retriever.from_documents(chunks)
        return EnsembleRetriever(
            retrievers = [bm25_retriever,vector_retriever],
            weights = [0.4,0.6]
        )

    @staticmethod
    def create_rewrite_retriever(
            retriever,
            llm
    ):
        """创建带查询重写的检索器"""
        return RePhraseQueryRetriever.from_llm(retriever = retriever,llm = llm)

    @staticmethod
    def create_faiss_with_ivfflat(chunk, embedding):
        """创建带IVFFLAT索引的FAISS检索器"""
        from langchain_community.vectorstores import FAISS
        db = FAISS.from_documents(chunk, embedding)
        return change_faiss_index_IVFFLAT(db)

    @staticmethod
    def create_parent_child_retriever(
            vecstore,
            docstore,
            docs,
            splitter
    ):
        parent_splitter, child_splitter = splitter.Parent_Child_splitter()
        retriever = ParentDocumentRetriever(
            vecstore=vecstore,
            docstore=docstore,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter
        )
        retriever.add_documents(docs)
        return retriever
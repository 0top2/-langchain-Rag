from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter


def compress_retriever(retriever,embedding,similar):
    base_compressor = EmbeddingsFilter(
                                embeddings =embedding,
                                similarity_threshold=similar)
    compressed_retriever = ContextualCompressionRetriever(
                                base_compressor = base_compressor,
                                base_retriever = retriever,
    )
    return compressed_retriever
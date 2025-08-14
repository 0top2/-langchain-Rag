import hashlib
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..abstraction_base.splitter_base import SplitterBase


class HybridSplitter(SplitterBase):
    """混合分块策略（递归+语义）"""
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, docs, embedding):
        # 递归字符拆分
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "。", ""]
        )
        chunks = recursive_splitter.split_documents(docs)
        # 语义拆分
        semantic_splitter = SemanticChunker(embeddings=embedding)
        result = []
        for doc in chunks:
            result.extend(semantic_splitter.split_documents([doc]))
        # 增强元数据
        for i, doc in enumerate(result):
            content_hash = hashlib.sha256(doc.page_content.encode()).hexdigest()[:8]
            doc.metadata["id"] = f"chunk_{i}_{content_hash}"
        return result

class ParentChildSplitter(SplitterBase):
    """父-子文档分块策略"""
    def __init__(self, parent_chunk_size: int, child_chunk_size: int):
        self.parent_chunk_size = parent_chunk_size
        self.child_chunk_size = child_chunk_size

    def split(self, docs, embedding):
        # 此处返回父文档拆分结果（根据实际需求调整）
        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=self.parent_chunk_size)
        return parent_splitter.split_documents(docs)
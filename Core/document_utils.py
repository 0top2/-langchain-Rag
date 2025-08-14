import hashlib
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredExcelLoader, \
    CSVLoader, DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from GitHub_Prepared_Rag.Config.config import *
from typing import List
from langchain.schema import Document


def load_doc() -> List[Document]:
    loading_map = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".csv": CSVLoader,
        # 可以继续添加其他文件类型的加载器
    }
    pdf = DirectoryLoader(
        path=DirectoryLoader_load_path,
        glob="**/*.pdf",
        loader_cls = PyPDFLoader
    )
    text = DirectoryLoader(
        path=DirectoryLoader_load_path,
        glob="**/*.{txt,md}",
        loader_cls = TextLoader
    )
    csv = DirectoryLoader(
        path=DirectoryLoader_load_path,
        glob="**/*.csv",
        loader_cls = CSVLoader
    )
    xlsx = DirectoryLoader(
        path=DirectoryLoader_load_path,
        glob="**/*.xlsx",
        loader_cls=UnstructuredExcelLoader
    )
    # print(pdf.load()+text.load()+csv.load()+xlsx.load())
    return pdf.load()+text.load()+csv.load()+xlsx.load()




def Parent_Child_splitter():
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=300)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1500)
    return parent_splitter,child_splitter
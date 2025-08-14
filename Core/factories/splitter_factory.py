from GitHub_Prepared_Rag.Core.implementations.splitter_impl import HybridSplitter, ParentChildSplitter
from GitHub_Prepared_Rag.Config.config import *

class SplitterFactory:
    @staticmethod
    def create_splitter(strategy_type=None):
        strategy_type = strategy_type or split_strategy
        if strategy_type == 'hybrid':
            return HybridSplitter(
                chunk_size=300,
                chunk_overlap=50
            )
        elif strategy_type == 'parent_child':
            return ParentChildSplitter(
                parent_chunk_size=1500,  # 可从config.yml读取
                child_chunk_size=300
            )
        else:
            raise ValueError(f"不支持的分块策略: {strategy_type}")
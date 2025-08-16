from GitHub_Prepared_Rag.Core.implementations.splitter_impl import HybridSplitter, ParentChildSplitter
from GitHub_Prepared_Rag.Config.config import *

class SplitterFactory:
    @staticmethod
    def create_splitter(strategy_type=None):
        strategy_type = strategy_type or split_strategy['type']
        if strategy_type == 'hybrid':
            return HybridSplitter()
        elif strategy_type == 'parent_child':
            return ParentChildSplitter()
        else:
            raise ValueError(f"不支持的分块策略: {strategy_type}")
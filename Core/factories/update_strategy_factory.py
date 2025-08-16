from GitHub_Prepared_Rag.Core.implementations.update_strategy_impl import *
from GitHub_Prepared_Rag.Config.config import *
class StrategyFactory:
    @staticmethod
    def create_strategy():
        if update_database == 'none':
            return NoUpdateStrategy()
        elif update_database == "drop_and_recreate":
            return DropAndRecreateStrategy()
        elif update_database == "append":
            return AppendStrategy()
        else:
            raise ValueError(f"不支持的更新策略: {update_database}")

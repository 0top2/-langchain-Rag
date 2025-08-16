from GitHub_Prepared_Rag.Core.implementations.update_strategy_impl import AppendStrategy, DropAndRecreateStrategy


class DocWatcherUpdatedFactory:
    @staticmethod
    def createDocUpdatedPattern(pattern):
        if pattern =='created':
            return AppendStrategy()
        elif pattern =='deleted' or pattern =='modified':
            return DropAndRecreateStrategy()

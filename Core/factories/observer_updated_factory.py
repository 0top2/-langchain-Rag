from GitHub_Prepared_Rag.Core.update_strategy import AppendStrategy, DropAndRecreateStrategy


class ObserverUpdatedFactory:
    @staticmethod
    def createObserverUpdatedPattern(pattern):
        if pattern =='created':
            return AppendStrategy()
        elif pattern =='deleted' or pattern =='modified':
            return DropAndRecreateStrategy()

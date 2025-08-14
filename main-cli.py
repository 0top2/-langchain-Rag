import asyncio
import time
from Core.RAGManager import RagManager
from GitHub_Prepared_Rag.Config.config import DirectoryLoader_load_path
from GitHub_Prepared_Rag.Core.DocWatcher import docWatcher
from GitHub_Prepared_Rag.Core.chain_builder import Window
from GitHub_Prepared_Rag.Core.embedding_utils import embedding
manager = RagManager()
async def main():
    manager = RagManager()
    # 初始化文档监测器（监听Rag_source目录）
    watcher = docWatcher(watch_dir=DirectoryLoader_load_path)
    # 将RagManager注册为观察者（文档变化时通知它更新）
    watcher.add_observer(manager)
    # 启动监测器（非阻塞方式，用线程运行）
    import threading
    threading.Thread(target=watcher.start_watching, daemon=True).start()
    id_store = {}
    print("")
    id = input("请输入窗口id:")
    if id not in id_store:
        start = time.time()
        id_store[id] = Window(manager=manager,id=id)
        end = time.time()
    current_window = id_store[id]
    use  = end - start
    print(f"对话'{id}'创建完毕,用时:{use},请开始对话!")
    while True:
        question = input("用户:")
        if question.lower() in ['return','break']:
            print("成功退出!")
            break
        if question == '切换会话':
            new_id = input("请问您要切换到的会话id是:")
            change_start = time.time()
            if new_id not in id_store:
                id_store[new_id] = Window(manager=manager,id=new_id)
            current_window = id_store[new_id]
            change_end = time.time()
            spend = change_end - change_start
            print(f"\n切换成功,用时{spend},请您继续对话!")
            question = input("用户:")
        await current_window.run(question)

if __name__ == '__main__':
    asyncio.run(main())


import asyncio
import time
from Core.RAGManager import RagManager
from GitHub_Prepared_Rag.Core.chain_builder import Window
manager = RagManager()
async def main():
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


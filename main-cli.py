import asyncio
import time
from data_preparing import embedding,cache_embedding
from chain_builder import Window
from data_preparing import llm
embedding = embedding()
cache_embedding = cache_embedding(embedding)
llm = llm()
async def main():
    id_store = {}
    id = input("请输入窗口id:")
    if id not in id_store:
        start = time.time()
        id_store[id] = Window(id=id,embedding=embedding,cache=cache_embedding,llm=llm)
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
            if new_id not in id_store:
                id_store[new_id] = Window(id=new_id,embedding=embedding,cache=cache_embedding,llm=llm)
            current_window = id_store[new_id]
            print("\n切换成功,请您继续对话!")
            question = input("用户:")
        await current_window.run(question)

if __name__ == '__main__':
    asyncio.run(main())


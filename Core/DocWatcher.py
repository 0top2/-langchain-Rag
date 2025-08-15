import time
from pathlib import Path
from watchdog.observers import Observer
from .observe_pattern import Subscriber
from watchdog.events import FileSystemEventHandler
from .document_utils import load_doc,load_single_doc
class docWatcher(Subscriber,FileSystemEventHandler):
    def __init__(self, watch_dir: str):
        super().__init__()
        self.watch_dir = Path(watch_dir)
        self.last_modified = {}  # 记录文件最后修改时间，避免重复触发
        self.observer = Observer()
        self.observer.schedule(self, str(self.watch_dir), recursive=True)

    # def on_created(self, event):  # 新增：处理文件创建（添加）事件
    #     if not event.is_directory:  # 过滤目录事件，只处理文件事件
    #         file_path = Path(event.src_path)
    #         if file_path.suffix not in ['.pdf']:
    #             return
    #         # 新文件无需判断重复，直接处理
    #         print(f"检测到新文档添加: {file_path.name}")
    #         updated_docs = load_doc()
    #         self.notify(updated_docs)

    def on_deleted(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix not in ['.pdf']:
                return
            print(f"\n检测到文档删除: {file_path.name}")
            # 从记录中移除已删除文件
            if str(file_path) in self.last_modified:
                del self.last_modified[str(file_path)]
            updated_docs = load_doc()
            self.notify(updated_docs,'deleted')

    def on_created(self, event):
        if not event.is_directory:  # 过滤目录事件，只处理文件事件
            file_path = Path(event.src_path)  # 获取触发事件的文件路径
            # 过滤非目标文件类型（只处理pdf、docx等文档）
            if file_path.suffix not in ['.pdf']:
                return  # 非目标类型，直接返回
            # 避免短时间内重复触发（如文件保存可能触发多次修改事件）
            current_mtime = file_path.stat().st_mtime  # 获取当前文件的最后修改时间戳
            if not self.last_modified.get(str(file_path)):
                self.last_modified[str(file_path)] = current_mtime  # 更新记录的修改时间
                print(f"\n检测到文档添加: {file_path.name}")  # 打印文件变化信息
                updated_docs = load_single_doc(file_path)
                self.notify(updated_docs,'created')
    def on_modified(self, event):  # 重写FileSystemEventHandler的方法，处理文件修改事件
        if not event.is_directory:  # 过滤目录事件，只处理文件事件
            file_path = Path(event.src_path)  # 获取触发事件的文件路径
            # 过滤非目标文件类型（只处理pdf、docx等文档）
            if file_path.suffix not in ['.pdf']:
                return  # 非目标类型，直接返回
            # 避免短时间内重复触发（如文件保存可能触发多次修改事件）
            current_mtime = file_path.stat().st_mtime  # 获取当前文件的最后修改时间戳
            if self.last_modified.get(str(file_path)) == current_mtime:
                return  # 已有时间戳,说明已经创建,且时间戳未变，说明是重复事件，直接返回
            else:
                if self.last_modified.get(str(file_path)):
                    self.last_modified[str(file_path)] = current_mtime  # 更新记录的修改时间
                    print(f"\n检测到文档变化: {file_path.name}")  # 打印文件变化信息
                    updated_docs = load_doc()  # 我有个更好的想法:只加载当前的file,然后db.add_document(file)
                    self.notify(updated_docs,'modified')  # 通知所有注册的观察者（传递最新文档）

    def start_watching(self):
        print(f"开始监控文档目录: {self.watch_dir}")
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
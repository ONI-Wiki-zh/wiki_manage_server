import threading
from queue import Queue


# 处理函数，你可以根据需要修改这个函数
def process_data(data):
    # 在这里添加你的处理逻辑
    return data


# 线程工作函数
def worker():
    while True:
        data = q.get()
        if data is None:
            break
        result = process_data(data)
        results.append(result)
        q.task_done()


if __name__ == '__main__':
    # 输入数组
    data = list(range(102))  # 这是一个示例数组，你可以替换为你自己的数组

    # 创建队列和结果列表
    q = Queue()
    results = []

    # 创建线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # 将数据分块并添加到队列中
    for i in range(0, len(data), 10):
        q.put(data[i:i + 10])

    # 等待所有任务完成
    q.join()

    # 停止工作线程
    for i in range(3):
        q.put(None)
    for t in threads:
        t.join()

    # 打印结果
    for res in results:
        print(res)

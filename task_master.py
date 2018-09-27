# task_master.py

import random, time, queue
from multiprocessing.managers import BaseManager


task_queue = queue.Queue()
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


def task_q():
    return task_queue
def result_q():
    return result_queue



if __name__ == '__main__':
	# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
	QueueManager.register('get_task_queue', callable=task_q)
	QueueManager.register('get_result_queue', callable=result_q)
	manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
	manager.start()
	# 获得通过网络访问的Queue对象:
	task = manager.get_task_queue()
	result = manager.get_result_queue()
	# 放几个任务进去:
	# for i in range(10):
	#     n = random.randint(0, 10000)
	#     print('Put task %d...' % n)
	#     task.put(n)
	# 从result队列读取结果:
	print('Try get results...')
	while True:
	    r = result.get()
	    if r:
	    	print('Result: %s' % r)
	    else:
	    	continue
	# 关闭:
	manager.shutdown()
	print('master exit.')
import time, queue, threading, schedule
from multiprocessing.managers import BaseManager
from wechat_sender import Sender
from weather_beta import Weather
from translation_beta import YouDaoTranslation
from multiinfo_beta import GetInfo
from stock_beta import Stock
from settings_beta import YouDao_Lang

sender = Sender(token='houwei2018')


task_queue = queue.Queue()
result_queue = queue.Queue()

lock = threading.Lock()
stock_user = dict()
is_schedule = []

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


def task_q():
    return task_queue

def result_q():
    return result_queue

def send_list(msg, user, *args, **kw):
	if msg == 'stock':
		msg = Stock.get_info()[0]
	elif msg == 'weather':
		msg = Weather('上海').wxpy()
	elif msg == 'translate':
		msg = YouDaoTranslation(kw['trans'], lang=kw['lang']).wxpy()
	elif msg == 'smzdm':
		msg = GetInfo(kw['num']).smzdm()
	elif msg == 'global':
		msg = GetInfo(kw['url']).enterprise()
	# print(msg)
	# print(user)
	return sender.send_to(msg, user)

def get_task():
	while True:
		try:
			r = result.get()
			print(r)
			if r[:3] == '#大盘':
				s = Stock.info(r[3:])
				if s.interval == -1:
					send_list('stock', s.name)
				else:
					send_list(s.is_start(), s.name)
					lock.acquire()
					stock_user.update({s.puid:'%s&%s&%s&%s&%d&%.2f' % (s.puid, s.name, s.trigger, s.status, s.interval, s.change)})
					lock.release()
					print('get_task:', stock_user)
			elif r[:3] == '#天气':
				send_list('weather', r.split('&')[2])
			elif r[:3] == '#翻译':
				if r[3:].split(' ', 1)[0] not in YouDao_Lang.keys():
					kw = {'trans': r[3:].split('&')[0], 'lang': 'ez'}
				else:
					kw = {'trans': r[5:].split('&')[0], 'lang': r[3:5]}
				send_list('translate', r.split('&')[2], **kw)
			elif r[:2] == '#买':
				kw = {'num': r[2:]}
				send_list('smzdm', r.split('&')[2], **kw)
			elif r[:3] == '#动态':
				kw = {'url': r[3:].split('@')[0]}
				send_list('global', r.split('@')[2], **kw)
		except Exception as e:
			pass

def execute_task():
	while True:
		schedule.run_pending()
		if stock_user:
			lock.acquire()
			for k, v in stock_user.items():
				s = Stock.info(v)
				sender.send_to(s.is_run(), s.name)
				try:
					if not s.trigger or s.interval == 0:
						schedule.clear(s.puid)
						if s.puid in is_schedule:
							is_schedule.remove(s.puid)
					elif s.puid not in is_schedule:
						schedule.every(s.interval).minutes.do(send_list, 'stock', s.name).tag(s.puid)
						is_schedule.append(s.puid)
					else:
						pass
				except Exception as e:
					if e == 'ValueError':
						print('%s is not in schedule queue. => %s' % (s.name, e))
					else:
						print('%s-Exception => %s' % (execute_task.__name__, e))
				finally:
					pass
				stock_user.update({s.puid:'%s&%s&%s&%s&%d&%.2f' % (s.puid, s.name, s.trigger, s.status, s.interval, s.change)})
				# print('exe_task:', stock_user)
				# print(schedule.jobs)
				# print(is_schedule)
				time.sleep(0.5)
			lock.release()


def main():
	thread_get_task = threading.Thread(target=get_task, args=(), name='Thread-get_task')
	thread_execute_task = threading.Thread(target=execute_task, args=(), name='Thread-execute_task')
	thread_get_task.start()
	thread_execute_task.start()
	thread_get_task.join()
	thread_execute_task.join()
	print('task over!!!')


if __name__ == '__main__':
	QueueManager.register('get_task_queue', callable=task_q)
	QueueManager.register('get_result_queue', callable=result_q)
	manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
	manager.start()
	# 获得通过网络访问的Queue对象:
	task = manager.get_task_queue()
	result = manager.get_result_queue()
	print('Try get results...')
	main()
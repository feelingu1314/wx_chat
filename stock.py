#  process stock message

import tushare as ts
import time
from datetime import datetime


class Stock(object):

	def __init__(self, puid, name, trigger, status, interval=0, change=0.00):
		self.puid = puid
		self.name = name
		self.trigger = trigger
		self.status = status
		self.interval = interval
		self.change = change

	@staticmethod
	def stock_time():
		# 开盘时间: tm_wday < 6, tm_hour=> 9:30-11:30, 13:00-15:00(include public holiday..)
		start_am = 93000  # 093000
		end_am = 113000
		start_pm = 130000
		end_pm = 150000
		now = int(time.strftime('%H%M%S'))

		if time.localtime(time.time()).tm_wday < 6:
			if now == start_am or now == start_pm:
				return 'opening'
			elif now == end_am or now == end_pm:
				return 'closing'
			elif now in range(start_am, end_am) or now in range(start_pm, end_pm):
				return 'working'
			else:
				return 'resting'
		else:
			return 'off-working'

	@classmethod
	def info(cls, value):
		raw = value.split('&')
		if len(raw) == 3:
			if raw[0] == '':
				trigger = False
				interval = -1
			elif raw[0] == '+':
				trigger = True
				interval = 20
			elif raw[0] == '-':
				trigger = False
				interval = 0
			elif isinstance(int(raw[0]), int) or isinstance(float(raw[0]), float):
				trigger = True
				interval = int(raw[0]) or float(raw[0])
			else:
				raise ValueError('trigger must be one of +, -, integer, float')
			puid = raw[1]
			name = raw[2]
			change = 0
			status = cls.stock_time()
		elif len(raw) == 6:
			puid = raw[0]
			name = raw[1]
			if raw[2] == 'True':
				trigger = True
			else:
				trigger = False
			status = cls.stock_time()
			interval = raw[4]
			change = raw[5]
		else:
			raise ValueError('incorrect arguments: %s' % value)
		s = cls(puid, name, trigger, status, interval=int(interval), change=float(change))
		return s

	@staticmethod
	def get_info():
			df = ts.get_index()
			new_df = df[['name', 'change', 'open', 'preclose', 'close', 'high', 'low', 'volume', 'amount']]
			index_name = new_df.columns.values

			info = {
				'名称': '',
				'涨跌幅': 0,
				'今日开盘': 0,
				'昨日收盘': 0,
				'今日收盘': 0,
				'今日最高': 0,
				'今日最低': 0,
				'成交量(手)': 0,
				'成交金额(亿元)': 0,
	        }

			seq = 0
			for num in range(1):  # num=0 => A股指数, 表示目前只取A股指数信息
				for k in list(info.keys()):
					info[k] = new_df[index_name[seq]][num]
					seq += 1
			#  显示文本内容
			content = '时间：%s\n\n' % datetime.now().time().strftime('%H:%M:%S')
			#  字符串输出+显示当日涨幅
			for k, v in info.items():
				if k == '今日收盘':
					if float(v) <= float(info['昨日收盘']):
						tip = '📉'
					else:
						tip = '📈'
					v = '%s   %s' % (v, tip)
				content += '%s: %s\n' % (k, v)
			return content, info

	def is_status(self, status, delta=0.2):
		result, result_dict = self.get_info()
		if status == 'opening':
			msg = '上证指数[开盘]\n\n%s' % result
			self.trigger = True
		elif status == 'closing':
			msg = '上证指数[收盘]\n\n%s' % result
			self.trigger = False
		elif status == 'working':
			if abs(result_dict['涨跌幅'] - self.change) >= delta:  # 涨跌幅绝对值>=0.3触发
				msg = '上证指数[%.2f]\n\n%s' % (result_dict['涨跌幅']-self.change, result)
				self.change = result_dict['涨跌幅']
			else:
				msg = ''
		else:
			msg = ''
		return msg


	def is_start(self):
		# msg = '上证指数查询:\n#大盘 => 单次查询\n#大盘10 => 间隔10分钟通知\n#大盘+ => 开启通知（20分钟)\n#大盘- => 关闭通知'
		if self.trigger:
			if self.status == 'off-working':
				msg = '非交易日...'
				self.trigger = False
				# self.interval = 0
			elif self.status == 'resting':
				msg = '非交易时间...'
				self.trigger = False
			else:
				msg = '上证指数\n[通知] => 开启\n[周期] => %dmins\n\n%s' % (self.interval, self.get_info()[0])
		else:
			msg = '上证指数\n[通知] => 关闭\n\n%s' % (self.get_info()[0])
		return msg


	def is_run(self):

		return self.is_status(self.status)
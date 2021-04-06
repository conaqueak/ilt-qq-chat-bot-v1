import time

def transToChinese(name):
	# 大逃杀地图
	if name == 'Kings Canyon':
		name = '诸王峡谷'
	elif name == "World's Edge":
		name = '世界尽头'
	elif name == "Olympus":
		name = '奥林匹斯'
	elif name == "Storm Point":
		name = '风暴点'
	# 竞技场地图
	elif name == 'Party crasher':
		name = '派对破坏者'
	elif name == 'Phase runner':
		name = '相位穿梭器'
	elif name == 'Drop Off':
		name = '原料场'
	elif name == 'Habitat':
		name = '栖息地'
	elif name == 'Overflow':
		name = '熔岩流'
	elif name == 'Artillery':
		name = '火炮'
	elif name == 'Thermal Station':
		name = '终点站'
	elif name == 'Golden Gardens':
		name = '花园'
	return name

def endTime(timestamp):
	return time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(timestamp))

def timeRemain(second):
	if second < 0:
		return False
	elif second == 0:
		return '即刻'
	elif second < 60:
		return f'{second}秒'
	elif second % 60 == 0 and second < 60 * 60:
		return f'{second // 60}分钟'
	elif second < 60 * 60:
		return f'{second // 60}分{second % 60}秒'
	elif second % (60 * 60) == 0 and second < 24 * 60 * 60:
		return f'{int(second / 60 // 60)}小时'
	elif second < 24 * 60 * 60:
		return f'{int(second / 60 // 60)}时{int(second / 60 % 60)}分'
	elif second % (24 * 60 * 60) == 0:
		return f'{int(second / 60 / 60 // 24)}天'
	else:
		return f'{int(second / 60 / 60 // 24)}天{int(second / 60 / 60 % 24)}时'
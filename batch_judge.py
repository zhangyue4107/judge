import requests
import json
import jsonpath
import time

file_path = r'no3/result.py'

retry = 3

submission_ids = []

headers = {
	'Content-Type': 'application/json;charset=UTF-8',
	'Cookie': '_ga=GA1.1.1065990939.1634542749; csrftoken=gH6UwQPnUQAvEybQPTg9q2M8pJUhthX5Rw3P5O3MEX0ku6nvbKDkK5BNmSnJcnTc; sessionid=ubhiberfkbp4mkv69wnoz0m9cbo0703t; _gid=GA1.1.1505999452.1634731569; _gat=1',
	'X-CSRFToken': 'gH6UwQPnUQAvEybQPTg9q2M8pJUhthX5Rw3P5O3MEX0ku6nvbKDkK5BNmSnJcnTc'
}


def batch_judge(file_path, times, domain='http://localhost'):
	i = 0
	retry_times = 0
	while i < times:
		result_file = open(file_path, 'r', encoding='utf-8')
		result = ''

		for line in result_file.readlines():
			result += line

		body = {
			"problem_id": 4,
			"language": "Python3",
			"code": result
		}

		res = requests.post(
			headers=headers,
			url=domain + '/api/submission',
			json=body
		)
		try:
			submission_id = jsonpath.jsonpath(json.loads(res.content.decode()), '$..submission_id')[0]
			submission_ids.append(submission_id)
			i += 1
		except:
			time.sleep(10)
			if retry_times < retry:
				retry_times += 1
				continue
			else:
				raise Exception('超出最大重试次数')

	return submission_ids


def calculate_submission_memory_duration(submission_ids, domain='http://localhost'):
	memories = []
	durations = []
	i = 0
	retry_times = 0
	while i < len(submission_ids):
		try:
			path = '/api/submission?id=' + submission_ids[i]
			res = requests.get(
				url=domain + path,
				headers=headers
			)
			memory = jsonpath.jsonpath(json.loads(res.content.decode()), '$..memory_cost')[0]
			duration = jsonpath.jsonpath(json.loads(res.content.decode()), '$..time_cost')[0]
			memories.append(int(memory))
			durations.append(int(duration))
			i += 1
		except:
			time.sleep(10)
			if retry_times < retry:
				retry_times += 1
				continue
			else:
				raise Exception('超出最大重试次数')

	return memories, durations


if __name__ == '__main__':
	submission_ids = batch_judge(file_path=file_path, times=10)
	memory, duration = calculate_submission_memory_duration(submission_ids)
	print('======内存统计=======')
	print('内存消耗统计 ' + str(memory))
	print('内存平均值 = ' + str(sum(memory) / len(memory)/1024/1024)+'mb')
	print('内存最大值 = ' + str(max(memory)/1024/1024)+'mb')
	print('内存最小值 = ' + str(min(memory)/1024/1024)+'mb')
	print('======时间统计=======')
	print('时间消耗统计 ' + str(duration))
	print('时间平均值 = ' + str(sum(duration) / len(duration))+'ms')
	print('时间最大值 = ' + str(max(duration))+'ms')
	print('时间最小值 = ' + str(min(duration))+'ms')

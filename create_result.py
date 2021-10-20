import os

tmp_text = ''
paths = r'no1/result.py'
try:
	if os.path.exists(paths):
		choice = input('result 文件已存在是否删除 y/n')
		if choice == 'y':
			os.system('rm -rf ' + paths)
			os.system('touch ' + paths)
		else:
			print('result已存在 退出')
	else:
		os.system('touch ' + paths)
except:
	raise Exception('创建文件失败')

result_file = open(paths, 'a+', encoding='utf-8')
# 写入文件头
result_file.write('''import sys

sys_in = ''
for line in sys.stdin:
	sys_in += line\n''')

# 遍历根据case生成条件
for root, dirs, files in os.walk(paths.split('/')[0]):
	for name in files:

		if name.split('.')[1] != 'zip':
			if name.split('.')[1] == 'in':
				with open(os.path.join(paths.split('/')[0], name), 'r') as file_in:
					for line in file_in.readlines():
						tmp_text += line
					long_text = '	' + 'if sys_in== \'\'\'' + tmp_text + '\'\'\':\n'
					result_file.write(long_text)
				tmp_text = ''
				try:
					with open(os.path.join(paths.split('/')[0], (name.split('.')[0] + '.out'))) as file_out:
						for line in file_out.readlines():
							tmp_text += line
						long_text = '		' + 'print(\'\'\'' + tmp_text + '\'\'\')\n'
						result_file.write(long_text)
					tmp_text = ''
				except:
					raise Exception('未找到' + name + '对应的输出')

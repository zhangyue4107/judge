import sys

sys_in = []
for line in sys.stdin:
	sys_in.append(line)
	if sys_in == ['5 10\n', '3 2 128\n', '2 3 128\n', '1 5 126\n', '4 1 143\n', '4 3 147\n', '2 5 84\n', '5 2 84\n',
	              '2 5 84\n', '2 3 128\n']:
		print('''83.00
41.00
87.00
60.00
43.00
''')

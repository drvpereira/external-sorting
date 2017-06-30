import random, math

file_size = 4 * 100000000 # ~4GB

f = open('large-file-to-sort.txt', 'w')

index = 0
old_progress = -1

while index < file_size:
	f.write(str(random.randrange(-file_size, file_size)) + "\n")
	index += 1

	progress = math.floor(index * 100 / file_size)
	if progress != old_progress:
		print(str(progress) + '%')
		old_progress = progress

f.close()
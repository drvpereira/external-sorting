import os.path, math

chunk_size = 100 * 100000 # ~100 MB

def get_chunk_name(path_to_file, chunk_number):
	filename_parts = path_to_file.split('.')
	return filename_parts[0] + '-chunk_' + str(chunk_number) + '.' + filename_parts[1]

def get_merged_chunk_name(path_to_file, left_chunk, right_chunk):
	filename_parts = path_to_file.split('.')
	return filename_parts[0] + '-merged_' + str(left_chunk) + '-' + str(right_chunk) + '.' + filename_parts[1]

def get_sorted_name(path_to_file):
	filename_parts = path_to_file.split('.')
	return filename_parts[0] + '-sorted.' + filename_parts[1]

def write_sorted_buffer_to_file(sorting_buffer, f_chunk, chunk_number):
	sorting_buffer.sort()
	for element in sorting_buffer:
		f_chunk.write(str(element) + '\n')
	f_chunk.close()

def external_sort(path_to_file):
	sorting_buffer = []
	chunk_number = 1
	line_counter = 0

	f_source = open(path_to_file, 'r')
	f_chunk = open(get_chunk_name(path_to_file, chunk_number), 'w')

	for line in f_source:
		line_counter += 1
		sorting_buffer.append(int(line))
		
		if line_counter == chunk_size:
			write_sorted_buffer_to_file(sorting_buffer, f_chunk, chunk_number)
			sorting_buffer = []
			chunk_number += 1
			line_counter = 0
			f_chunk = open(get_chunk_name(path_to_file, chunk_number), 'w')

	if len(sorting_buffer) > 0:
		chunk_number += 1
		write_sorted_buffer_to_file(sorting_buffer, f_chunk, chunk_number)

	f_source.close()
	merge_files(path_to_file, chunk_number)
	os.rename(path_to_file, get_sorted_name(path_to_file))

def merge_files(path_to_file, number_of_chunks):
	chunk_index = 1
	merge_index = 1

	while chunk_index < number_of_chunks:
		merge_halves(path_to_file, merge_index, chunk_index, chunk_index + 1)		
		merge_index += 1
		chunk_index += 2

	if (chunk_index - 2) > 1:
		merge_files(path_to_file, math.ceil(chunk_index / 2))

def merge_halves(path_to_file, merge_index, chunk_left, chunk_right):
	left_half = open(get_chunk_name(path_to_file, chunk_left), 'r')
	left_pointer = left_half.readline()

	if os.path.exists(get_chunk_name(path_to_file, chunk_right)):
		right_half = open(get_chunk_name(path_to_file, chunk_right), 'r')
		right_pointer = right_half.readline()
	else:
		right_half = None
		right_pointer = None
	
	merged_chunk = open(get_merged_chunk_name(path_to_file, chunk_left, chunk_right), 'w')	

	while left_pointer and right_pointer:
		left_value = int(left_pointer)
		right_value = int(right_pointer)

		if left_value <= right_value:
			merged_chunk.write(str(left_value) + '\n')
			left_pointer = left_half.readline()
		else:
			merged_chunk.write(str(right_value) + '\n')
			right_pointer = right_half.readline()

	while left_pointer:
		merged_chunk.write(left_pointer)
		left_pointer = left_half.readline()

	while right_pointer:
		merged_chunk.write(right_pointer)
		right_pointer = right_half.readline()
			
	left_half.close()
	os.remove(get_chunk_name(path_to_file, chunk_left))

	if right_half:
		right_half.close()
		os.remove(get_chunk_name(path_to_file, chunk_right))
	
	merged_chunk.close()
	os.rename(get_merged_chunk_name(path_to_file, chunk_left, chunk_right), get_chunk_name(path_to_file, merge_index))

external_sort('large-file-to-sort.txt')
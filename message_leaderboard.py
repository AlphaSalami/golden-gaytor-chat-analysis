import re
from collections import Counter
import os
import glob
import time
import concurrent.futures
import fnmatch
from .constants import Constants


class GetResults():

	def __init__(self, messages, num_top, username, in_position):

		self.messages = messages
		self.num_top = int(num_top)
		self.username = username
		self.in_position = int(in_position)-1

	def get_top(self):
		m_leaders = self.messages[0:self.num_top]
		for pos, user in enumerate(m_leaders, 1):
			print(f"{pos}. {user[0]} sent {user[1]} messages")
		print()

	def get_specific(self):
		for x, user in enumerate(self.messages):
			if self.username == user[0]:
				message_count = self.messages[x][1]
				print(f"{self.username} has sent {message_count} messages and is in position {x+1}\n")
				return
		

	def get_byposition(self):
		user = self.messages[self.in_position]
		print(f"{user[0]} has sent {user[1]} messages and is in position {self.in_position+1}\n")


class GenerateLeaderboard():

	def __init__(self, path, top_number, specific_username, specific_pos_num) -> None:
		self.constants = Constants(path)
		self.pattern = "\*.irc"
		self.reg = "(] <\w+>)"
		self.top_number = top_number
		self.specific_username = specific_username
		self.specific_pos_num = specific_pos_num


	def process_names(self, names_lst):
		processed_dct = {}
		for i in names_lst:
			processed_dct |= {i[0][3:-1]: i[1]}
		processed_list = list(zip(processed_dct.keys(), processed_dct.values()))
		return processed_list
		
	def process_data(self, all_data):
		message_counter = Counter(all_data)
		processed_counter = self.process_names(message_counter.most_common())
		return processed_counter

	def get_files(self, file):
		file_name = os.path.basename(file)
		with open(self.constants.rawYear+file_name, "r", encoding="utf-8") as f:
			data = f.read()
			messages = re.findall(self.reg, data)
			return messages

	def count_files(self):
		count = len(fnmatch.filter(os.listdir(self.constants.rawYear), '*.irc'))
		return count


	def run(self):

		#get file data
		time1 = time.time()
		files = glob.glob(self.constants.rawYear + self.pattern)
		with concurrent.futures.ThreadPoolExecutor(max_workers=31) as executor:
			future = [executor.submit(self.get_files, file) for file in files]

		file_data = [f.result() for f in future]
		flat_data = [item for sublist in file_data for item in sublist]
		num_files = self.count_files()

		timetaken1 = time.time() - time1

		#process data
		time2 = time.time()
		data = self.process_data(flat_data)
		timetaken2 = time.time() - time2
		
		#return data

		print(f"{len(flat_data)} total messages from {len(data)} unique chatters\n")
		time3 = time.time()
		Results = GetResults(data, self.top_number, self.specific_username, self.specific_pos_num)
		Results.get_top()
		Results.get_specific()
		Results.get_byposition()
		timetaken3 = time.time() - time3

		print(f"Time for getting data: {timetaken1}")
		print(f"Time for process data: {timetaken2}")
		print(f"Time to return data: {timetaken3}")
		print(f"Total time taken: {timetaken1+timetaken2+timetaken3}")
		print(f"Files processed: {num_files}")

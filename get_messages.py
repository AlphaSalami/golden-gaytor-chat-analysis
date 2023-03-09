import os
import glob
from .constants import Constants
from .compress_folder import Compress


class GetMessages():


	def __init__(self, path) -> None:
		self.constants = Constants(path)
		self.path = path
		self.target = "alphasalami"
		self.src = "./"
		self.pattern = "\*.irc"


	def get_messages(self, file, outfile):

		messages = []

		with open(file, "r", encoding="utf-8") as f:
			data = f.readlines()

		for d in data:
			if f"] <{self.target}>" in d:
				messages.append(d)

		print("".join(messages))
		print(len(messages))

		with open(self.src + outfile, "w", encoding="utf-8") as of:
			of.write(str(len(messages)) + " messages\n" + "".join(messages))

	def run(self):

		files = glob.glob(self.src + self.pattern)
		print(len(files))
		if len(files) == 0:
			src = self.constants.rawMonth
			files = glob.glob(src + self.pattern)	
			
		for file in files:
			file_name = os.path.basename(file)
			outfile = f"{self.target}- " + file_name
			if not os.path.exists(f"{self.constants.procMonth}/alphasalami/{outfile}"):
				self.get_messages(file, outfile)
			

		comp = Compress(self.path)
		comp.run()


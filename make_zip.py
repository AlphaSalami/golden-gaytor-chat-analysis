import os
import glob
import shutil
from zipfile import ZipFile
from .constants import Constants


class MakeZip():

	def __init__(self, path, target) -> None:
		self.constants = Constants(path)
		self.target = target
		self.src = "./../"
		self.pattern = "\*.irc"
		self.path = path


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

		files = glob.glob(self.constants.rawYear + self.pattern)	
			
		for file in files:
			file_name = os.path.basename(file)
			outfile = f"{self.target}- " + file_name
			if not os.path.exists(f"{self.constants.procYear}/{self.target}/{outfile}"):
				self.get_messages(file, outfile)
				
		files2 = glob.glob(self.src + self.pattern)
		if not os.path.exists(f"{self.constants.procYear}/{self.target}/"):
			os.mkdir(f"{self.constants.procYear}/{self.target}/")
		for file in files2:
			shutil.move(file, f"{self.constants.procYear}/{self.target}/")

		outputFileName = self.target + " - " + self.path
		dirName = self.constants.procYear + self.target + "/"

		shutil.make_archive(outputFileName, "zip", dirName)
			

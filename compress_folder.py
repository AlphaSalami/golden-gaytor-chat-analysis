import os
import shutil
import glob
from .constants import Constants

class Compress():

	def __init__(self, path) -> None:
		self.constants = Constants(path)
		self.target = "alphasalami"
		self.src = "./"
		if not os.path.exists(f"{self.constants.procMonth}{self.target}/"):
			os.mkdir(f"{self.constants.procMonth}{self.target}/")
		if not os.path.exists(f"{self.constants.procYear}{self.target}/"):
			os.mkdir(f"{self.constants.procYear}{self.target}/")
		self.a_year = f"{self.constants.procYear}{self.target}/"
		self.a_dest = f"{self.constants.procMonth}{self.target}/"
		self.a_pattern = self.src + f"{self.target}*"
		self.b_pattern = "\*.irc"


	def run(self):
		for file in glob.iglob(self.a_pattern, recursive=True):
			file_name = os.path.basename(file)
			if not os.path.exists(f"{self.constants.procYear}{file_name}"):
				shutil.copyfile(file, self.a_year + file_name)
			shutil.move(file, self.a_dest + file_name)
			print("Moved:", file)

		b_files = glob.glob(self.src + self.b_pattern)
		for file in b_files:
			file_name = os.path.basename(file)
			if not os.path.exists(f"{self.constants.rawYear}{file_name}"):
				shutil.copyfile(file, self.constants.rawYear + file_name)
			shutil.move(file, self.constants.rawMonth + file_name)
			print("Moved:", file)

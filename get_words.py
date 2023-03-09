from collections import Counter
import os
import shutil
import glob
import time
from .constants import Constants

class GetWords():

    def __init__(self, path) -> None:
        self.constants = Constants(path)
        self.pattern = "\*.irc"

    def get_words(self, file):
        word_counter = Counter()
        file_name = os.path.basename(file)
        with open(self.constants.rawYear+file_name, "r", encoding="utf-8") as f:
            data = f.readlines()
            line_count = len(data)
        for line in data:
            step = line.split(">")
            all_data = step[1].strip().split(" ")
            word_counter.update(all_data)
        return word_counter, line_count


    def run(self):
        files = glob.glob(self.constants.rawYear + self.pattern)
        total_word_count = Counter()
        lines = 0
        time1 = time.time()
        for file in files:
            file_data, line_c = self.get_words(file)
            total_word_count.update(file_data)
            lines += line_c

        final_count = total_word_count.most_common()
        uses = sum(total_word_count.values())
        with open("words.log", "w", encoding="utf-8") as f:
            f.write(f"Total of {lines} lines and {uses} words\n\n")
            for count, element in enumerate(final_count, 1):
                word = element[0]
                if not word:
                    word = "<message deleted> (timeout by moderator)"
                word_count = element[1]
                f.write(f"{count}: {word_count} uses of {word}\n")

        shutil.move("words.log", self.constants.baseFolder + "words.log")
        timetaken = time.time() - time1
        print(f"[+] Log generated ({timetaken}s)")


from collections import Counter
import os
import glob
import shutil
import time
from .constants import Constants


class ChatterWords():

    def __init__(self, path, target) -> None:
        self.constants = Constants(path)
        self.target = target
        self.pattern = "\*.irc"


    def get_words(self, file):
        word_counter = Counter()
        messages = 0
        file_name = os.path.basename(file)
        with open(self.constants.rawYear+file_name, "r", encoding="utf-8") as f:
            data = f.readlines()
        for line in data:
            step = line.split(">")
            if self.target in step[0]:
                all_data = step[1].strip().split(" ")
                word_counter.update(all_data)
                messages += 1
        return word_counter, messages

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
        with open(f"{self.target} words.log", "w", encoding="utf-8") as f:
            f.write(f"Total of {lines} messages and {uses} words\n\n")
            for count, element in enumerate(final_count, 1):
                word = element[0]
                if not word:
                    word = "<message deleted> (timeout by moderator)"
                word_count = element[1]
                f.write(f"{count}: {word_count} uses of {word}\n")
        if os.path.exists(f"{self.constants.chatterWordDest}/{self.target} words.log"):
            os.remove(f"{self.constants.chatterWordDest}/{self.target} words.log")
        shutil.move(f"{self.target} words.log", self.constants.chatterWordDest, f"{self.target} words.log")
        timetaken = time.time() - time1
        print(f"[+] Log generated ({timetaken}s)")

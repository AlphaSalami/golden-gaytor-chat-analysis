from collections import Counter
import os
import glob
import re
import shutil
import time
from .constants import Constants

class WordCount():
        
    def __init__(self, path, target_word) -> None:
        self.constants = Constants(path)
        self.target_word = target_word
        self.pattern = "\*.irc"
        self.reg = "(] <\w+>)"


    def get_words(self, file):
        word_counter = Counter()
        file_name = os.path.basename(file)
        with open(self.constants.rawYear+file_name, "r", encoding="utf-8") as f:
            data = f.readlines()
        for line in data:
            step = line.split(">")
            chatter_name = re.findall(self.reg, line)
            all_data = step[1].strip().split(" ")
            for word in all_data:
                if word == self.target_word:
                    try:
                        word_counter[chatter_name[0]] += 1
                    except:
                        pass
        return word_counter


    def run(self):
        files = glob.glob(self.constants.rawYear + self.pattern)
        total_word_count = Counter()
        time1 = time.time()
        for file in files:
            file_data = self.get_words(file)
            total_word_count.update(file_data)

        final_count = total_word_count.most_common()
        uses = sum(total_word_count.values())
        with open(f"{self.target_word} count leaderboard.log", "w", encoding="utf-8") as f:
            f.write(f"Total of {uses} uses of {self.target_word} from {len(final_count)} users\n\n")
            for count, element in enumerate(final_count, 1):
                chatter = element[0][2:]
                word_count = element[1]
                f.write(f"{count}: {chatter} used {self.target_word} {word_count} times\n")

        if os.path.exists(f"{self.constants.wordCountDest}{self.target_word} count leaderboard.log"):
            os.remove(f"{self.constants.wordCountDest}{self.target_word} count leaderboard.log")
        shutil.move(f"{self.target_word} count leaderboard.log", self.constants.wordCountDest, f"{self.target_word} count leaderboard.log")
        timetaken = time.time() - time1
        print(f"[+] Log generated ({timetaken}s)")


import os
import glob
import shutil
import time
from .constants import Constants


class WordContains():

    def __init__(self, path, user, word) -> None:
        self.constants = Constants(path)
        self.target_user = user
        self.target_word = word
        self.src = f"{self.constants.rawYear}/"
        if not os.path.exists(f"{self.constants.userWordsDest}/{self.target_user}/"):
            os.mkdir(f"{self.constants.userWordsDest}/{self.target_user}/")
        self.dest = f"{self.constants.userWordsDest}/{self.target_user}/"
        self.pattern = "\*.irc"
        self.user_messages_containing = []


    def get_messages(self, file):
        file_name = os.path.basename(file)
        with open(self.src+file_name, "r", encoding="utf-8") as f:
            data = f.readlines()
        for line in data:
            if self.target_user in line.split(">")[0]:
                if self.target_word in line:
                    self.user_messages_containing.append(line)
        return self.user_messages_containing


    def run(self):
        files = glob.glob(self.src + self.pattern)
        total_words = []
        time1 = time.time()
        for file in files:
            temp_words = self.get_messages(file)
            total_words.append(temp_words)
        uses = len(total_words[0])

        with open(f"{self.target_word} chats.log", "w", encoding="utf-8") as f:
            f.write(f"{uses} of {self.target_word} used by {self.target_user}\n\n")
            for line in total_words[0]:
                f.write(f"{line}")

        if os.path.exists(f"{self.constants.userWordsDest}/{self.target_user}/{self.target_word} chats.log"):
            os.remove(f"{self.constants.userWordsDest}/{self.target_user}/{self.target_word} chats.log")
        shutil.move(f"{self.target_word} chats.log", self.dest + f"{self.target_word} chats.log")
        timetaken = time.time() - time1
        print(f"[+] Log generated ({timetaken}s)")


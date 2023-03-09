import re
from collections import Counter
from .constants import Constants

class MostMessages():

    def __init__(self, path, title) -> None:
        self.constants = Constants(path)
        self.streamName = title
        self.file = self.streamName + ".irc"
        self.reg = "(] <\w+>)"
        
    
    def run(self):
        with open(self.constants.rawYear+self.file, "r", encoding="utf-8") as f:
            data = f.read()
            allData = re.findall(self.reg, data)

        sortedData = Counter(allData)
        topData = sortedData.most_common(15)


        print(f"{len(allData)} messages total. {len(sortedData)} unique chatters.\n")

        for count, user in enumerate(topData, 1):
            username = user[0][3:-1]
            messageCount = user[1]
            print(f"{count}. {username} sent {messageCount} messages")

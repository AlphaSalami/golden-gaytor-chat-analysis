import bin_py

path = "crump"


def runMostMessages(streamName):
    mostMessages = bin_py.most_messages.MostMessages(path, streamName)
    mostMessages.run()


def runMessageLeaderboard(top, username, position):
    messageLeaderboard = bin_py.message_leaderboard.GenerateLeaderboard(path, top, username, position)
    messageLeaderboard.run()


def runGetWords():
    getWords = bin_py.get_words.GetWords(path)
    getWords.run()


def runChatterWords(target):
    chatterWords = bin_py.chatter_words.ChatterWords(path, target)
    chatterWords.run()


def runCompareWordCount(word):
    compareWordCount = bin_py.compare_word_count.WordCount(path, word)
    compareWordCount.run()


def runGetChatterLog(chatter):
    makeZip = bin_py.make_zip.MakeZip(path, chatter)
    makeZip.run()


def runCheckContainsWord(chatter, word):
    checkContains = bin_py.check_word_contains.WordContains(path, chatter, word)
    checkContains.run()


def main():
    getMessage = bin_py.get_messages.GetMessages(path)
    getMessage.run()
    while True:
        try:
            userInput = str(input("\n------What do you wanna do------\n\n1: Most messages for single stream\n2: Display message leaderboard\n3: Generate log of all words\n4: Generate log for chatter sent words\n5: Generate log for most sent words\n6: Generate chat log zip for specific user\n7: Log of mesages containing word\n\n"))

            if userInput == "1":
                streamNameInput = str(input("Please enter the stream name\n"))
                runMostMessages(streamNameInput)

            elif userInput == "2":
                top = input("How many results:\n") or 0
                top = top if top != 0 else 20

                username = input("Enter username:\n") or 0
                username = username if username != 0 else "alphasalami"

                position = input("Enter position:\n") or 0
                position = position if position != 0 else 69

                runMessageLeaderboard(top, username, position)

            elif userInput == "3":
                runGetWords()

            elif userInput == "4":
                targetUserInput = str(input("Please enter the chatter username\n"))
                runChatterWords(targetUserInput)

            elif userInput == "5":
                targetWordInput = str(input("Please enter the word\n"))
                runCompareWordCount(targetWordInput)
        
            elif userInput == "6":
                targetChatter = str(input("Please enter chatter name\n"))
                runGetChatterLog(targetChatter)

            elif userInput == "7":
                targetChatter = str(input("Please enter chatter name\n"))
                targetStr = str(input("Please enter phrase\n"))
                runCheckContainsWord(targetChatter, targetStr)

            elif userInput == "-1":
                exit()

            else:
                print("Please choose a valid input")
        except Exception as e:
            print("Stop tryna break it xdd:", e)


main()

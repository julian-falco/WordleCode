def import_words(filename):
    """Import words from given text file into a list"""

    # open file
    file = open(filename, "r")
    file.readline() # skip first line of file (source link)

    # put all words into a word list
    word_list = []
    for word in file.readlines():
        word_list.append(word.strip())
    
    # close the file and return the word list
    file.close()
    return word_list

def compare(response, answer):
    """Find the number of green and yellow squares based on a given response and answer"""

    greens = 0
    yellows = 0
    green_letters = set() # keep track of each found green letter

    # find green letters first
    for i in range(len(answer)):
        if response[i] == answer[i]:
            greens += 1
            green_letters.add(response[i])
    
    # find yellow letters (letter is not marked as yellow if it was found as green)
    for i in range(len(answer)):
        if (response[i] not in green_letters) and (response[i] in answer):
            yellows += 1
    
    return greens, yellows

def convert_to_score(greens, yellows):
    """Based on green and yellow squares, create a score of how good the guess was"""

    # best possible guess -- all five letters correct
    if greens == 5:
        return 1
    
    # each green square is a full point
    points = greens

    # each yellow is worth 1 divided by the number of unkown squares
    if yellows > 0:
        unknowns = 5 - 1 - greens
        points += yellows / unknowns
    
    return points

def store_scores(list, filename):
    """Store a list of scores into a text file"""

    file = open(filename, "w")
    for score in list:
        file.write(f"{score[0]} {score[1]}\n")
    file.close()

def test_words():
    """For programmer use: test individual cases"""

    answer = input("\nanswer: ")
    response = input("response: ")

    greens, yellows = compare(response, answer)
    score = convert_to_score(greens, yellows) * 5

    print(greens, yellows, score)

def main():
    # import lists of words
    answers = import_words("PossibleAnswers.txt")
    allowed = answers + import_words("AllowedResponses.txt") # all possible gueses is the two files combined
    allowed.sort()

    allowed_scored = [] # master list

    # inform user of progress
    alpha = "a"
    print("Working on: 'a'")

    for response in allowed:

        # inform user of progess
        if response[0] != alpha:
            alpha = response[0]
            print(f"Working on: '{alpha}'")

        # score each possible response with each known answer and add them up
        score = 0
        for answer in answers:
            greens, yellows = compare(response, answer)
            score += convert_to_score(greens, yellows)
        
        # add averaged score to master list
        allowed_scored.append((score / len(answers), response))
    
    # sort from max to min
    allowed_scored.sort()
    allowed_scored.reverse()

    store_scores(allowed_scored, "ResponseScoresAveraged.txt")
        
if __name__ == "__main__":
    main()

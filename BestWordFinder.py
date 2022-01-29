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

    response_letters = [[letter, ""] for letter in response]
    answer_letters = [[letter, ""] for letter in answer]

    # find green letters
    for i in range(len(answer_letters)):
        if response_letters[i][0] == answer_letters[i][0]:
            response_letters[i][1] = "g"
            answer_letters[i][1] = "g"
    
    # find yellow letters
    for i in range(len(response_letters)):
        if response_letters[i][1] == "g":
            continue # do not check if already flagged as green
        for j in range(len(answer_letters)):
            if answer_letters[j][1] != "":
                continue # do not check if already flagged
            if response_letters[i][0] == answer_letters[j][0]:
                if answer_letters[j][1] == "y":
                    break
                else:
                    response_letters[i][1] = "y"
                    answer_letters[j][1] = "y"
                break
    
    return response_letters

def convert_to_score(response_letters):
    """Based on green and yellow squares, create a score of how good the guess was"""

    score = 0

    # count all the greens (worth one full point)
    for letter in response_letters:
        if letter[1] == "g":
            score += 1
    if score >= 4:
        return score
    
    # count and score each yellow
    for i in range(len(response_letters)):
        if response_letters[i][1] == "y":
            possible_spaces = 0
            for j in range(len(response_letters)):
                if j == i: 
                    continue # discount if same index
                elif response_letters[j][1] == "g": 
                    continue # discount if letters is already found
                elif response_letters[j][0] == response_letters[i][0]:
                    continue # discount if same letter is found elsewhere
                else:
                    possible_spaces += 1
            score += 1 / possible_spaces
    
    return score
    

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

    response_scored = compare(response, answer)
    score = convert_to_score(response_scored)

    print(response_scored, score)

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
            response_letters = compare(response, answer)
            score += convert_to_score(response_letters)
        
        # add averaged score to master list
        allowed_scored.append((score / len(answers), response))
    
    # sort from max to min
    allowed_scored.sort()
    allowed_scored.reverse()

    store_scores(allowed_scored, "ResponseScoresAveraged.txt")
        
if __name__ == "__main__":
    main()

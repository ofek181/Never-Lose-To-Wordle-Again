import argparse
from collections import Counter


def get_values_for_guesses_and_solutions(cheat: bool) -> list:
    """
    returns the database of words as a python list.
    :param cheat: chooses between the two databases.
    :return: list of all the words.
    """
    database = []
    # get all values for the user's possible guesses
    if not cheat:
        with open("possible_guesses") as guess_file:
            for line in guess_file:
                database.append(line.rstrip())

    # get all values for the game's possible solutions
    else:
        with open("possible_solutions") as solution_file:
            for line in solution_file:
                database.append(line.rstrip())

    return database


class WordleSolver:
    """
    A class which implements the solver script.
    """
    def __init__(self, data: list) -> None:
        """
        initialize the class' attributes.
        :param data: current database.
        """
        # initialize possible guesses and solutions as the entire dictionary
        self.data = data

    def filter_words(self, word: str, positions: str) -> list:
        """
        filters all the non-optional words based on the information given.
        :param word: entered word by the user.
        :param positions: information about the location of each letter
        :return: a filtered database of all the remaining optional words.
        """
        # get character counter dictionary from the given word
        counter = Counter(word)
        # get number of appearances of each character
        appearances = dict.fromkeys(counter, 0)
        no_appearances = dict.fromkeys(counter, False)
        for idx, value in enumerate(positions):
            if value == '1' or value == '2':
                appearances[word[idx]] += 1
            elif value == '3':
                no_appearances[word[idx]] = True
            else:
                raise AssertionError("Value needs to be 1, 2 or 3")

        # define a function to count the number of appearances of each letter
        def check_letter_count(data_word: str) -> bool:
            """
            checks if a given number of letters is coordinated with the number of letters from a word in the database.
            :param data_word: a word from the chosen database.
            :return: True whether the word shan't be filtered and False if the word shall be filtered.
            """
            for key in appearances:
                if no_appearances[key]:
                    if data_word.count(key) != appearances[key]:
                        return False
                else:
                    if data_word.count(key) < appearances[key]:
                        return False

            return True

        # filter out all guesses that don't contain at least the same amount of characters
        filtered_guesses = filter(check_letter_count, self.data)
        self.data = list(filtered_guesses)

        # define a function to check letter positions with value of 1
        def check_letter_position(data_word: str) -> bool:
            """
            checks whether the word's letters' positions match to those of the dataset's word.
            :param data_word: a word from the chosen database.
            :return: True whether the word shan't be filtered and False if the word shall be filtered.
            """
            for i, val in enumerate(positions):
                if val == '1' and data_word[i] != word[i]:
                    return False
                if val == '2' and data_word[i] == word[i]:
                    return False

            return True

        # filter out all guesses that don't contain the same positions
        filtered_guesses = filter(check_letter_position, self.data)
        self.data = list(filtered_guesses)

        return self.data


def main():
    # get parser object to handle the user's input
    parser = argparse.ArgumentParser(description='Enter a bool variable --wide to choose '
                                                 'between the different databases:\n'
                                                 'no input - all possible solutions database -2315 words\n'
                                                 '--wide - all possible guesses database (wider search) -12972 words\n',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--wide', default=True, action='store_false', help='Bool type')
    args = parser.parse_args()

    # initialize solver class
    data = get_values_for_guesses_and_solutions(args.wide)
    ws = WordleSolver(data)

    # print out instructions
    print('Welcome to wordleSolver!\n' +
          'Enter your guessed word then enter a 1/2/3 string with the following rules:\n' +
          '1 - letter is in the correct positions\n' +
          '2 - letter exists in the solution but is currently not in the correct positions\n' +
          '3 - letter does not exist in the solution\n' +
          'example: other 33213')

    # get input from the user and apply filters
    n_tries = 6
    while n_tries > 0:
        # filter out words
        word = input()
        positions = input()
        filtered_words = ws.filter_words(word, positions)
        print(filtered_words)
        n_tries -= 1

        if len(filtered_words) <= 1:
            exit()


if __name__ == '__main__':
    main()

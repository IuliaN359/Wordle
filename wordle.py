
import random



class Wordle:

    green="#38b858"
    yellow="#f8af00"
    dark_grey="#4a4a4a"


    def __init__(self):
        self.word=None
        self.used_words=[]

    def choosing_word(self, file):
        with open(file, "r") as file:
            words=file.read().split()
        self.word=random.choice(words)

    def game_logic(self,guess):
        if guess==self.word:
            return [self.green]*5
        word_list=list(self.word)
        guess_list=list(guess)
        lst=[None]*5

        for i in range(5):
            if guess_list[i]==word_list[i]:
                lst[i]=self.green
                word_list[i]=None
                guess_list[i]=None

        for i in range(5):
            if guess_list[i] is not None:
                if guess_list[i] in word_list:
                    lst[i]=self.yellow
                    word_list[word_list.index(guess_list[i])]=None
                else:
                    lst[i]=self.dark_grey
        return lst


class Score:

    def addScore(self, status: str, word: str, steps: int):
        with open("scores.txt", "a") as file:
            file.write(f"{status} {word} {steps}\n")

    def getScores(self):
        scores = []
        with open("scores.txt", "r") as file:
            for line in file:
                if line.strip():
                    status, word, steps = line.strip().split()
                    scores.append([status, word, int(steps)])
        return scores


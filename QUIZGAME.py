import requests
import random


amount = [1000, 2000, 5000, 10000, 20000, 40000, 80000, 160000, 320000,
          650000, 1250000, 2500000, 5000000, 10000000, 100000000]


class GameFlow:
    def __init__(self):
        self.diff = 1
        self.prizeMoney = 0
        self.i = 0
        self.lifeline = {1: '2x', 2: 'Flip the question', 3: 'Expert Advice'}
        self.flag = True
        self.flag2 = False

    def getQuestions(self, n):
        self.diff = n
        baseurl = "https://quizzrapi.herokuapp.com/difficulty/"+str(self.diff)
        question = requests.get(baseurl)
        ques = question.json()
        return ques

    @staticmethod
    def displayQuestion(question):
        print('==================================================================')
        print('Q.', question['question'])
        a = question['a']
        b = question['b']
        c = question['c']
        d = question['d']
        print("A: {}    B: {}".format(a, b))
        print("C: {}    D: {}".format(c, d))

    def process(self, question):
        answer = question['answer']
        self.displayQuestion(question)
        ans = input('Answer: ').lower()
        if ans == 'quit':
            print('{} has quit the game'.format(name))
            print('Total prize money won: {}'.format(self.prizeMoney))
            exit(0)
        elif ans == 'll':
            return self.lifelines(question, answer)
        if ans == answer:
            return True
        return False

    def winnings(self, amt):
        print('***Correct Answer***')
        self.prizeMoney = amt
        print('Money won: {}'.format(amt))
        print('Total prize money: {}'.format(self.prizeMoney))
        return self.prizeMoney

    def bonusQuestion(self):
        print('* * * * * * * * * * * * * * * Congratulations * * * * * * * * * * * * * * *')
        print('* * * * * * * * * * * * * * * {} won the game * * * * * * * * * * * * * * * '.format(name))
        print('* * * * * * * Prize money won: {} * * * * * * * * * * * *'.format(self.prizeMoney))

    def gameFlow(self):
        while self.i <= 8:
            question = self.getQuestions(random.randint(1, 3))
            val = self.process(question)
            if val:
                self.winnings(amount[self.i])
                self.i += 1
            else:
                print('Incorrect answer\nCorrect answer was: {}'.format(question['answer'].upper()))
                self.flag = False
                self.flag2 = True
                break
        if self.flag:
            while self.i <= 14:
                question = self.getQuestions(random.randint(4, 5))
                val = self.process(question)
                if val:
                    self.winnings(amount[self.i])
                    self.i += 1
                else:
                    self.flag2 = True
                    break
        if self.flag2:
            if 8 > self.i >= 5:
                self.prizeMoney = 40000
            elif self.i >= 8:
                self.prizeMoney = 320000
            else:
                self.prizeMoney = 0
            print('Prize money won = {}'.format(self.prizeMoney))
        if not self.flag2:
            self.bonusQuestion()

    def lifelines(self, question, answer):
        print('___________________________________________________________')
        if len(self.lifeline) > 0:
            print('Available lifeline are: ')
            [print("{}: {}".format(j, self.lifeline[j])) for j in self.lifeline.keys()]
            ll = int(input('Enter the number: '))
            if ll in self.lifeline.keys():
                if self.lifeline[ll] == '2x':
                    del self.lifeline[ll]
                    return self.func2x(question, answer)
            #     if self.lifeline[ll-1] == 'NUll':
            #         print('Already used !!')
            #         self.lifelines(question, answer)
            #     var = self.func2x(question, answer, ll-1)
            #     return var
                elif self.lifeline[ll] == 'Flip the question':
                    del self.lifeline[ll]
                    return self.process(self.ftq(question['id']))
            # elif str(ll) == '2:':
            #     new_question = self.ftq(question['id'], ll-1)
            #     return self.process(new_question)
                elif self.lifeline[ll] == 'Expert Advice':
                    self.ed(answer)
                    del self.lifeline[ll]
                    return self .process(question)
            # elif str(ll) == '3':
            #     self.ed(answer, ll-1)
            #     return self.process(question)
        else:
            print('No lifeline left')
            print("You can quit the game if you don't know the answer.")
            return self.process(question)

    def func2x(self, question, answer):
        self.displayQuestion(question)
        print('Note: You can give two answers to this question, correct answer will be accepted')
        for i in range(2):
            ans = input('Answer: ')
            if answer == ans:
                return True
            else:
                print('Oops!! wrong answer\nPlease try again')
        return False

    def ftq(self, qid):
        question = self.getQuestions(4)
        if question['id'] == qid:
            question = self.getQuestions(4)
        return question

    @staticmethod
    def ed(answer):
        print('I believe the answer is {}'.format(answer.upper()))


print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
print('                     Ultimate Quiz Game                     ')
print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
game = GameFlow()
print('Rules:\n'
      '1. There will be two checkpoints at i)Q4, ii)Q7\n'
      '2. Type quit as answer to quit the game\n'
      '3. You will have 3 lifeline (2x, Flip the question, Expert Advice)\n'
      "  -type 'll' as answer for using lifelines\n")
input('               *Hit enter to start the game*                ')
print('____________________________________________________________')
name = input('Please enter your name: ')
game.gameFlow()

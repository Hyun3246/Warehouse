import random

class Deck():
    def __init__(self, size):
        self.card_list = [i for i in range(size)]
        self.card_in_play_list = []
        self.discards_list = []
        random.shuffle(self.card_list)
    
    def deal(self):
        if len(self.card_list) < 1:
            random.shuffle(self.discards_list)
            self.card_list = self.discards_list
            self.discards_list = []
            print("Reshuffling...!!!")
        new_card = self.card_list.pop()
        self.card_in_play_list.append(new_card)
        return new_card
    
    def new_hand(self):
        self.discards_list += self.card_in_play_list
        self.card_in_play_list.clear()

a = Deck(5)

print(a.card_list)

card_to_submit = input("제출할 카드를 입력하세요: ")

card_to_submit = card_to_submit.split(', ')

print(card_to_submit)

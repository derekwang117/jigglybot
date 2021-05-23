import random


def convert_to_value(x):
    x = x % 13
    if x > 0:
        x += 1
    if x > 10:
        x = 10
    return x


def convert_to_card(x):
    x = x % 13
    if x == 0:
        card = 'Ace'
    elif x == 10:
        card = 'Jack'
    elif x == 11:
        card = 'Queen'
    elif x == 12:
        card = 'King'
    else:
        card = str(x+1)
    return '{0}'.format(card)


# suits are club: 0-12, diamond: 13-25, heart: 26-38, spade: 39-51
def get_value(hand: list):
    values = list(map(convert_to_value, hand))
    ace_count = values.count(0)
    total = sum(values)

    while ace_count > 0 and total + (ace_count - 1) + 11 <= 21:
        ace_count -= 1
        total += 11
    total += ace_count

    return total


def read_hand(hand: list):
    read = []
    for card in hand:
        read.append(convert_to_card(card))
    return read


class BlackJackBoard:

    def __init__(self):
        # 4 decks
        self.deck = [*range(0, 208)]
        self.dealer = []
        self.player = []
        self.isDone = False
        self.isWinner = -1

        self.hit(self.player)
        self.hit(self.player)
        self.hit(self.dealer)
        self.hit(self.dealer)

    def draw_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def hit(self, hand: list):
        new_card = self.draw_card()
        hand.append(new_card)
        if (get_value(hand)) > 21:
            return False
        return True

    def user_state(self):
        state = 'Your hand: {}'.format(read_hand(self.player))
        return state

    def dealer_state(self):
        state = "The dealer: {}".format(read_hand(self.dealer))
        return state

    def dealer_start(self):
        state = "The dealer's first card is {}".format(convert_to_card(self.dealer[0]))
        return state

    def end(self):
        self.isDone = True

    @property
    def isWinner(self):
        return self.__isWinner

    @isWinner.setter
    def isWinner(self, int):
        self.__isWinner = int

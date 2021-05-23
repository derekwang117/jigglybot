import random


def convert_to_value(x):
    x = x % 13
    if x > 0:
        x += 1
    if x > 10:
        x = 10
    return x


def convert_to_card(x):
    if x < 13:
        suit = 'Clubs'
    elif x < 26:
        suit = 'Diamonds'
    elif x < 39:
        suit = 'Hearts'
    else:
        suit = 'Spades'
    x = x % 13
    if x == 0:
        card = 'Ace'
    elif x == 11:
        card = 'Jack'
    elif x == 12:
        card = 'Queen'
    elif x == 13:
        card = 'King'
    else:
        card = str(x)
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
    list = []
    for card in hand:
        list.append(convert_to_card(convert_to_value(card)))
    return list


class BlackJackBoard:

    def __init__(self):
        self.deck = [*range(0, 52)]
        self.dealer = []
        self.player = []
        self.isDone = False

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

    def check_win(self):
        self.isDone = True
        if get_value(self.player) > get_value(self.dealer):
            return True
        else:
            return False

    def board_state(self, user):
        state = '{0}: {1}\n The dealer has {2} cards'.format(user, read_hand(self.player), len(self.dealer))
        return state

    def end(self):
        self.isDone = True


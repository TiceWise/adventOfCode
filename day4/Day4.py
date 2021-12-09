import numpy as np

f = open('input.txt')

drawn_numbers = np.array(list(f.readline().strip().split(',')))
print(drawn_numbers)

drawn_numbers = drawn_numbers.astype(int)

bingo_cards = np.array([])
while True:
    line = f.readline()
    if not line:
        break
    if line != '\n':
        bingo_cards = np.append(bingo_cards, np.array(list(line.strip().split(' '))))

bingo_cards = bingo_cards[bingo_cards != '']

bingo_cards = np.reshape(bingo_cards, (-1, 5, 5))
bingo_cards = bingo_cards.astype(int)
print(bingo_cards.shape)

score_cards = np.zeros(bingo_cards.shape, dtype=bool)

for number in drawn_numbers:
    print(number)
    score_cards = score_cards + (bingo_cards == number)
    if np.any(np.all(score_cards, axis=1)) or np.any(np.all(score_cards, axis=2)):
        card_number = np.nonzero(np.all(score_cards, axis=1))[0]
        card = bingo_cards[card_number, :, :]
        score_card = score_cards[card_number, :, :]
        sum_of_remaining = np.sum(card * np.invert(score_card))
        print(number)
        print(sum_of_remaining)
        print(card)
        print(f'{number} * {sum_of_remaining} = answer: {number * sum_of_remaining}')

        # ----------- Part 2 -----------
        bingo_cards = np.delete(bingo_cards, card_number, axis=0)
        score_cards = np.delete(score_cards, card_number, axis=0)
        print(bingo_cards)
    if np.any(np.all(score_cards, axis=2)):
        card_number = np.nonzero(np.all(score_cards, axis=2))[0]
        card = bingo_cards[card_number, :, :]
        score_card = score_cards[card_number, :, :]
        sum_of_remaining = np.sum(card * np.invert(score_card))
        print(number)
        print(sum_of_remaining)
        print(card)
        print(f'{number} * {sum_of_remaining} = answer: {number * sum_of_remaining}')

        # ----------- Part 2 -----------
        bingo_cards = np.delete(bingo_cards, card_number, axis=0)
        score_cards = np.delete(score_cards, card_number, axis=0)
        print(bingo_cards)

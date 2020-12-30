def combat(cards1, cards2, recursive):
    combat_states = set()
    while len(cards1) and len(cards2):
        if recursive:
            combat_state = (tuple(cards1), tuple(cards2))
            if combat_state in combat_states:
                return (cards1, 1)
            combat_states.add(combat_state)
        card1 = cards1.pop(0)
        card2 = cards2.pop(0)
        # recursive combat
        if recursive and len(cards1) >= card1 and len(cards2) >= card2:
            _, winner_num = combat(cards1[:card1], cards2[:card2], recursive)
            winner = cards1 if winner_num == 1 else cards2
        # normal combat
        else:
            winner = cards1 if card1 > card2 else cards2

        if winner == cards1:
            cards1.extend([card1, card2])
        else:
            cards2.extend([card2, card1])
    return (cards2, 2) if len(cards2) else (cards1, 1)


def get_deck_value(deck):
    return sum(c * (i + 1) for i, c in enumerate(reversed(deck)))


def main():
    with open("inputs/day22.txt", "r") as file:
        p1, p2 = file.read().split("\n\n")
        cards1 = [int(c) for c in p1.split("\n")[1:]]
        cards2 = [int(c) for c in p2.split("\n")[1:]]

    # part1
    winning_deck, _ = combat(list(cards1), list(cards2), recursive=False)
    print(get_deck_value(winning_deck))

    # part2
    winning_deck, _ = combat(list(cards1), list(cards2), recursive=True)
    print(get_deck_value(winning_deck))


if __name__ == "__main__":
    main()

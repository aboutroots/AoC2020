MOVES = 10000000
EXTEND_CUPS_TO = 1000000


def im_so_fast_boiiiii():
    """https://www.youtube.com/watch?v=Xw1k20DpHfA"""

    # yeah subtract 1 form cup values, it makes everything easier
    cups = [int(x) - 1 for x in list("389125467")]
    cups.extend(list(range(len(cups), EXTEND_CUPS_TO)))
    sorted_cups = sorted(cups)

    # these will be useful
    min_cup = sorted_cups[0]
    max_cup = sorted_cups[-1]
    max_cup2 = sorted_cups[-2]
    max_cup3 = sorted_cups[-3]
    max_cup4 = sorted_cups[-4]
    current_cup = cups[0]

    # prepare linked list
    linked_list = {}
    for index in range(len(cups)):
        next_few = cups[index : index + 3]
        if index in next_few:
            index_in_cups = index + next_few.index(index)
        else:
            index_in_cups = cups.index(index)

        next_i = index_in_cups + 1 if index_in_cups < len(cups) - 1 else 0
        next_cup = cups[next_i]
        linked_list[index] = next_cup
    """
    at this point we have a linked list (yeah I know its a dictionary, its easier for
     me to work on dictionaries)
    
    KEY is the cup value
    VALUE is the cup value of the next cup
    
    Example:
    for cups  278014356 (remember we subtracted "1")
    we have linked list: 
    {
        2: 7,
        7: 8,
        8: 0,
        0 :1,
        1: 4,
        4: 3,
        3: 5,
        5: 6
        6: 2
    }
    
    We dont use initial "cups" from this point forward. (only linked list)
    """

    for move in range(MOVES):
        next_cup = linked_list[current_cup]
        next_cup_2 = linked_list[next_cup]
        next_cup_3 = linked_list[next_cup_2]
        next_three_cups = [next_cup, next_cup_2, next_cup_3]

        destination_cup = current_cup
        while True:
            destination_cup = destination_cup - 1
            if destination_cup in next_three_cups:
                continue
            if destination_cup < min_cup:
                # i know its ugly, at this point I dont care
                if max_cup not in next_three_cups:
                    destination_cup = max_cup
                elif max_cup2 not in next_three_cups:
                    destination_cup = max_cup2
                elif max_cup3 not in next_three_cups:
                    destination_cup = max_cup3
                elif max_cup4 not in next_three_cups:
                    destination_cup = max_cup4
                break
            else:
                break

        # Fun stuff: change pointers in linked list
        next_after_destination = linked_list[destination_cup]
        next_after_selected_3 = linked_list[next_cup_3]

        linked_list[destination_cup] = next_cup
        linked_list[next_cup_3] = next_after_destination
        linked_list[current_cup] = next_after_selected_3

        current_cup = linked_list[current_cup]

    first_after_one = linked_list[0]
    second_after_one = linked_list[first_after_one]

    # remember we subtracted "1"? we need to add it now
    first = first_after_one + 1
    second = second_after_one + 1
    print(first, second, first * second)


def main():
    import cProfile
    import pstats

    cProfile.run("im_so_fast_boiiiii()", "{}.profile".format(__file__))
    s = pstats.Stats("{}.profile".format(__file__))
    s.strip_dirs()
    s.sort_stats("time").print_stats(10)


if __name__ == "__main__":
    main()

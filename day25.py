from common import file_to_lines


def transform(subject_number, loopsize):
    value = 1
    for _ in range(loopsize):
        _, value = divmod(value * subject_number, 20201227)
    return value


# def handshake():
#     # card
#     secret_card_loopsize = 10
#     subject = 7
#     card_public_key = transform(7, secret_card_loopsize)
#
#     # door
#     secret_door_loopsize = 11
#     subject = 7
#     door_public_key = transform(7, secret_door_loopsize)
#
#     # card
#     encryption_key = transform(door_public_key, secret_card_loopsize)
#     encryption_key = transform(card_public_key, secret_door_loopsize)


def find_loopsize(p_keys, subject):
    value = 1
    loopsize = 0
    while True:
        loopsize += 1
        _, value = divmod(value * subject, 20201227)
        print(loopsize, value, p_keys[0], p_keys[1])
        if value == p_keys[0]:
            return loopsize, p_keys[1]
        if value == p_keys[1]:
            return loopsize, p_keys[0]


def first(p_keys):
    # print(transform(11161639, 11002971))
    card_pkey, door_pkey = p_keys
    loopsize, pkey = find_loopsize(p_keys, 7)
    encryption_key = transform(pkey, loopsize)
    print(encryption_key)


def second(rows):
    pass


def main():
    # p_keys = [5764801, 17807724]  # 14897079
    p_keys = [15628416, 11161639]
    first(p_keys)
    second(p_keys)


if __name__ == "__main__":
    main()

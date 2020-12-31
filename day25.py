def transform(subject_number, loopsize):
    value = 1
    for _ in range(loopsize):
        _, value = divmod(value * subject_number, 20201227)
    return value

def find_loopsize(p_keys, subject):
    value = 1
    loopsize = 0
    while True:
        loopsize += 1
        _, value = divmod(value * subject, 20201227)
        if value == p_keys[0]:
            return loopsize, p_keys[1]
        if value == p_keys[1]:
            return loopsize, p_keys[0]


p_keys = [5764801, 17807724]
loopsize, pkey = find_loopsize(p_keys, 7)
encryption_key = transform(pkey, loopsize)
print(encryption_key)

def compute(numbers, n):
    mem = {num: index + 1 for index, num in enumerate(numbers[:-1])}
    last_spoken = numbers[-1]
    for turn in range(len(numbers), n):
        current = turn - mem[last_spoken] if last_spoken in mem else 0
        mem[last_spoken] = turn
        last_spoken = current
    return last_spoken

print(compute([0, 14, 1, 3, 7, 9], 2020))
print(compute([0, 14, 1, 3, 7, 9], 30000000))

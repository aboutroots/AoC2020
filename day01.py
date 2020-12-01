from common import file_to_lines

def get_2_numbers(rows):
    for idx1, row in enumerate(rows):
        num = int(row)
        if num > 2020:
            continue
        for idx2, row2 in enumerate(rows[idx1 + 1:]):
            num2 = int(row2)
            if num2 > 2020:
                continue
            if num + num2 == 2020:
                return (num, num2)

def get_3_numbers(rows):
    for idx1, row in enumerate(rows):
        num = int(row)
        if num > 2020:
            continue
        for idx2, row2 in enumerate(rows[idx1 + 1:]):
            num2 = int(row2)
            if num2 > 2020:
                continue
            for idx3, row3 in enumerate(rows[idx2 + 1:]):
                num3 = int(row3)
                if num3 > 2020:
                    continue
                if num + num2 + num3 == 2020:
                    return (num, num2, num3)



def main():
    rows = file_to_lines('inputs/day01.txt')
    numbers = get_3_numbers(rows)
    print(numbers[0] * numbers[1] * numbers[2])




if __name__ == '__main__':
    main()
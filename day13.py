import math
from common import file_to_lines


def first(rows):
    earliest = int(rows[0].strip())
    buses = [int(bus) for bus in rows[1].split(",") if bus != "x"]
    counter = earliest
    while True:
        for bus in buses:
            if counter % bus == 0:
                return (counter - earliest) * bus
        counter += 1


def lcm(arr):
    # get least common multip. from array of integers
    result = arr[0]
    for i in arr[1:]:
        result = result * i // math.gcd(result, i)
    return result


def second(rows):
    buses = [
        (int(bus), index) for index, bus in enumerate(rows[1].split(",")) if bus != "x"
    ]
    counter = 0
    step = buses[0][0]
    while True:
        success = True
        for bus, index in buses:
            expected = (counter + index) % bus == 0
            if expected:
                step = lcm([step, bus])
            else:
                success = False
                break

        if success:
            return counter
        counter += step


def main():
    rows = file_to_lines("inputs/day13.txt")
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()

import re
from functools import partial

from common import file_to_lines


class ValidatorsFactory:
    def create_min_max_validator(self, min, max):
        return partial(self._check_minmax, min, max)

    def create_min_max_map_validator(self, map):
        return partial(self._check_minmax_map, map)

    def create_regex_validator(self, pattern):
        return partial(self._check_regex, pattern)

    def create_includes_validator(self, array):
        return partial(self._check_contains, array)

    def _check_minmax_map(self, map, value):
        search = re.search(r"\d*(\D*)", value)
        if not search:
            return False
        key = search.group(1)
        if key not in map:
            return False
        return self._check_minmax(map[key][0], map[key][1], value.rstrip(key))

    @staticmethod
    def _check_contains(array, value):
        return value in array

    @staticmethod
    def _check_minmax(min, max, value):
        return min <= int(value) <= max

    @staticmethod
    def _check_regex(pattern, value):
        re_pattern = re.compile(pattern)
        return re_pattern.match(value)


class PassportValidator:
    def __init__(self):
        self.validators = ValidatorsFactory()

        self.rules = {
            "byr": self.validators.create_min_max_validator(1920, 2002),
            "iyr": self.validators.create_min_max_validator(2010, 2020),
            "eyr": self.validators.create_min_max_validator(2020, 2030),
            "hgt": self.validators.create_min_max_map_validator(
                {
                    "cm": (150, 193),
                    "in": (59, 76),
                }
            ),
            "hcl": self.validators.create_regex_validator(r"^#[a-f0-9]{6}$"),
            "ecl": self.validators.create_includes_validator(
                ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            ),
            "pid": self.validators.create_regex_validator(r"^[0-9]{9}$"),
        }

    def validate_presence(self, credentials):
        return all([key in credentials for key in self.rules.keys()])

    def validate(self, credentials):
        if not self.validate_presence(credentials):
            return False

        return all(
            [validator(credentials[key]) for key, validator in self.rules.items()]
        )


def row_to_creds(row):
    return dict([(pair.split(':')) for pair in row.split()])


def first(rows):
    pass_validator = PassportValidator()
    return sum(pass_validator.validate_presence(row_to_creds(row)) for row in rows)


def second(rows):
    pass_validator = PassportValidator()
    return sum(pass_validator.validate(row_to_creds(row)) for row in rows)


def main():
    rows = file_to_lines("inputs/day04.txt", separate_with_empty=True)
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()

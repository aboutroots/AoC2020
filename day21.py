from common import file_to_lines


def parse_line(row):
    ingredients, allergens = row.strip().strip(")").split(" (contains ")
    ingredients = ingredients.split(" ")
    allergens = allergens.split(", ")
    return allergens, ingredients


def compute(meals):
    all_ingredients_with_duplicates = []
    all_allergens = set()
    for line in meals:
        allergens, names = parse_line(line)
        all_ingredients_with_duplicates.extend(names)
        all_allergens.update(set(allergens))

    proposed_names = {}
    solved = {}

    while len(solved) != len(all_allergens):
        for meal in meals:
            allergens, names = parse_line(meal)
            for allergen in allergens:
                if allergen in solved:
                    continue

                if allergen not in proposed_names:
                    proposed_names[allergen] = set(names) - set(solved.values())
                else:
                    proposed_names[allergen] &= set(names)

                if len(proposed_names[allergen]) == 1:
                    name = proposed_names[allergen].pop()
                    solved[allergen] = name
                    del proposed_names[allergen]
                    for other_allergen in proposed_names.keys():
                        proposed_names[other_allergen].discard(name)

    # part1
    c = sum(1 for ing in all_ingredients_with_duplicates if ing not in solved.values())
    print(c)
    # part2
    print(",".join([a[1] for a in sorted(solved.items())]))


rows = file_to_lines("inputs/day21.txt")
compute(rows)

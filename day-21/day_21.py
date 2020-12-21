"""
https://adventofcode.com/2020/day/21
"""

# Read input: foods' ingredients and some (but not necessarily all) allergens
with open('day-21/input.txt') as fp:
    lines = fp.read().split('\n')
food_to_ingredients = dict()
food_to_allergens = dict()
for i, line in enumerate(lines):
    f, a = line.split('(contains ')
    food_to_ingredients[i] = f.strip(' ').split(' ')
    food_to_allergens[i] = a.strip(')').split(', ')
nfoods = len(food_to_ingredients)

# determine unique allergens and ingredients
unique_allergens = set(
    [a for sublist in food_to_allergens.values() for a in sublist])
unique_ingredients = set(
    [f for sublist in food_to_ingredients.values() for f in sublist])

# map from ingredient to foods in which it appears
ingredient_to_foods = dict()
for ingredient in unique_ingredients:
    ingredient_to_foods[ingredient] = [
        i for i in range(nfoods) if ingredient in food_to_ingredients[i]]

# map from allergen to foods in which it appears
allergen_to_foods = dict()
for allergen in unique_allergens:
    allergen_to_foods[allergen] = [
        i for i in range(nfoods) if allergen in food_to_allergens[i]]

# determine the foods which may correspond to allergens
allergen_to_common_ingredients = dict()
for allergen, foods in allergen_to_foods.items():
    common_ingredients = set(food_to_ingredients[foods[0]])
    for food in foods[1:]:
        common_ingredients.intersection_update(set(food_to_ingredients[food]))
    allergen_to_common_ingredients[allergen] = common_ingredients


ingredient_to_allergen = dict()  # this is what we need to solve the problem
correspondence = True
while correspondence:
    correspondence = False
    for a in unique_allergens:  # find 1-to-1 correspondences
        if len(allergen_to_common_ingredients[a]) == 1:
            correspondence = True
            ingredient = allergen_to_common_ingredients[a].pop()
            ingredient_to_allergen[ingredient] = a
            break
    if correspondence:  # update the mapping
        for a in unique_allergens:
            if ingredient in allergen_to_common_ingredients[a]:
                allergen_to_common_ingredients[a].remove(ingredient)

# determine the ingredients which cannot possibly contain a listed allergen
safe_ingredients = set(
    [ing for ing in unique_ingredients if ing not in ingredient_to_allergen])

# Problem 1: count the number of times a safe ingredient appears
nsafe = 0
for _, ingredients in food_to_ingredients.items():
    for ing in ingredients:
        if ing in safe_ingredients:
            nsafe += 1
print(f'problem 1: {nsafe}')

# Arrange the ingredients alphabetically *by allergen* and separate them by
# commas to produce your canonical dangerous ingredient list.
ingredients, allergens = list(zip(*ingredient_to_allergen.items()))
isort = [i[0] for i in sorted(enumerate(allergens), key=lambda x:x[1])]
dangerous_ingredients = ",".join(
    [ing for ing in [ingredients[i] for i in isort]])
print(f'problem 2: {dangerous_ingredients}')

import random

from exceptions.exceptions import NonExistentCombinationsException


def create_tags_combinations(tags, tags_amount):
    if tags_amount == 1:
        return tags
    if tags_amount == 2:
        return two_tags_combination(tags)
    if tags_amount == 3:
        return three_tags_combination(tags)
    if tags_amount == 5:
        return five_tags_combination(tags)

    raise NonExistentCombinationsException('There\'s no algorithm created for {} tags combinatory'.format(tags_amount))


def two_tags_combination(tags):
    result = []
    for i in range(len(tags) - 1):
        result.append([tags[i], tags[i + 1]])
        if i + 2 < len(tags):
            result.append([tags[i], tags[i + 2]])
    result.append([tags[0], tags[-1]])
    random.shuffle(result)

    return result


def three_tags_combination(tags):
    result = []
    for i in range(len(tags) - 2):
        result.append([tags[i], tags[i + 1], tags[i + 2]])
        if i + 3 < len(tags) - 1:
            result.append([tags[i], tags[i + 2], tags[i + 3]])
    result.append([tags[0], tags[-1], tags[-2]])
    random.shuffle(result)

    return result


def five_tags_combination(tags):
    result = []
    for i in range(len(tags) - 4):
        result.append([tags[i], tags[i + 1], tags[i + 2], tags[i + 3], tags[i + 4]])
        if i + 5 < len(tags) - 3:
            result.append([tags[i], tags[i + 2], tags[i + 3], tags[i + 4], tags[i + 5]])
    result.append([tags[0], tags[-1], tags[-2]])
    random.shuffle(result)

    return result

def two_tags_combination(tags):
    result = []
    for i in range(len(tags) - 1):
        result.append([tags[i], tags[i + 1]])
        if i + 2 < len(tags):
            result.append([tags[i], tags[i + 2]])
    result.append([tags[0], tags[-1]])

    return result


def three_tags_combination(tags):
    result = []
    for i in range(len(tags) - 2):
        result.append([tags[i], tags[i + 1], tags[i + 2]])
        if i + 3 < len(tags) - 1:
            result.append([tags[i], tags[i + 2], tags[i + 3]])
        result.append([tags[0], tags[-1], tags[-2]])

    return result


def five_tags_combination(tags):
    result = []
    for i in range(len(tags) - 4):
        result.append([tags[i], tags[i + 1], tags[i + 2], tags[i + 3], tags[i + 4]])
        if i + 5 < len(tags) - 3:
            result.append([tags[i], tags[i + 2], tags[i + 3], tags[i + 4], tags[i + 5]])
        result.append([tags[0], tags[-1], tags[-2]])

    return result

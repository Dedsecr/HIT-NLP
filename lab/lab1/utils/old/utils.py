def find_in_list(lis, x):
    for l in lis:
        if x == l:
            return True
    return False

def remove_repeated_ele(words):
    new_words = [words[0]]
    for i in range(1, len(words)):
        if words[i] != words[i - 1]:
            new_words.append(words[i])
    return new_words
from .utils import *

mod = 100007

def remove_repeated_words(words):
    new_words = [words[0]]
    for i in range(1, len(words)):
        if words[i] != words[i - 1]:
            new_words.append(words[i])
    return new_words

def get_single_words(words):
    single_words = []
    words = [_ for w in words for _ in w]
    for word in words:
        for sw in word:
            if not find_in_list(single_words, sw): single_words.append(sw)
    return single_words

def hash(word, hash_base):
    hash_base_, hash_res = 1, 0
    codes = word.encode('utf-8')
    for code in codes:
        hash_res += hash_base_ * code
        hash_base_ *= hash_base
    hash_res %= mod
    return hash_res

def get_hash_base(single_words):
    print(single_words)
    hash_base_candidates = range(mod)
    for hash_base in hash_base_candidates:
        legal = True
        hashes = []
        for word in single_words:
            hash_res = hash(word, hash_base)
            if find_in_list(hashes, hash_res):
                legal = False
                break
            else: hashes.append(hash_res)
        if legal: 
            hashes.sort()
            print(hashes)
            print(len(hashes))
            print(max(hashes))
            return hash_base
    return -1



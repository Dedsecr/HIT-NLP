from .utils import *

mod = 8647

def get_single_words(words):
    single_words = []
    words = [_ for w in words for _ in w]
    for word in words:
        for sw in word:
            if not find_in_list(single_words, sw): single_words.append(sw)
    return single_words

def hash(word, hash_base):
    hash_base_, hash_res = 1, 0
    codes = word.encode('gbk')
    # print(codes)
    for code in codes:
        hash_res += hash_base_ * code
        hash_base_ *= hash_base
    hash_res %= mod
    return hash_res

def get_hash_base(single_words):
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
            return hash_base, max(hashes)
    return -1, -1



import unigram
import numpy as np


def preprocess(src_path):
    src_file = open(src_path, 'r', encoding='gbk')
    src_lines = src_file.readlines()
    dst_lines = []
    for src_line in src_lines:
        if src_line == '\n':
            continue
        dst_line = []
        for word in src_line[23:].split():
            dst_line.append(word[1 if word[0] == '[' else 0:word.index('/')])
        dst_lines.append(dst_line)
    return dst_lines


def gen_two_gram_dic(src_path, dic_path):
    two_gram_dic = {}
    data_lines = preprocess(src_path)
    for line in data_lines:
        line.insert(0, 'BOS')
        line.append('EOS')
        for i in range(len(line) - 1):
            cur_word = line[i + 1]
            pre_word = line[i]
            if cur_word not in two_gram_dic.keys():
                two_gram_dic[cur_word] = {}
            if pre_word not in two_gram_dic[cur_word]:
                two_gram_dic[cur_word][pre_word] = 1
            else:
                two_gram_dic[cur_word][pre_word] += 1

    two_gram_dic = {i: two_gram_dic[i] for i in sorted(two_gram_dic)}
    for word in two_gram_dic:
        two_gram_dic[word] = {i: two_gram_dic[word][i] for i in sorted(two_gram_dic[word])}
    dic_file = open(dic_path, 'w')
    for word in two_gram_dic:
        write_line = word + ' '
        for p_word in two_gram_dic[word]:
            write_line += p_word + ' ' + str(two_gram_dic[word][p_word]) + ' '
        write_line += '\n'
        dic_file.write(write_line)


def load_dic(dic_path):
    dic_file = open(dic_path, 'r')
    dic_lines = dic_file.readlines()
    two_gram_dic = {}
    for line in dic_lines:
        temp = line.strip().split()
        two_gram_dic[temp[0]] = {}
        for i in range(int((len(temp) - 1) / 2)):
            two_gram_dic[temp[0]][temp[i * 2 + 1]] = int(temp[i * 2 + 2])

    return two_gram_dic


def load_freq(freq_path):
    freq_file = open(freq_path, 'r', encoding='utf-8')
    freq_lines = freq_file.readlines()
    freq_dic = {}
    for line in freq_lines:
        if line == '\n':
            continue
        freq_dic[line.split()[0]] = int(line.split()[1])
    return freq_dic


def get_dag(sentence, freq_dic):
    dag = {}
    n = len(sentence)
    for k in range(n):
        cur_list = []
        i = k
        frag = sentence[k]
        while i < n and frag in freq_dic:
            if freq_dic[frag] > 0:
                cur_list.append(i)
            i += 1
            frag = sentence[k:i + 1]
        if len(cur_list) == 0:
            cur_list.append(k)
        dag[k] = cur_list
    return dag


def calc_log_pos(pre_word, post_word, post_pre_dic, freq_dic):
    pre_freq = freq_dic.get(pre_word, 0)
    combine_freq = post_pre_dic.get(post_word, {}).get(pre_word, 0)
    return np.log(combine_freq + 1) - np.log(pre_freq + 1)


def dp_on_dag(sentence, dag, dic, freq_dic):
    pos_p_by_pre = {}
    pos_p_by_pre['BOS'] = {}
    for i in dag[3]:
        pos_p_by_pre['BOS'][(3, i + 1)] = calc_log_pos('BOS', sentence[3:i + 1], dic, freq_dic)
    cur_start = 3
    while cur_start < len(sentence) - 3:
        for pre_end in dag[cur_start]:
            pre_word = sentence[cur_start:pre_end + 1]
            all_post_p = {}
            if sentence[pre_end + 1: pre_end + 4] == 'EOS':
                all_post_p['EOS'] = calc_log_pos(pre_word, 'EOS', dic, freq_dic)
            else:
                for post_end in dag[pre_end + 1]:
                    post_word = sentence[pre_end + 1:post_end + 1]
                    all_post_p[(pre_end + 1, post_end + 1)] = calc_log_pos(pre_word, post_word, dic, freq_dic)
            pos_p_by_pre[(cur_start, pre_end + 1)] = all_post_p
        cur_start += 1

    pre_by_post = {}  # 某个词的所有前词
    # print(pos_p_by_pre)
    for pre_word in pos_p_by_pre:
        for post_word in pos_p_by_pre[pre_word]:
            if post_word not in pre_by_post.keys():
                pre_by_post[post_word] = []
            pre_by_post[post_word].append(pre_word)

    all_words = list(pos_p_by_pre.keys())
    all_words.append('EOS')
    route = {}
    for word in all_words:  # 遍历全切分词中的所有词
        if word == 'BOS':
            route[word] = (0.0, 'BOS')
            continue
        pre_words = pre_by_post[word]
        route[word] = max((pos_p_by_pre[pre][word] + route[pre][0], pre) for pre in pre_words)
    return route


def two_gram(src_encoding, src_path, freq_path, dst_path, dic_path):
    src_file = open(src_path, 'r', encoding=src_encoding)
    dst_file = open(dst_path, 'w', encoding='utf-8')
    src_lines = src_file.readlines()

    two_gram_dic = load_dic(dic_path)
    freq_dic = load_freq(freq_path)

    for line in src_lines:
        if line == '\n':
            dst_file.write(line)
            continue
        header = line[:19]
        temp = line[19:].strip()
        sentence = 'BOS' + temp.strip() + 'EOS'
        fully_dag = get_dag(sentence, freq_dic)
        # print(fully_dag)
        # break
        route = dp_on_dag(sentence, fully_dag, two_gram_dic, freq_dic)
        # print(route)
        cur_word = 'EOS'
        frag_sentence = ''
        while cur_word != 'BOS':
            word = route[cur_word][1]
            if word != 'BOS':
                frag_sentence = sentence[word[0]:word[1]] + '/ ' + frag_sentence
            cur_word = word
        frag_sentence = header + '/ ' + frag_sentence + '\n'
        dst_file.write(frag_sentence)


# preprocess('data/data_1/199801_seg&pos.txt')
# two_gram('data/data_1/199801_seg&pos.txt', 'output/data_1/2-gram_dic.txt')
# dic = load_dic('output/data_1/2-gram_dic.txt')
two_gram('gbk', 'data/data_1/199801_sent.txt', 'data/data_1/dic_unigram.txt',
         'output/data_1/two_gram_output.txt', 'output/data_1/2-gram_dic.txt')

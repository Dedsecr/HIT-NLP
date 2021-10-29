
def get_dict(input_path):
    with open(input_path, 'r') as f:
        lines = [l[:-1].split('  ') for l in f.readlines()]
    segs = [l[i] for l in lines for i in range(1, len(l))]
    dic = {}
    for _seg in segs:
        if len(_seg) == 0: continue
        seg, attribute = _seg.split('/')
        if seg not in dic:
            dic[seg] = {}
            dic[seg][attribute] = 1
        elif attribute not in dic[seg]:
            dic[seg][attribute] = 1
        else:
            dic[seg][attribute] = dic[seg][attribute] + 1
    return dic

def print_dict(dic, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for seg in dic.keys():
            for attribute in dic[seg]:
                f.write("{} {} {}\n".format(seg, attribute, dic[seg][attribute]))

if __name__ == '__main__':
    input_path, output_path = 'data_1/199801_seg&pos.txt', 'data_1/dic.txt'
    dic = get_dict(input_path)
    print_dict(dic, output_path)
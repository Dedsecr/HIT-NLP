import os

def get_hash(token):
    return ord(token) & 0x7FFFFFFF

def del_old_file(file):
    if os.path.exists(file):
        os.remove(file)

def post_process(segs):
    now, result_segs = '', []
    for i in range(len(segs)):
        if segs[i].isascii():
            now += segs[i]
        elif len(now) > 0:
            result_segs.append(now)
            now = segs[i]
        else:
            result_segs.append(segs[i])
    if len(now) > 0:
        result_segs.append(now)
    return post_process_1(result_segs)

def post_process_1(segs):
    now, result_segs = '', []
    num = '０１２３４５６７８９'
    for i in range(len(segs)):
        if segs[i] in num:
            now += segs[i]
        elif len(now) > 0:
            result_segs.append(now)
            now = segs[i]
        else:
            result_segs.append(segs[i])
    if len(now) > 0:
        result_segs.append(now)
    return result_segs

## 字母的处理
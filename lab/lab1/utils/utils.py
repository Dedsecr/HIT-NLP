import os

def get_hash(token):
    return ord(token) & 0x7FFFFFFF

def del_old_file(file):
    if os.path.exists(file):
        os.remove(file)
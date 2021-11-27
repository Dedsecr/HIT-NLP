from fmm_bmm import *
from fmm_bmm_old import *
from split_data import *
from utils import *
from trie import *
from dict import *
from evaluation import *

def part_3_1():
    '''
    此节为3.1内容，首先将199801_seg&pos.txt（DATA1_SEG_POS）分为训练集199801_train_pos.txt（DATA1_TRAIN_POS）和测试集199801_test_pos.txt（DATA1_TEST_POS）
    然后将199801_sent.txt分为测试集199801_test_content.txt（DATA1_TEST_CONTENT）
    以上文件都保存在./data/中
    再将199801_train_pos.txt（DATA1_TRAIN_POS）生成词典dic.txt（DATA1_DICT），保存在./output/MM/中
    '''
    split_data()
    dict = Dict(DATA1_TRAIN_POS, MM_DICT)
    dict.get_dict()

    print('Part 3.1 finished')

def part_3_2():
    '''
    此节为3.2内容，mm.MM()函数的参数MM_type为F时是FMM，为B时是BMM
    '''
    mm = MM_OLD(MM_DICT, DATA1_CONTENT)
    
    with open(MM_TIMECOST, 'w', encoding='utf8') as f:
        f.write('Before Optimization:\n')
        time_FMM = mm.MM(MM_type='F', timer=True)
        f.write('\tFMM: time: {:.2f}s\n'.format(time_FMM))
        time_BMM = mm.MM(MM_type='B', timer=True)
        f.write('\tBMM: time: {:.2f}s\n'.format(time_BMM))
    
    print('Part 3.2 finished')

def part_3_3(only_test_data=False):
    '''
    此节为3.3内容，若您未运行3.2节，请先运行3.4节再运行本节，确保./output/MM/中有seg_FMM.txt和seg_BMM.txt
    本节输出为./output/MM/中的score.txt（DATA1_SCORE）
    '''
    test_data = DATA1_SEG_POS if not only_test_data else DATA1_TEST_POS
    with open(MM_SCORE, 'w', encoding='utf8') as f:
        f.write('FMM: ' + str(Evaluation(test_data, MM_FMM)) + '\n')
        f.write('BMM: ' + str(Evaluation(test_data, MM_BMM)) + '\n')
    
    print('Part 3.3 finished')

def part_3_4(only_test_data=False):
    '''
    此节为3.4内容，分别测试3个优化算法，'AVL', 'HASH' 和 'HASH1'，通过改变dict_type参数，可以改变优化算法类型
    mm.MM()函数的参数MM_type为F时是FMM，为B时是BMM
    注意，每个算法会覆盖上一个算法的结果，因此./output/MM/中只会有一对seg_FMM.txt和seg_BMM.txt
    算法的用时会被记录在./output/MM/中的TimeCost.txt（DATA1_TIMECOST）中
    '''
    test_data = DATA1_CONTENT if not only_test_data else DATA1_TEST_CONTENT
    f_timecost = open(MM_TIMECOST, 'a', encoding='utf8')
    f_timecost.write('After Optimization:\n')
    
    # mm = MM(DATA1_DICT, test_data)
    # time_FMM = mm.MM(MM_type='F', dict_type='AVL', timer=True)
    # time_BMM = mm.MM(MM_type='B', dict_type='AVL', timer=True)
    # f_timecost.write('using AVL:\n')
    # f_timecost.write('\tFMM: time: {:.2f}s\n'.format(time_FMM))
    # f_timecost.write('\tBMM: time: {:.2f}s\n'.format(time_BMM))
    
    # mm = MM(DATA1_DICT, test_data)
    # time_FMM = mm.MM(MM_type='F', dict_type='HASH', timer=True)
    # time_BMM = mm.MM(MM_type='B', dict_type='HASH', timer=True)
    # f_timecost.write('using HASH:\n')
    # f_timecost.write('\tFMM: time: {:.2f}s\n'.format(time_FMM))
    # f_timecost.write('\tBMM: time: {:.2f}s\n'.format(time_BMM))

    mm = MM(MM_DICT, test_data)
    time_FMM = mm.MM(MM_type='F', dict_type='HASH1', timer=True)
    time_BMM = mm.MM(MM_type='B', dict_type='HASH1', timer=True)
    f_timecost.write('using HASH1:\n')
    f_timecost.write('\tFMM: time: {:.2f}s\n'.format(time_FMM))
    f_timecost.write('\tBMM: time: {:.2f}s\n'.format(time_BMM))

    f_timecost.close()
    print('Part 3.4 finished')

if __name__ == '__main__':
    """
        请依次运行3.1-3.4节
        注意，不建议您运行3.2节，因为它的运行时间实在太太太太太太长了，可跳过
        注意，若您已经运行了3.2节但没有运行完，请先运行3.4节再运行3.3节，否则会找不到文件
        3.4节运行时间大约为2分钟，分别测试了3个优化算法

        注意，虽然3.1节生成了训练集和测试集，但本代码中默认字典为训练集生成的字典，而测试时使用全文
        若您想用3.4节测试3.1节生成的测试集，则需要将part_3_4和part_3_3的参数only_test_data设置为True
    """
    part_3_1()
    # part_3_2()  ## 不建议您运行3.2节，原因如上
    part_3_4()
    part_3_3()
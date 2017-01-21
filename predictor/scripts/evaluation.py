# coding: utf-8
import random_predictor
from pdb import *

def methodname2exename(method_name):
    ret_name = None
    if method_name == 'random':
        ret_name = 'random_predictor.random_predict'
    return ret_name


def check_result(predict_result, t_dat):
    try:
        predict_result == t_dat['Result']
    except:
        print(t_dat)
        set_trace()
    return predict_result == t_dat['Result']

# 毎回の
def check_round_result(round_checker):
    ret_result = {'num': len(round_checker), '1': 0, '2': 0, '3': 0}
    for round_num, round_result in round_checker.items():
        tmp_result = check_each_round(round_result)
        if tmp_result != 0:
            ret_result[str(tmp_result)] += 1
    return ret_result


# 1, 2, 3等が当たってたら番号、当たってなければ0を返す
def check_each_round(result_arr):
    differ_num = 0
    for each_arr in result_arr:
        for index_num, each_result in each_arr.items():
            if each_result[0] != each_result[1]:
                differ_num += 1
    ret_result = 0 if differ_num > 2 else differ_num + 1
            
    return ret_result

def calc_accuracy(result_dict):
    # calc accuracy
    result_dict['accuracy'] = result_dict['correct_num'] / float(result_dict['data_sum'])

    # round accuracy
    result_dict['round_accuracy'] = (result_dict['round_result']['1'] +
                                     result_dict['round_result']['2'] +
                                     result_dict['round_result']['1']) / float(result_dict['round_result']['num'])
    
    return result_dict

def evaluate(method_name, test_data):
    result_dict = {'data_sum': len(test_data), 'correct_num': 0}
    # for round eval
    round_checker = {}
    for t_dat in test_data:
        round_num = t_dat['Round']
        # extract necessary data
        
        # evaluate given method
        predict_result = eval(methodname2exename(method_name))(t_dat)

        # check answer
        if check_result(predict_result, t_dat):
            result_dict['correct_num'] += 1

        # register round result
        if round_num not in round_checker:
            round_checker[round_num] = []
        round_checker[round_num].append({t_dat['No']: [t_dat['Result'], predict_result]})

    result_dict['round_result'] = check_round_result(round_checker)
    # calc accuracy
    result_dict = calc_accuracy(result_dict)
    
    return result_dict
        
def display_result(test_result):
    for method, result in test_result.items():
        # print method name
        print("{0:<10}:  {1: <10}".format("method".upper(), method.title()))
        # print game prediction info
        print("  {}".format("game prediction".upper()))
        print("\t{0:<10}:{1:>10,d}".format("total".upper(), result['data_sum']))
        print("\t{0:<10}:{1:>10,d}".format("correct".upper(), result['correct_num']))
        print("\t{0:<10}:{1:>10.3f}({2:.0f}%)".format("accuracy".upper(), result['accuracy'], result['accuracy'] * 100))
        
        # print round prediction info
        round_result = result['round_result']
        first = round_result['1']
        second = round_result['2']
        third = round_result['3']
        correct_num = first + second + third
        accuracy = correct_num / float(round_result['num'])
        print("  {}".format("round prediction".upper()))
        print("\t{0:<10}:{1:>10,d}".format("total".upper(), round_result['num']))
        print("\t{0:<10}:{1:>10,d}".format("correct".upper(), correct_num))
        print("\t{0:<10}:{1:>10.3f}({2:.0f}%)".format("accuracy".upper(), accuracy, accuracy * 100))        
        print("\t({0}:{3}, {1}:{4}, {2}:{5})".format("first".upper(),
                                                                             "second".upper(),
                                                                             "third".upper(),
                                                                             first, second, third))

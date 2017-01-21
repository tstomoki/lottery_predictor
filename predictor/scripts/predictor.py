# coding: utf-8
import numpy as np
import pandas as pd
from optparse import OptionParser
from pdb import *
import evaluation

FILE_DELIMITER = "\t"

def check_valid_data(data_dict):
    flag = False
    if len(data_dict.keys()) > 1:
        flag = True
    return flag
    

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def load_data_for_prediction(input_filepath):
    ret_arr = []
    f = open(input_filepath, 'r')
    line = f.readline()
    headers = line.strip().split(FILE_DELIMITER)
    index = 0
    while line:
        line = f.readline()
        data_list = line.strip().split(FILE_DELIMITER)
        # cast int if it can
        elements = [int(elem) if represents_int(elem) else elem for elem in data_list]
        insert_dict = dict(zip(headers, elements))
        if check_valid_data(insert_dict):
            ret_arr.append(insert_dict)
        index += 1
    return ret_arr


# 宝くじ開催回毎に区切る
def get_answer_for_each_round(df):
    uniq_rounds = df.Round.unique()
    set_trace()
    for round_num in sorted(uniq_rounds):
        target_games = df[df['Round'] == round_num]
        if len(target_games.No) == 13:
            answer_num = []
            for no in sorted(target_games.No):
                result_num = target_games[target_games['No'] == no].Result.values[0]
                if not represents_int(result_num):
                    result_num = "*" if result_num != '中止' else '-'
                answer_num.append(str(result_num))
            display_str = ''.join(answer_num)
            print("第%3d回: %s" % (round_num, display_str))
                
        
    

def toto_predict(input_filepath):
    # load data
    data_arr = load_data_for_prediction(input_filepath)

    # split data

    # learn model

    # evaluation
    ## random prediction
    
    # prediction
    test_result = {}
    ## for test
    test_data = data_arr
    test_result['random'] = evaluation.evaluate('random', test_data)
    evaluation.display_result(test_result)
    

if __name__ == '__main__':
    # usage: python predictor/scripts/predictor.py -f data/data20170110.tsv
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      help="input data FILE", type="string", dest="input_filename")
    (options, args) = parser.parse_args()
    toto_predict(options.input_filename)

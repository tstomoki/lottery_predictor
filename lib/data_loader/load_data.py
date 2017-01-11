# coding: utf-8
# this module is utilized for loading the data into mysql
import csv
import MySQLdb
from optparse import OptionParser
from pdb import *

CANCEL_RESULT = 102
HEADER_TYPES = {'Date': 'DATE',
                'Location': 'VARCHAR(32)',
                'Round': 'Int',
                'Home':'VARCHAR(32)',
                'Score':'VARCHAR(32)',
                'Away':'VARCHAR(32)',
                'Result':'Int'}

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def generate_table_create_sql(headers, table_name):
    sql = "create table %s (" % (table_name)
    add_attributes = []
    for header in headers:
        add_attributes.append("%s %s" % (header, HEADER_TYPES[header]))
    sql += ','.join(add_attributes) + ')'
    return sql

def load_data(file_path, table_name):
    conn = MySQLdb.connect(
        user='root',
        passwd='',
        db='toto'
    )
    c = conn.cursor()

    f = open(file_path)
    line = f.readline()
    headers = line.strip().split("\t")

    # テーブル一覧の取得
    c.execute('show tables')
    table_tuple = c.fetchall()
    table_tuple = [element for tupl in table_tuple for element in tupl]
    if (table_tuple is None) or (table_name not in table_tuple):
        print("%sを作成" % (table_name))
        sql = generate_table_create_sql(headers, table_name)
        c.execute(sql)

    sql = 'insert into ' + table_name + ' values (%s, %s, %s, %s, %s, %s, %s)'
    i = 0
    while line:
        line = f.readline()
        insert_list = []
        for index, elem in enumerate(line.strip().split("\t")):
            insert_elem = int(elem) if represents_int(elem) else elem
            insert_list.append(insert_elem)
        try:
            if '中止' in insert_list:
                # 試合が中止だった場合
                insert_list[-1] = CANCEL_RESULT
            elif len(insert_list) != len(HEADER_TYPES.keys()):
                # HEADER_TYPESの数に合わなかった場合
                continue
            c.execute(sql, tuple(insert_list))
        except:
            print("Something happen at %d" % i)
            print(tuple(insert_list))
            print(len(insert_list))
        i += 1
        conn.commit()

if __name__ == '__main__':
    # usage: python lib/data_loader/load_data.py -f data/data20170110.tsv
    parser = OptionParser()
    parser.add_option("-f", "--file",
                      help="input data FILE", type="string", dest="input_filename")
    parser.add_option("-t", "--tname",
                      help="create table name", type="string", dest="table_name", default="test")    
    (options, args) = parser.parse_args()
    load_data(options.input_filename, options.table_name)

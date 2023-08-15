# -*- coding:utf-8 -*-

"""
本文档已经实现：
1、登陆baostock远端服务器
2、下载或更新正在交易的市场数据
3、将已经退市的市场数据存放到ARCHIVE文件夹
"""

import datetime
import os
import shutil

import pandas as pd
import baostock as bs
from queue import Queue
from tqdm import tqdm

from Utils import PARAMETER, BEGIN_DATE, DOWNLOAD_ROWPATH, ARCHIVE_PATH, START_DATE

# d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写
# 指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
FREQUENCY = 'd'  # 此处需根据实际情况修改


# 获取市场最新交易的股票列表
def get_codelist():
    result = bs.query_all_stock(day=str(get_enddate().date())).get_data()
    codelist = []
    for i in result['code']:
        if 'sh.6' in i:
            codelist.append(i)
        elif 'sz.00' in i:
            codelist.append(i)
        elif 'sz.30' in i:
            codelist.append(i)
        else:
            pass

    return codelist


# 获取本次更新的日期
def get_enddate():
    now = datetime.datetime.now()
    if now.hour < 20:
        target_time = now - datetime.timedelta(1)
    else:
        target_time = now

    return target_time


# 选取爬取的参数
def get_para(f):
    if f.isdigit() is True:
        return 1
    elif f == 'd':
        return 0
    else:
        return 2


# 根据爬取的周期，创建对应的地址参数
def get_pathname(f):
    if f.isdigit() is True:
        i = f + 'mins'
    elif f == 'd':
        i = 'days'
    elif f == 'w':
        i = 'weeks'
    else:
        i = 'months'

    return i


# 下载函数
def save_marketdata(queue, path):
    bar = tqdm(range(queue.qsize()))
    while not queue.empty():
        try:
            for _ in bar:
                array = queue.get()
                code = array[0]
                start_date = array[1]
                end_date = str(get_enddate().date())
                bar.set_description('{}正在下载！'.format(code))

                rs = bs.query_history_k_data_plus(code,
                                                  PARAMETER[get_para(FREQUENCY)],
                                                  start_date=start_date, end_date=end_date,
                                                  frequency=FREQUENCY, adjustflag="2")

                if rs.error_code == '0':
                    if start_date != START_DATE:
                        df = pd.read_csv("{}{}.csv".format(path, code), encoding='utf-8')
                        result = pd.concat([df, rs.get_data()], axis=0, ignore_index=True)
                    else:
                        result = rs.get_data()
                    result.to_csv("{}{}.csv".format(path, code), index=False)
                    bar.set_description('{}更新成功！'.format(code))
                else:
                    raise Exception('{} is failed!, error is {},{}'.format(code, rs.error_msg, rs.error_code))
        except Exception as e:
            print(e)
            break


# 构造已有的股票更新时间的文件，并保存
def update_checkfile(path):
    code_list = []
    name = os.listdir(path)
    for i in name:
        if 'csv' in i and 'check_update' not in i:
            code_list.append(i[:9])
        else:
            pass

    last_time = []
    for code in code_list:
        single_df = pd.read_csv('{}{}.csv'.format(path, code), encoding='utf-8')
        last_time.append(single_df['date'].max())

    check_df = pd.DataFrame({'code': code_list, 'last_update': last_time}).sort_values(by='code')
    check_df.to_csv('{}check_update.csv'.format(path), index=False)


# 路径检查，无路径就建立
def path_check(path):
    if os.path.exists(path) is False:
        os.makedirs(path)
    else:
        pass


# 构造队列
def set_queue(path):
    exist_code = set()
    name = os.listdir(path)
    for i in name:
        if 'csv' in i and 'check_update' not in i:
            exist_code.add(i[:9])
        else:
            pass
    row_code = set(get_codelist())
    # 退市股票不再更新,移出目录
    storge_path = ARCHIVE_PATH.format(get_pathname(FREQUENCY))
    path_check(storge_path)
    for i in exist_code - row_code:
        old_path = f'{path}{i}.csv'
        new_path = f'{storge_path}{i}.csv'
        shutil.move(old_path, new_path)
    # 构造队列
    q = Queue()
    for i in row_code:
        if i in row_code & exist_code:  # 更新文件
            single_df = pd.read_csv(f'{path}{i}.csv', encoding='utf-8')
            start_date = single_df['date'].max()
            if start_date is None:
                start_date = BEGIN_DATE
            else:
                pass
        else:
            start_date = BEGIN_DATE
        x = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        t = datetime.datetime.strptime(str(get_enddate().date()), '%Y-%m-%d')
        if x < t:
            time = (x + datetime.timedelta(1)).date()
            q.put([i, str(time)])

    return q


def main():
    file_path = DOWNLOAD_ROWPATH.format(get_pathname(FREQUENCY))
    path_check(file_path)
    lg = bs.login()
    print('登录状态{},返回代码：{}'.format(lg.error_msg, lg.error_code))  # 显示登陆返回信息

    queue = set_queue(file_path)
    if queue.empty():
        print('所有数据已下载完毕')
    else:
        save_marketdata(queue, file_path)

    bs.logout()


if __name__ == '__main__':
    main()

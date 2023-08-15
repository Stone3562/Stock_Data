# coding=utf-8

BEGIN_DATE = '2020-06-30'
START_DATE = '2020-07-01'

# 可根据实际情况改变，将自动创建该地址
DOWNLOAD_ROWPATH = '/Users/stone/Desktop/market_datas/{}_K/'

# 退市公司文件存储地址
ARCHIVE_PATH = '/Users/stone/Desktop/market_datas/archive/{}_K/'


PARAMETER = ['date,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST',
             'date,time,open,high,low,close,volume,amount,adjustflag',
             'date,open,high,low,close,volume,amount,adjustflag,turn,pctChg']
# PARAMETER[i]-->日K线指标：[0],分钟线指标：[1],周月线指标：[2]

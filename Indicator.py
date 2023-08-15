# coding=utf-8
"""
本文档实现的函数有：
1、macd数据处理
2、缠论笔处理
3、元数据表新增变动'change'类目
4、改变元数据表数据结构，并返回新数据表值
"""


def caculate_ema(close, cycle):
    ema = []
    multiplier = 2 / (cycle + 1)
    for i in range(len(close)):
        if i == 0:
            ema.append(close[i])
        else:
            ema.append(close[i] * multiplier + (1 - multiplier) * ema[i - 1])
    return ema


def set_macd(data_frame):
    close = data_frame['close'].values.tolist()

    ema12 = caculate_ema(close, 12)
    ema26 = caculate_ema(close, 26)

    DIF = []
    for i in range(len(close)):
        DIF.append(ema12[i] - ema26[i])

    DEA = caculate_ema(DIF, 9)

    MACD = []
    for i in range(len(close)):
        MACD.append((DIF[i] - DEA[i]) * 2)

    data_frame['DIF'] = DIF
    data_frame['DEA'] = DEA
    data_frame['MACD'] = MACD

    return data_frame


def set_cl(data_frame):
    high = data_frame['high'].to_list()
    low = data_frame['low'].to_list()
    trend = [0] * len(high)  # 上升趋势记为1，下降趋势记为-1
    conclude = [0] * len(high)  # 该根k线非包含记录1，是包含记录0

    # 处理包含
    for i in range(1, len(high)):
        if high[i] > high[i - 1]:
            if low[i] > low[i - 1]:  # 无包含，上升趋势
                trend[i] = 1
                conclude[i] = 1
            else:  # 有包含
                if trend[i - 1] == 1:  # 上升趋势
                    low[i] = low[i - 1]
                    trend[i] = 1
                else:  # 下降趋势
                    high[i] = high[i - 1]
                    trend[i] = -1
        elif high[i] < high[i - 1]:
            if low[i] < low[i - 1]:  # 无包含，下降趋势
                trend[i] = -1
                conclude[i] = 1
            else:  # 有包含
                if trend[i - 1] == 1:  # 上升趋势
                    high[i] = high[i - 1]
                    trend[i] = 1
                else:  # 下降趋势
                    low[i] = low[i - 1]
                    trend[i] = -1
        elif high[i] == high[i - 1]:  # 肯定有包含
            if trend[i - 1] == 1:  # 上升趋势
                high[i] = high[i - 1]
                trend[i] = 1
            else:  # 下降趋势
                low[i] = low[i - 1]
                trend[i] = -1

    # 潜在分型列表，顶分型记为1，底分型记为-1
    potential_fx = [0] * len(trend)
    for i in range(1, len(trend)):  # 识别潜在分型
        ifx = trend[i] - trend[i - 1]
        if ifx == 2:  # 底分型
            potential_fx[i - 1] = -1
        elif ifx == -2:  # 顶分型
            potential_fx[i - 1] = 1
        else:  # 无分型
            pass

    # 识别潜在分型在fx的索引位置，并记录
    potential_fx_index = []
    for i in range(1, len(potential_fx)):
        if potential_fx[i] != 0:
            potential_fx_index.append(i)
        else:
            pass

    # 筛选真正分型的索引位置，并记录
    true_fx_index = []
    start = 0
    for i in range(1, len(potential_fx_index)):
        end = i
        # 判断是否为0，是0，计算对应区间的conclude是否大于3
        if sum(potential_fx[potential_fx_index[start]: potential_fx_index[end] + 1]) == 0:
            # 如果大于3，则确认分型，记录该分型点位，下一个开始即从此开始，否则进入下一个循环
            if sum(conclude[potential_fx_index[start]: potential_fx_index[end] + 1]) > 3:
                true_fx_index.append(potential_fx_index[i])
                start = i
            else:
                pass
        else:
            pass

    # 记录真正分型的值，顶记录高，底记录低
    true_fx_index.insert(0, potential_fx_index[0])
    fx_value = [0] * len(trend)
    for i in true_fx_index:
        if potential_fx[i] == -1:
            fx_value[i] = low[i]
        else:
            fx_value[i] = high[i]

    # 删除掉高点低于低点或低点高于高点的点
    ab = []
    for i in range(1, len(true_fx_index)):
        ab.append(
            [
                [potential_fx[true_fx_index[i - 1]], fx_value[true_fx_index[i - 1]]],
                [potential_fx[true_fx_index[i]], fx_value[true_fx_index[i]]],
                true_fx_index[i - 1],
                true_fx_index[i]
            ]
        )
    for i in ab:
        if i[0][0] > i[1][0] and i[0][1] >= i[1][1] or \
                i[0][0] < i[1][0] and i[0][1] <= i[1][1]:
            pass
        else:
            fx_value[i[2]] = 0
            fx_value[i[3]] = 0

    for i in range(len(fx_value)):
        if fx_value[i] == 0:
            fx_value[i] = None
        else:
            pass

    data_frame['FX'] = fx_value

    return data_frame


def set_change(data_frame):
    close = data_frame['close']
    preclose = data_frame['preclose']
    change = [0]

    for i in range(1, close.count()):
        chg = close[i] - preclose[i]
        change.append(chg)

    data_frame['change'] = change

    return data_frame


def set_indicator(data_frame):
    set_change(data_frame)
    set_macd(data_frame)
    set_cl(data_frame)

    data_frame[['open', 'close', 'low', 'high', 'FX', 'preclose', 'turn', 'pctChg', 'change', 'DIF', 'DEA', 'MACD']] = \
        data_frame[
            ['open', 'close', 'low', 'high', 'FX', 'preclose', 'turn', 'pctChg', 'change', 'DIF', 'DEA', 'MACD']].round(
            decimals=2)

    return data_frame

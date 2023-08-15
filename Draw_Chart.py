# coding=utf-8


import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid
from Indicator import set_indicator

ANA_CODE = 'sz.300133'
ROW_PATH = '/Users/stone/Desktop/market_datas/days_K/'
export_path = '/Users/stone/Desktop/'


def setmarklinedata_chan(data_frame):  # 主图辅助线的画法，需要有起点和终点，两两成组，如需标注数据，则在第一个数据点加入value值
    chan = []
    new_chan = []

    for i in range(data_frame['FX'].count()):
        if data_frame['FX'][i] != 0:
            chan.append([i, data_frame['FX'][i]])
        else:
            pass
    for i in range(1, len(chan)):
        new_chan.append(
            [
                {
                    'xAxis': chan[i - 1][0],
                    'yAxis': chan[i - 1][1]
                },
                {
                    'xAxis': chan[i][0],
                    'yAxis': chan[i][1]
                }
            ]
        )

    return new_chan


def draw_line(data_frame):
    kline = (
        Kline()
        .add_xaxis(data_frame.index.to_list())
        .add_yaxis(
            series_name=f'{ANA_CODE}日线图',
            y_axis=data_frame[['open', 'close', 'low', 'high']].values.tolist(),  # 其组织形式为：open，close，lowest，highest
            xaxis_index=0,
            yaxis_index=0,
            itemstyle_opts=opts.ItemStyleOpts(
                color='#ef232a',
                color0="#14b143",
                border_color="#ef232a",
                border_color0="#14b143",
            ),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值", value_dim='highest'),
                    opts.MarkPointItem(type_="min", name="最小值", value_dim='lowest'),
                ],
                symbol='circle',
                symbol_size=5,
                label_opts=opts.LabelOpts(
                    position='left',
                    distance=50,
                )
            ),
            # 主图加入辅助线的设置之一，具体解析见data的获取(setmarklinedata_chan()函数)
            # markline_opts=opts.MarkLineOpts(
            #     linestyle_opts=opts.LineStyleOpts(
            #         color='blue',
            #     ),
            #     data=setmarklinedata_chan(set_data),
            #     symbol='circle',
            #     symbol_size=3,
            # ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f'{ANA_CODE}日线图', pos_left='5'),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            legend_opts=opts.LegendOpts(
                is_show=False
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                axis_pointer_type='cross'
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    range_start=80,
                    range_end=100,
                    xaxis_index=[0, 0]
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    pos_top="93%",
                    range_start=80,
                    range_end=100,
                    xaxis_index=[0, 1],
                ),
                opts.DataZoomOpts(
                    is_show=False,
                    range_start=80,
                    range_end=100,
                    xaxis_index=[0, 2]
                )
            ],

        )

    )

    chan_line = (
        Line()
        .add_xaxis(data_frame.index.to_list())
        .add_yaxis(
            series_name='chan-line',
            y_axis=data_frame["FX"].values.tolist(),
            is_smooth=False,
            is_connect_nones=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(opacity=1, color='blue'),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=1,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                split_number=3,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(
                is_show=True
            ),
        )
    )

    volume_bar = (
        Bar()
        .add_xaxis(data_frame.index.to_list())
        .add_yaxis(
            series_name="volume",
            y_axis=data_frame["volume"].values.tolist(),
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color='#FDDA0D '
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=1,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                axis_pointer_type='cross'
            ),
        )
    )

    macd_line = (
        Line()
        .add_xaxis(data_frame.index.to_list())
        .add_yaxis(
            series_name='DEA',
            y_axis=data_frame["DEA"].values.tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True,
        )
        .add_yaxis(
            series_name='DIF',
            y_axis=data_frame["DIF"].values.tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True,
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                axis_pointer_type='cross'
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    macd_bar = (
        Bar()
        .add_xaxis(data_frame.index.to_list())
        .add_yaxis(
            series_name='MACD',
            y_axis=data_frame["MACD"].values.tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color='#dcd0ff '
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                axis_pointer_type='cross'
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    overlap_kline_withline = kline.overlap(chan_line)
    overlap_macd = macd_line.overlap(macd_bar)

    grid_chart = (
        Grid(init_opts=opts.InitOpts(width='1386px', height='810px'))
        .add(
            overlap_kline_withline,
            grid_opts=opts.GridOpts(
                pos_left="3%",
                pos_right="1%",
                height="60%"
            ),
        )
        .add(
            overlap_macd,
            grid_opts=opts.GridOpts(
                pos_left="3%",
                pos_right="1%",
                pos_top="72%",
                height="12%"
            ),
        )
        .add(
            volume_bar,
            grid_opts=opts.GridOpts(
                pos_left="3%",
                pos_right="1%",
                pos_top="85%",
                height="8%"
            ),
        )
    )

    return grid_chart


def save_html():
    row_data = pd.read_csv(f'{ROW_PATH}{ANA_CODE}.csv', index_col=0)
    set_data = set_indicator(row_data)
    chart = draw_line(set_data)
    chart.render(f'{export_path}{ANA_CODE}.html')


def main():
    save_html()


if __name__ == '__main__':
    main()

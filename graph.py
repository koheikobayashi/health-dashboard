import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from healthdata import HealthData
import matplotlib.pyplot as plt
import plotly.express as px

# Plotlyのデフォルトテーマをライトモードに設定
pio.templates.default = "plotly_white"

# グラフの設定
MARGIN = dict(l=40, r=20, t=40, b=40)
HEIGHT = 350

MARGIN_FAMILY = dict(l=40, r=20, t=20, b=20)
HEIGHT_FAMILY = 250

data = HealthData()

def today_vital():
    """
    1日の心拍数・呼吸数の推移をプロットする関数
    """
    df = data.get_today_heartrate_respiratory()
    time = df["時間"]
    respiration_rate = df["呼吸数"]
    heart_rate = df["心拍数"]

    # 各データの平均値
    avg_respiration = respiration_rate.mean()
    avg_heart_rate = heart_rate.mean()

    # 図の作成
    fig = go.Figure()

    # 呼吸数のプロット
    fig.add_trace(go.Scatter(
        x=time, y=respiration_rate,
        mode="lines+markers+text",
        name="呼吸数",
        line=dict(color="skyblue", width=4),
        marker=dict(size=8, color="skyblue"),
        text=[f"{int(y)}" if y == respiration_rate.max() else "" for y in respiration_rate],
        textposition="top center",
    ))

    # 心拍数のプロット
    fig.add_trace(go.Scatter(
        x=time, y=heart_rate,
        mode="lines+markers+text",
        name="心拍数",
        line=dict(color="orange", width=4),
        marker=dict(size=8, color="orange"),
        text=[f"{int(y)}" if y == heart_rate.max() else "" for y in heart_rate],
        textposition="top center",
    ))

    # 平均線とラベルの追加
    for avg, color, label in zip(
        [avg_respiration, avg_heart_rate],
        ["skyblue", "orange"],
        ["呼吸数", "心拍数"]
    ):
        fig.add_hline(y=avg, line=dict(color=color, dash="dash"))
        fig.add_annotation(
            xref="paper", y=avg, x=1.02, yanchor="middle",
            text=f"(平均) {avg:.1f}", showarrow=False, font=dict(color=color)
        )

    # レイアウトの設定
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=MARGIN,
        height=HEIGHT,
    )

    return fig

def create_weekly_boxplot(identifier):
    """
    1週間の心拍数・呼吸数のボックスプロットを作成する関数
    """
    df = data.get_weekly_heartrate_respiratory()
    selectbox_key = f"selectbox_{identifier}"

    selected_metric = st.selectbox(
        "",
        options=["呼吸数","心拍数"],
        index=0,
        key=selectbox_key
    )

    columns_mapping = {
        "心拍数": ["心拍数最小値", "心拍数Q1", "心拍数中央値", "心拍数Q3", "心拍数最大値"],
        "呼吸数": ["呼吸数最小値", "呼吸数Q1", "呼吸数中央値", "呼吸数Q3", "呼吸数最大値"]
    }
    selected_columns = columns_mapping[selected_metric]

    # ボックスプロットの作成
    fig = go.Figure()

    for i, date in enumerate(df["日付"]):
        values = df.loc[i, selected_columns]
        fig.add_trace(
            go.Box(
                y=values,
                name=date,
                marker_color="pink" if selected_metric == "心拍数" else "lightblue"
            )
        )

    # レイアウト設定
    fig.update_layout(
        yaxis_title=f"{selected_metric}",
        template="plotly_white",
        showlegend=False,
        margin=MARGIN,
        height=HEIGHT,
    )

    return fig

def sleep_time():
    """
    今日と昨日の睡眠時間と活動時間の比較を横棒グラフで表示する関数
    """
    df = data.get_today_yesterday_sleep_active()

    categories = ["今日","昨日"]
    sleep_hours = [df.at[0, "昨日の睡眠時間"], df.at[0, "本日の睡眠時間"]]
    active_hours = [df.at[0, "昨日の活動時間"], df.at[0, "本日の活動時間"]]

    fig = go.Figure()



    # 活動時間のバー
    fig.add_trace(go.Bar(
        x=active_hours,
        y=categories,
        orientation="h",
        name="活動時間",
        marker=dict(color="orange"),
        text=active_hours,
        textposition="inside",
        textfont=dict(color="white", size=14),
    ))

        # 睡眠時間のバー
    fig.add_trace(go.Bar(
        x=sleep_hours,
        y=categories,
        orientation="h",
        name="睡眠時間",
        marker=dict(color="lightblue"),
        text=sleep_hours,
        textposition="inside",
        textfont=dict(color="white", size=14),
    ))

    # レイアウトの調整
    fig.update_layout(
        xaxis=dict(range=[0, 9], showticklabels=False),
        yaxis=dict(title=""),
        barmode="group",
        height=200,
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False,
    )

    return fig

def sleep_active_area():
    """
    1ヶ月の睡眠時間と活動時間の内訳をエリアチャートで表示する関数
    """

    df = data.get_monthly_sleep_active()
    df["日付_再計算"] = pd.to_datetime(df["日付"],format="%Y-%m-%d").dt.strftime("%-m/%-d")
    dates = df["日付_再計算"]
    sleep_hours = df["睡眠時間"]
    active_hours = df["活動時間"]

    fig = go.Figure()

    # 睡眠時間のエリアチャート
    fig.add_trace(go.Scatter(
        x=dates,
        y=sleep_hours,
        mode='lines',
        name="睡眠時間",
        line=dict(color="skyblue"),
        fill='tozeroy'
    ))

    # 活動時間のエリアチャート
    fig.add_trace(go.Scatter(
        x=dates,
        y=sleep_hours + active_hours,
        mode='lines',
        name="活動時間",
        line=dict(color="orange"),
        fill='tonexty'
    ))

    # レイアウトの設定
    fig.update_layout(
        yaxis_title="時間（h）",
        xaxis=dict(tickformat="%m/%d"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=MARGIN,
        height=HEIGHT,
    )

    return fig

def create_heatmap(df, value_col, title, colorscale, zmax):
    """
    ヒートマップを作成する共通関数
    """
    pivot_table = df.pivot_table(index="週目", columns="曜日", values=value_col, aggfunc="mean")
    pivot_table = pivot_table.loc[::-1]  # 週目の順序を逆にする

    ordered_columns = ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"]
    pivot_table = pivot_table[ordered_columns]

    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale=colorscale,
        zmin=0,
        zmax=zmax,
        hoverongaps=False,
        showscale=False
    ))

    # 各セルに数値を表示
    # text_values = np.where(
    #     np.isnan(pivot_table.values),
    #     "",
    #     pivot_table.values.astype(int)
    # )

    # for i, row in enumerate(text_values):
    #     for j, val in enumerate(row):
    #         if val != "":
    #             fig.add_trace(go.Scatter(
    #                 x=[ordered_columns[j]],
    #                 y=[pivot_table.index[i]],
    #                 text=str(val),
    #                 mode="text",
    #                 textfont=dict(size=12, color="black"),
    #                 showlegend=False,
    #                 hoverinfo="none"
    #             ))

    # レイアウトの調整
    fig.update_layout(
        title=title,
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=MARGIN,
        height=HEIGHT,
    )

    return fig

def create_heatmap_number(df, value_col, title, colorscale, zmax):
    """
    ヒートマップを作成する共通関数
    """
    pivot_table = df.pivot_table(index="週目", columns="曜日", values=value_col, aggfunc="mean")
    pivot_table = pivot_table.loc[::-1]  # 週目の順序を逆にする

    ordered_columns = ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"]
    pivot_table = pivot_table[ordered_columns]

    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale=colorscale,
        zmin=0,
        zmax=zmax,
        hoverongaps=False,
        showscale=False
    ))

    # 各セルに数値を表示
    text_values = np.where(
        np.isnan(pivot_table.values),
        "",
        pivot_table.values.astype(int)
    )

    for i, row in enumerate(text_values):
        for j, val in enumerate(row):
            if val != "":
                fig.add_trace(go.Scatter(
                    x=[ordered_columns[j]],
                    y=[pivot_table.index[i]],
                    text=str(val),
                    mode="text",
                    textfont=dict(size=12, color="black"),
                    showlegend=False,
                    hoverinfo="none"
                ))

    # レイアウトの調整
    fig.update_layout(
        title=title,
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=MARGIN,
        height=HEIGHT,
    )

    return fig

def sleep_heatmap():
    """
    よく眠れている日、そうでない日の可視化をヒートマップで表示する関数
    """
    df = data.month_sleep_roomout_heatmap()
    colorscale = [
        [0, "lightgray"],
        [0.01, "lightblue"],
        [1, "deepskyblue"]
    ]
    fig = create_heatmap(df, "睡眠時間", "週目", colorscale, zmax=500)
    return fig

def fall_down_heatmap():
    """
    転倒検知をヒートマップで表示する関数
    """
    df = data.get_fall_detection_data()
    colorscale = [
        [0, "lightgray"],
        [0.01, "rgb(255,255,204)"],
        [0.5, "rgb(252,141,89)"],
        [1, "rgb(215,48,39)"]
    ]
    fig = create_heatmap_number(df, "転倒検知", "", colorscale, zmax=10)
    return fig

def distance_graph():
    """
    ベッド内・ベッド外の移動距離をプロットする関数
    """
    df = data.get_movement_distance_breakdown()
    time_labels = df["時刻"]
    bed_inside = df["ベッド内移動距離"]
    bed_outside = df["ベッド外移動距離"]

    max_bed_inside = bed_inside.max()
    max_bed_outside = bed_outside.max()

    fig = go.Figure()

    # ベッド内移動距離
    fig.add_trace(go.Scatter(
        x=time_labels, y=bed_inside,
        mode="lines+markers+text",
        name="ベッド内移動距離（cm）",
        line=dict(color="lightblue", width=4),
        marker=dict(size=8, color="lightblue"),
        text=[f"{y/1000:.2f}K" if y == max_bed_inside else "" for y in bed_inside],
        textposition="top center",
    ))

    # ベッド外移動距離
    fig.add_trace(go.Scatter(
        x=time_labels, y=bed_outside,
        mode="lines+markers+text",
        name="ベッド外移動距離（cm）",
        line=dict(color="darkblue", width=4),
        marker=dict(size=8, color="darkblue"),
        text=[f"{y/1000:.2f}K" if y == max_bed_outside else "" for y in bed_outside],
        textposition="top center",
    ))

    # レイアウトの設定
    fig.update_layout(
        yaxis_title="距離（m）",
        yaxis=dict(tickprefix="", tickformat=",", range=[0, 3000]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=MARGIN,
        height=HEIGHT,
    )

    return fig

def room_heatmap():
    """
    入退室数をヒートマップで表示する関数
    """
    df = data.get_weekly_room_entry_exit()
    pivot_table = df.pivot(index="日付_再調整", columns="時刻", values="入退室数")
    pivot_table = pivot_table.loc[::-1]

    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Greys',
        colorbar=dict(title="入退室数"),
        showscale=False
    ))

    # レイアウトの調整
    fig.update_layout(
        xaxis_title="時間(h）",
        xaxis_nticks=24,
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_autorange=True,
        margin=MARGIN,
        height=HEIGHT
    )

    return fig

def anomaly_detect():
    """
    異常検知のログを表示する関数
    """
    df = data.get_alert_log()
    df = df.sort_values(by=["時刻"],ascending=False)
    
    # 行のハイライト
    styled_log_data = df.style.apply(highlight_danger, axis=1)
    
    # ヘッダーのスタイルを設定
    styled_log_data = styled_log_data.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [
                ('background-color', 'orange'),  # ヘッダー背景色
                ('color', 'white'),             # ヘッダーテキスト色
                ('font-size', '16px'),          # フォントサイズ
                ('text-align', 'center')        # テキスト位置
            ]
        }]
    )

    # DataFrameをStreamlitで表示
    st.dataframe(styled_log_data, height=400, width=700, hide_index=True)

def highlight_danger(row):
    """
    危険度が「危険」の場合に行をハイライトする関数
    """
    return ['background-color: lightcoral' if row["危険度"] == "危険" else '' for _ in row]


def heartrate_gauge():
        # データ設定
    current_value = data.get_real_time_heart_rate()
    max_value = 150      # 最大値

    # Plotlyでドーナツ型ゲージを作成
    fig = go.Figure(go.Pie(
        values=[current_value, max_value - current_value],  # 現在値と残りの値
        labels=[f"{current_value}", f"{max_value}"],  # ラベルを表示
        hole=0.7,  # ドーナツ型の中央の大きさ
        textinfo='none',  # テキスト情報を非表示（中心部に大きく表示させるため）
        marker=dict(colors=['pink', 'lightgray'])  # 色設定
    ))

    # 中央のテキスト
    fig.add_trace(go.Scatter(
        x=[0], y=[0],  # 中央の位置
        text=[f"<b>{current_value}</b>"],  # 表示する値
        mode='text',
        textfont=dict(size=40, color='black')  # フォントサイズと色
    ))

    # レイアウト設定
    fig.update_layout(
        showlegend=False,  # 凡例を非表示
        paper_bgcolor='rgba(0,0,0,0)',  # グラフ全体の背景
        plot_bgcolor='rgba(0,0,0,0)',  # プロット領域の背景
        margin=MARGIN_FAMILY,
        height=HEIGHT_FAMILY,
            xaxis=dict(
        showgrid=False,  # グリッドラインを非表示
        zeroline=False,  # ゼロ線を非表示
        visible=False    # 軸自体を非表示
    ),
    yaxis=dict(
        showgrid=False,  # グリッドラインを非表示
        zeroline=False,  # ゼロ線を非表示
        visible=False    # 軸自体を非表示
    ),
    )

    return fig


def sleep_or_active_heatmap():

    df = data.sleep_and_active_heatmap()


    # カテゴリーに対応する色を設定
    category_colors = {
        '就寝': 'blue',       # 青
        '室外': 'orange',     # オレンジ
        '室内': 'lightblue'   # 水色
    }

    # 2. データの前処理
    df['最新の一ヶ月の日付'] = pd.to_datetime(df['最新の一ヶ月の日付'], format="%Y-%m-%d") 
    df = df.sort_values(by='最新の一ヶ月の日付',ascending=False)

    # 日付を文字列に変換（表示のため）
    df['日付_str'] = df['最新の一ヶ月の日付'].dt.strftime("%-m/%-d")

    # ピボットテーブルを作成（行：日付、列：時刻、値：カテゴリー）
    pivot_table = df.pivot(index='日付_str', columns='時刻(hour)', values='カテゴリー')

    # 日付を降順に並べ替え（最新の日付が上になるように）
    pivot_table = pivot_table.iloc[::-1]

    # カテゴリーを数値にマッピング
    category_mapping = {'就寝': 0, '室内': 1, '室外': 2}
    heatmap_data = pivot_table.replace(category_mapping)

    # 3. ヒートマップの作成

    # カスタムカラースケールを定義
    colorscale = ['blue', 'lightblue', 'orange']

    # ヒートマップを作成
    fig = px.imshow(
        heatmap_data,
        labels=dict(x='時刻(hour)', y='日付', color='カテゴリー'),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale=colorscale,
        aspect='auto'
    )

    # カラーバーの設定
    fig.update_coloraxes(
        colorbar=dict(
            tickvals=[0, 1, 2],
            ticktext=['就寝', '室内', '室外']
        ),
        cmin=0,
        cmax=2,
        showscale=False  # カラーバーを非表示にする場合は True を False に変更
    )

    # x軸の設定（時刻を整数表示）
    fig.update_xaxes(
        dtick=1,
        tickmode='linear'
    )

    # y軸の設定
    fig.update_yaxes(
        tickmode='linear'
    )

    # レイアウトの更新
    fig.update_layout(
        xaxis_title='時刻(hour)',
        yaxis_autorange=True,  # y軸を逆順にする
        height=HEIGHT_FAMILY,
        margin=MARGIN_FAMILY
    )

    # 4. 結果の表示
    
    return fig


def sleep_active_chart():
    # サンプルデータを作成
    df= data.past_week_sleep_time()

    df["日付"] = pd.to_datetime(df["最新の一週間分の日付"],format="%Y-%m-%d").dt.strftime("%-m/%-d")

    # 平均値を計算
    avg_blue = df["睡眠時間"].mean()
    avg_orange = df["活動時間（室外時間）"].mean()

    # 図を作成
    fig = go.Figure()

    # 青色のデータ
    fig.add_trace(go.Scatter(
        x=df["日付"],
        y=df["睡眠時間"],
        mode="lines+markers+text",
        name="睡眠時間",
        line=dict(color="skyblue", width=3),
        marker=dict(size=8, color="skyblue"),
        text=[f"{y:.2f}" if y == df["睡眠時間"].max() else "" for y in df["睡眠時間"]],  # 最大値を表示
        textfont=dict(color="skyblue", size=14),
        textposition="top center",
    ))

    # オレンジ色のデータ
    fig.add_trace(go.Scatter(
        x=df["日付"],
        y=df["活動時間（室外時間）"],
        mode="lines+markers+text",
        name="活動時間",
        line=dict(color="orange", width=3),
        marker=dict(size=8, color="orange"),
        text=[f"{y:.2f}" if y == df["活動時間（室外時間）"].max() else "" for y in df["活動時間（室外時間）"]],  # 最大値を表示
        textfont=dict(color="orange", size=14),
        textposition="top center",
    ))

    # 平均線を追加
    fig.add_hline(y=avg_blue, line=dict(color="skyblue", dash="dash"))
    fig.add_hline(y=avg_orange, line=dict(color="orange", dash="dash"))

    # 平均値のラベルを追加
    fig.add_annotation(
        xref="paper", y=avg_blue, x=1.02, yanchor="middle",
        text=f"{avg_blue:.1f}", showarrow=False, font=dict(color="skyblue")
    )
    fig.add_annotation(
        xref="paper", y=avg_orange, x=1.02, yanchor="middle",
        text=f"{avg_orange:.1f}", showarrow=False, font=dict(color="orange")
    )

    # レイアウトを設定
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=200,
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(
        tickmode="array",
        tickvals=df["最新の一週間分の日付"],
        ticktext=df["最新の一週間分の日付"]  # 日付を「9/1, 9/2」形式で表示
        ),
    )

    return fig


def rader_chart():
    # データの定義
    df = data.rader_chart()
    categories = df["カテゴリー"].tolist()  # カテゴリ名
    values = df["スコア"].tolist()  # 各カテゴリの値

    # categories = ["睡眠時間", "活動時間", "睡眠リズム", "バイタルパターン"]  # カテゴリ名
    # values = [4, 3, 5, 4]  # 各カテゴリの値

    # レーダーチャート用のデータを作成
    values += values[:1]  # 閉じるために最初の値を最後に追加
    categories += categories[:1]  # 閉じるために最初のカテゴリ名を最後に追加

    # レーダーチャートを作成
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',  # エリアを塗りつぶす
        name='データ',
        line=dict(color="deepskyblue"),
        fillcolor="rgba(135,206,250,0.5)",  # 半透明の青色
        marker=dict(size=6)  # 点のサイズ
    ))

    # レイアウトを設定
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],  # 値の範囲を0～5に設定
                tickvals=[1, 2, 3, 4, 5],  # ラベルを設定
                tickfont=dict(size=10)  # フォントサイズ
            )
        ),
        showlegend=False,  # 凡例を非表示
        margin=dict(t=40, b=20, l=60, r=50),
        height=HEIGHT_FAMILY,
        paper_bgcolor='rgba(0,0,0,0)',  # グラフ全体の背景
        plot_bgcolor='rgba(0,0,0,0)',  # プロット領域の背景
    )
    return fig


def donut_chart():
    
    df = data.donut_chart()
    # データ定義
    labels = df["カテゴリー"].tolist()
    values = df["外出"].tolist()

    # カラースケール
    colors = ["orange", "darkblue", "limegreen", "skyblue"]

    # ドーナツチャートを作成
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,  # ドーナツチャートの中心穴のサイズ
        marker=dict(colors=colors),
        textinfo='percent+label',  # ラベルとパーセンテージを表示
        textposition='outside',  # ラベルを円の外側に表示
        showlegend=False  # 凡例を非表示
    )])

    # レイアウトの調整
    fig.update_layout(
        margin=MARGIN_FAMILY,
        height=HEIGHT_FAMILY,
        annotations=[
            dict(
                text="",
                x=0.5, y=0.5, font_size=20, showarrow=False  # 中心にテキストを追加
            )
        ],
        paper_bgcolor='rgba(0,0,0,0)',  # グラフ全体の背景
        plot_bgcolor='rgba(0,0,0,0)',  # プロット領域の背景

    )
    return fig


def time_log():

    df = data.record()
    st.dataframe(df, use_container_width=True,hide_index=True,height=550)





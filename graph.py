import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from healthdata import HealthData

# Plotlyのデフォルトテーマをライトモードに設定
pio.templates.default = "plotly_white"

# グラフの共通設定
MARGIN = dict(l=40, r=20, t=40, b=40)
HEIGHT = 350

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
        options=["心拍数", "呼吸数"],
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

    categories = ["昨日", "今日"]
    sleep_hours = [df.at[0, "昨日の睡眠時間"], df.at[0, "本日の睡眠時間"]]
    active_hours = [df.at[0, "昨日の活動時間"], df.at[0, "本日の活動時間"]]

    fig = go.Figure()

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

    # レイアウトの調整
    fig.update_layout(
        xaxis=dict(range=[0, 9], showticklabels=False, title="活動時間(h)"),
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
    dates = df["日付"]
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
    df = data.get_monthly_sleep_active()
    colorscale = [
        [0, "lightgray"],
        [0.01, "lightblue"],
        [1, "deepskyblue"]
    ]
    fig = create_heatmap(df, "睡眠時間", "", colorscale, zmax=10)
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
    fig = create_heatmap(df, "転倒検知", "", colorscale, zmax=10)
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
        margin=MARGIN,
        height=HEIGHT
    )

    return fig

def anomaly_detect():
    """
    異常検知のログを表示する関数
    """
    df = data.get_alert_log()
    styled_log_data = df.style.apply(highlight_danger, axis=1)
    st.dataframe(styled_log_data, height=400, width=700)

def highlight_danger(row):
    """
    危険度が「危険」の場合に行をハイライトする関数
    """
    return ['background-color: lightcoral' if row["危険度"] == "危険" else '' for _ in row]

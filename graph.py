import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st

# Plotlyのデフォルトテーマをライトモードに設定
pio.templates.default = "plotly_white"

def today_vital():
  # サンプルデータ
  time = [f"{hour}:00" for hour in range(1, 24)]
  respiration_rate = np.random.normal(20, 5, 23).clip(10, 30)  # 呼吸数データ
  heart_rate = np.random.normal(80, 15, 23).clip(60, 120)  # 心拍数データ

  # 各データの平均値
  avg_respiration = np.mean(respiration_rate)
  avg_heart_rate = np.mean(heart_rate)

  # 図の作成
  fig = go.Figure()

  # 呼吸数のプロット
  fig.add_trace(go.Scatter(
      x=time, y=respiration_rate,
      mode="lines+markers+text",
      name="呼吸数",
      line=dict(color="skyblue", width=4),
      marker=dict(size=8, color="skyblue"),
      text=[f"{int(y)}" if y == max(respiration_rate) else "" for y in respiration_rate], # 最大値に表示
      textposition="top center",
  ))

  # 心拍数のプロット
  fig.add_trace(go.Scatter(
      x=time, y=heart_rate,
      mode="lines+markers+text",
      name="心拍数",
      line=dict(color="orange", width=4),
      marker=dict(size=8, color="orange"),
      text=[f"{int(y)}" if y == max(heart_rate) else "" for y in heart_rate], # 最大値に表示
      textposition="top center",
  ))

  # 平均線の追加
  fig.add_hline(y=avg_respiration, line=dict(color="skyblue", dash="dash"))
  fig.add_hline(y=avg_heart_rate, line=dict(color="orange", dash="dash"))

  # 平均値のラベル
  fig.add_annotation(
      xref="paper", y=avg_respiration, x=1.02, yanchor="middle",
      text=f"(平均) {avg_respiration:.1f}", showarrow=False, font=dict(color="skyblue")
  )
  fig.add_annotation(
      xref="paper", y=avg_heart_rate, x=1.02, yanchor="middle",
      text=f"(平均) {avg_heart_rate:.1f}", showarrow=False, font=dict(color="orange")
  )

  # レイアウトの設定
  fig.update_layout(
      xaxis=dict(tickmode='linear', tick0=0, dtick=1),
      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
  )

  fig.update_layout(
    font=dict(color="black"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=40, r=40, t=80, b=40),
    height=400, 
  )

  return fig


def box_plot():
  # サンプルデータを生成
  np.random.seed(42)
  dates = ["8/18", "8/19", "8/20", "8/21", "8/22", "8/23"]
  data = {date: np.random.normal(85, 5, 100) for date in dates}

  # ボックスプロットのデータを準備
  fig = go.Figure()

  for date, values in data.items():
      fig.add_trace(go.Box(
          y=values,
          name=date,
          boxpoints=False,  # 外れ値のポイントを非表示
          marker_color='skyblue',  # ボックスの色
          line=dict(color='lightblue')  # ラインの色
      ))

  # レイアウト設定
  fig.update_layout(
      yaxis=dict(range=[65, 100]),  # Y軸の範囲を画像と同様に設定
      showlegend=False
  )

  fig.update_layout(
    font=dict(color="black"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=40, r=40, t=80, b=40),
    height=400, 
  )

  return fig

def distance_graph():

    # サンプルデータ
    time_labels = [f"{hour}:00" for hour in range(24)]  # 0:00から23:00までの時刻
    bed_inside = np.random.uniform(0, 1200, 24)  # ベッド内移動距離のサンプルデータ
    bed_outside = np.random.uniform(0, 3000, 24) # ベッド外移動距離のサンプルデータ

    # 最大値を取得
    max_bed_inside = max(bed_inside)
    max_bed_outside = max(bed_outside)

    # 図の作成
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    fig.update_layout(
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        height=400, 
    )

    return fig

def loom_heatmap():

    # サンプルデータの作成
    dates = pd.date_range("2023-09-01", periods=11).strftime('%m/%d')  # 9月1日から9月11日
    hours = list(range(1, 25))  # 1時から24時

    # ヒートマップの値をランダムに生成
    data = np.random.rand(len(dates), len(hours)) * 100

    # ヒートマップの作成
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=hours,
        y=dates,
        colorscale='Greys',  # カラースケールをグレーに設定
        colorbar=dict(title="値")
    ))

    # レイアウトの調整
    fig.update_layout(
        xaxis_title="時間(h）",
        xaxis_nticks=24,  # x軸を24区切りに
    )

    fig.update_layout(
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        height=400, 
    )
    return fig


def sleep_time():

    data = {
    "カテゴリ": ["昨日", "今日"],
    "睡眠時間": [7.5, 8.5],
    "活動時間": [4.5, 3.3]
    }

    # 横棒グラフを作成
    fig = go.Figure()

    # 睡眠時間のバー
    fig.add_trace(go.Bar(
        x=data["睡眠時間"],
        y=data["カテゴリ"],
        orientation="h",
        name="睡眠時間",
        marker=dict(color="lightblue"),
        text=data["睡眠時間"],  # ラベルを表示
    textposition="inside",  # ラベルを棒グラフの内側に配置
    textfont=dict(color="white", size=14),  # ラベルの色を白に設定
    ))

    # 活動時間のバー
    fig.add_trace(go.Bar(
        x=data["活動時間"],
        y=data["カテゴリ"],
        orientation="h",
        name="活動時間",
        marker=dict(color="orange"),
        text=data["活動時間"],  # ラベルを表示
    textposition="inside",  # ラベルを棒グラフの内側に配置
    textfont=dict(color="white", size=14),  # ラベルの色を白に設定
    ))

    # レイアウトの調整
    fig.update_layout(
        xaxis=dict(range=[0, 9],showticklabels=False,title="活動時間(h)"),  # X軸の範囲を設定
        yaxis=dict(title=""),
        barmode="group",  # 並列表示に設定
        height=200,
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False,  # 凡例を非表示
   
    )

    # 表示
    return fig


def sleep_heatmap():

    # サンプルデータ
    dates = pd.date_range("2023-09-01", periods=30)
    sleep_hours = np.random.uniform(5, 10, len(dates))  # 睡眠時間のサンプルデータ
    active_hours = np.random.uniform(5, 10, len(dates))  # 活動時間のサンプルデータ

    # 図の作成
    fig = go.Figure()

    # 睡眠時間のエリアチャート
    fig.add_trace(go.Scatter(
        x=dates,
        y=sleep_hours,
        mode='lines',
        name="睡眠時間",
        line=dict(color="skyblue"),
        fill='tozeroy'  # Y軸のゼロから塗りつぶし
    ))

    # 活動時間のエリアチャート
    fig.add_trace(go.Scatter(
        x=dates,
        y=sleep_hours + active_hours,
        mode='lines',
        name="活動時間",
        line=dict(color="orange"),
        fill='tonexty'  # 前のトレースから次のY軸まで塗りつぶし
    ))

    # レイアウトの設定
    fig.update_layout(
        yaxis_title="時間（h）",
        xaxis=dict(tickformat="%m/%d"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(t=20, b=20)
    )
    
    fig.update_layout(
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        height=400, 
    )
    # 表示
    return fig

def sleep_heatmap2():

    # サンプルデータの作成
    weeks = ["1w", "2w", "3w", "4w", "5w", "6w"]
    days = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

    # ランダムなデータを生成（ヒートマップの値）
    data = np.random.randint(0, 10, size=(len(weeks), len(days)))

    # ヒートマップの作成
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=days,
        y=weeks,
        colorscale='Blues',  # 青系のカラースケール
        colorbar=dict(title="値")
    ))

    # レイアウトの調整
    fig.update_layout(
        yaxis_title="週",
        xaxis=dict(tickmode="array", tickvals=list(range(len(days))), ticktext=days),
        yaxis=dict(tickmode="array", tickvals=list(range(len(weeks))), ticktext=weeks),
        margin=dict(t=30, b=30, l=30, r=30)
    )

    fig.update_layout(
        font=dict(color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        height=300, 
    )

    # 表示
    return fig

def fall_down():
        # データの準備
    # ヒートマップ用データ
    heatmap_data = pd.DataFrame(
        {
            0: [1, 2, 1, 1, 1, 1],
            1: [1, 1, 1, 2, 1, 1],
            2: [1, 1, 4, 1, 1, 1],
            3: [1, 1, 1, 1, 2, 1],
            4: [1, 1, 1, 1, 7, 1],
            5: [1, 1, 1, 1, 1, 1],
        },
        index=["1w", "2w", "3w", "4w", "5w", "6w"],
    )

    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="YlOrRd",
        labels={"color": "回数"},
    )
    fig.update_layout(
        yaxis_title="週",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig

def anomaly_detect():

    # ログ用データ
    log_data = pd.DataFrame(
        {
            "時刻": [
                "2024/09/30 21:10",
                "2024/09/29 16:27",
                "2024/09/28 05:45",
                "2024/09/27 13:15",
                "2024/09/26 23:50",
                "2024/09/25 08:25",
                "2024/09/24 17:12",
                "2024/09/23 02:05",
                "2024/09/22 14:35",
                "2024/09/21 06:55",
            ],
            "危険度": ["注意", "危険", "注意", "注意", "危険", "危険", "危険", "注意", "注意", "危険"],
            "アラート内容": [
                "頻脈",
                "無呼吸",
                "夜中の移動",
                "頻呼吸",
                "転倒",
                "頻脈",
                "無呼吸",
                "夜中の移動",
                "頻呼吸",
                "転倒",
            ],
            "アラートメッセージ": [
                "心拍数が上昇傾向です。体調を観察してください。",
                "無呼吸が頻発しています。至急医療対応が必要です。",
                "早朝に施設内を移動していました。見守りを強化してください。",
                "呼吸数が通常より高いです。安静にしてください。",
                "就寝前に転倒を検知しました。怪我の確認をお願いします。",
                "心拍数が非常に高いです。緊急対応を行ってください。",
                "複数回の無呼吸を検知しました。医師の診察が必要です。",
                "夜間の移動を検知しました。見守りをお願いします。",
                "呼吸数が増加しています。体調を確認してください。",
                "起床時に転倒を検知しました。対応をお願いします。",
            ],
        }
    )

    styled_log_data = log_data.style.apply(highlight_danger, axis=1)
    st.dataframe(styled_log_data, height=400, width=700)

def highlight_danger(row):
    if row["危険度"] == "危険":
        return ["background-color: lightcoral"] * len(row)
    return [""] * len(row)

        

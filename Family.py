import streamlit as st
import pandas as pd
import graph
import parts
from healthdata import HealthData

# ページの設定
st.set_page_config(page_title="Health Dashboard", page_icon=":bar_chart:", layout="wide")

parts.load_css("assets/styles.css")
col1, col2 = st.columns(2)


with col1:
  with st.container():
    # リアルタイムの心拍数（左）
    parts.display_header("本日のご様子", "#B45470")
    column_1, column_2 = st.columns(2)

    with column_1:
      parts.display_center_text("起床時間")
      parts.display_large_number("8時32分", unit="")

    with column_2:
      parts.display_center_text("活動時間")
      parts.display_large_number("8時32分", unit="")

    column_1, column_2 = st.columns(2)

    with column_1:
      parts.display_center_text("現在の心拍数")
      fig1 = graph.heartrate_gauge()
      st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with column_2:
      parts.display_center_text("本日の行動記録")
      st.title("test")



  with st.container():
    # リアルタイムの呼吸数（右）
    parts.display_header("睡眠、活動時間", "#B45470")
    column_1, column_2 = st.columns(2)

    with column_1:
      parts.display_center_text("就寝時間")
      parts.display_large_number("8時32分", unit="")

    with column_2:
      parts.display_center_text("睡眠時間")
      parts.display_large_number("8時32分", unit="")

    with st.container():
      parts.display_center_text("睡眠時間、室内、室外（就寝：青、室内：水色、室外：オレンジ）")
      fig5 = graph.sleep_heatmap()
      st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

    parts.display_center_text("睡眠時間と活動時間の推移")
    column_1, column_2 = st.columns(2)

    with column_1:
      parts.display_center_text("就寝時間")
      fig1 = graph.today_vital()
      st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with column_2:
      parts.display_center_text("睡眠時間")
      parts.display_large_number("8時32分", unit="")


with col2:
    parts.display_header("本日のご様子", "#B45470")
    parts.display_center_text("睡眠時間と活動時間の推移")
    with st.container():
      column_1, column_2 = st.columns(2)

      with column_1:
        parts.display_center_text("就寝時間")
        fig4 = graph.rader_chart()
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

      with column_2:
        parts.display_large_number("8時32分", unit="")

    parts.display_center_text("睡眠時間と活動時間の推移")
    with st.container():
      column_1, column_2 = st.columns(2)

      with column_1:
        parts.display_center_text("就寝時間")
        fig5 = graph.donut_chart()
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
        

      with column_2:
        parts.display_large_number("8時32分", unit="")

    parts.display_center_text("睡眠時間と活動時間の推移")
    graph.anomaly_detect()
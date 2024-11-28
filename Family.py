import streamlit as st
import pandas as pd
import graph
import parts
from healthdata import HealthData

# データの取得
data = HealthData()

# ダミーデータの取得
today_sleep_time = data.get_today_sleep_time()

# ページの設定
st.set_page_config(page_title="Health Dashboard", page_icon=":bar_chart:", layout="wide")

parts.load_css("assets/styles-family.css")
col1, col2 = st.columns(2)


with col1:
  with st.container():
    # リアルタイムの心拍数（左）
    parts.display_header("本日のご様子", "#EC8177")
    column_1, column_2 = st.columns(2)

    with column_1:
      parts.display_center_text("起床時間")
      parts.display_large_number_family("8時32分", unit="")

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
      st.markdown("""
          <div class="record-container" style="background-color:#FCFFEA;">
              <div class="record">午前8:32分　起床されました。<br>午前9:15分　外出されました。<br>午後4:32分　自室に戻られました。<br>午後9:32分　ベッドに入られました。</div>
          </div>
      """, unsafe_allow_html=True)



  with st.container():
    # リアルタイムの呼吸数（右）
    parts.display_header("睡眠、活動時間", "#24BED4")
    column_1, column_2 = st.columns(2)

    with column_1:
      parts.display_center_text("就寝時間")
      parts.display_large_number(today_sleep_time, unit="")

    with column_2:
      parts.display_center_text("睡眠時間")
      parts.display_large_number("8時32分", unit="")

    with st.container():
      parts.display_center_text("睡眠時間、室内、室外（就寝：青、室内：水色、室外：オレンジ）")
      fig2 = graph.sleep_and_active_heatmap()
      st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    parts.display_center_text("睡眠時間と活動時間の推移")
    column_1, column_2 = st.columns(2)

    with column_1:
      fig3 = graph.sleep_active_chart()
      st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with column_2:
      st.markdown("""
          <div class="record-container" style="background-color:#E8F6FF;">
              <div class="record">午前8:32分　起床されました。<br>午前9:15分　外出されました。<br>午後4:32分　自室に戻られました。<br>午後9:32分　ベッドに入られました。</div>
          </div>
      """, unsafe_allow_html=True)


with col2:
    parts.display_header("今月のご様子", "#FCB917")
    parts.display_center_text("健康スコア")
    with st.container():
      column_1, column_2 = st.columns(2)

      with st.container():
          with column_1:
            fig4 = graph.rader_chart()
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

          with column_2:
              st.markdown("""
                  <div class="record-container" style="background-color:#FFF39A;">
                      <div class="record">午前8:32分　起床されました。<br>午前9:15分　外出されました。<br>午後4:32分　自室に戻られました。<br>午後9:32分　ベッドに入られました。</div>
                  </div>
              """, unsafe_allow_html=True)

    parts.display_center_text("施設内での過ごされ方")
    with st.container():
      column_1, column_2 = st.columns(2)

      with column_1:
        st.markdown("""
            <div class="record-container" style="background-color:#CBF7C4;">
                <div class="record">午前8:32分　起床されました。<br>午前9:15分　外出されました。<br>午後4:32分　自室に戻られました。<br>午後9:32分　ベッドに入られました。</div>
            </div>
        """, unsafe_allow_html=True)
        

      with column_2:
        fig5 = graph.donut_chart()
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

    parts.display_center_text("今月の活動記録")
    fig6 = graph.time_log()
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

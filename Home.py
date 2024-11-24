import streamlit as st
import pandas as pd
import graph
from healthdata import HealthData

# ページの設定
st.set_page_config(page_title="Health Dashboard", page_icon=":bar_chart:", layout="wide")

# カスタムCSSの定義
custom_css = """
<style>
/* 全体の背景色 */
.stMainBlockContainer{
    background-color: #DEDEDE;
}
/* ヘッダーのスタイル */
.styled-header, .styled-header2 {
    text-align: center;
    font-size: 2em;
    font-weight: bold;
    color: white;
    margin-top: 10px;
    margin-bottom: 0;
}

.styled-header2 {
    margin: 10px 10px 0 10px;
}

/* センターテキストのスタイル */
.center-text {
    text-align: center;
    font-size: 0.9em;
    font-weight: bold;
    margin: 10px 5px;
    background-color: white;
}

/* 大きな数値表示のスタイル */
.large-number {
    text-align: center;
    font-size: 3em;
    font-weight: bold;
    margin: 0px 10px;
}

/* 小さなテキストのスタイル */
.small-text {
    font-size: 24px;
    font-weight: normal;
}

/* 割合表示のスタイル */
.percentage-text {
    text-align: center;
    font-size: 1em;
    font-weight: bold;
    color: red;
    margin-top: 0;
}

/* カスタムコンテナ */
.custom-container {
    background-color: #f9f9f9; /* 背景色 */
    border: 1px solid #ddd;   /* 枠線 */
    text-align: center;       /* テキストを中央揃え */
    background-color: white;
    margin: 0 10px;
    padding: 10px;
}

div[data-testid="stVerticalBlockBorderWrapper"]{
    margin: 0px 10px;
}
            
.stVerticalBlock > div[data-testid="stVerticalBlockBorderWrapper"]:last-child {
    background-color: #FAFAFA;
    margin: 0;
}
 
/* カラムのレスポンシブデザイン */
[data-testid="stColumn"] {
    width: calc(33.33% - 1rem) !important;
    flex: 1 1 calc(33.33% - 1rem) !important;
    background-color: #FAFAFA;
}
@media (max-width: 1500px) {
    [data-testid="stColumn"] {
        width: calc(33.33% - 1rem) !important;
    }
}
@media (max-width: 1350px) {
    [data-testid="stColumn"] {
        width: calc(50% - 1rem) !important;
    }
}
@media (max-width: 900px) {
    [data-testid="stColumn"] {
        width: calc(100% - 1rem) !important;
    }
}

/* ツールバーやフッターの非表示 */
#MainMenu, header, footer, div[data-testid="stToolbar"], div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0;
    position: fixed;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ヘッダーを表示する関数
def display_header(title, bg_color):
    st.markdown(f"""
    <div style="background-color: {bg_color};" class="styled-header">{title}</div>
    """, unsafe_allow_html=True)

# センターにテキストを表示する関数
def display_center_text(text):
    st.markdown(f'<div class="center-text">{text}</div>', unsafe_allow_html=True)

# 大きな数値と割合を表示する関数
def display_large_number(number, unit="", percentage=None):
    percentage_text = f'<p class="percentage-text">{percentage}</p>' if percentage else ''
    unit_text = f'<span class="small-text"> {unit}</span>' if unit else ''
    st.markdown(
        f"""
        <div class="custom-container">
            <p class="large-number">{number}{unit_text}</p>
            {percentage_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# データの取得
data = HealthData()

# ダミーデータの取得
real_time_heart_rate = data.get_real_time_heart_rate()
heart_rate_increase_decrease = data.get_heart_rate_change_ratio()

real_time_respiratory_rate = data.get_real_time_respiratory_rate()
respiratory_increase_decrease = data.get_respiratory_rate_change_ratio()

today_wakeup_time = data.get_today_wakeup_time()
today_sleep_time = data.get_today_sleep_time()

today_room = data.get_today_room_entry_exit_count()
today_yesterday_room = data.get_room_entry_exit_change_ratio()

today_move = data.get_today_movement_distance()
today_yesterday_move = data.get_movement_distance_change_ratio()

# 3つのカラムを作成
col1, col2, col3 = st.columns(3)

# ---------------------------
# カラム1：バイタル
# ---------------------------
with col1:
    display_header("バイタル", "#B45470")
    column_1, column_2 = st.columns(2)

    # リアルタイムの心拍数（左）
    with column_1:
        display_center_text("リアルタイムの心拍数")
        display_large_number(real_time_heart_rate, unit="", percentage=f"{heart_rate_increase_decrease * 100:.2f}%")

    # リアルタイムの呼吸数（右）
    with column_2:
        display_center_text("リアルタイムの呼吸数")
        display_large_number(real_time_respiratory_rate, unit="", percentage=f"{respiratory_increase_decrease * 100:.2f}%")

    # グラフの表示
    display_center_text("1日の心拍数・呼吸数の推移")
    fig1 = graph.today_vital()
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    display_center_text("1週間の心拍数・呼吸数の推移")
    with st.container():
        fig2 = graph.create_weekly_boxplot(identifier="boxplot_vital")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ---------------------------
# カラム2：睡眠・活動時間
# ---------------------------
with col2:
    display_header("睡眠・活動時間", "#12728B")
    column_1, column_2 = st.columns(2)

    # 起床時間と就寝時間（左）
    with column_1:
        display_center_text("本日の起床時間")
        display_large_number(today_wakeup_time)
        display_center_text("本日の就寝時間")
        display_large_number(today_sleep_time)

    # 睡眠時間・活動時間のグラフ（右）
    with column_2:
        display_center_text("睡眠時間・活動時間")
        fig3 = graph.sleep_time()
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # グラフの表示
    display_center_text("一ヶ月の睡眠時間と活動時間の内訳")
    fig4 = graph.sleep_active_area()
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    display_center_text("よく眠れている日、そうでない日の可視化")
    fig5 = graph.sleep_heatmap()
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

# ---------------------------
# カラム3：移動距離・入退室
# ---------------------------
with col3:
    display_header("移動距離・入退室", "#0BBCAE")
    column_1, column_2 = st.columns(2)

    # 本日の入退室数（左）
    with column_1:
        display_center_text("本日の入退室数")
        display_large_number(today_room, unit="回", percentage=f"{today_yesterday_room * 100:.2f}%")

    # 本日の移動距離（右）
    with column_2:
        display_center_text("本日の移動距離")
        display_large_number(today_move, unit="m", percentage=f"{today_yesterday_move * 100:.2f}%")

    # グラフの表示
    display_center_text("本日の移動距離の内訳")
    fig6 = graph.distance_graph()
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

    display_center_text("入退室の多い日・時刻")
    fig7 = graph.room_heatmap()
    st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})

# ---------------------------
# 転倒・異常検知
# ---------------------------
st.markdown(f"""
<div style="background-color: #54B45E;" class="styled-header2">転倒・異常検知</div>
""", unsafe_allow_html=True)

# レイアウトを左右2列に分割
col_left, col_right = st.columns(2)

# 左列: 転倒検知ヒートマップ
with col_left:
    display_center_text("転倒検知した日、回数")
    fig8 = graph.fall_down_heatmap()
    st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})

# 右列: 異常検知ログ
with col_right:
    display_center_text("異常検知ログ")
    graph.anomaly_detect()

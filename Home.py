import streamlit as st
import pandas as pd
import graph
import data


# ページの設定
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# カスタムCSSの定義
st.markdown("""
<style>
.stMainBlockContainer{
    background-color: #DEDEDE;
}

/* ヘッダーのスタイル */
.styled-header {
    text-align: center;
    font-size: 2em;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.styled-header2 {
    text-align: center;
    font-size: 2em;
    font-weight: bold;
    color: white;
    margin: 10px 10px 0 10px;
}
            
/* ボトムバーのスタイル */
.bottom-bar {
    height: 10px;
    margin-bottom: 20px;
}

/* センターテキストのスタイル */
.center-text {
    text-align: center;
    font-size: 0.9em;
    font-weight: bold;
    margin-bottom: 10px;
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
            
.custom-container {
    background-color: #f9f9f9; /* 背景色 */
    border: 1px solid #ddd;   /* 枠線 */
    text-align: center;       /* テキストを中央揃え */
    background-color: white;
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
""", unsafe_allow_html=True)

# カスタムCSSを読み込む


# ヘッダーとボトムバーを表示する関数
def display_header(title, bg_color, bar_color):
    st.markdown(f"""
    <div style="background-color: {bg_color};" class="styled-header">{title}</div>
    """, unsafe_allow_html=True)

# センターにテキストを表示する関数
def display_center_text(text):
    st.markdown(f'<div class="center-text">{text}</div>', unsafe_allow_html=True)

# 大きな数値と割合を表示する関数
def display_large_number(number, percentage):
    # st.markdown(f'<p class="large-number">{number}</p>', unsafe_allow_html=True)
    # st.markdown(f'<p class="percentage-text">{percentage}</p>', unsafe_allow_html=True)
    if percentage:
        st.markdown(
            f"""
            <div class="custom-container">
                <p class="large-number">{number}</p>
                <p class="percentage-text">{percentage}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="custom-container">
                <p class="large-number">{number}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------
# メインコンテンツの表示開始
# ---------------------------

# ダミーデータの設定

real_time_heart_rate = data.real_time_heart_rate()

heart_rate_increase_decrease = data.heart_rate_increase_decrease()

real_time_respiratory_rate = data.real_time_respiratory_rate()

respiratory_increase_decrease = data.respiratory_increase_decrease()

today_wakeup_time = data.today_wakeup_time()

today_sleep_time = data.today_sleep_time()

today_room = data.today_room()

today_yesterday_room = data.today_yesterday_room()

today_move = data.today_move()

today_yesterday_move = data.today_yesterday_move()


# 3つのカラムを作成
col1, col2, col3 = st.columns(3)

# ---------------------------
# カラム1：バイタル
# ---------------------------
with col1:
    display_header("バイタル", "#B45470", "#CB899C")
    column_1, column_2 = st.columns(2)

    # リアルタイムの心拍数（左）
    with column_1:
        display_center_text("リアルタイムの心拍数")
        display_large_number(real_time_heart_rate, str(heart_rate_increase_decrease)+"%")

    # リアルタイムの心拍数（右）
    with column_2:
        display_center_text("リアルタイムの呼吸数")
        display_large_number(real_time_respiratory_rate, str(respiratory_increase_decrease)+"%")

    # グラフの表示
    display_center_text("1日の心拍数・呼吸数の推移")
    fig1 = graph.today_vital()
    st.plotly_chart(fig1,use_container_width=True,config={"displayModeBar": False})

    display_center_text("1週間の心拍数・呼吸数の推移")
    with st.container():
        fig2 = graph.box_plot()
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar": False})

# ---------------------------
# カラム2：睡眠・活動時間
# ---------------------------
with col2:
    display_header("睡眠・活動時間", "#12728B", "#72A4A7")
    column_1, column_2 = st.columns(2)

    # 起床時間と就寝時間（左）
    with column_1:
        display_center_text("本日の起床時間")
        display_large_number(today_wakeup_time, "")
        display_center_text("本日の就寝時間")
        display_large_number(today_sleep_time, "")

    # 睡眠時間・活動時間のグラフ（右）
    with column_2:
        display_center_text("睡眠時間・活動時間")
        fig3 = graph.sleep_time()
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar": False})


    # グラフの表示
    display_center_text("一ヶ月の睡眠時間と活動時間の内訳")
    fig4 = graph.sleep_active_area()
    st.plotly_chart(fig4,use_container_width=True,config={"displayModeBar": False})

    display_center_text("よく眠れている日、そうでない日の可視化")
    fig5 = graph.sleep_heatmap()
    st.plotly_chart(fig5,use_container_width=True,config={"displayModeBar": False})

# ---------------------------
# カラム3：移動距離・入退室
# ---------------------------
with col3:
    display_header("移動距離・入退室", "#0BBCAE", "#4BD6C3")
    column_1, column_2 = st.columns(2)

    # 本日の入退室数（左）
    with column_1:
        display_center_text("本日の入退室数")
        display_large_number(f'{today_room}<span class="small-text"> 回</span>', str(today_yesterday_room)+"%")

    # 本日の移動距離（右）
    with column_2:
        display_center_text("本日の移動距離")
        display_large_number(f'{today_move}<span class="small-text"> m</span>', str(today_yesterday_move)+"%")

    # グラフの表示
    display_center_text("本日の移動距離の内訳")
    fig6 = graph.distance_graph()
    st.plotly_chart(fig6,use_container_width=True,config={"displayModeBar": False})

    display_center_text("入退室の多い日・時刻")
    fig7 = graph.room_heatmap()
    st.plotly_chart(fig7,use_container_width=True,config={"displayModeBar": False})




# 転倒・異常検知


with st.container():
    st.markdown(f"""
    <div style="background-color: #54B45E;" class="styled-header2">転倒・異常検知</div>
    """, unsafe_allow_html=True)
    # レイアウトを左右2列に分割
    col1, col2 = st.columns([1, 1])  # 左右の比率を1:1に設定

    # 左列: Plotlyでヒートマップを作成
    with col1:
        display_center_text("転倒検知した日、回数")
        fig7 = graph.fall_down()
        st.plotly_chart(fig7, use_container_width=True,config={"displayModeBar": False})

    # 右列: 異常検知ログを表示
    with col2:
        display_center_text("異常検知ログ")
        # 各行の背景色を危険度で設定
        graph.anomaly_detect()

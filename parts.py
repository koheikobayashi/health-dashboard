import streamlit as st
import pandas as pd
import graph


# ヘッダーを表示する関数
def display_header(title, bg_color):
    st.markdown(f"""
    <div style="background-color: {bg_color};" class="styled-header">{title}</div>
    """, unsafe_allow_html=True)

# 外部CSSファイルを読み込む関数
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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


# 大きな数値と割合を表示する関数
def display_large_number_family(hour, minute, unit):
    st.markdown(
        f"""
        <div class="custom-container">
            <p class="large-number-family">{hour}<span style="font-size:18px;">　{unit}　</span>{minute}<span style="font-size:14px;">　分</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
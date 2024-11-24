import pandas as pd


real_time_df = pd.read_csv("./data/リアルタイムの心拍数・呼吸数.csv")

today_heartrate_respiratory_df = pd.read_csv("./data/1日の心拍数・呼吸数の推移.csv")

week_heartrate_respiratory_df = pd.read_csv("./data/1週間の心拍数・呼吸数の最大値・最小値.csv")


# リアルタイムの心拍数
def real_time_heart_rate():
    return real_time_df.at[0, "リアルタイムの心拍数"]


# 昨日の心拍数との比較
def heart_rate_increase_decrease():
    return round(real_time_df.at[0, "リアルタイムの心拍数"] / real_time_df.at[0, "昨日の心拍数の平均"],2)


# リアルタイムの呼吸数
def real_time_respiratory_rate():
    return real_time_df.at[0, "リアルタイムの呼吸数"]


# 昨日の呼吸数との比較
def respiratory_increase_decrease():
    return round(real_time_df.at[0, "リアルタイムの呼吸数"] / real_time_df.at[0, "昨日の呼吸数の平均"],2)


# 一日の心拍数の最大値、最小値
def today_heartrate_respiratory():
    return today_heartrate_respiratory_df


# 1週間の心拍数・呼吸数の最大値・最小値
def week_heartrate_respiratory():
    return week_heartrate_respiratory_df
import pandas as pd


#　ダミーデータインポート
real_time_df = pd.read_csv("./data/リアルタイムの心拍数・呼吸数.csv")

today_heartrate_respiratory_df = pd.read_csv("./data/1日の心拍数・呼吸数の推移.csv")

week_heartrate_respiratory_df = pd.read_csv("./data/1週間の心拍数・呼吸数の最大値・最小値.csv")

heartrate_respiratory_df = pd.read_csv("./data/1週間の心拍数・呼吸数の最大値・最小値.csv")

today_sleep_active_time_df = pd.read_csv("./data/本日・昨日の睡眠・活動時間.csv")

month_sleep_active_time_df = pd.read_csv("./data/一ヶ月の睡眠時間と活動時間の内訳.csv")

today_room_move_df = pd.read_csv("./data/本日の入退室数・移動距離.csv")

bet_in_out_distance_df = pd.read_csv("./data/本日の移動距離の内訳.csv")

week_room_in_out_df = pd.read_csv("./data/入退室の多い日・時刻.csv")

fall_down_df = pd.read_csv("./data/転倒検知した日、回数.csv")

alert_log_df = pd.read_csv("./data/異常検知ログ.csv")

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


# 本日の起床時間
def today_wakeup_time():
    return today_sleep_active_time_df.at[0, "本日の起床時間"]


# 本日の就寝時間
def today_sleep_time():
    return today_sleep_active_time_df.at[0, "本日の就寝時間"]


# 睡眠時間・活動時間
def today_yesterday_sleep_active():
    return today_sleep_active_time_df


# 一ヶ月の睡眠時間と活動時間の内訳
def month_yesterday_sleep_active():
    return month_sleep_active_time_df


# 本日の入退室数
def today_room():
    return today_room_move_df.at[0, "本日の入退室数"]


# 昨日の入退室数
def today_yesterday_room():
    return round(today_room_move_df.at[0, "本日の入退室数"] / today_room_move_df.at[0, "昨日の入退室数"],2)


# 本日の移動距離
def today_move():
    return today_room_move_df.at[0, "本日の移動距離"]


# 昨日の入退室数
def today_yesterday_move():
    return round(today_room_move_df.at[0, "本日の移動距離"] / today_room_move_df.at[0, "昨日の移動距離"],2)


# 今日の移動距離の内訳
def bet_in_out_distance():
    return bet_in_out_distance_df


# 入退室の多い日・時刻
def week_room_in_out():
    week_room_in_out_df["日付_再調整"] = pd.to_datetime(week_room_in_out_df["日付"]).dt.strftime("%-m月%d日")
    return week_room_in_out_df


# 転倒検知した日、回数
def fall_down():
    return fall_down_df


# 異常検知ログ
def alert_log():
    return alert_log_df
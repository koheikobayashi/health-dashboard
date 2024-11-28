import pandas as pd
import os

class HealthData:
    def __init__(self):
        # データディレクトリのパスを設定
        data_dir = os.path.join('.', 'data')
        
        # ダミーデータのインポート（エンコーディングを指定）
        self.real_time_df = pd.read_csv(
            os.path.join(data_dir, "realtime.csv"), encoding='utf-8-sig'
        )
        self.today_heartrate_respiratory_df = pd.read_csv(
            os.path.join(data_dir, "todayheart.csv"), encoding='utf-8-sig'
        )
        self.week_heartrate_respiratory_df = pd.read_csv(
            os.path.join(data_dir, "todayheartmax.csv"), encoding='utf-8-sig'
        )
        self.today_sleep_active_time_df = pd.read_csv(
            os.path.join(data_dir, "active.csv"), encoding='utf-8-sig'
        )
        self.month_sleep_active_time_df = pd.read_csv(
            os.path.join(data_dir, "week_sleep.csv"), encoding='utf-8-sig'
        )
        self.today_room_move_df = pd.read_csv(
            os.path.join(data_dir, "move.csv"), encoding='utf-8-sig'
        )
        self.bet_in_out_distance_df = pd.read_csv(
            os.path.join(data_dir, "todaymove.csv"), encoding='utf-8-sig'
        )
        self.week_room_in_out_df = pd.read_csv(
            os.path.join(data_dir, "room.csv"), encoding='utf-8-sig'
        )
        self.fall_down_df = pd.read_csv(
            os.path.join(data_dir, "fall.csv"), encoding='utf-8-sig'
        )
        self.alert_log_df = pd.read_csv(
            os.path.join(data_dir, "log.csv"), encoding='utf-8-sig'
        )
        self.today_move_log_df = pd.read_csv(
            os.path.join(data_dir, "today_move_log.csv"), encoding='utf-8-sig'
        )
        self.vital_pattern_df = pd.read_csv(
            os.path.join(data_dir, "vitalpattern.csv"), encoding='utf-8-sig'
        )
        self.health_score_df = pd.read_csv(
            os.path.join(data_dir, "vitalpattern.csv"), encoding='utf-8-sig'
        )
        self.live_log_df = pd.read_csv(
            os.path.join(data_dir, "vitalpattern.csv"), encoding='utf-8-sig'
        )
        self.family_sleep_active_time_df = pd.read_csv(
            os.path.join(data_dir, "family_sleep_active_time.csv"), encoding='utf-8-sig'
        )
        self.record_df = pd.read_csv(
            os.path.join(data_dir, "record.csv"), encoding='utf-8-sig'
        )
        self.sleep_and_active_heatmap_df = pd.read_csv(
            os.path.join(data_dir, "sleep-active-heatmap.csv"), encoding='utf-8-sig'
        )
        self.past_week_sleep_time_df = pd.read_csv(
            os.path.join(data_dir, "past-week-sleep-time.csv"), encoding='utf-8-sig'
        )
        self.rader_chart_df = pd.read_csv(
            os.path.join(data_dir, "rader-chart.csv"), encoding='utf-8-sig'
        )
        self.donut_chart_df = pd.read_csv(
            os.path.join(data_dir, "donut-chart.csv"), encoding='utf-8-sig'
        )
        self.today_wakeup_active_time_df = pd.read_csv(
            os.path.join(data_dir, "today-wakeup-active-time.csv"), encoding='utf-8-sig'
        )
        self.staff_vital_df = pd.read_csv(
            os.path.join(data_dir, "staff-vital.csv"), encoding='utf-8-sig'
        )

    

    # リアルタイムの心拍数を取得
    def get_real_time_heart_rate(self):
        return self.real_time_df.at[0, "リアルタイムの心拍数"]

    # 昨日の心拍数との比較（増減率）
    def get_heart_rate_change_ratio(self):
        return round(
            self.real_time_df.at[0, "リアルタイムの心拍数"] /
            self.real_time_df.at[0, "昨日の心拍数の平均"],
            2,
        )

    # リアルタイムの呼吸数を取得
    def get_real_time_respiratory_rate(self):
        return self.real_time_df.at[0, "リアルタイムの呼吸数"]

    # 昨日の呼吸数との比較（増減率）
    def get_respiratory_rate_change_ratio(self):
        return round(
            self.real_time_df.at[0, "リアルタイムの呼吸数"] /
            self.real_time_df.at[0, "昨日の呼吸数の平均"],
            2,
        )

    # 一日の心拍数と呼吸数の推移データを取得
    def get_today_heartrate_respiratory(self):
        return self.today_heartrate_respiratory_df.copy()

    # 1週間の心拍数・呼吸数の最大値・最小値データを取得
    def get_weekly_heartrate_respiratory(self):
        return self.week_heartrate_respiratory_df.copy()

    # 本日の起床時間を取得
    def get_today_wakeup_time(self):
        return self.today_sleep_active_time_df.at[0, "本日の起床時間"]

    # 本日の就寝時間を取得
    def get_today_sleep_time(self):
        return self.today_sleep_active_time_df.at[0, "本日の就寝時間"]

    # 本日と昨日の睡眠時間・活動時間データを取得
    def get_today_yesterday_sleep_active(self):
        return self.today_sleep_active_time_df.copy()

    # 一ヶ月の睡眠時間と活動時間の内訳データを取得
    def get_monthly_sleep_active(self):
        return self.month_sleep_active_time_df.copy()

    # 本日の入退室数を取得
    def get_today_room_entry_exit_count(self):
        return self.today_room_move_df.at[0, "本日の入退室数"]

    # 昨日の入退室数との比較（増減率）
    def get_room_entry_exit_change_ratio(self):
        return round(
            self.today_room_move_df.at[0, "本日の入退室数"] /
            self.today_room_move_df.at[0, "昨日の入退室数"],
            2,
        )

    # 本日の移動距離を取得
    def get_today_movement_distance(self):
        return self.today_room_move_df.at[0, "本日の移動距離"]

    # 昨日の移動距離との比較（増減率）
    def get_movement_distance_change_ratio(self):
        return round(
            self.today_room_move_df.at[0, "本日の移動距離"] /
            self.today_room_move_df.at[0, "昨日の移動距離"],
            2,
        )

    # 本日の移動距離の内訳データを取得
    def get_movement_distance_breakdown(self):
        return self.bet_in_out_distance_df.copy()

    # 入退室の多い日・時刻データを取得
    def get_weekly_room_entry_exit(self):
        df = self.week_room_in_out_df.copy()
        df["日付"] = pd.to_datetime(df["日付"])
        df["日付_再調整"] = df["日付"].apply(lambda x: f"{x.month}月{x.day}日")
        return df

    # 転倒検知した日、回数データを取得
    def get_fall_detection_data(self):
        return self.fall_down_df.copy()

    # 異常検知ログデータを取得
    def get_alert_log(self):
        return self.alert_log_df.copy()

    # 本日の行動記録
    def today_move_log(self):
        return self.today_move_log_df.at[0, "テキスト"]
    
    # バイタルパターンのテキスト
    def vital_pattern_log(self):
        return self.vital_pattern_df.at[0, "テキスト"]

    # 健康スコアのテキスト
    def health_score_log(self):
        return self.health_score_df.at[0, "テキスト"]
    
    # 施設で過ごされ方のテキスト
    def live_log(self):
        return self.live_log_df.at[0, "テキスト"]
    
    # 今日の活動時間
    def family_active_time(self):
        return self.family_sleep_active_time_df.at[0, "今日の活動時間"]

    # 今日の睡眠時間
    def family_sleep_time(self):
        return self.family_sleep_active_time_df.at[0, "今日の睡眠時間"]
    
    # 施設での過ごされ方のレコード
    def record(self):
        return self.record_df
    
    # 睡眠時間、室内、室外
    def sleep_and_active_heatmap(self):
        return self.sleep_and_active_heatmap_df
    
    # 睡眠時間と活動時間の推移
    def past_week_sleep_time(self):
        return self.past_week_sleep_time_df
    
    # レーダーチャート
    def rader_chart(self):
        return self.rader_chart_df
    
    # ドーナツチャート
    def donut_chart(self):
        return self.donut_chart_df
    
    # 起床時間、活動時間
    def today_wakeup_active_time(self):
        return self.today_wakeup_active_time_df
    
    # スタッフ用ページのバイタルデータ
    def staff_vital(self):
        return self.staff_vital_df
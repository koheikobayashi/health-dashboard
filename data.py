import pandas as pd

def real_time_heart_rate():
    real_time_df = pd.read_csv("./data/リアルタイムの心拍数・呼吸数.csv")
    return real_time_df.at[0, "心拍数"]
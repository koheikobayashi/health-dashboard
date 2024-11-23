# 環境
macOS Venture 13.7.1
Python 3.9.19


# 手順
cd health-dashboard
python -m venv health-dashboard
（Macの場合）source health-dashboard/bin/activate
（Windowsの場合）health-dashboard\Scripts\activate
pip install -r requirements.txt
streamlit run Home.py


# セキュリティリスクの件
unsafe_allow_htmlの使用理由
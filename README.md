# 環境
macOS Venture 13.7.1
Python 3.9.19


# 手順
cd health-dashboard
python -m venv health-dashboard
（Macの場合）source health-dashboard/bin/activate
（Windowsの場合）health-dashboard\Scripts\activate
pip install -r requirements.txt
（スタッフの方用ページ表示）streamlit run Staff.py
（ご家族様用ページ表示）streamlit run Family.py


# セキュリティリスクの件
* cssでレスポンシブデザインを設定するとき、streamlitでは他のwebフレームワークのようにHTML内でstyle.cssを読み込むことができず、「st.markdown(custom_css, unsafe_allow_html=True)」のようにスクリプト中でcssを読み込みます。
* その際のオプションで「unsafe_allow_html=True」を設定する必要があるのですが、これを設定するとサニタイズが無効となり、XSSなどのセキュリティリスクが発生します。

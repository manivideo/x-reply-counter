import streamlit as st
from main import count_replies

st.set_page_config(page_title="Xリプライカウンター", layout="centered")
st.title("X（旧Twitter）リプライ数カウントツール")

st.markdown("以下の情報を入力してください：")

username = st.text_input("🔍 検索するアカウント名（@なし）", "")
target_date = st.date_input("📅 検索する日付")
login_id = st.text_input("👤 ログイン用アカウント（メールまたはID）", "")
login_pass = st.text_input("🔑 ログインパスワード", type="password")

if st.button("▶ リプライ数をカウントする"):
    if not username or not login_id or not login_pass:
        st.error("すべての項目を入力してください")
    else:
        with st.spinner("カウント中です…最大2分ほどかかります"):
            count = count_replies(username, target_date.strftime("%Y-%m-%d"), login_id, login_pass)
            st.success(f"{target_date} の @{username} のリプライ数は {count} 件です。")

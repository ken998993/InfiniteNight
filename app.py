import streamlit as st
import os
import shutil

# -----------------------------------------------------------------------------
# 頁面配置 (全螢幕遊戲視窗)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="無限之夜 Infinite Night - 網頁版",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 尋找 Web 導出檔案來源 (優先使用 InfiniteNight-1.0-dists/InfiniteNight-1.0-web)
candidate_source_dirs = [
    os.path.join(BASE_DIR, "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web"),
    os.path.join(BASE_DIR, "..", "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web"),
    os.path.join(BASE_DIR, "web"),
    os.path.join(BASE_DIR, "InfiniteNight-1.0-web")
]

source_web_dir = next((d for d in candidate_source_dirs if os.path.exists(os.path.join(d, "index.html"))), None)

# 自動將導出檔案同步至 static/ 目錄，啟用 Streamlit 內部靜態伺服器 (免 127.0.0.1 端口)
if source_web_dir:
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR, exist_ok=True)
    
    # 檢查 static/ 是否已有 index.html，若無或來源更新則同步複製
    target_index = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(target_index) or (os.path.getmtime(os.path.join(source_web_dir, "index.html")) > os.path.getmtime(target_index)):
        try:
            for item in os.listdir(source_web_dir):
                s = os.path.join(source_web_dir, item)
                d = os.path.join(STATIC_DIR, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        except Exception as e:
            st.error(f"靜態檔案同步失敗: {e}")

# 檢查 static 內部是否已就緒
has_game = os.path.exists(os.path.join(STATIC_DIR, "index.html"))

# -----------------------------------------------------------------------------
# 頂部導航與控制面板
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .game-title {
        font-size: 1.6rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #00ffff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

col_t1, col_t2 = st.columns([3, 2])
with col_t1:
    st.markdown('<div class="game-title">🌌 《無限之夜 Infinite Night》 網頁即玩版</div>', unsafe_allow_html=True)
    if has_game:
        st.caption("✅ 採用 Streamlit 內部原生靜態路由 (/app/static/index.html) 載入")
    else:
        st.caption("⚠️ 尋找 Web 導出檔案中...")

with col_t2:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.link_button("🌐 在新分頁全螢幕打開", "/app/static/index.html", use_container_width=True)
    with btn_col2:
        if st.button("🔄 重新載入", use_container_width=True):
            st.rerun()

# -----------------------------------------------------------------------------
# 內嵌 16:9 高畫質遊戲視窗 (使用 Streamlit 內部路徑 app/static/index.html)
# -----------------------------------------------------------------------------
if has_game:
    st.components.v1.iframe(
        src="app/static/index.html",
        width=1280,
        height=750,
        scrolling=False
    )
else:
    st.error("⚠️ 未在 `InfiniteNight-1.0-dists/InfiniteNight-1.0-web` 中找到 `index.html`！請確認目錄完整性。")

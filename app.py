import streamlit as st
import os
import shutil

# -----------------------------------------------------------------------------
# 頁面配置 (全螢幕純淨遊戲模式)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="無限之夜 Infinite Night",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 注入 CSS：隱藏 Streamlit 所有標題、導航列、頁尾與邊距，實現 100% 純淨全螢幕遊戲畫布
st.markdown("""
<style>
    /* 隱藏 Streamlit 預設頂部 Header、選單按鈕與頁尾 */
    header, footer, #MainMenu, .stDeployButton, [data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* 消除所有頁面邊距，填滿視窗 */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100vw !important;
        margin: 0 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* 讓遊戲 iframe 填滿整個瀏覽器視窗 */
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 尋找 Web 導出檔案來源
candidate_source_dirs = [
    os.path.join(BASE_DIR, "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web"),
    os.path.join(BASE_DIR, "..", "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web"),
    os.path.join(BASE_DIR, "web"),
    os.path.join(BASE_DIR, "InfiniteNight-1.0-web")
]

source_web_dir = next((d for d in candidate_source_dirs if os.path.exists(os.path.join(d, "index.html"))), None)

# 自動同步至 static/ 目錄
if source_web_dir:
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR, exist_ok=True)
    
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
        except:
            pass

# -----------------------------------------------------------------------------
# 直接渲染純淨全螢幕遊戲視窗
# -----------------------------------------------------------------------------
st.components.v1.iframe(
    src="app/static/index.html",
    scrolling=False
)

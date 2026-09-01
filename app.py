import streamlit as st
import os
import sys
import threading
import http.server
import socketserver
import shutil
import time

# -----------------------------------------------------------------------------
# 頁面配置 (全螢幕遊戲視窗)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="無限之夜 Infinite Night - Web 版",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 尋找 Ren'Py Web 導出的檔案目錄
candidate_web_dirs = [
    os.path.join(BASE_DIR, "web"),
    os.path.join(BASE_DIR, "..", "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web"),
    os.path.join(BASE_DIR, "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web"),
    os.path.join(BASE_DIR, "InfiniteNight-1.0-web")
]

WEB_DIR = next((d for d in candidate_web_dirs if os.path.exists(os.path.join(d, "index.html"))), None)

# 如果本地已有導出檔但尚未放到 web/，自動同步複製一份到 web/ 方便 Streamlit Cloud 部署
local_export = os.path.join(BASE_DIR, "..", "InfiniteNight-1.0-dists", "InfiniteNight-1.0-web")
target_web = os.path.join(BASE_DIR, "web")
if os.path.exists(local_export) and not os.path.exists(target_web):
    try:
        shutil.copytree(local_export, target_web)
        WEB_DIR = target_web
    except:
        pass

PORT = 8042

# -----------------------------------------------------------------------------
# 啟動支援 WebAssembly 的本機 HTTP 伺服器 (包含 COOP / COEP 標頭)
# -----------------------------------------------------------------------------
class WasmHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # WebAssembly 與 SharedArrayBuffer 必需之跨域標頭
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        pass  # 靜音存取記錄

@st.cache_resource
def run_background_server(web_directory, port=8042):
    if not web_directory or not os.path.exists(web_directory):
        return False
    try:
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", port), WasmHTTPHandler)
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        return True
    except OSError:
        # 端口已在使用中，代表伺服器已在運行
        return True
    except Exception as e:
        st.error(f"伺服器啟動失敗: {e}")
        return False

# 啟動背景 Web 遊戲服務
if WEB_DIR:
    run_background_server(WEB_DIR, PORT)

# -----------------------------------------------------------------------------
# 頂部導航與控制面板
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, #091224, #1e1b4b);
        padding: 10px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        border: 1px solid #334155;
    }
    .game-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00ffff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

col_t1, col_t2 = st.columns([3, 2])
with col_t1:
    st.markdown('<div class="game-title">🌌 《無限之夜 Infinite Night》 網頁即玩版</div>', unsafe_allow_html=True)
    st.caption("基於 Ren'Py 8.5 WebAssembly / HTML5 引擎構建")

with col_t2:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.link_button("🌐 在新視窗全螢幕打開", f"http://127.0.0.1:{PORT}/index.html", use_container_width=True)
    with btn_col2:
        if st.button("🔄 重新載入遊戲", use_container_width=True):
            st.rerun()

# -----------------------------------------------------------------------------
# 內嵌 16:9 高畫質遊戲視窗
# -----------------------------------------------------------------------------
if WEB_DIR:
    st.components.v1.iframe(
        src=f"http://127.0.0.1:{PORT}/index.html",
        width=1280,
        height=740,
        scrolling=False
    )
else:
    st.error("⚠️ 未找到 Ren'Py Web 導出檔案 (index.html)。請確認 `InfiniteNight-1.0-web` 目錄存在！")
    st.info("若尚未導出 Web 版，可在 Ren'Py SDK 啟動器中點選：【Web (Beta)】➔【Build Web Package】即可自動產生導出包！")

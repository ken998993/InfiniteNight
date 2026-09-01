import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 頁面基本配置 (Cyberpunk / Infinite Night 主題風格)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="無限之夜 Infinite Night - 遊戲數據控制台",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "game", "jsonData")

# 自訂 CSS 樣式
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00ffff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-text {
        color: #8892b0;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 資料載入與儲存輔助函式
# -----------------------------------------------------------------------------
def load_json_file(filename):
    file_path = os.path.join(JSON_DIR, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取 {filename} 失敗: {e}")
            return None
    return None

def save_json_file(filename, data):
    file_path = os.path.join(JSON_DIR, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        st.error(f"儲存 {filename} 失敗: {e}")
        return False

# 載入所有資料庫
items_data = load_json_file("items.json") or {}
bloodlines_data = load_json_file("bloodlines.json") or {}
monsters_data = load_json_file("monsters_db.json") or {}
team_data = load_json_file("team_data.json") or {}
map_nodes = load_json_file("map_nodes.json") or {}
side_quests = load_json_file("side_quests.json") or {}
home_base = load_json_file("home_base_db.json") or {}

# -------------------------------------------------------------
# 側邊欄導航
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌌 無限之夜 控制台")
    st.markdown("---")
    menu = st.radio(
        "選擇管理模組",
        [
            "📊 數據總覽 (Dashboard)",
            "🗡️ 道具與裝備庫 (Items)",
            "🧬 血統與強化庫 (Bloodlines)",
            "🧟 怪物與敵人庫 (Monsters)",
            "👥 輪迴小隊與隊員 (Team & Members)",
            "🗺️ 地圖與任務節點 (Maps & Quests)",
            "⚔️ 數值平衡與戰鬥模擬 (Simulator)"
        ]
    )
    st.markdown("---")
    st.caption("版本: v1.0.0 | 引擎: Ren'Py + Streamlit")

# -------------------------------------------------------------
# 1. 數據總覽 (Dashboard)
# -------------------------------------------------------------
if menu == "📊 數據總覽 (Dashboard)":
    st.markdown('<div class="main-header">📊 遊戲數據核心總覽</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">即時監控主神空間數據庫容量與數值分佈</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🗡️ 道具總數", len(items_data))
    with col2:
        st.metric("🧬 血統總數", len(bloodlines_data))
    with col3:
        st.metric("🧟 怪物種類", len(monsters_data))
    with col4:
        st.metric("👥 輪迴隊員", len(team_data.get("members", [])) if isinstance(team_data, dict) else len(team_data))

    st.markdown("### 📈 數據分佈統計")
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        if items_data:
            categories = [item.get("type", "other") for item in items_data.values()]
            df_cat = pd.DataFrame(categories, columns=["類型"]).value_counts().reset_index()
            df_cat.columns = ["類型", "數量"]
            fig_pie = px.pie(df_cat, values="數量", names="類型", title="道具類型分佈", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)

    with d_col2:
        if bloodlines_data:
            costs = [b.get("cost_points", b.get("cost", 0)) for b in bloodlines_data.values()]
            b_names = list(bloodlines_data.keys())
            df_b = pd.DataFrame({"血統": b_names, "點數需求": costs})
            fig_bar = px.bar(df_b, x="血統", y="點數需求", title="各血統兌換點數", color="點數需求", color_continuous_scale="Viridis")
            st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------------------------------------
# 2. 道具與裝備庫 (Items)
# -------------------------------------------------------------
elif menu == "🗡️ 道具與裝備庫 (Items)":
    st.markdown('<div class="main-header">🗡️ 道具與裝備庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">查詢、篩選、新增或修改主神空間兌換道具</div>', unsafe_allow_html=True)

    if items_data:
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            search_kw = st.text_input("🔍 搜尋道具名稱 / ID / 標籤", "")
        with col_s2:
            all_types = ["全部"] + list(set([item.get("type", "other") for item in items_data.values()]))
            selected_type = st.selectbox("道具類別篩選", all_types)

        filtered_items = {}
        for k, v in items_data.items():
            name = v.get("name", k)
            itype = v.get("type", "other")
            tags = " ".join(v.get("tags", []))
            
            if selected_type != "全部" and itype != selected_type:
                continue
            if search_kw and (search_kw.lower() not in k.lower() and search_kw.lower() not in name.lower() and search_kw.lower() not in tags.lower()):
                continue
            filtered_items[k] = v

        st.caption(f"共找到 {len(filtered_items)} 個道具")

        table_rows = []
        for k, v in filtered_items.items():
            table_rows.append({
                "ID": k,
                "名稱": v.get("name", k),
                "類型": v.get("type", "-"),
                "價格 (點數)": v.get("cost", 0),
                "支線劇情需求": v.get("rank_cost", "-"),
                "描述": v.get("description", "-"),
                "標籤": ", ".join(v.get("tags", []))
            })
        df_items = pd.DataFrame(table_rows)
        st.dataframe(df_items, use_container_width=True, height=450)

        with st.expander("🛠️ 檢視 / 編輯道具詳細數值"):
            edit_id = st.selectbox("選擇要編輯的道具 ID", list(items_data.keys()))
            if edit_id:
                item_obj = items_data[edit_id]
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    e_name = st.text_input("道具名稱", item_obj.get("name", edit_id))
                    e_type = st.text_input("類型 (weapon, equipment, consumable, tactical, material...)", item_obj.get("type", "consumable"))
                    e_cost = st.number_input("獎勵點消耗 (Points)", min_value=0, value=int(item_obj.get("cost", 0)))
                with e_col2:
                    e_rank = st.text_input("支線劇情等級 (如 D, C, B, A, S)", str(item_obj.get("rank_cost", "")))
                    e_desc = st.text_area("道具詳細說明", item_obj.get("description", ""))
                
                if st.button("💾 儲存修改至 items.json"):
                    items_data[edit_id]["name"] = e_name
                    items_data[edit_id]["type"] = e_type
                    items_data[edit_id]["cost"] = e_cost
                    items_data[edit_id]["rank_cost"] = e_rank
                    items_data[edit_id]["description"] = e_desc
                    if save_json_file("items.json", items_data):
                        st.success(f"成功儲存道具 [{edit_id}]！")
                        st.rerun()

# -------------------------------------------------------------
# 3. 血統與強化庫 (Bloodlines)
# -------------------------------------------------------------
elif menu == "🧬 血統與強化庫 (Bloodlines)":
    st.markdown('<div class="main-header">🧬 血統與強化庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">檢視各大強化體系、屬性倍率加成與基因鎖相容性</div>', unsafe_allow_html=True)

    if bloodlines_data:
        b_tabs = st.tabs(list(bloodlines_data.keys()))
        for idx, (b_id, b_info) in enumerate(bloodlines_data.items()):
            with b_tabs[idx]:
                st.subheader(f"🧬 {b_info.get('name', b_id)}")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**兌換消耗**: `{b_info.get('cost_points', b_info.get('cost', 0))} 點數`")
                    st.markdown(f"**支線劇情等級**: `{b_info.get('rank_cost', '無')}`")
                    st.markdown(f"**類別標籤**: `{' / '.join(b_info.get('tags', []))}`")
                with c2:
                    st.markdown(f"**背景描述**:\n\n{b_info.get('description', '無描述')}")

                stats = b_info.get("stat_bonus", b_info.get("stats", {}))
                if stats:
                    st.markdown("#### ⚡ 屬性增益加成")
                    df_stats = pd.DataFrame({"屬性": list(stats.keys()), "加成值": list(stats.values())})
                    fig_stat = px.bar(df_stats, x="屬性", y="加成值", color="加成值", color_continuous_scale="Purples")
                    st.plotly_chart(fig_stat, use_container_width=True)

# -------------------------------------------------------------
# 4. 怪物與敵人庫 (Monsters)
# -------------------------------------------------------------
elif menu == "🧟 怪物與敵人庫 (Monsters)":
    st.markdown('<div class="main-header">🧟 怪物與敵人庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">生化危機、異形等副本怪物的生命、攻擊力與擊殺獎勵</div>', unsafe_allow_html=True)

    if monsters_data:
        df_monsters = pd.DataFrame.from_dict(monsters_data, orient="index")
        st.dataframe(df_monsters, use_container_width=True)
    else:
        st.info("尚未載入或暫無 monsters_db.json 資料。")

# -------------------------------------------------------------
# 5. 輪迴小隊與隊員 (Team & Members)
# -------------------------------------------------------------
elif menu == "👥 輪迴小隊與隊員 (Team & Members)":
    st.markdown('<div class="main-header">👥 輪迴小隊與隊員狀態</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">檢視中洲隊核心成員 (鄭吒、詹嵐、零點等) 的當前能力與基因鎖階段</div>', unsafe_allow_html=True)

    if team_data:
        st.json(team_data)
    else:
        st.info("尚未載入或暫無 team_data.json 資料。")

# -------------------------------------------------------------
# 6. 地圖與任務節點 (Maps & Quests)
# -------------------------------------------------------------
elif menu == "🗺️ 地圖與任務節點 (Maps & Quests)":
    st.markdown('<div class="main-header">🗺️ 關卡地圖與支線任務</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">劇情節點樹、生化危機街道地圖節點與隱藏支線</div>', unsafe_allow_html=True)

    tab_map, tab_quests = st.tabs(["🗺️ 地圖節點 (Map Nodes)", "📜 支線任務 (Side Quests)"])
    with tab_map:
        if map_nodes:
            st.json(map_nodes)
        else:
            st.info("暫無地圖節點資料")
    with tab_quests:
        if side_quests:
            st.json(side_quests)
        else:
            st.info("暫無支線任務資料")

# -------------------------------------------------------------
# 7. 數值平衡與戰鬥模擬 (Simulator)
# -------------------------------------------------------------
elif menu == "⚔️ 數值平衡與戰鬥模擬 (Simulator)":
    st.markdown('<div class="main-header">⚔️ 戰鬥數值平衡模擬器</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">模擬輪迴者裝備不同武器、血統與基因鎖狀態下的輸出 DPS 與生存期望</div>', unsafe_allow_html=True)

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        st.subheader("👤 角色設定")
        base_hp = st.number_input("基礎生命值 (HP)", min_value=50, max_value=5000, value=100)
        base_atk = st.number_input("基礎攻擊力 (ATK)", min_value=1, max_value=500, value=25)
        gene_lock = st.selectbox("基因鎖階段 (Gene Lock)", ["未開啟", "一階 (戰鬥本能 +50% ATK)", "二階 (肉體解放 +100% ATK, +50% HP)", "三階 (思維模擬 +180% ATK)", "四階 (基因微觀掌控 +300% ATK)"])
        crit_rate = st.slider("暴擊機率 (%)", 0, 100, 25) / 100.0
        crit_dmg = st.slider("暴擊傷害倍率", 1.5, 5.0, 2.0)

    with col_sim2:
        st.subheader("🧟 目標敵人設定")
        m_hp = st.number_input("敵人生命值 (HP)", min_value=10, max_value=50000, value=400)
        m_def = st.number_input("敵人防禦減傷 (%)", min_value=0, max_value=90, value=10) / 100.0
        m_atk = st.number_input("敵人攻擊力 (ATK)", min_value=1, max_value=500, value=20)
        m_spd = st.number_input("敵人攻擊間隔 (秒)", min_value=0.5, max_value=5.0, value=1.5)

    lock_multiplier = 1.0
    hp_multiplier = 1.0
    if "一階" in gene_lock:
        lock_multiplier = 1.5
    elif "二階" in gene_lock:
        lock_multiplier = 2.0
        hp_multiplier = 1.5
    elif "三階" in gene_lock:
        lock_multiplier = 2.8
        hp_multiplier = 1.8
    elif "四階" in gene_lock:
        lock_multiplier = 4.0
        hp_multiplier = 2.5

    actual_player_hp = base_hp * hp_multiplier
    expected_atk = (base_atk * lock_multiplier) * (1.0 - crit_rate + crit_rate * crit_dmg) * (1.0 - m_def)
    hits_to_kill_monster = max(1, int(m_hp / expected_atk) + (1 if m_hp % expected_atk > 0 else 0))
    time_to_kill_monster = hits_to_kill_monster * 0.4
    
    monster_dps = m_atk / m_spd
    time_player_survives = actual_player_hp / monster_dps

    st.markdown("---")
    st.subheader("📊 模擬運算結果")
    r_col1, r_col2, r_col3, r_col4 = st.columns(4)
    with r_col1:
        st.metric("🔥 期望單擊傷害", f"{expected_atk:.1f}")
    with r_col2:
        st.metric("⏱️ 擊殺怪物所需時間", f"{time_to_kill_monster:.1f} 秒 ({hits_to_kill_monster} 次攻擊)")
    with r_col3:
        st.metric("🛡️ 玩家有效生命值", f"{actual_player_hp:.0f}")
    with r_col4:
        battle_result = "🏆 勝利 (無損/輕微)" if time_to_kill_monster < time_player_survives * 0.5 else ("⚠️ 慘勝 (重創)" if time_to_kill_monster < time_player_survives else "💀 死亡 (滅團)")
        st.metric("⚔️ 戰局預測", battle_result)

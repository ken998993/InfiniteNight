import streamlit as st
import json
import os
from collections import Counter

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

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
# 支援多種常見資料夾路徑 (本地 / Streamlit Cloud / subpath)
possible_json_dirs = [
    os.path.join(BASE_DIR, "game", "jsonData"),
    os.path.join(BASE_DIR, "jsonData"),
    os.path.join(BASE_DIR, "..", "game", "jsonData")
]
JSON_DIR = next((d for d in possible_json_dirs if os.path.exists(d)), os.path.join(BASE_DIR, "game", "jsonData"))

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
    for candidate_dir in possible_json_dirs:
        fp = os.path.join(candidate_dir, filename)
        if os.path.exists(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                st.error(f"讀取 {filename} 失敗: {e}")
                return None
    return None

def save_json_file(filename, data):
    file_path = os.path.join(JSON_DIR, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"儲存 {filename} 失敗: {e}")
        return False

# 載入原始 JSON 並標準化為 List
raw_items = load_json_file("items.json") or {}
items_list = raw_items.get("items", raw_items if isinstance(raw_items, list) else list(raw_items.values()))

raw_bloodlines = load_json_file("bloodlines.json") or {}
bloodlines_list = raw_bloodlines.get("bloodlines", raw_bloodlines if isinstance(raw_bloodlines, list) else list(raw_bloodlines.values()))

raw_monsters = load_json_file("monsters_db.json") or {}
monsters_list = raw_monsters.get("monsters", raw_monsters if isinstance(raw_monsters, list) else list(raw_monsters.values()))

raw_team = load_json_file("team_data.json") or {}
team_list = raw_team.get("members", raw_team if isinstance(raw_team, list) else list(raw_team.values()))

raw_map = load_json_file("map_nodes.json") or {}
map_list = raw_map.get("map_nodes", raw_map if isinstance(raw_map, list) else list(raw_map.values()))

raw_quests = load_json_file("side_quests.json") or {}
quests_list = raw_quests.get("side_quests", raw_quests if isinstance(raw_quests, list) else list(raw_quests.values()))

# -----------------------------------------------------------------------------
# 側邊欄導航
# -----------------------------------------------------------------------------
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
    st.caption("引擎: Ren'Py + Streamlit | 平台: Streamlit Cloud Ready")

# -----------------------------------------------------------------------------
# 1. 數據總覽 (Dashboard)
# -----------------------------------------------------------------------------
if menu == "📊 數據總覽 (Dashboard)":
    st.markdown('<div class="main-header">📊 遊戲數據核心總覽</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">即時監控主神空間數據庫容量與數值分佈</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🗡️ 道具總數", len(items_list))
    with col2:
        st.metric("🧬 血統總數", len(bloodlines_list))
    with col3:
        st.metric("🧟 怪物種類", len(monsters_list))
    with col4:
        st.metric("👥 輪迴隊員", len(team_list))

    st.markdown("### 📈 數據分佈統計")
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        if items_list:
            st.markdown("#### 🗡️ 道具類型分佈")
            cat_counts = Counter([item.get("type", "other") for item in items_list])
            if HAS_PLOTLY and HAS_PANDAS:
                df_cat = pd.DataFrame(list(cat_counts.items()), columns=["類型", "數量"])
                fig_pie = px.pie(df_cat, values="數量", names="類型", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.bar_chart(cat_counts)

    with d_col2:
        if bloodlines_list:
            st.markdown("#### 🧬 血統列表")
            b_names = [b.get("name", b.get("id", "未知")) for b in bloodlines_list]
            st.write(b_names)

# -----------------------------------------------------------------------------
# 2. 道具與裝備庫 (Items)
# -----------------------------------------------------------------------------
elif menu == "🗡️ 道具與裝備庫 (Items)":
    st.markdown('<div class="main-header">🗡️ 道具與裝備庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">查詢、篩選、新增或修改主神空間兌換道具</div>', unsafe_allow_html=True)

    if items_list:
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            search_kw = st.text_input("🔍 搜尋道具名稱 / ID / 標籤", "")
        with col_s2:
            all_types = ["全部"] + sorted(list(set([item.get("type", "other") for item in items_list if isinstance(item, dict)])))
            selected_type = st.selectbox("道具類別篩選", all_types)

        filtered_items = []
        for item in items_list:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id", "")
            name = item.get("name", item_id)
            itype = item.get("type", "other")
            tags = " ".join(item.get("tags", []))
            
            if selected_type != "全部" and itype != selected_type:
                continue
            if search_kw and (search_kw.lower() not in item_id.lower() and search_kw.lower() not in name.lower() and search_kw.lower() not in tags.lower()):
                continue
            filtered_items.append(item)

        st.caption(f"共找到 {len(filtered_items)} 個道具")

        table_rows = []
        for item in filtered_items:
            table_rows.append({
                "ID": item.get("id", "-"),
                "名稱": item.get("name", "-"),
                "類型": item.get("type", "-"),
                "價格 (點數)": item.get("cost_points", item.get("cost", 0)),
                "支線等級": str(item.get("cost_fate_shard", item.get("rank_cost", "-"))),
                "效果值": item.get("effect_val", "-"),
                "說明": item.get("desc", item.get("description", "-")),
                "標籤": ", ".join(item.get("tags", []))
            })
        
        if HAS_PANDAS:
            df_items = pd.DataFrame(table_rows)
            st.dataframe(df_items, use_container_width=True, height=450)
        else:
            st.dataframe(table_rows, use_container_width=True, height=450)

        with st.expander("🛠️ 檢視 / 編輯道具詳細數值"):
            item_map = {item.get("id", f"idx_{i}"): item for i, item in enumerate(items_list)}
            edit_id = st.selectbox("選擇要編輯的道具 ID", list(item_map.keys()))
            if edit_id:
                item_obj = item_map[edit_id]
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    e_name = st.text_input("道具名稱", item_obj.get("name", edit_id))
                    e_type = st.text_input("類型 (weapon, equipment, consumable, tactical, material...)", item_obj.get("type", "consumable"))
                    e_cost = st.number_input("獎勵點消耗 (Points)", min_value=0, value=int(item_obj.get("cost_points", item_obj.get("cost", 0))))
                with e_col2:
                    e_rank = st.text_input("支線劇情等級 (如 D, C, B, A, S)", str(item_obj.get("cost_fate_shard", item_obj.get("rank_cost", ""))))
                    e_desc = st.text_area("道具詳細說明", item_obj.get("desc", item_obj.get("description", "")))
                
                if st.button("💾 儲存修改至 items.json"):
                    item_obj["name"] = e_name
                    item_obj["type"] = e_type
                    if "cost_points" in item_obj:
                        item_obj["cost_points"] = e_cost
                    else:
                        item_obj["cost"] = e_cost
                    if "cost_fate_shard" in item_obj:
                        item_obj["cost_fate_shard"] = e_rank if e_rank else None
                    else:
                        item_obj["rank_cost"] = e_rank
                    item_obj["desc"] = e_desc
                    
                    # 寫回原始結構
                    save_payload = {"items": items_list} if isinstance(raw_items, dict) and "items" in raw_items else items_list
                    if save_json_file("items.json", save_payload):
                        st.success(f"成功儲存道具 [{edit_id}]！")
                        st.rerun()

# -----------------------------------------------------------------------------
# 3. 血統與強化庫 (Bloodlines)
# -----------------------------------------------------------------------------
elif menu == "🧬 血統與強化庫 (Bloodlines)":
    st.markdown('<div class="main-header">🧬 血統與強化庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">檢視各大強化體系、屬性倍率加成與基因鎖相容性</div>', unsafe_allow_html=True)

    if bloodlines_list:
        b_tabs = st.tabs([b.get("name", b.get("id", f"Bloodline {i}")) for i, b in enumerate(bloodlines_list)])
        for idx, b_info in enumerate(bloodlines_list):
            with b_tabs[idx]:
                st.subheader(f"🧬 {b_info.get('name', '未命名血統')}")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**能量屬性**: `{b_info.get('energy_name', '無')}`")
                    st.markdown(f"**類別標籤**: `{' / '.join(b_info.get('tags', []))}`")
                with c2:
                    st.markdown(f"**背景描述**:\n\n{b_info.get('desc', b_info.get('description', '無描述'))}")

                grades = b_info.get("grades", {})
                if grades:
                    st.markdown("#### ⚡ 各階級能力解鎖")
                    for grade_key, grade_val in grades.items():
                        with st.expander(f"⭐ {grade_val.get('name', grade_key)} (點數: {grade_val.get('points', 0)} / 支線: {grade_val.get('fate_shard', '無')})"):
                            st.json(grade_val.get("attributes", {}))
                            st.write("**技能列表:**", grade_val.get("skills", []))

# -----------------------------------------------------------------------------
# 4. 怪物與敵人庫 (Monsters)
# -----------------------------------------------------------------------------
elif menu == "🧟 怪物與敵人庫 (Monsters)":
    st.markdown('<div class="main-header">🧟 怪物與敵人庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">生化危機、異形等副本怪物的生命、攻擊力與擊殺獎勵</div>', unsafe_allow_html=True)

    if monsters_list:
        for m in monsters_list:
            with st.expander(f"🧟 {m.get('name', m.get('id', '未知怪物'))} (EXP: +{m.get('exp_reward', 0)})"):
                st.json(m)
    else:
        st.info("尚未載入或暫無 monsters_db.json 資料。")

# -----------------------------------------------------------------------------
# 5. 輪迴小隊與隊員 (Team & Members)
# -----------------------------------------------------------------------------
elif menu == "👥 輪迴小隊與隊員 (Team & Members)":
    st.markdown('<div class="main-header">👥 輪迴小隊與隊員狀態</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">檢視中洲隊核心成員 (鄭吒、詹嵐、零點等) 的當前能力與基因鎖階段</div>', unsafe_allow_html=True)

    if team_list:
        st.json(team_list)
    else:
        st.info("尚未載入或暫無 team_data.json 資料。")

# -----------------------------------------------------------------------------
# 6. 地圖與任務節點 (Maps & Quests)
# -----------------------------------------------------------------------------
elif menu == "🗺️ 地圖與任務節點 (Maps & Quests)":
    st.markdown('<div class="main-header">🗺️ 關卡地圖與支線任務</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">劇情節點樹、生化危機街道地圖節點與隱藏支線</div>', unsafe_allow_html=True)

    tab_map, tab_quests = st.tabs(["🗺️ 地圖節點 (Map Nodes)", "📜 支線任務 (Side Quests)"])
    with tab_map:
        if map_list:
            st.json(map_list)
        else:
            st.info("暫無地圖節點資料")
    with tab_quests:
        if quests_list:
            st.json(quests_list)
        else:
            st.info("暫無支線任務資料")

# -----------------------------------------------------------------------------
# 7. 數值平衡與戰鬥模擬 (Simulator)
# -----------------------------------------------------------------------------
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

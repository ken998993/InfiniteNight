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
    import plotly.graph_objects as go
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
possible_json_dirs = [
    os.path.join(BASE_DIR, "game", "jsonData"),
    os.path.join(BASE_DIR, "jsonData"),
    os.path.join(BASE_DIR, "..", "game", "jsonData")
]
JSON_DIR = next((d for d in possible_json_dirs if os.path.exists(d)), os.path.join(BASE_DIR, "game", "jsonData"))

# 自訂 Cyberpunk CSS 樣式
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #00ffff, #ff007f, #9b5de5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .sub-text {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 資料載入與多型容錯輔助函式
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

def extract_list(data, preferred_key=None):
    """安全解析可能為 list 或 dict 的 JSON 資料，確保 100% 回傳 list"""
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if preferred_key and preferred_key in data:
            val = data[preferred_key]
            if isinstance(val, list):
                return val
        for k in ["items", "bloodlines", "monsters", "members", "stages", "side_quests", "base_tiers", "data"]:
            if k in data and isinstance(data[k], list):
                return data[k]
        return list(data.values())
    return []

def save_json_file(filename, data):
    file_path = os.path.join(JSON_DIR, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"儲存 {filename} 失敗: {e}")
        return False

# -----------------------------------------------------------------------------
# 載入所有資料庫
# -----------------------------------------------------------------------------
raw_items = load_json_file("items.json")
items_list = extract_list(raw_items, "items")

raw_bloodlines = load_json_file("bloodlines.json")
bloodlines_list = extract_list(raw_bloodlines, "bloodlines")

raw_monsters = load_json_file("monsters_db.json")
monsters_list = extract_list(raw_monsters, "monsters")

raw_team = load_json_file("team_data.json")
team_list = extract_list(raw_team, "members")

raw_reserve = load_json_file("reserve_members.json")
reserve_list = extract_list(raw_reserve, "members")

raw_home_base = load_json_file("home_base_db.json")
base_tiers_list = extract_list(raw_home_base, "base_tiers")

raw_map = load_json_file("map_nodes.json")
map_list = extract_list(raw_map, "stages")

raw_quests = load_json_file("side_quests.json")
quests_list = extract_list(raw_quests, "side_quests")

# -----------------------------------------------------------------------------
# 側邊欄導航
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌌 《無限之夜》主神終端")
    st.caption("Game Master & Balance Studio")
    st.markdown("---")
    menu = st.radio(
        "選擇控制台模組",
        [
            "📊 數據總覽 (Dashboard)",
            "🗡️ 道具與裝備庫 (Items)",
            "🧬 血統與強化庫 (Bloodlines)",
            "🧟 怪物與敵人庫 (Monsters)",
            "👥 輪迴小隊與隊員 (Team & Members)",
            "🏰 主神基地與工坊 (Home Base)",
            "🗺️ 關卡與任務 (Stages & Quests)",
            "⚔️ 數值平衡與戰鬥模擬 (Simulator)"
        ]
    )
    st.markdown("---")
    st.info(f"📂 資料庫路徑:\n`{JSON_DIR}`")
    st.caption("版本: v1.0.0 | Ren'Py 8.5 相容")

# -----------------------------------------------------------------------------
# 1. 數據總覽 (Dashboard)
# -----------------------------------------------------------------------------
if menu == "📊 數據總覽 (Dashboard)":
    st.markdown('<div class="main-header">📊 主神空間數據核心總覽</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">即時監控輪迴世界各模組容量、數值分佈與資料庫健康度</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("🗡️ 道具總數", len(items_list))
    with c2:
        st.metric("🧬 血統強化體系", len(bloodlines_list))
    with c3:
        st.metric("🧟 怪物種類", len(monsters_list))
    with c4:
        st.metric("👥 主隊 / 預備隊員", f"{len(team_list)} / {len(reserve_list)}")
    with c5:
        st.metric("🏰 基地階級數", len(base_tiers_list))

    st.markdown("---")
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        if items_list:
            st.markdown("#### 🗡️ 道具類別數量分佈")
            cat_counts = Counter([item.get("type", "other") for item in items_list if isinstance(item, dict)])
            if HAS_PLOTLY and HAS_PANDAS:
                df_cat = pd.DataFrame(list(cat_counts.items()), columns=["類型", "數量"])
                fig_pie = px.pie(df_cat, values="數量", names="類型", hole=0.4, color_discrete_sequence=px.colors.sequential.Plasma)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.bar_chart(cat_counts)

    with d_col2:
        if monsters_list:
            st.markdown("#### 🧟 怪物 EXP 擊殺獎勵分佈")
            m_exp = {m.get("name", m.get("id", "未知")): m.get("exp_reward", 0) for m in monsters_list if isinstance(m, dict)}
            st.bar_chart(m_exp)

# -----------------------------------------------------------------------------
# 2. 道具與裝備庫 (Items)
# -----------------------------------------------------------------------------
elif menu == "🗡️ 道具與裝備庫 (Items)":
    st.markdown('<div class="main-header">🗡️ 道具與裝備庫管理</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">查詢、篩選、新增或線上修改主神空間兌換道具</div>', unsafe_allow_html=True)

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
            item_map = {item.get("id", f"idx_{i}"): item for i, item in enumerate(items_list) if isinstance(item, dict)}
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
        b_tabs = st.tabs([b.get("name", b.get("id", f"Bloodline {i}")) for i, b in enumerate(bloodlines_list) if isinstance(b, dict)])
        for idx, b_info in enumerate(bloodlines_list):
            if not isinstance(b_info, dict):
                continue
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
                            st.write("**解鎖技能:**", grade_val.get("skills", []))

# -----------------------------------------------------------------------------
# 4. 怪物與敵人庫 (Monsters)
# -----------------------------------------------------------------------------
elif menu == "🧟 怪物與敵人庫 (Monsters)":
    st.markdown('<div class="main-header">🧟 怪物與敵人數據庫</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">生化危機、異形等各世界怪物的戰鬥六圍、技能組與掉落物表</div>', unsafe_allow_html=True)

    if monsters_list:
        for m in monsters_list:
            if isinstance(m, dict):
                with st.expander(f"🧟 {m.get('name', m.get('id', '未知怪物'))} (EXP: +{m.get('exp_reward', 0)})"):
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.write("**基礎屬性:**", m.get("stats", {}))
                    with col_m2:
                        st.write("**掉落物表:**", m.get("drop_table", {}))
                    st.write("**技能組:**", m.get("skills", []))
    else:
        st.info("尚未載入或暫無 monsters_db.json 資料。")

# -----------------------------------------------------------------------------
# 5. 輪迴小隊與隊員 (Team & Members)
# -----------------------------------------------------------------------------
elif menu == "👥 輪迴小隊與隊員 (Team & Members)":
    st.markdown('<div class="main-header">👥 輪迴小隊成員狀態</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">檢視中洲隊核心成員與預備隊員的屬性數值、基因鎖與裝備欄位</div>', unsafe_allow_html=True)

    t_tab1, t_tab2 = st.tabs(["⭐ 中洲核心主隊 (Main Team)", "🎖️ 預備新進成員 (Reserve Pool)"])
    
    with t_tab1:
        if team_list:
            for member in team_list:
                if isinstance(member, dict):
                    with st.expander(f"👤 {member.get('name', '未命名')} - {member.get('role', '隊員')} (HP: {member.get('hp', 0)}/{member.get('max_hp', 0)})"):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.markdown(f"**血統體系**: `{member.get('bloodline', '無')}`")
                            st.markdown(f"**基因鎖階段**: `第 {member.get('gene_lock', 0)} 階`")
                            st.markdown(f"**獎勵點數餘額**: `{member.get('points', 0)}`")
                        with c2:
                            st.markdown(f"**體力 (CON)**: `{member.get('con', 0)}` | **力量 (STR)**: `{member.get('str', 0)}`")
                            st.markdown(f"**敏捷 (SPD)**: `{member.get('spd', 0)}` | **智力 (INT)**: `{member.get('int', 0)}`")
                            st.markdown(f"**精神 (MND)**: `{member.get('mnd', 0)}`")
                        with c3:
                            st.markdown(f"**主手武器**: `{member.get('equipped_main_hand', '無')}`")
                            st.markdown(f"**身體防具**: `{member.get('equipped_torso', '無')}`")
                            st.markdown(f"**狀態**: `{member.get('status', '正常')}`")
        else:
            st.info("暫無主隊成員資料。")

    with t_tab2:
        if reserve_list:
            for member in reserve_list:
                if isinstance(member, dict):
                    with st.expander(f"🎖️ {member.get('name', '新人')} - {member.get('role', '新人')} ({member.get('archetype_ref', '')})"):
                        st.json(member)
        else:
            st.info("暫無預備成員資料。")

# -----------------------------------------------------------------------------
# 6. 主神基地與工坊 (Home Base)
# -----------------------------------------------------------------------------
elif menu == "🏰 主神基地與工坊 (Home Base)":
    st.markdown('<div class="main-header">🏰 主神基地與團隊工坊</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">檢視基地等級、重力修煉槽位與團隊全員光環</div>', unsafe_allow_html=True)

    if base_tiers_list:
        for tier in base_tiers_list:
            if isinstance(tier, dict):
                with st.expander(f"🏰 階級 {tier.get('tier', 1)}: {tier.get('name', '')} (消耗點數: {tier.get('cost_points', 0)} / 支線: {tier.get('cost_shard', '無')})"):
                    st.markdown(f"**最大工坊槽位**: `{tier.get('max_slots', 0)}`")
                    st.markdown(f"**副本回血率**: `{tier.get('hp_mp_regen_rate', 0) * 100}%`")
                    st.markdown(f"**被動光環效果**: `{tier.get('passive_desc', '')}`")
                    st.caption(tier.get('desc', ''))
    else:
        st.info("尚未載入主神基地資料。")

# -----------------------------------------------------------------------------
# 7. 關卡與任務 (Stages & Quests)
# -----------------------------------------------------------------------------
elif menu == "🗺️ 關卡與任務 (Stages & Quests)":
    st.markdown('<div class="main-header">🗺️ 關卡節點與支線任務</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">劇情推進節點、生化危機街道地圖與隱藏支線檢定</div>', unsafe_allow_html=True)

    tab_map, tab_quests = st.tabs(["🗺️ 關卡地圖 (Map Nodes)", "📜 支線任務 (Side Quests)"])
    with tab_map:
        if map_list:
            for stage in map_list:
                if isinstance(stage, dict):
                    with st.expander(f"📍 {stage.get('stage_name', stage.get('stage_id', '關卡'))}"):
                        st.json(stage.get("map_nodes", []))
        else:
            st.info("暫無地圖節點資料")
    with tab_quests:
        if quests_list:
            for q in quests_list:
                if isinstance(q, dict):
                    with st.expander(f"📜 {q.get('quest_title', q.get('quest_id', '任務'))}"):
                        st.write("**對話內容:**", q.get("dialogue_lines", []))
                        st.write("**決策分支:**", q.get("choices", []))
        else:
            st.info("暫無支線任務資料")

# -----------------------------------------------------------------------------
# 8. 數值平衡與戰鬥模擬 (Simulator)
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

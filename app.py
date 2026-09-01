import streamlit as st
import json
import os
import random
import time

# -----------------------------------------------------------------------------
# 頁面配置 (Cyberpunk / Infinite Night 沉浸風格)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="無限之夜 Infinite Night - 輪迴世界",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 Cyberpunk UI 樣式
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #00f0ff, #ff007f, #ffe600);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0,240,255,0.4);
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .combat-log {
        background-color: #0b0f19;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        color: #38bdf8;
        height: 220px;
        overflow-y: auto;
    }
    .status-card {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 載入 JSON 資料庫 (容錯多路徑)
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
possible_json_dirs = [
    os.path.join(BASE_DIR, "game", "jsonData"),
    os.path.join(BASE_DIR, "jsonData"),
    os.path.join(BASE_DIR, "..", "game", "jsonData")
]
JSON_DIR = next((d for d in possible_json_dirs if os.path.exists(d)), os.path.join(BASE_DIR, "game", "jsonData"))

def load_game_json(filename):
    for candidate_dir in possible_json_dirs:
        fp = os.path.join(candidate_dir, filename)
        if os.path.exists(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
    return None

ITEMS_DB = load_game_json("items.json") or {}
BLOODLINES_DB = load_game_json("bloodlines.json") or {}
MONSTERS_DB = load_game_json("monsters_db.json") or {}

# -----------------------------------------------------------------------------
# 初始化遊戲存檔狀態 (Session State)
# -----------------------------------------------------------------------------
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "顧臨淵",
        "role": "輪迴破局者",
        "level": 1,
        "exp": 0,
        "level_cap": 30,
        "hp": 250,
        "max_hp": 250,
        "mp": 120,
        "max_mp": 120,
        "energy_name": "無",
        "energy": 0,
        "max_energy": 0,
        "points": 1500,
        "shards": {"D": 1, "C": 0, "B": 0, "A": 0, "S": 0},
        "stats": {"con": 30, "str": 25, "spd": 25, "int": 50, "mnd": 25},
        "bloodline": None,
        "bloodline_grade": None,
        "gene_lock": 0,
        "gene_lock_active": False,
        "weapon": {"name": "高頻電磁軍刀", "atk": 35, "type": "melee"},
        "armor": {"name": "奈米戰術防彈衣", "def": 15},
        "inventory": [
            {"id": "item_heal_spray", "name": "輪迴止血急救噴霧", "count": 3, "effect": "heal_hp", "val": 100},
            {"id": "item_mp_potion", "name": "強效精神穩定劑", "count": 2, "effect": "heal_mp", "val": 60}
        ]
    }

if "game_state" not in st.session_state:
    st.session_state.game_state = "hub"  # "hub", "mission_explore", "battle", "game_over"

if "combat" not in st.session_state:
    st.session_state.combat = {
        "enemy": None,
        "log": ["🌌 輪迴終端連線成功。主神空間整備中..."],
        "turn": 1
    }

if "mission" not in st.session_state:
    st.session_state.mission = {
        "name": "生化危機・蜂巢地下設施",
        "progress": 0,
        "stage": 1,
        "events_cleared": []
    }

def add_log(text):
    st.session_state.combat["log"].append(f"[{time.strftime('%H:%M:%S')}] {text}")

# -----------------------------------------------------------------------------
# 戰鬥輔助邏輯
# -----------------------------------------------------------------------------
def start_battle(enemy_type="agile_zombie"):
    p = st.session_state.player
    enemy_stats = {
        "agile_zombie": {"name": "敏捷型突變喪屍", "hp": 120, "max_hp": 120, "atk": 22, "def": 8, "spd": 28, "exp": 80, "points": 150, "drop_shard": "D", "shard_rate": 0.3},
        "licker": {"name": "爬行者 (Licker)", "hp": 260, "max_hp": 260, "atk": 45, "def": 18, "spd": 35, "exp": 180, "points": 350, "drop_shard": "D", "shard_rate": 0.6},
        "tyrant": {"name": "暴君 (Tyrant T-002)", "hp": 650, "max_hp": 650, "atk": 75, "def": 30, "spd": 20, "exp": 500, "points": 1200, "drop_shard": "C", "shard_rate": 1.0}
    }
    target = enemy_stats.get(enemy_type, enemy_stats["agile_zombie"]).copy()
    st.session_state.combat["enemy"] = target
    st.session_state.combat["turn"] = 1
    st.session_state.player["gene_lock_active"] = False
    st.session_state.game_state = "battle"
    add_log(f"⚠️ 警告！遭遇敵方目標：【{target['name']}】！進入戰鬥！")

def player_attack(action_type="normal", skill=None):
    p = st.session_state.player
    e = st.session_state.combat["enemy"]
    if not e or e["hp"] <= 0:
        return

    # 計算玩家基礎攻擊
    base_atk = p["stats"]["str"] * 1.2 + p["weapon"]["atk"]
    
    # 基因鎖加成
    if p["gene_lock_active"]:
        lock_multiplier = 1.0 + p["gene_lock"] * 0.5
        base_atk *= lock_multiplier

    # 暴擊判定
    is_crit = (random.random() < (0.15 + (p["stats"]["spd"] * 0.005) + (0.25 if p["gene_lock_active"] else 0.0)))
    crit_mult = 2.0 if is_crit else 1.0

    damage = 0
    if action_type == "normal":
        damage = max(5, int((base_atk * crit_mult) - e["def"]))
        e["hp"] = max(0, e["hp"] - damage)
        crit_str = " 🔥【暴擊 CRITICAL!】" if is_crit else ""
        add_log(f"⚔️ {p['name']} 揮動【{p['weapon']['name']}】斬擊，對【{e['name']}】造成 {damage} 點傷害！{crit_str}")

    elif action_type == "skill" and skill:
        if p["mp"] >= skill.get("mp_cost", 0) and p["energy"] >= skill.get("energy_cost", 0):
            p["mp"] -= skill.get("mp_cost", 0)
            p["energy"] -= skill.get("energy_cost", 0)
            skill_dmg = base_atk * skill.get("mult", 1.8) * crit_mult
            damage = max(10, int(skill_dmg - e["def"] * 0.5))
            e["hp"] = max(0, e["hp"] - damage)
            
            # 特殊吸血或特效
            if skill.get("heal", 0) > 0:
                heal_amt = skill["heal"]
                p["hp"] = min(p["max_hp"], p["hp"] + heal_amt)
                add_log(f"🩸 釋放【{skill['name']}】！撕裂造成 {damage} 傷害，並汲取恢復了 {heal_amt} 點生命！")
            else:
                add_log(f"⚡ 釋放血統戰技【{skill['name']}】！爆發造成 {damage} 點毀滅性傷害！")
        else:
            add_log("⚠️ 精神力或血統能量不足，無法施展技能！")
            return

    # 敵方死亡判定
    if e["hp"] <= 0:
        win_battle(e)
        return

    # 敵方反擊回合
    enemy_turn(e)

def enemy_turn(e):
    p = st.session_state.player
    # 閃避判定 (基於 SPD 差)
    dodge_chance = min(0.4, max(0.05, (p["stats"]["spd"] - e["spd"]) * 0.01))
    if random.random() < dodge_chance:
        add_log(f"💨 {p['name']} 身形一閃，成功殘影閃避了【{e['name']}】的致命攻擊！")
    else:
        raw_e_atk = e["atk"] * random.uniform(0.85, 1.15)
        e_dmg = max(5, int(raw_e_atk - p["armor"]["def"] - (p["stats"]["con"] * 0.3)))
        p["hp"] = max(0, p["hp"] - e_dmg)
        add_log(f"💥 【{e['name']}】發動猛烈反撲！對 {p['name']} 造成 {e_dmg} 點實質傷害！")
        
        if p["hp"] <= 0:
            st.session_state.game_state = "game_over"
            add_log("💀 你的生命跡象歸零... 輪迴突圍失敗！")

def win_battle(e):
    p = st.session_state.player
    add_log(f"🏆 成功殲滅目標【{e['name']}】！戰鬥勝利！")
    
    # 獎勵點數與經驗值
    p["points"] += e["points"]
    p["exp"] += e["exp"]
    add_log(f"✨ 獲得獎勵：+{e['points']} 獎勵點數，+{e['exp']} 經驗值 (EXP)")

    # 命運碎片掉落
    if random.random() < e.get("shard_rate", 0):
        shard_rank = e.get("drop_shard", "D")
        p["shards"][shard_rank] = p["shards"].get(shard_rank, 0) + 1
        add_log(f"💎 狂喜！從敵方殘骸中搜尋到：【{shard_rank} 階命運碎片】 x1！")

    # 升級檢查
    check_level_up()

    # 推進副本進度
    st.session_state.mission["progress"] += 25
    st.session_state.game_state = "mission_explore"

def check_level_up():
    p = st.session_state.player
    req_exp = p["level"] * 100
    while p["exp"] >= req_exp:
        if p["level"] < p["level_cap"]:
            p["exp"] -= req_exp
            p["level"] += 1
            p["max_hp"] += 20
            p["hp"] = p["max_hp"]
            p["max_mp"] += 10
            p["mp"] = p["max_mp"]
            p["stats"]["con"] += 2
            p["stats"]["str"] += 2
            p["stats"]["spd"] += 2
            p["stats"]["int"] += 2
            p["stats"]["mnd"] += 2
            add_log(f"🌟 等級突破！恭喜晉升至【Lv. {p['level']}】！生命/精神全滿，全屬性提升！")
            req_exp = p["level"] * 100
        else:
            add_log(f"⚠️ 經驗值已滿，但受到【等級上限 (Lv. {p['level_cap']})】枷鎖限制！請突破基因鎖或加載高階血統！")
            break

# -------------------------------------------------------------
# 頂部狀態列 (玩家即時 HUD 面板)
# -------------------------------------------------------------
p = st.session_state.player
col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
with col_h1:
    st.markdown(f"**👤 {p['name']}** (Lv. {p['level']} / {p['level_cap']})")
    hp_pct = max(0.0, min(1.0, p['hp'] / p['max_hp']))
    st.progress(hp_pct, text=f"HP: {p['hp']}/{p['max_hp']}")
with col_h2:
    st.markdown(f"**🧬 基因鎖**: `第 {p['gene_lock']} 階`")
    mp_pct = max(0.0, min(1.0, p['mp'] / p['max_mp']))
    st.progress(mp_pct, text=f"MP: {p['mp']}/{p['max_mp']}")
with col_h3:
    st.markdown(f"**🩸 當前血統**: `{p['bloodline'] or '無 (純人類)'}`")
    st.caption(f"裝備: {p['weapon']['name']} / {p['armor']['name']}")
with col_h4:
    st.markdown(f"**💰 獎勵點數**: `{p['points']} pts`")
    shards_txt = " | ".join([f"{k}:{v}" for k, v in p['shards'].items() if v > 0]) or "無"
    st.markdown(f"**💎 命運碎片**: `{shards_txt}`")
with col_h5:
    st.markdown(f"**⚡ 戰鬥六圍總覽**")
    st.caption(f"體質 {p['stats']['con']} | 力量 {p['stats']['str']} | 敏捷 {p['stats']['spd']} | 智力 {p['stats']['int']} | 精神 {p['stats']['mnd']}")

st.markdown("---")

# =============================================================================
# 場景 1: 🏛️ 主神空間 (Main God Hub)
# =============================================================================
if st.session_state.game_state == "hub":
    st.markdown('<div class="main-header">🏛️ 主神空間・輪迴樞紐大廳</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">在巨大的光團之下，你可以進行全身修復、兌換高階血統、強化身體六圍與整備戰術裝備。</div>', unsafe_allow_html=True)

    hub_tab1, hub_tab2, hub_tab3, hub_tab4, hub_tab5 = st.tabs([
        "🚀 副本傳送門 (Mission)",
        "💫 全身修復 (Restore)",
        "🧬 血統強化儀 (Bloodline)",
        "🛒 主神物資兌換 (Shop)",
        "🏋️ 重力修煉室 (Training)"
    ])

    # 1. 副本傳送門
    with hub_tab1:
        st.subheader("🌌 選擇出擊輪迴世界副本")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("""
            ### 🧟 副本 1：生化危機・蜂巢地下突圍
            * **難度階級**: `⭐⭐ (入門~進階)`
            * **任務目標**: 突破生化地下防禦閘門，擊敗攔截的突變敏捷喪屍、爬行者與終極暴君 T-002。
            * **通關獎勵**: `2000 點數 + D階命運碎片 x2 + C階命運碎片 x1`
            """)
            if st.button("🚀 即刻傳送進入【生化危機・蜂巢】", type="primary", use_container_width=True):
                st.session_state.mission = {
                    "name": "生化危機・蜂巢地下設施",
                    "progress": 0,
                    "stage": 1,
                    "events_cleared": []
                }
                st.session_state.game_state = "mission_explore"
                add_log("🌌 白光閃爍！傳送抵達生化危機・蜂巢 B1 層入口！")
                st.rerun()

        with col_m2:
            st.markdown("""
            ### 👽 副本 2：異形・諾史莫號太空孤艦 (即將解鎖)
            * **難度階級**: `⭐⭐⭐⭐ (極度危險)`
            * **任務目標**: 在封閉太空船中搜尋倖存者，抵禦異形幼蟲抱臉體與成年禁衛異形。
            * **前置需求**: `基因鎖一階 + 基礎等級 Lv.15`
            """)
            st.button("🔒 權限尚未解鎖", disabled=True, use_container_width=True)

    # 2. 全身修復
    with hub_tab2:
        st.subheader("💫 主神全身光柱修復")
        st.write("主神的光芒能瞬間修復任何致命創傷、斷肢與精神疲勞。")
        cost_heal = int((p["max_hp"] - p["hp"]) * 0.5 + (p["max_mp"] - p["mp"]) * 0.5)
        if cost_heal == 0:
            st.success("✨ 你的身體處於巔峰完美狀態，無需修復！")
        else:
            st.warning(f"目前受傷狀態需要消耗：`{cost_heal} 點數`")
            if st.button(f"💖 支付 {cost_heal} 點數進行全身光柱修復"):
                if p["points"] >= cost_heal:
                    p["points"] -= cost_heal
                    p["hp"] = p["max_hp"]
                    p["mp"] = p["max_mp"]
                    st.success("✨ 溫暖的白光降臨！全身傷勢痊癒，狀態完全恢復！")
                    st.rerun()
                else:
                    st.error("❌ 獎勵點數不足！")

    # 3. 血統強化儀
    with hub_tab3:
        st.subheader("🧬 融合高階輪迴血統")
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown("""
            #### 🩸 變異吸血鬼血統 (D級)
            * **消耗**: `1000 點數 + D階命運碎片 x1`
            * **特性**: 解鎖【血族能量】、解鎖技能【嗜血撕咬】、等級上限 +20、生命上限 +50、力量 +15、敏捷 +15。
            """)
            if p["bloodline"] == "變異吸血鬼 (D級)":
                st.button("✅ 已加載此血統", disabled=True)
            else:
                if st.button("🧬 兌換並融合【變異吸血鬼血統】"):
                    if p["points"] >= 1000 and p["shards"]["D"] >= 1:
                        p["points"] -= 1000
                        p["shards"]["D"] -= 1
                        p["bloodline"] = "變異吸血鬼 (D級)"
                        p["level_cap"] += 20
                        p["max_hp"] += 50
                        p["hp"] = p["max_hp"]
                        p["energy_name"] = "血族能量"
                        p["max_energy"] = 100
                        p["energy"] = 100
                        p["stats"]["str"] += 15
                        p["stats"]["spd"] += 15
                        st.success("🎉 基因重組完成！成功融合【變異吸血鬼血統】！等級上限擴充至 Lv.50！")
                        st.rerun()
                    else:
                        st.error("❌ 點數或 D 階命運碎片不足！")

        with b_col2:
            st.markdown("""
            #### ⚡ 初階賽亞人戰士血統 (C級)
            * **消耗**: `3000 點數 + C階命運碎片 x1`
            * **特性**: 解鎖【氣 (Ki)】、解鎖技能【氣功波】、瀕死戰力翻倍、力量 +35、體質 +30。
            """)
            if p["bloodline"] == "賽亞人 (C級)":
                st.button("✅ 已加載此血統", disabled=True)
            else:
                if st.button("🧬 兌換並融合【賽亞人戰士血統】"):
                    if p["points"] >= 3000 and p["shards"]["C"] >= 1:
                        p["points"] -= 3000
                        p["shards"]["C"] -= 1
                        p["bloodline"] = "賽亞人 (C級)"
                        p["level_cap"] += 25
                        p["max_hp"] += 100
                        p["hp"] = p["max_hp"]
                        p["energy_name"] = "氣 (Ki)"
                        p["max_energy"] = 150
                        p["energy"] = 150
                        p["stats"]["str"] += 35
                        p["stats"]["con"] += 30
                        st.success("🎉 金色氣焰爆發！成功融合【賽亞人戰士血統】！")
                        st.rerun()
                    else:
                        st.error("❌ 點數或 C 階命運碎片不足！")

    # 4. 主神物資商城
    with hub_tab4:
        st.subheader("🛒 主神空間武器裝備與戰術物資")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown("#### 🗡️ 高頻電磁光刃 (ATK +60)")
            st.write("消耗: `800 點數`")
            if st.button("兌換 高頻電磁光刃"):
                if p["points"] >= 800:
                    p["points"] -= 800
                    p["weapon"] = {"name": "高頻電磁光刃", "atk": 60, "type": "melee"}
                    st.success("武器裝備成功！")
                    st.rerun()
                else:
                    st.error("點數不足！")

        with s2:
            st.markdown("#### 🛡️ 特種外骨骼裝甲 (DEF +35)")
            st.write("消耗: `1200 點數 + D階碎片 x1`")
            if st.button("兌換 外骨骼裝甲"):
                if p["points"] >= 1200 and p["shards"]["D"] >= 1:
                    p["points"] -= 1200
                    p["shards"]["D"] -= 1
                    p["armor"] = {"name": "特種外骨骼裝甲", "def": 35}
                    st.success("防具裝備成功！")
                    st.rerun()
                else:
                    st.error("資源不足！")

        with s3:
            st.markdown("#### 💊 輪迴急救噴霧 x3")
            st.write("消耗: `300 點數` (立即回滿 150 HP)")
            if st.button("購買 急救噴霧組"):
                if p["points"] >= 300:
                    p["points"] -= 300
                    found = False
                    for item in p["inventory"]:
                        if item["id"] == "item_heal_spray":
                            item["count"] += 3
                            found = True
                            break
                    if not found:
                        p["inventory"].append({"id": "item_heal_spray", "name": "輪迴止血急救噴霧", "count": 3, "effect": "heal_hp", "val": 150})
                    st.success("購買成功！已存入背包。")
                    st.rerun()
                else:
                    st.error("點數不足！")

    # 5. 重力修煉室
    with hub_tab5:
        st.subheader("🏋️ 10倍超重力修煉室")
        st.write("消耗獎勵點數對自身肉體進行極限淬鍊，直接提升六圍屬性。每提升 5 點屬性消耗 200 點數。")
        t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)
        with t_col1:
            if st.button("體質 CON +5"):
                if p["points"] >= 200:
                    p["points"] -= 200
                    p["stats"]["con"] += 5
                    p["max_hp"] += 25
                    p["hp"] = p["max_hp"]
                    st.success("體質提升！")
                    st.rerun()
        with t_col2:
            if st.button("力量 STR +5"):
                if p["points"] >= 200:
                    p["points"] -= 200
                    p["stats"]["str"] += 5
                    st.success("力量提升！")
                    st.rerun()
        with t_col3:
            if st.button("敏捷 SPD +5"):
                if p["points"] >= 200:
                    p["points"] -= 200
                    p["stats"]["spd"] += 5
                    st.success("敏捷提升！")
                    st.rerun()
        with t_col4:
            if st.button("智力 INT +5"):
                if p["points"] >= 200:
                    p["points"] -= 200
                    p["stats"]["int"] += 5
                    p["max_mp"] += 20
                    p["mp"] = p["max_mp"]
                    st.success("智力提升！")
                    st.rerun()
        with t_col5:
            if st.button("精神 MND +5"):
                if p["points"] >= 200:
                    p["points"] -= 200
                    p["stats"]["mnd"] += 5
                    st.success("精神提升！")
                    st.rerun()

# =============================================================================
# 場景 2: 🗺️ 副本探索模式 (Mission Explore)
# =============================================================================
elif st.session_state.game_state == "mission_explore":
    m = st.session_state.mission
    st.markdown(f'<div class="main-header">🧟 {m["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-text">目前深入進度：{m["progress"]}%</div>', unsafe_allow_html=True)
    st.progress(m["progress"] / 100.0)

    if m["progress"] >= 100:
        st.balloons()
        st.success("🎉 恭喜！你成功擊潰暴君並清空蜂巢地下設施，完成本次副本突圍！")
        if st.button("🏆 領取通關獎勵並返回主神空間", type="primary"):
            p["points"] += 2000
            p["shards"]["D"] += 2
            p["shards"]["C"] += 1
            st.session_state.game_state = "hub"
            add_log("🏆 蜂巢任務結算完成！獲得 +2000 點數，D階碎片 x2，C階碎片 x1！")
            st.rerun()

    else:
        st.markdown("### 📍 前方通道與遭遇事件")
        
        # 根據進度顯示不同事件
        if m["progress"] == 0:
            st.info("🚨 進入蜂巢 B1 層閘門，警報狂鳴，前方長廊湧出大量敏捷型喪屍群！")
            if st.button("⚔️ 拔出武器，迎擊【敏捷型突變喪屍】！", type="primary"):
                start_battle("agile_zombie")
                st.rerun()

        elif m["progress"] == 25:
            st.info("🚪 發現一間被電子鎖死的高級醫務室，門上顯示需要進行智力破解。")
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                if st.button(f"🧠 進行智力檢定破解 (需要 INT >= 40，當前 INT: {p['stats']['int']})"):
                    if p["stats"]["int"] >= 40:
                        st.success("✨ 電子防爆門成功解鎖！在醫護箱中搜刮到【高階急救噴霧 x2】與【500 點數】！")
                        p["points"] += 500
                        for item in p["inventory"]:
                            if item["id"] == "item_heal_spray":
                                item["count"] += 2
                        m["progress"] += 25
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("❌ 智力不足，電子鎖自毀觸發毒氣！HP 受到 40 點傷害！")
                        p["hp"] = max(10, p["hp"] - 40)
                        m["progress"] += 25
                        st.rerun()
            with e_col2:
                if st.button("繞過醫務室，繼續前進"):
                    m["progress"] += 25
                    st.rerun()

        elif m["progress"] == 50:
            st.warning("⚠️ 天花板傳來刺耳的爬行刮擦聲！一隻長著外露大腦與利爪的【爬行者 (Licker)】從陰影中撲落！")
            if st.button("⚔️ 迎戰【爬行者 (Licker)】！", type="primary"):
                start_battle("licker")
                st.rerun()

        elif m["progress"] == 75:
            st.error("🚨 警告！B3 培養槽爆裂！終極生化生物武器【暴君 (Tyrant T-002)】甦醒，巨型利爪直直朝你轟來！")
            if st.button("🔥 決死一戰！挑戰【暴君 T-002】！", type="primary"):
                start_battle("tyrant")
                st.rerun()

# =============================================================================
# 場景 3: ⚔️ 即時回合指令戰鬥 (Combat Battle)
# =============================================================================
elif st.session_state.game_state == "battle":
    e = st.session_state.combat["enemy"]
    st.markdown(f'<div class="main-header">⚔️ 戰鬥遭遇：{e["name"]}</div>', unsafe_allow_html=True)

    # 雙方血條展示
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown(f"**👤 {p['name']}**")
        p_pct = max(0.0, min(1.0, p['hp'] / p['max_hp']))
        st.progress(p_pct, text=f"HP: {p['hp']}/{p['max_hp']} | MP: {p['mp']}/{p['max_mp']}")
        if p["bloodline"]:
            eng_pct = max(0.0, min(1.0, p['energy'] / p['max_energy'])) if p['max_energy'] > 0 else 0.0
            st.progress(eng_pct, text=f"{p['energy_name']}: {p['energy']}/{p['max_energy']}")
    
    with col_b2:
        st.markdown(f"**🧟 {e['name']}**")
        e_pct = max(0.0, min(1.0, e['hp'] / e['max_hp']))
        st.progress(e_pct, text=f"敵人 HP: {e['hp']}/{e['max_hp']}")

    st.markdown("---")

    # 戰術指令控制台
    st.subheader("🎮 戰術行動指令")
    cmd1, cmd2, cmd3, cmd4 = st.columns(4)

    with cmd1:
        if st.button(f"🗡️ 普通斬擊 ({p['weapon']['name']})", use_container_width=True):
            player_attack("normal")
            st.rerun()

    with cmd2:
        # 血統技能
        if p["bloodline"] == "變異吸血鬼 (D級)":
            if st.button("🩸 嗜血撕咬 (吸血+高傷)", use_container_width=True):
                player_attack("skill", {"name": "嗜血撕咬", "energy_cost": 25, "mp_cost": 15, "mult": 2.2, "heal": 35})
                st.rerun()
        elif p["bloodline"] == "賽亞人 (C級)":
            if st.button("⚡ 氣功波 (極大傷害)", use_container_width=True):
                player_attack("skill", {"name": "氣功波", "energy_cost": 40, "mp_cost": 25, "mult": 3.2, "heal": 0})
                st.rerun()
        else:
            if st.button("👊 蓄力重擊 (消耗 20 MP)", use_container_width=True):
                player_attack("skill", {"name": "蓄力重擊", "energy_cost": 0, "mp_cost": 20, "mult": 1.6, "heal": 0})
                st.rerun()

    with cmd3:
        # 基因鎖開啟
        if not p["gene_lock_active"]:
            if st.button("🧬 開啟基因鎖爆發！", use_container_width=True):
                if p["gene_lock"] == 0:
                    # 臨時突破一階
                    p["gene_lock"] = 1
                    p["gene_lock_active"] = True
                    add_log("⚡【潛能爆發】在生死邊緣打破基因鎖第一階！進入戰鬥本能模式，攻擊力暴增！")
                else:
                    p["gene_lock_active"] = True
                    add_log(f"🧬 開啟基因鎖第 {p['gene_lock']} 階！細胞活性全開！")
                st.rerun()
        else:
            st.button("🔥 基因鎖狀態生效中 (+50% ATK)", disabled=True, use_container_width=True)

    with cmd4:
        # 道具使用
        spray = next((i for i in p["inventory"] if i["id"] == "item_heal_spray" and i["count"] > 0), None)
        if spray:
            if st.button(f"💊 使用急救噴霧 (餘 {spray['count']})", use_container_width=True):
                spray["count"] -= 1
                p["hp"] = min(p["max_hp"], p["hp"] + 120)
                add_log(f"💊 使用【輪迴止血急救噴霧】！傷口瞬間止血，恢復 120 HP！")
                enemy_turn(e)
                st.rerun()
        else:
            st.button("💊 急救噴霧耗盡", disabled=True, use_container_width=True)

    # 戰鬥日誌 (Combat Log)
    st.markdown("### 📜 戰況即時日誌")
    log_text = "\n".join(reversed(st.session_state.combat["log"][-10:]))
    st.text_area("戰鬥記錄", log_text, height=180, disabled=True)

# =============================================================================
# 場景 4: 💀 遊戲結束 / 陣亡重置 (Game Over)
# =============================================================================
elif st.session_state.game_state == "game_over":
    st.error("💀 【輪迴突圍失敗 - 角色已陣亡】")
    st.write("你在殘酷的生化危機蜂巢中倒下了。主神將扣除 500 點數將你從瀕死中復活修復。")
    if st.button("💫 復活並返回主神空間", type="primary"):
        p["hp"] = p["max_hp"]
        p["mp"] = p["max_mp"]
        p["points"] = max(0, p["points"] - 500)
        st.session_state.game_state = "hub"
        add_log("💫 主神修復了你的肉體，你重新回到了主神空間。")
        st.rerun()

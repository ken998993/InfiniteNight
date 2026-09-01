# ==========================================
# 遊戲全域資料與初始化方法集中管理 (game_init.rpy)
# ==========================================

# 全域常用轉場特效
define flash = Fade(0.1, 0.0, 0.3, color="#ffffff")
define flash_red = Fade(0.1, 0.0, 0.3, color="#ff0000")

# 全域全螢幕背景縮放變換 (保證所有背景圖 100% 填滿 1920x1080 且無黑邊與馬賽克邊)
transform bg_full_screen:
    xsize 1920
    ysize 1080
    xalign 0.5
    yalign 0.5

# 全域基礎背景與角色圖元宣告
image trial_room = Transform("images/trial_room.png", xsize=1920, ysize=1080)
image zombie_street = Transform("images/zombie_street.PNG", xsize=1920, ysize=1080)
image bg_main_room_topdown = Transform("images/bg_main_room_topdown.png", xsize=1920, ysize=1080)
image lengyue = Transform("images/coldmoon.PNG", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side lengyue = Transform("images/coldmoon.PNG", xsize=240, ysize=240, fit="contain")
image zhao_hu = Transform("images/gansterA.PNG", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side zhao_hu = Transform("images/gansterA.PNG", xsize=240, ysize=240, fit="contain")
image zhou_yang = Transform("images/panicWokrer.PNG", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side zhou_yang = Transform("images/panicWokrer.PNG", xsize=240, ysize=240, fit="contain")
image qian_fugui = Transform("images/fatoldman.PNG", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side qian_fugui = Transform("images/fatoldman.PNG", xsize=240, ysize=240, fit="contain")
image xiangtian = Transform("images/xiangtian.PNG", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side xiangtian = Transform("images/xiangtian.PNG", xsize=240, ysize=240, fit="contain")
image suxiao = Transform("images/femalewriter.PNG", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side suxiao = Transform("images/femalewriter.PNG", xsize=240, ysize=240, fit="contain")
image aurora_captain = Transform("images/securegurde.jpg", xalign=0.5, yalign=0.5, xsize=720, ysize=960, fit="contain")
image side aurora_captain = Transform("images/securegurde.jpg", xsize=240, ysize=240, fit="contain")
image agile_zombie = Transform("images/agile_zombie.jpg", xalign=0.5, yalign=0.32, xsize=550, ysize=550, fit="contain")
image side agile_zombie = Transform("images/agile_zombie.jpg", xsize=240, ysize=240, fit="contain")
image zombie = Transform("images/zombie.jpg", xalign=0.5, yalign=0.32, xsize=550, ysize=550, fit="contain")
image side zombie = Transform("images/zombie.jpg", xsize=240, ysize=240, fit="contain")
image MOB_ZOMBIE_01 = Transform("images/zombie.jpg", xalign=0.5, yalign=0.32, xsize=550, ysize=550, fit="contain")

transform item_show_center:
    xalign 0.5
    yalign 0.32

image tactical_hazmat_armor = Transform("images/tactical_hazmat_armor.jpg", xalign=0.5, yalign=0.32, xsize=500, ysize=500, fit="contain")
image high_explosive = Transform("images/high_explosive_fragmentation_grenade.jpg", xalign=0.5, yalign=0.32, xsize=500, ysize=500, fit="contain")
image item_grenade = Transform("images/high_explosive_fragmentation_grenade.jpg", xalign=0.5, yalign=0.32, xsize=500, ysize=500, fit="contain")
image bg_aurora_core = Transform("images/adamcore.jpg", xsize=1920, ysize=1080)
image adamcore = Transform("images/adamcore.jpg", xalign=0.5, yalign=0.32, xsize=550, ysize=550, fit="contain")
image adam_ai = Transform("images/adamcore.jpg", xalign=0.5, yalign=0.32, xsize=550, ysize=550, fit="contain")
image side adam_ai = Transform("images/adamcore.jpg", xsize=240, ysize=240, fit="contain")
image zombieCityMap = Transform("images/zombieCityMap.jpg", xsize=1920, ysize=1080)
image bg_zombie_city_map = Transform("images/zombieCityMap.jpg", xsize=1920, ysize=1080)
image spaceShip = Transform("images/spaceShip.jpg", xsize=1920, ysize=1080)
image bg_spaceShip = Transform("images/spaceShip.jpg", xsize=1920, ysize=1080)

init python:
    import json

    # 1. 封裝取得團隊名單的方法 (自 jsonData/team_data.json 讀取)
    def get_team_roster():
        global team_roster
        if 'team_roster' in globals() and team_roster:
            for m in team_roster:
                if "冷月" in str(m.get('name', '')):
                    m['avatar'] = "images/coldmoon.PNG"
                if "項天" in str(m.get('name', '')):
                    m['avatar'] = "images/xiangtian.PNG"
                if "蘇曉" in str(m.get('name', '')):
                    m['avatar'] = "images/femalewriter.PNG"
                if 'level' not in m or int(m.get('level', 0)) < 1:
                    m['level'] = 1
                if 'exp' not in m:
                    m['exp'] = 0
                for k in ['level', 'exp', 'hp', 'max_hp', 'mp', 'max_mp', 'points', 'atk_bonus', 'gene_lock', 'con', 'str', 'spd', 'int', 'mnd']:
                    if k in m:
                        try:
                            m[k] = int(m[k])
                        except Exception:
                            m[k] = 100 if 'hp' in k else (1 if k == 'level' else 0)
            return team_roster
        try:
            with renpy.file("jsonData/team_data.json") as f:
                team_roster = json.load(f)
                for m in team_roster:
                    if "冷月" in str(m.get('name', '')):
                        m['avatar'] = "images/coldmoon.PNG"
                    if "項天" in str(m.get('name', '')):
                        m['avatar'] = "images/xiangtian.PNG"
                    if "蘇曉" in str(m.get('name', '')):
                        m['avatar'] = "images/femalewriter.PNG"
                    if 'level' not in m or int(m.get('level', 0)) < 1:
                        m['level'] = 1
                    if 'exp' not in m:
                        m['exp'] = 0
                    for k in ['level', 'exp', 'hp', 'max_hp', 'mp', 'max_mp', 'points', 'atk_bonus', 'gene_lock', 'con', 'str', 'spd', 'int', 'mnd']:
                        if k in m:
                            try:
                                m[k] = int(m[k])
                            except Exception:
                                m[k] = 100 if 'hp' in k else (1 if k == 'level' else 0)
        except Exception as e:
            team_roster = [
                {
                    "name": "顧臨淵 (你)",
                    "role": "異數隊長 / 輪迴破局者",
                    "combat_role": "全能平衡 / 成長型",
                    "bloodline": "無 (可兼修多重體系)",
                    "level": 1,
                    "exp": 0,
                    "points": 1000,
                    "con": 30, "str": 25, "spd": 25, "int": 60, "mnd": 25,
                    "hp": 250, "max_hp": 250,
                    "mp": 150, "max_mp": 150,
                    "neili_current": 0, "neili_max": 0,
                    "blood_current": 0, "blood_max": 0,
                    "mental_current": 0, "mental_max": 0,
                    "qi_current": 0, "qi_max": 0,
                    "calc_current": 0, "calc_max": 0,
                    "gene_lock": 0, "survival_pressure": 0,
                    "status": "良好",
                    "skills": [],
                    "equipped_main_hand": "weapon_gauss_rifle",
                    "desc": "跳脫一切原定劇情與因果宿命之外的異數（Anomaly）。"
                }
            ]
        return team_roster

    # 計算升到下一級所需經驗值 (每級 * 100 點 EXP)
    def get_next_level_exp(level):
        lvl = max(1, int(level))
        return lvl * 100

    # 單一隊員獲得經驗值與升級檢查
    def add_member_exp(member, exp_amount):
        if not member or exp_amount <= 0:
            return {"leveled_up": False, "level_ups": 0, "old_level": int(member.get("level", 1) if member else 1), "new_level": int(member.get("level", 1) if member else 1)}
            
        cur_lvl = max(1, int(member.get("level", 1)))
        cur_exp = max(0, int(member.get("exp", 0))) + int(exp_amount)
        cap = calculate_level_cap(member) if 'calculate_level_cap' in globals() else 30
        
        level_ups = 0
        old_lvl = cur_lvl
        
        while True:
            next_req = get_next_level_exp(cur_lvl)
            if cur_exp >= next_req:
                if cur_lvl < cap:
                    cur_exp -= next_req
                    cur_lvl += 1
                    level_ups += 1
                    # 升級屬性成長：生命上限+10、精神上限+5，並同步恢復當前生命與精神
                    member["max_hp"] = int(member.get("max_hp", 100)) + 10
                    member["hp"] = min(member["max_hp"], int(member.get("hp", 100)) + 10)
                    member["max_mp"] = int(member.get("max_mp", 50)) + 5
                    member["mp"] = min(member["max_mp"], int(member.get("mp", 50)) + 5)
                else:
                    cur_lvl = cap
                    cur_exp = min(cur_exp, next_req)
                    break
            else:
                break
                
        member["level"] = cur_lvl
        member["exp"] = cur_exp
        
        return {
            "leveled_up": (level_ups > 0),
            "level_ups": level_ups,
            "old_level": old_lvl,
            "new_level": cur_lvl,
            "cap_reached": (cur_lvl >= cap)
        }

    # 全體出戰隊員獲得經驗值並同步回隊伍存檔
    def add_team_exp(exp_amount, battle_state=None):
        global team_roster
        roster = get_team_roster()
        leveled_members = []
        
        p_team = battle_state.get('player_team', roster) if battle_state else roster
        for mem in p_team:
            if int(mem.get("hp", 0)) > 0 or not battle_state:
                res = add_member_exp(mem, exp_amount)
                if res.get("leveled_up"):
                    leveled_members.append((mem.get("name", "隊員"), res["old_level"], res["new_level"]))
                    
        # 同步回全局 team_roster 存檔
        for p_mem in p_team:
            m_name = p_mem.get('name')
            for r_mem in roster:
                if r_mem.get('name') == m_name:
                    r_mem['level'] = p_mem.get('level', 1)
                    r_mem['exp'] = p_mem.get('exp', 0)
                    r_mem['max_hp'] = p_mem.get('max_hp', 100)
                    r_mem['hp'] = p_mem.get('hp', 100)
                    r_mem['max_mp'] = p_mem.get('max_mp', 50)
                    r_mem['mp'] = p_mem.get('mp', 50)
                    
        if battle_state and 'logs' in battle_state:
            battle_state['logs'].append(f"✨【戰鬥經驗結算】擊敗全體敵方目標，參戰隊員全員獲得 +{exp_amount} 點角色經驗值！")
            for m_name, old_l, new_l in leveled_members:
                battle_state['logs'].append(f"🎉【角色升級！】隊員【{m_name}】升級至 Lv. {new_l}！(生命上限 +10，精神上限 +5)")
                
        if leveled_members and renpy.loadable("audio/levelup.ogg"):
            renpy.sound.play("audio/levelup.ogg")
            
        return leveled_members

    # 2. 安全更新隊員點數的方法
    def update_member_points(new_points):
        global points, team_roster
        points = new_points
        roster = get_team_roster()
        if roster and len(roster) > 0:
            roster[0]["points"] = points

    # 3. 跨系統通用：自 monsters_db.json 即時建立戰鬥敵人物件 (支援 exp_reward 掉落)
    def create_battle_enemy(monster_id, name_suffix="", status=None):
        m_data = None
        try:
            with renpy.file("jsonData/monsters_db.json") as f:
                for item in json.load(f).get("monsters", []):
                    if item.get("id") == monster_id:
                        m_data = item
                        break
        except Exception:
            pass
        if m_data:
            stats = m_data.get("stats", {})
            hp_val = int(stats.get("hp", 100))
            atk_val = int(stats.get("atk", 20))
            exp_val = int(m_data.get("exp_reward", m_data.get("exp", 50)))
            m_name = m_data.get("name", monster_id)
            if name_suffix:
                m_name = f"{m_name} {name_suffix}"
            avatar_val = m_data.get("avatar", "images/core_idle.PNG")
            if not avatar_val or avatar_val == "images/core_idle.PNG":
                if monster_id == "agile_zombie" or "敏捷" in m_name:
                    avatar_val = "images/agile_zombie.jpg"
                elif monster_id == "MOB_ZOMBIE_01" or "腐屍" in m_name or "喪屍" in m_name:
                    avatar_val = "images/zombie.jpg"
            return {
                "id": monster_id,
                "name": m_name,
                "hp": hp_val,
                "max_hp": hp_val,
                "atk": atk_val,
                "exp": exp_val,
                "status": status or ("嗜血狂暴" if "敏捷" in m_name else "戰鬥戒備"),
                "avatar": avatar_val
            }
        return {
            "id": monster_id,
            "name": f"{monster_id} {name_suffix}".strip(),
            "hp": 100,
            "max_hp": 100,
            "atk": 15,
            "exp": 50,
            "status": status or "狂暴",
            "avatar": "images/core_idle.PNG"
        }

    # 4. 存檔讀取後自動校驗回調 (保證讀檔時角色能力招式與血統 100% 回到存檔當下的狀態)
    def sync_roster_after_load():
        global team_roster
        if 'team_roster' in globals() and team_roster:
            for mem in team_roster:
                if "冷月" in str(mem.get('name', '')):
                    mem['avatar'] = "images/coldmoon.PNG"
                if "項天" in str(mem.get('name', '')):
                    mem['avatar'] = "images/xiangtian.PNG"
                if "蘇曉" in str(mem.get('name', '')):
                    mem['avatar'] = "images/femalewriter.PNG"
                if 'sync_member_skills_from_bloodlines' in globals():
                    sync_member_skills_from_bloodlines(mem)

    config.after_load_callbacks.append(sync_roster_after_load)

# ==========================================
# Ren'Py 原生動態存檔變數聲明 (支援存讀檔與時間回溯)
# ==========================================
default last_active_speaker_avatar = None
default team_roster = [
    {
        "name": "顧臨淵 (你)",
        "role": "異數隊長 / 輪迴破局者",
        "combat_role": "全能平衡 / 成長型",
        "bloodline": "無 (可兼修多重體系)",
        "avatar": "images/core_idle.PNG",
        "points": 1000,
        "con": 30, "str": 25, "spd": 25, "int": 60, "mnd": 25,
        "hp": 250, "max_hp": 250,
        "mp": 150, "max_mp": 150,
        "neili_current": 0, "neili_max": 0,
        "blood_current": 0, "blood_max": 0,
        "mental_current": 0, "mental_max": 0,
        "qi_current": 0, "qi_max": 0,
        "calc_current": 0, "calc_max": 0,
        "gene_lock": 0, "survival_pressure": 0,
        "status": "良好",
        "skills": [],
        "equipped_head": "EQ_TECH_HELMET_01",
        "equipped_torso": "EQ_TECH_ARMOR_01",
        "equipped_hands": "EQ_TECH_GLOVES_01",
        "equipped_feet": "EQ_TECH_BOOTS_01",
        "equipped_necklace": "EQ_TECH_NECKLACE_01",
        "equipped_main_hand": "weapon_plasma_katana",
        "equipped_off_hand": "EQ_TECH_SHIELD_01",
        "equipped_mount": None,
        "desc": "剛被選入輪迴空間的新人，配備基礎戰術單兵裝備，正努力在殘酷的生存法則中活下去。"
    },
    {
        "name": "冷月",
        "role": "資深執行者",
        "combat_role": "靈活爆發 / 念動雙槍",
        "bloodline": "解開基因鎖一階 (資深執行者)",
        "avatar": "images/coldmoon.PNG",
        "points": 3500,
        "con": 50, "str": 45, "spd": 40, "int": 70, "mnd": 45,
        "hp": 350, "max_hp": 350,
        "mp": 200, "max_mp": 200,
        "neili_current": 0, "neili_max": 0,
        "blood_current": 0, "blood_max": 0,
        "mental_current": 50, "mental_max": 100,
        "qi_current": 0, "qi_max": 0,
        "calc_current": 0, "calc_max": 0,
        "gene_lock": 1,
        "survival_pressure": 20,
        "status": "冷靜戒備",
        "skills": [],
        "equipped_head": None,
        "equipped_torso": "EQ_TECH_ARMOR_01",
        "equipped_hands": None,
        "equipped_feet": None,
        "equipped_necklace": None,
        "equipped_main_hand": "weapon_gauss_rifle",
        "equipped_off_hand": None,
        "equipped_mount": None,
        "desc": "冷酷沉穩的資深執行者，手持銀色雙槍，歷經多場生死洗禮，擔任新人的引導者。"
    },
    {
        "name": "項天",
        "role": "前外企白領 / 潛能霸王",
        "combat_role": "紅炎肉搏 / 混元血魄雙修",
        "bloodline": "無 (潛藏混元血脈與紅炎天賦)",
        "avatar": "images/xiangtian.PNG",
        "points": 800,
        "con": 48, "str": 46, "spd": 40, "int": 35, "mnd": 35,
        "hp": 300, "max_hp": 300,
        "mp": 160, "max_mp": 160,
        "neili_current": 30, "neili_max": 100,
        "blood_current": 30, "blood_max": 100,
        "mental_current": 0, "mental_max": 0,
        "qi_current": 30, "qi_max": 100,
        "calc_current": 0, "calc_max": 0,
        "gene_lock": 0,
        "survival_pressure": 10,
        "status": "警惕備戰",
        "skills": [],
        "equipped_head": None,
        "equipped_torso": None,
        "equipped_hands": "EQ_TECH_GLOVES_01",
        "equipped_feet": "EQ_TECH_BOOTS_01",
        "equipped_necklace": None,
        "equipped_main_hand": "weapon_plasma_katana",
        "equipped_off_hand": None,
        "equipped_mount": None,
        "desc": "原為普通外企白領，體內潛藏著無比恐怖的爆發力與紅炎天賦，生死邊緣能同時激發混元內力與血族狂暴雙重能量。"
    },
    {
        "name": "蘇曉",
        "role": "作家 / 新人",
        "combat_role": "精神掃描 / 心靈防護",
        "bloodline": "無 (精神力特化潛能)",
        "avatar": "images/femalewriter.PNG",
        "points": 500,
        "con": 20, "str": 15, "spd": 25, "int": 100, "mnd": 50,
        "hp": 200, "max_hp": 200,
        "mp": 250, "max_mp": 250,
        "neili_current": 0, "neili_max": 0,
        "blood_current": 0, "blood_max": 0,
        "mental_current": 100, "mental_max": 100,
        "qi_current": 0, "qi_max": 0,
        "calc_current": 0, "calc_max": 0,
        "gene_lock": 0,
        "survival_pressure": 15,
        "status": "敏銳感知",
        "skills": [],
        "equipped_head": "EQ_MAGIC_HOOD_01",
        "equipped_torso": None,
        "equipped_hands": "EQ_MAGIC_BRACER_01",
        "equipped_feet": None,
        "equipped_necklace": "EQ_MAGIC_NECKLACE_01",
        "equipped_main_hand": None,
        "equipped_off_hand": None,
        "equipped_mount": None,
        "desc": "具備敏銳的精神力感知天賦，能在危機四伏的戰場中提前察覺殺意，並為隊友構築心靈屏障。"
    }
]

default points = 1000
default fate_shards = {"D": 2, "C": 0, "B": 0, "A": 0, "S": 0}
default inventory = [
    {"id": "item_heal_spray", "count": 3},
    {"id": "item_mp_potion", "count": 2},
    {"id": "item_grenade", "count": 2},
    {"id": "weapon_gauss_rifle", "count": 1},
    {"id": "weapon_plasma_katana", "count": 1},
    {"id": "EQ_TECH_HELMET_01", "count": 1},
    {"id": "EQ_TECH_ARMOR_01", "count": 1},
    {"id": "EQ_TECH_GLOVES_01", "count": 1},
    {"id": "EQ_TECH_BOOTS_01", "count": 1},
    {"id": "EQ_TECH_NECKLACE_01", "count": 1},
    {"id": "EQ_TECH_SHIELD_01", "count": 1}
]
default last_deployed_party = [
    {"name": "顧臨淵 (你)", "position": "frontline"},
    {"name": "冷月", "position": "frontline"},
    {"name": "項天", "position": "frontline"},
    {"name": "蘇曉", "position": "backline"}
]
default current_main_stage_index = 2
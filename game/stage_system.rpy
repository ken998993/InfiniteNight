# ==========================================
# 關卡雙模式與戰鬥資料庫載入器系統 (stage_system.rpy)
# ==========================================

init python:
    import json
    import random

    if 'stage_cleared_states' not in globals():
        stage_cleared_states = {
            "STAGE_1_1": False
        }

    if 'node_quest_cleared_states' not in globals():
        node_quest_cleared_states = {
            "NODE_1_1_EXPLORE": False,
            "NODE_1_1_SERVER": False
        }

    # 1. 載入 3 個 JSON 資料庫
    def get_stages_config():
        try:
            with renpy.file("jsonData/map_nodes.json") as f:
                return json.load(f).get("stages", [])
        except Exception:
            return []

    def get_side_quests_config():
        try:
            with renpy.file("jsonData/side_quests.json") as f:
                return json.load(f).get("side_quests", [])
        except Exception:
            return []

    def get_monsters_db():
        try:
            with renpy.file("jsonData/monsters_db.json") as f:
                return json.load(f).get("monsters", [])
        except Exception:
            return []

    def get_stage_by_id(stage_id):
        stages = get_stages_config()
        for st in stages:
            if st.get("stage_id") == stage_id:
                return st
        return stages[0] if stages else {}

    def get_side_quest_by_id(quest_id):
        quests = get_side_quests_config()
        for q in quests:
            if q.get("quest_id") == quest_id:
                return q
        return None

    def get_monster_by_id(monster_id):
        m_list = get_monsters_db()
        for m in m_list:
            if m.get("id") == monster_id:
                return m
        return None

    # 2. 隊伍智力與幸運掉落率加成
    def get_team_max_int():
        roster = get_team_roster() if 'get_team_roster' in globals() else []
        max_int = 50
        for m in roster:
            if m.get("hp", 0) > 0:
                m_mp = m.get("max_mp", 50)
                if m_mp > max_int:
                    max_int = m_mp
                if m.get("class_type") == "Scholar" or "Scholar" in m.get("role", ""):
                    max_int = max(max_int, 100)
        return max_int

    # 3. 戰鬥結算掉落率計算 (含隊伍最高智力加成)
    def calculate_monster_drops(monster_id_list):
        max_int = get_team_max_int()
        int_bonus = max(0, ((max_int - 50) / 50.0) * 0.02)
        
        dropped_summary = {}
        
        for m_id in monster_id_list:
            m_data = get_monster_by_id(m_id)
            if not m_data:
                continue
                
            drop_tbl = m_data.get("drop_table", {})
            # 1. 普通掉落物判定
            for c_drop in drop_tbl.get("common_drops", []):
                chance = c_drop.get("drop_chance", 0.8)
                if random.random() <= chance:
                    min_q = c_drop.get("min_quantity", 1)
                    max_q = c_drop.get("max_quantity", 1)
                    qty = random.randint(min_q, max_q)
                    itm_id = c_drop.get("item_id")
                    itm_name = c_drop.get("item_name", "素材")
                    if itm_id not in dropped_summary:
                        dropped_summary[itm_id] = {"name": itm_name, "count": 0}
                    dropped_summary[itm_id]["count"] += qty
                    
            # 2. 稀有掉落物判定 (加上 INT 幸運加成)
            for r_drop in drop_tbl.get("rare_drops", []):
                base_chance = r_drop.get("drop_chance", 0.1)
                final_chance = min(1.0, base_chance + int_bonus)
                if random.random() <= final_chance:
                    min_q = r_drop.get("min_quantity", 1)
                    max_q = r_drop.get("max_quantity", 1)
                    qty = random.randint(min_q, max_q)
                    itm_id = r_drop.get("item_id")
                    itm_name = r_drop.get("item_name", "稀有物品")
                    if itm_id not in dropped_summary:
                        dropped_summary[itm_id] = {"name": itm_name, "count": 0}
                    dropped_summary[itm_id]["count"] += qty
                    
        # 將獲得的所有掉落物加入背包或命運碎片
        for itm_id, info in dropped_summary.items():
            cnt = info["count"]
            if itm_id == "CURRENCY_FATE_SHARD_RARE":
                add_fate_shard("C", cnt)
            elif itm_id == "CURRENCY_FATE_SHARD_EPIC":
                add_fate_shard("B", cnt)
            else:
                add_item(itm_id, cnt)
                
        return dropped_summary, int_bonus


# ==========================================
# 關卡節點地圖探索畫面 (stage_map_node_screen)
# ==========================================
screen stage_map_node_screen(stage_id="STAGE_1_1"):

    $ st_data = get_stage_by_id(stage_id)
    $ nodes = st_data.get("map_nodes", [])
    $ max_int = get_team_max_int()
    $ player = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]

    window:
        background "#05070ddd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1740, 960)
        padding (30, 25)
        background "#0d121ff5"

        vbox:
            spacing 10
            xalign 0.5

            # 頂部標題
            hbox:
                spacing 35
                xalign 0.5
                text f"【 🗺️ {st_data.get('stage_name', '副本戰術地圖')} · 自由探索模式 】" size 24 color "#00ffff" bold True yalign 0.5
                text f"隊伍最高智力 (INT): {max_int}" size 17 color "#ffcc00" bold True yalign 0.5
                text f"隊長 HP: {player.get('hp',100)}/{player.get('max_hp',100)}" size 17 color "#ff6666" yalign 0.5
                text f"個人點數: {points} 點" size 17 color "#66ff66" yalign 0.5

            text "點擊下方地圖節點可觸發【首次支線對話與智鬥檢定】或進入【多波次怪物刷怪戰鬥】！" size 15 color "#bbbbbb" xalign 0.5

            null height 15

            # 5 個節點卡片
            hbox:
                spacing 20
                xalign 0.5

                for node in nodes:
                    $ n_id = node.get("node_id")
                    $ n_name = node.get("node_name")
                    $ n_type = node.get("node_type")
                    $ sq_id = node.get("side_quest_id")
                    $ is_sq_done = node_quest_cleared_states.get(n_id, False)

                    frame:
                        xysize (320, 680)
                        background "#161e30ee"
                        padding (18, 15)
                        vbox:
                            spacing 10
                            text f"◈ {n_name}" size 18 color "#00ffff" bold True
                            
                            if n_type == "main_story":
                                text "【主線防禦閘門】" size 14 color "#66ff66"
                                text "前哨防線，可重複刷怪獲取基礎喪屍血液與零件。" size 12 color "#aaaaaa"
                                null height 20
                                text "✅ 主線劇情已通關" size 14 color "#66ff66" xalign 0.5
                                null height 350
                                button:
                                    xysize (284, 52)
                                    background "#245e33"
                                    hover_background "#358a4b"
                                    action Return(("enter_node_battle", n_id, stage_id))
                                    text "⚔️ 進入刷怪戰鬥" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5

                            elif n_type == "side_quest":
                                if not is_sq_done:
                                    text "【❓ 隱藏支線未探索】" size 14 color "#ffff00" bold True
                                    text "有未知智鬥謎題或特殊密室可探索。" size 12 color "#cccccc"
                                    null height 20
                                    text "💡 智者可進行高階駭入檢定" size 13 color "#00ffcc" xalign 0.5
                                    null height 350
                                    button:
                                        xysize (284, 52)
                                        background "#665e2d"
                                        hover_background "#8f843e"
                                        action Return(("enter_side_quest", sq_id, n_id, stage_id))
                                        text "🧩 觸發支線劇情與智鬥" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5
                                else:
                                    text "【✅ 支線已破解 · 刷怪點】" size 14 color "#66ff66" bold True
                                    text "密室已解鎖，在此可大量刷取高階素材與零件。" size 12 color "#aaaaaa"
                                    null height 20
                                    text "🔥 怪物持續刷新中" size 13 color "#ffaa00" xalign 0.5
                                    null height 350
                                    button:
                                        xysize (284, 52)
                                        background "#245e33"
                                        hover_background "#358a4b"
                                        action Return(("enter_node_battle", n_id, stage_id))
                                        text "⚔️ 進入刷怪戰鬥" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5

                            elif n_type == "farming":
                                text "【🔥 生化核心刷怪區】" size 14 color "#ff6666" bold True
                                text "大量變異腐屍與舔食者盤踞，刷取喪屍血液的最快地點！" size 12 color "#cccccc"
                                null height 20
                                text "🩸 喪屍血液掉落率 100%" size 13 color "#ff4444" bold True xalign 0.5
                                null height 350
                                button:
                                    xysize (284, 52)
                                    background "#5e2424"
                                    hover_background "#8a3535"
                                    action Return(("enter_node_battle", n_id, stage_id))
                                    text "⚔️ 狂暴刷怪戰鬥" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5

                            elif n_type == "boss":
                                text "【👹 暴君終極培養槽】" size 14 color "#ff4444" bold True
                                text "迎戰強大的暴君 T-002 突變體！高機率掉落高階基因與作戰服！" size 12 color "#cccccc"
                                null height 20
                                text "👑 Boss 級戰鬥挑戰" size 13 color "#ffcc00" bold True xalign 0.5
                                null height 350
                                button:
                                    xysize (284, 52)
                                    background "#7a1b1b"
                                    hover_background "#a82424"
                                    action Return(("enter_node_battle", n_id, stage_id))
                                    text "☠️ 挑戰暴君 Boss" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5

            null height 5

            textbutton "【 🚪 退出探索，返回輪迴廣場 】":
                xalign 0.5
                action Return("leave_stage")
                text_size 19
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


# ==========================================
# 支線劇情對話與智者檢定畫面 (side_quest_modal_screen)
# ==========================================
screen side_quest_modal_screen(quest_id):

    $ quest = get_side_quest_by_id(quest_id)
    $ max_int = get_team_max_int()

    window:
        background "#000000ee"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1400, 750)
        padding (35, 30)
        background "#0f1628fa"

        vbox:
            spacing 15
            xalign 0.5

            text f"【 📜 支線劇情探索 · {quest.get('quest_title', '未知密室')} 】" size 24 color "#ffcc00" bold True xalign 0.5
            text f"隊伍最高智力 (INT)：{max_int} 點" size 16 color "#00ffcc" bold True xalign 0.5

            null height 10

            # 對話展示區
            frame:
                xysize (1320, 220)
                background "#141c30"
                padding (20, 15)
                vbox:
                    spacing 10
                    for line in quest.get("dialogue_lines", []):
                        hbox:
                            spacing 15
                            text f"【{line.get('speaker')}】：{line.get('text')}" size 16 color "#ffffff"

            null height 10

            text "【 選擇隊伍推進方案 】" size 18 color "#ffaa00" bold True

            # 選擇肢按鈕列
            vbox:
                spacing 12
                for idx, choice in enumerate(quest.get("choices", [])):
                    $ req_i = choice.get("req_int", 0)
                    $ is_int_check = (req_i > 0)
                    $ can_pass = (max_int >= req_i)

                    button:
                        xysize (1320, 65)
                        background ("#1e4d2b" if (not is_int_check or can_pass) else "#4d2b1e")
                        hover_background "#2d7340"
                        padding (20, 12)
                        action Return(("choose_side_quest_option", quest_id, idx, can_pass))

                        hbox:
                            spacing 20
                            yalign 0.5
                            text f"▶ {choice.get('option_text')}" size 16 color "#ffffff" bold True
                            if is_int_check:
                                if can_pass:
                                    text f"【 智力檢定已達標 ({max_int}/{req_i}) - 100% 成功 】" size 14 color "#66ff66" bold True
                                else:
                                    text f"【 智力不足 ({max_int}/{req_i}) - 將觸發警報 】" size 14 color "#ff6666" bold True

            null height 5

            textbutton "【 🚪 暫時離開密室 】":
                xalign 0.5
                action Return("leave_side_quest")
                text_size 16
                text_idle_color "#aaaaaa"
                text_hover_color "#ffffff"


# ==========================================
# 關卡節點探索主循環 (stage_map_hub)
# ==========================================
label stage_map_hub(stage_id="STAGE_1_1"):
    call screen stage_map_node_screen(stage_id)
    $ sm_res = _return
    
    if isinstance(sm_res, tuple) and len(sm_res) >= 2:
        $ act_type = sm_res[0]
        
        # 1. 進入節點刷怪戰鬥
        if act_type == "enter_node_battle":
            $ n_id = sm_res[1]
            $ st_id = sm_res[2] if len(sm_res) > 2 else stage_id
            
            # 戰前跳出 6 人戰術配置畫面
            call screen party_deployment_screen
            $ dep_res = _return
            
            python:
                # 構建戰鬥 state
                deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
                for m in deployed_team:
                    m['has_acted'] = False
                    
                node_monsters = ["MOB_ZOMBIE_01", "MOB_ZOMBIE_01", "MOB_LICKER_01"]
                if "FARM" in n_id:
                    node_monsters = ["MOB_ZOMBIE_01", "MOB_ZOMBIE_02", "MOB_LICKER_01", "MOB_ZOMBIE_01"]
                elif "BOSS" in n_id:
                    node_monsters = ["MOB_TYRANT_01", "MOB_LICKER_01", "MOB_LICKER_01"]
                    
                b_node_state = {
                    'round_number': 1,
                    'player_team': deployed_team,
                    'world_id': 'zombie',
                    'enemies': [
                        {"id": m_id, "name": f"生化目標 {chr(65+i)}", "hp": 120, "max_hp": 120, "atk": 18, "status": "嗜血狂暴", "avatar": "images/core_idle.PNG"}
                        for i, m_id in enumerate(node_monsters)
                    ],
                    'logs': [
                        f"⚔️ 進入節點【{n_id}】！遭遇 {len(node_monsters)} 隻生化變異目標！",
                        "💡 戰鬥支援前後排站位機制，擊殺目標可獲得豐富素材與命運碎片！"
                    ],
                    'current_turn_name': '第 1 回合 · 我方行動階段',
                    'is_player_turn': True,
                    'selected_actor': None,
                    'target_mode': None,
                    'selected_skill': None
                }
                
            call screen battle_screen(b_node_state)
            z "🎉【節點清理完成】已肅清該區域所有威脅！"
            jump expression "stage_map_hub"
            
        # 2. 觸發支線劇情與智鬥
        elif act_type == "enter_side_quest":
            $ sq_id = sm_res[1]
            $ n_id = sm_res[2]
            $ st_id = sm_res[3]
            call screen side_quest_modal_screen(sq_id)
            $ sq_res = _return
            if isinstance(sq_res, tuple) and sq_res[0] == "choose_side_quest_option":
                $ is_pass = sq_res[3]
                if is_pass:
                    $ node_quest_cleared_states[n_id] = True
                    z "✨【智鬥檢定成功】成功破解核心安全協定！解鎖了隱藏資料與高階命運碎片！"
                else:
                    z "⚠️【智鬥檢定失敗】觸發了警報防衛系統！"
            jump expression "stage_map_hub"
            
    elif sm_res == "leave_stage":
        jump main_room_exploration
        
    jump main_room_exploration


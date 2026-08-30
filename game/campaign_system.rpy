# ==========================================
# 副本世界與地圖節點探索系統 (campaign_system.rpy)
# ==========================================

init python:
    # 1. 五大副本世界規格設定
    CAMPAIGN_WORLDS = {
        "zombie": {
            "name": "🟢 喪屍末日世界 · 蜂巢地下實驗室",
            "world_id": "zombie",
            "desc": "充斥著致命 T 病毒與腐蝕性生化毒氣的地下巨型生化基地。",
            "hazard_title": "⚠️ 環境危害：生化毒氣",
            "hazard_desc": "每回合結束時全體扣除 3% 生命上限。(裝備防毒面具或作戰服可完全豁免)",
            "hazard_type": "gas",
            "boss_name": "暴君 T-002 (基因突變體)",
            "boss_hp": 650,
            "boss_atk": 45,
            "shard_reward": "C"
        },
        "space": {
            "name": "🔵 太空真空世界 · 幽靈探索母艦",
            "world_id": "space",
            "desc": "失控飄浮在深空的巨型戰艦，內部無重力且艙外完全真空。",
            "hazard_title": "⚠️ 環境危害：失重真空",
            "hazard_desc": "槍械完全封印，近戰傷害降低 50%。(裝備噴射背包/飛行滑板或自帶飛行標籤可解除限制)",
            "hazard_type": "space",
            "boss_name": "異形母皇 (深空宿主)",
            "boss_hp": 750,
            "boss_atk": 50,
            "shard_reward": "B"
        },
        "paranormal": {
            "name": "🟣 靈異鬼怪世界 · 迷霧怨魂都市",
            "world_id": "paranormal",
            "desc": "被濃密陰煞黑霧籠罩的死寂都市，怨靈厲鬼在虛空中穿梭噬魂。",
            "hazard_title": "⚠️ 環境危害：幽靈虛無 & 煞氣噬魂",
            "hazard_desc": "物理/科技槍械傷害大幅降低 80%，每回合結束扣除 5 點精神力。(魔法武器與神聖/修真血統可打出全額傷害)",
            "hazard_type": "paranormal",
            "boss_name": "咒怨伽椰子 (怨念本體)",
            "boss_hp": 800,
            "boss_atk": 55,
            "shard_reward": "B"
        },
        "magic": {
            "name": "🟡 古文明魔法世界 · 太陽法老金字塔",
            "world_id": "magic",
            "desc": "埋藏在無盡黃沙之下的遠古魔導神殿，流淌著磅礡的古代奧術洪流。",
            "hazard_title": "⚠️ 環境危害：奧術共鳴 & 科技過載",
            "hazard_desc": "全體魔法技能傷害提升 30%，但純科技裝備每回合有 30% 機率短路癱瘓 1 回合。",
            "hazard_type": "magic",
            "boss_name": "亡靈大祭司·伊莫頓 (黃沙法老)",
            "boss_hp": 950,
            "boss_atk": 60,
            "shard_reward": "A"
        },
        "causality": {
            "name": "🔴 因果律世界 · 死神降臨都市",
            "world_id": "causality",
            "desc": "無形無相的死神正在編織命運鏈條，任何巧合都將化為致命殺機！",
            "hazard_title": "⚠️ 環境危害：死神因果律意外陷阱",
            "hazard_desc": "每回合結束時可能觸發隨機死神追殺判定。(開啟基因鎖洞察危險或佩戴定魂玉戒可化解)",
            "hazard_type": "causality",
            "boss_name": "死神因果化身 (命運執法者)",
            "boss_hp": 1200,
            "boss_atk": 70,
            "shard_reward": "S"
        }
    }

    # 2. 地圖節點狀態追蹤
    if 'current_campaign_world' not in globals():
        current_campaign_world = "zombie"

    if 'zombie_map_nodes_state' not in globals():
        zombie_map_nodes_state = {
            "node_gate": False,
            "node_infirmary": False,
            "node_cooling": False,
            "node_server": False,
            "node_incubation": False,
            "node_armory": False,
            "node_boss": False
        }

    # 喪屍末日地圖 7 大戰術熱點據點定義 (對接 images/zombieCityMap.jpg)
    ZOMBIE_MAP_NODES = [
        {
            "id": "node_gate",
            "name": "蜂巢生化隔離閘門",
            "type": "battle",
            "icon": "🛡️",
            "badge": "戰術前哨 · 遭遇戰",
            "badge_color": "#00ffcc",
            "x": 260,
            "y": 240,
            "desc": "蜂巢地下基地的第一道重型防線，有數隻敏捷型喪屍與變異腐屍在廢棄哨崗遊蕩！",
            "req_tip": "建議全員裝備基礎防具與武器，靈活運用近戰與射擊",
            "enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "毒素附著", "name": "變異腐屍 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "B", "status": "毒素附著", "name": "變異腐屍 B"},
                {"id": "agile_zombie", "suffix": "A", "status": "嗜血狂暴", "name": "敏捷型喪屍 A"},
                {"id": "agile_zombie", "suffix": "B", "status": "敏捷突進", "name": "敏捷型喪屍 B"}
            ],
            "repeatable_enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "毒素附著", "name": "巡邏腐屍 A"},
                {"id": "agile_zombie", "suffix": "A", "status": "敏捷突進", "name": "巡邏敏捷喪屍 A"}
            ],
            "reward_points": 400,
            "repeatable_points": 150,
            "reward_items": [{"id": "MAT_ZOMBIE_BLOOD", "name": "喪屍血液", "count": 6}, {"id": "MAT_TECH_PARTS", "name": "科技零件", "count": 3}],
            "repeatable_items": [{"id": "MAT_ZOMBIE_BLOOD", "name": "喪屍血液", "count": 3}, {"id": "MAT_TECH_PARTS", "name": "科技零件", "count": 1}]
        },
        {
            "id": "node_infirmary",
            "name": "B1 特種廢棄醫務室",
            "type": "quest",
            "icon": "💉",
            "badge": "支線劇情 · 智鬥探索",
            "badge_color": "#ffff00",
            "x": 680,
            "y": 180,
            "desc": "深埋在 B1 的密閉醫務室，高壓電子防爆鎖處於緊急鎖死狀態。內部留有珍貴的生化血清與急救噴霧！（首通獲得 C 階碎片與急救物資，支線不可重複解）",
            "req_tip": "【智者檢定】需要隊伍最高智力 (INT) >= 100 (智者可無損解鎖，否則引發警報戰鬥)",
            "req_int": 100,
            "enemies": [
                {"id": "agile_zombie", "suffix": "A", "status": "嗜血狂暴", "name": "敏捷型喪屍 A"},
                {"id": "agile_zombie", "suffix": "B", "status": "狂暴突進", "name": "敏捷型喪屍 B"},
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "毒液噴濺", "name": "變異腐屍 A"}
            ],
            "repeatable_enemies": [
                {"id": "agile_zombie", "suffix": "A", "status": "殘存遊蕩", "name": "醫務室敏捷喪屍 A"},
                {"id": "agile_zombie", "suffix": "B", "status": "嗜血狂暴", "name": "醫務室敏捷喪屍 B"}
            ],
            "reward_points": 600,
            "repeatable_points": 200,
            "reward_shard": "C",
            "reward_items": [{"id": "item_heal_spray", "name": "輪迴止血急救噴霧", "count": 2}, {"id": "MAT_ZOMBIE_BLOOD", "name": "高純度喪屍血清", "count": 10}],
            "repeatable_items": [{"id": "MAT_ZOMBIE_BLOOD", "name": "喪屍血液", "count": 4}]
        },
        {
            "id": "node_cooling",
            "name": "地下毒氣冷卻管道區",
            "type": "battle",
            "icon": "💨",
            "badge": "支線戰役 · 管道伏擊",
            "badge_color": "#ff9900",
            "x": 280,
            "y": 660,
            "desc": "濃煙滾滾的生化冷卻走廊，酸性毒氣不斷洩漏。3 隻高敏捷型喪屍正倒吊在管道上方伺機撲殺！",
            "req_tip": "建議穿戴【tactical_hazmat_armor 戰術服】以免疫每回合毒氣扣血",
            "enemies": [
                {"id": "agile_zombie", "suffix": "A", "status": "暗處潛行", "name": "管道突變體 A"},
                {"id": "agile_zombie", "suffix": "B", "status": "致命飛撲", "name": "管道突變體 B"},
                {"id": "agile_zombie", "suffix": "C", "status": "嗜血狂暴", "name": "管道突變體 C"}
            ],
            "repeatable_enemies": [
                {"id": "agile_zombie", "suffix": "A", "status": "管道潛行", "name": "管道敏捷喪屍 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "毒素附著", "name": "管道變異腐屍 A"}
            ],
            "reward_points": 500,
            "repeatable_points": 200,
            "reward_shard": "D",
            "reward_items": [{"id": "MAT_TECH_PARTS", "name": "防毒過濾模組零件", "count": 5}],
            "repeatable_items": [{"id": "MAT_TECH_PARTS", "name": "科技零件", "count": 2}]
        },
        {
            "id": "node_server",
            "name": "中央主控機房 (A.D.A.M. 核心)",
            "type": "quest",
            "icon": "🧠",
            "badge": "核心支線 · 智者入侵",
            "badge_color": "#ddaaff",
            "x": 960,
            "y": 360,
            "desc": "極光重工中央生物神經網絡主機。深層伺服器內封存著最高機密軍火藍圖與 AI 矩陣原始碼！（首通獲得亞當核心，支線不可重複解）",
            "req_tip": "【黑客/智者檢定】需要隊伍最高智力 (INT) >= 100",
            "req_int": 100,
            "enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "重裝防禦", "name": "機房生化守衛 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "B", "status": "毒素附著", "name": "機房生化守衛 B"},
                {"id": "agile_zombie", "suffix": "A", "status": "致命突進", "name": "機房敏捷守衛 A"}
            ],
            "repeatable_enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "巡邏警戒", "name": "機房守衛 A"},
                {"id": "agile_zombie", "suffix": "A", "status": "暗處潛行", "name": "機房敏捷守衛 A"}
            ],
            "reward_points": 1000,
            "repeatable_points": 250,
            "reward_shard": "B",
            "reward_items": [{"id": "ITEM_HIVE_AI_BACKUP", "name": "亞當神經元矩陣備份", "count": 1}, {"id": "MAT_TECH_PARTS", "name": "高階超導晶片", "count": 8}],
            "repeatable_items": [{"id": "MAT_TECH_PARTS", "name": "科技零件", "count": 3}]
        },
        {
            "id": "node_incubation",
            "name": "生化培育溫室 (狂暴刷怪區)",
            "type": "farming",
            "icon": "🔥",
            "badge": "狂暴刷怪 · 素材產出",
            "badge_color": "#ff4444",
            "x": 1420,
            "y": 240,
            "desc": "巨大的生化玻璃培養槽早已破碎，大量變異腐屍在營養液池中源源不絕地爬出，是收集素材的最佳地點！",
            "req_tip": "群怪密集，建議使用【high_explosive 高爆破片手雷】進行全體轟炸",
            "enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "毒素附著", "name": "培養體腐屍 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "B", "status": "毒素附著", "name": "培養體腐屍 B"},
                {"id": "MOB_ZOMBIE_01", "suffix": "C", "status": "嗜血狂化", "name": "培養體腐屍 C"},
                {"id": "agile_zombie", "suffix": "A", "status": "嗜血突擊", "name": "突變敏捷喪屍 A"},
                {"id": "agile_zombie", "suffix": "B", "status": "敏捷撲咬", "name": "突變敏捷喪屍 B"}
            ],
            "repeatable_enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "毒素附著", "name": "培養槽腐屍 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "B", "status": "毒素附著", "name": "培養槽腐屍 B"},
                {"id": "agile_zombie", "suffix": "A", "status": "嗜血突擊", "name": "培養槽敏捷喪屍 A"}
            ],
            "reward_points": 600,
            "repeatable_points": 300,
            "reward_items": [{"id": "MAT_ZOMBIE_BLOOD", "name": "大量喪屍血液", "count": 12}, {"id": "MAT_TECH_PARTS", "name": "廢棄科技組件", "count": 6}],
            "repeatable_items": [{"id": "MAT_ZOMBIE_BLOOD", "name": "喪屍血液", "count": 8}, {"id": "MAT_TECH_PARTS", "name": "科技零件", "count": 3}]
        },
        {
            "id": "node_armory",
            "name": "地下軍火管制庫",
            "type": "quest",
            "icon": "🎒",
            "badge": "戰術搜刮 · 軍火補給",
            "badge_color": "#66ff66",
            "x": 680,
            "y": 720,
            "desc": "極光重工安保清理隊的地下戰術裝備庫，防爆密碼鎖隱藏在牆壁銘牌之中。（首通搜刮獲得高爆破片手雷，不可重複搜刮）",
            "req_tip": "搜刮完畢後周圍有遊蕩腐屍出沒",
            "enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "遊蕩警戒", "name": "軍火庫腐屍 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "B", "status": "毒素附著", "name": "軍火庫腐屍 B"}
            ],
            "repeatable_enemies": [
                {"id": "MOB_ZOMBIE_01", "suffix": "A", "status": "遊蕩警戒", "name": "軍火庫腐屍 A"},
                {"id": "MOB_ZOMBIE_01", "suffix": "B", "status": "毒素附著", "name": "軍火庫腐屍 B"}
            ],
            "reward_points": 500,
            "repeatable_points": 150,
            "reward_items": [{"id": "high_explosive", "name": "high_explosive 高爆破片手雷", "count": 2}, {"id": "item_grenade", "name": "高爆破片手榴彈", "count": 2}],
            "repeatable_items": [{"id": "MAT_TECH_PARTS", "name": "科技零件", "count": 2}]
        },
        {
            "id": "node_boss",
            "name": "深層生物重裝試驗場 (暴君領主決戰)",
            "type": "boss",
            "icon": "☠️",
            "badge": "終極領主 · 暴君決戰",
            "badge_color": "#ff0033",
            "x": 1500,
            "y": 720,
            "desc": "浸泡在深層防腐液中的終極生化兵器——暴君 T-002 原型機！擁有極高的物理防禦與毀滅性重拳！（首殺獲得心臟標本與重裝戰術服）",
            "req_tip": "👑 終極首領戰！請確保全隊血量充足，裝備高階武器並備好急救噴霧",
            "enemies": [
                {"id": "MOB_TYRANT_01", "suffix": "", "status": "重裝霸體", "name": "👑 暴君 T-002 原型機"},
                {"id": "agile_zombie", "suffix": "護衛 A", "status": "致命突進", "name": "暴君親衛·敏捷喪屍 A"},
                {"id": "agile_zombie", "suffix": "護衛 B", "status": "嗜血狂暴", "name": "暴君親衛·敏捷喪屍 B"}
            ],
            "repeatable_enemies": [
                {"id": "MOB_TYRANT_01", "suffix": "殘影", "status": "重裝霸體", "name": "暴君 T-002 突變殘影"},
                {"id": "agile_zombie", "suffix": "A", "status": "致命突進", "name": "敏捷喪屍護衛 A"}
            ],
            "reward_points": 2000,
            "repeatable_points": 500,
            "reward_shard": "C",
            "reward_items": [{"id": "ITEM_TYRANT_HEART", "name": "極光暴君生化心臟標本", "count": 1}, {"id": "EQ_TECH_ARMOR_02", "name": "全封閉重裝生化作戰服", "count": 1}],
            "repeatable_items": [{"id": "MAT_ZOMBIE_BLOOD", "name": "高濃度喪屍血液", "count": 8}, {"id": "MAT_TECH_PARTS", "name": "高階合金零件", "count": 4}]
        }
    ]

    def reset_campaign_nodes():
        global campaign_nodes_state
        campaign_nodes_state = {
            "main_cleared": False,
            "shard_cleared": False,
            "riddle_cleared": False,
            "boss_unlocked": False
        }

    # 3. 依據主線劇情通關進度動態過濾已解鎖的世界 (未通關的世界完全隱藏)
    def get_unlocked_campaign_worlds():
        cur_idx = current_main_stage_index if 'current_main_stage_index' in globals() else 1
        world_rules = [
            ("zombie", 1),       # 第一世界 (基礎開啟)
            ("space", 3),        # 第二世界 (需通關太空母艦主線，cur_idx >= 3)
            ("paranormal", 4),   # 第三世界 (需通關咒怨凶宅主線，cur_idx >= 4)
            ("magic", 5),        # 第四世界 (需通關蜀山主線，cur_idx >= 5)
            ("causality", 6)     # 第五世界 (需通關印洲隊團戰主線，cur_idx >= 6)
        ]
        unlocked = []
        for w_key, req_idx in world_rules:
            if cur_idx >= req_idx:
                unlocked.append(w_key)
        return unlocked if unlocked else ["zombie"]

    # 4. 檢查隊伍環境懲罰豁免狀態
    def check_team_hazards(world_id):
        world = CAMPAIGN_WORLDS.get(world_id, CAMPAIGN_WORLDS["zombie"])
        h_type = world.get("hazard_type")
        roster = get_team_roster()
        player = roster[0] if roster else {}
        
        has_gas_mask = is_gas_immune(player) if 'is_gas_immune' in globals() else False
        has_flight = has_flight_capability(player) if 'has_flight_capability' in globals() else False
        has_magic = has_magic_damage(player) if 'has_magic_damage' in globals() else False
        has_lock = player.get("gene_lock", 0) > 0
        
        status = {
            "hazard_title": world.get("hazard_title", ""),
            "hazard_desc": world.get("hazard_desc", ""),
            "is_immune": False,
            "mitigation_msg": ""
        }
        
        if h_type == "gas":
            if has_gas_mask:
                status["is_immune"] = True
                status["mitigation_msg"] = "🛡️ 已裝備【防毒面具/全封閉作戰服】，生化毒氣完全無效！"
            else:
                status["is_immune"] = False
                status["mitigation_msg"] = "⚠️ 未配戴防毒裝備，每回合將損失 3% 生命值！"
                
        elif h_type == "space":
            if has_flight:
                status["is_immune"] = True
                status["mitigation_msg"] = "🚀 已裝備【噴射背包/飛行載具/自帶翅膀】，真空失重限制已解除！"
            else:
                status["is_immune"] = False
                status["mitigation_msg"] = "⚠️ 無飛行裝備，槍械遭到封印且近戰傷害減半！"
                
        elif h_type == "paranormal":
            if has_magic:
                status["is_immune"] = True
                status["mitigation_msg"] = "✨ 已裝備【魔法打擊武器/修真/神聖血統】，可對幽魂造成 100% 全額破煞傷害！"
            else:
                status["is_immune"] = False
                status["mitigation_msg"] = "⚠️ 未裝備魔法打擊，常規物理傷害將被幽魂削弱 80%！"
                
        elif h_type == "magic":
            status["is_immune"] = False
            status["mitigation_msg"] = "🔮 奧術洪流加持：魔法傷害 +30%，純科技設備每回合 30% 機率過載。"
            
        elif h_type == "causality":
            if has_lock:
                status["is_immune"] = True
                status["mitigation_msg"] = "🧬 基因鎖已開啟，敏銳預判並破除死神意外陷阱！"
            else:
                status["is_immune"] = False
                status["mitigation_msg"] = "⚠️ 死神凝視中，每回合有機率遭遇致命意外傷害！"
                
        return status


# ==========================================
# 副本世界選擇介面 (campaign_world_select_screen)
# ==========================================
screen campaign_world_select_screen():

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1700, 920)
        padding (35, 30)
        background "#0d111efa"

        vbox:
            spacing 15
            xalign 0.5

            text "【 🚪 輪迴傳送光門 · 副本世界自由探索 】" size 26 color "#ffcc00" bold True xalign 0.5
            text "已通關的輪迴世界可自由進入探索支線、解謎與刷取命運碎片（未通關的世界已隱藏）。" size 16 color "#bbbbbb" xalign 0.5

            null height 5

            $ unlocked_list = get_unlocked_campaign_worlds()

            hbox:
                spacing 25
                xalign 0.5
                box_wrap True

                for w_key in unlocked_list:
                    $ w_info = CAMPAIGN_WORLDS[w_key]
                    $ w_name = w_info.get("name")
                    $ w_desc = w_info.get("desc")
                    $ w_haz = w_info.get("hazard_title")
                    $ w_hdesc = w_info.get("hazard_desc")
                    $ w_boss = w_info.get("boss_name")
                    $ w_shard = w_info.get("shard_reward")

                    button:
                        xysize (510, 310)
                        background "#192238"
                        hover_background "#2a3960"
                        padding (20, 15)
                        action Return(("select_world", w_key))

                        vbox:
                            spacing 6
                            text "[w_name]" size 19 color "#00ffff" bold True
                            text "[w_desc]" size 13 color "#cccccc"
                            
                            null height 2
                            text "[w_haz]" size 14 color "#ff6666" bold True
                            text "[w_hdesc]" size 12 color "#ffaaaa"
                            
                            null height 2
                            text f"👹 終極領主：{w_boss}" size 13 color "#ffaa00"
                            text f"💎 通關獎勵：{w_shard} 階命運碎片 + 2000 點數" size 13 color "#66ff66" bold True
                            
                            null height 5
                            text "【 ⚡ 點擊鎖定座標傳送 】" size 14 color "#ffff00" bold True xalign 0.5

            null height 10

            textbutton "【 🚪 取消傳送，返回輪迴廣場 】":
                xalign 0.5
                action Return("cancel")
                text_size 20
                text_idle_color "#ff4444"
                text_hover_color "#ff8888"


# ==========================================
# 副本世界節點地圖探索畫面 (campaign_map_screen)
# ==========================================
screen campaign_map_screen():

    $ w_info = CAMPAIGN_WORLDS.get(current_campaign_world, CAMPAIGN_WORLDS["zombie"])
    $ w_name = w_info.get("name")
    $ haz_status = check_team_hazards(current_campaign_world)
    $ scale, alive_rookie_cnt = get_dynamic_difficulty_scale() if 'get_dynamic_difficulty_scale' in globals() else (1.0, 0)
    $ player = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]

    window:
        background "#05070ddd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1720, 960)
        padding (30, 25)
        background "#0d121ff2"

        vbox:
            spacing 12
            xalign 0.5

            # 頂部世界標題與環境警報列
            hbox:
                spacing 30
                xalign 0.5
                text "[w_name]" size 24 color "#00ffff" bold True yalign 0.5
                text f"難度係數：{int(scale*100)}% (存活新人: {alive_rookie_cnt}人)" size 17 color ("#ffaa00" if alive_rookie_cnt > 0 else "#66ff66") bold True yalign 0.5
                text f"隊長 HP：{player.get('hp',100)}/{player.get('max_hp',100)}" size 17 color "#ff6666" yalign 0.5
                text f"個人點數：{points} 點" size 17 color "#00ffcc" yalign 0.5

            # 環境危害與抵抗狀態通知條
            frame:
                xysize (1660, 50)
                background ("#221111ee" if not haz_status["is_immune"] else "#112211ee")
                padding (15, 10)
                hbox:
                    spacing 20
                    yalign 0.5
                    text "[haz_status['hazard_title']]" size 15 color ("#ff4444" if not haz_status["is_immune"] else "#66ff66") bold True
                    text "[haz_status['mitigation_msg']]" size 14 color "#ffffff"

            null height 10

            # --------------------------------
            # 地圖 5 大節點探索區域
            # --------------------------------
            text "【 🗺️ 副本自由戰術節點地圖 (請點選目標據點展開行動) 】" size 19 color "#ffcc00" bold True xalign 0.5

            hbox:
                spacing 25
                xalign 0.5

                # 節點 1：主線據點
                $ main_done = campaign_nodes_state.get("main_cleared", False)
                frame:
                    xysize (315, 600)
                    background "#1b253daa"
                    padding (15, 15)
                    vbox:
                        spacing 10
                        text "🚩 節點 1：主線據點" size 18 color "#00ffff" bold True
                        text "【前鋒突破防線】" size 15 color "#ffaa00"
                        text "擊破前哨警戒部隊，推進主線核心進度並解鎖後續探索據點。" size 13 color "#cccccc"
                        null height 15
                        if main_done:
                            text "✅ 已完全肅清" size 16 color "#66ff66" bold True xalign 0.5
                        else:
                            text "⚠️ 敵方駐守中" size 15 color "#ff4444" xalign 0.5
                            null height 180
                            button:
                                xysize (285, 55)
                                background "#2d5e38"
                                hover_background "#3e824e"
                                action Return(("enter_node", "main"))
                                text "⚔️ 發動突擊戰鬥" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

                # 節點 2：命運碎片據點
                $ shard_done = campaign_nodes_state.get("shard_cleared", False)
                frame:
                    xysize (315, 600)
                    background "#1b253daa"
                    padding (15, 15)
                    vbox:
                        spacing 10
                        text "💎 節點 2：碎片據點" size 18 color "#ddaaff" bold True
                        text "【精英試煉重地】" size 15 color "#ffaa00"
                        text "高危險度精英巢穴。擊敗精英鎮守者可直接掠奪高階命運碎片！" size 13 color "#cccccc"
                        null height 15
                        if shard_done:
                            text "✅ 碎片已搜刮" size 16 color "#66ff66" bold True xalign 0.5
                        else:
                            text "🔥 精英怪盤踞" size 15 color "#ff6666" xalign 0.5
                            null height 180
                            button:
                                xysize (285, 55)
                                background "#5e2d5e"
                                hover_background "#843e84"
                                action Return(("enter_node", "shard"))
                                text "⚔️ 挑戰精英強敵" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

                # 節點 3：NPC 智鬥/謎題據點
                $ riddle_done = campaign_nodes_state.get("riddle_cleared", False)
                frame:
                    xysize (315, 600)
                    background "#1b253daa"
                    padding (15, 15)
                    vbox:
                        spacing 10
                        text "🧠 節點 3：智鬥據點" size 18 color "#ffff66" bold True
                        text "【古老機關密室】" size 15 color "#ffaa00"
                        text "考驗智慧與推演。若隊伍有【智者 (Scholar)】新人可獲得專屬破局錦囊！" size 13 color "#cccccc"
                        null height 15
                        if riddle_done:
                            text "✅ 機關已破解" size 16 color "#66ff66" bold True xalign 0.5
                        else:
                            text "❓ 機關運轉中" size 15 color "#ffff00" xalign 0.5
                            null height 180
                            button:
                                xysize (285, 55)
                                background "#665e2d"
                                hover_background "#8f843e"
                                action Return(("enter_node", "riddle"))
                                text "🧩 進行智鬥推演" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

                # 節點 4：物資補給點
                frame:
                    xysize (315, 600)
                    background "#1b253daa"
                    padding (15, 15)
                    vbox:
                        spacing 10
                        text "🏪 節點 4：補給據點" size 18 color "#66ff66" bold True
                        text "【野外應急安全屋】" size 15 color "#ffaa00"
                        text "在殘酷戰場中暫時喘息，可直接購買應急止血噴霧、精神穩定劑與手榴彈。" size 13 color "#cccccc"
                        null height 15
                        text "🟢 安全屋運作中" size 15 color "#66ff66" xalign 0.5
                        null height 180
                        button:
                            xysize (285, 55)
                            background "#224455"
                            hover_background "#336688"
                            action Return(("enter_node", "supply"))
                            text "🛒 進入野外補給" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

                # 節點 5：最終領主決戰
                frame:
                    xysize (315, 600)
                    background "#2d1b1baa"
                    padding (15, 15)
                    vbox:
                        spacing 10
                        text "👹 節點 5：領主決戰" size 18 color "#ff4444" bold True
                        text f"【{w_info.get('boss_name')}】" size 14 color "#ffaaaa"
                        text "迎戰本世界最終首領！勝利後發放全額結算點數與命運碎片並回歸輪迴空間！" size 13 color "#cccccc"
                        null height 15
                        text f"HP: {w_info.get('boss_hp')} | ATK: {w_info.get('boss_atk')}" size 14 color "#ff6666" xalign 0.5
                        null height 180
                        button:
                            xysize (285, 55)
                            background "#7a1b1b"
                            hover_background "#a82424"
                            action Return(("enter_node", "boss"))
                            text "☠️ 挑戰終極領主" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

            null height 5

            # 返回輪迴空間按鈕
            textbutton "【 🚪 放棄探索，返回輪迴空間廣場 】":
                xalign 0.5
                action Return("return_hub")
                text_size 19
                text_idle_color "#ff4444"
                text_hover_color "#ff8888"


# ==========================================
# 喪屍末日專屬戰術地圖畫面 (zombie_city_map_screen)
# 使用 images/zombieCityMap.jpg 全圖背景與可點擊互動據點
# ==========================================
screen zombie_city_map_screen():

    default selected_node_id = None

    # 1. 全螢幕戰術地圖背景
    add "images/zombieCityMap.jpg" xsize 1920 ysize 1080

    # 2. 頂部賽博全息 HUD 狀態欄與右上角顯眼返回按鈕
    $ max_int = get_team_max_int() if 'get_team_max_int' in globals() else 20
    $ player = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]
    $ p_hp = player.get('hp', 100)
    $ p_max_hp = player.get('max_hp', 100)

    # 頂部戰況數值欄
    frame:
        xpos 30 ypos 20
        xysize (1480, 65)
        background "#050b18f0"
        padding (25, 10)

        hbox:
            spacing 25
            yalign 0.5

            text "【 🗺️ 極光重工遺址 · 喪屍末日戰術地圖 】" size 20 color "#00ffff" bold True yalign 0.5
            text f"🧬 隊長生命: {p_hp}/{p_max_hp}" size 16 color ("#66ff66" if p_hp > 50 else "#ff4444") bold True yalign 0.5
            text f"🧠 隊伍最高智力: {max_int}" size 16 color "#ffcc00" bold True yalign 0.5
            text f"💎 個人點數: {points} 點" size 16 color "#00ffcc" bold True yalign 0.5

    # 右上角高亮常駐返回輪迴空間按鈕
    button:
        xpos 1530 ypos 20
        xysize (360, 65)
        background "#8f2222fa"
        hover_background "#c42d2dfa"
        action Return("return_hub")

        hbox:
            xalign 0.5 yalign 0.5
            spacing 10
            text "🚪" size 22 yalign 0.5
            text "返回輪迴空間廣場" size 18 color "#ffffff" bold True yalign 0.5

    # 底部中央常駐返回輪迴空間按鈕
    button:
        xalign 0.5 ypos 1015
        xysize (620, 50)
        background "#050b18ee"
        hover_background "#1a2c4fee"
        action Return("return_hub")

        hbox:
            xalign 0.5 yalign 0.5
            spacing 10
            text "🌌" size 18 yalign 0.5
            text "【 🚪 退出當前地圖 · 安全返回輪迴空間廣場 】" size 17 color "#ff7777" bold True yalign 0.5

    # 3. 地圖上的 7 大戰術互動據點 Hotspots
    for node in ZOMBIE_MAP_NODES:
        $ n_id = node["id"]
        $ n_name = node["name"]
        $ n_icon = node["icon"]
        $ n_badge = node["badge"]
        $ n_bcolor = node["badge_color"]
        $ n_x = node["x"]
        $ n_y = node["y"]
        $ is_cleared = zombie_map_nodes_state.get(n_id, False)

        # 戰術點位標記 Frame (帶發光與懸浮互動)
        button:
            pos (n_x, n_y)
            background ("#0d1d36ea" if not is_cleared else "#0b261aea")
            hover_background ("#1a3a6cea" if not is_cleared else "#144732ea")
            padding (10, 8)
            action SetScreenVariable("selected_node_id", n_id)

            hbox:
                spacing 8
                yalign 0.5
                text f"{n_icon}" size 22 yalign 0.5
                vbox:
                    spacing 2
                    text f"{n_name}" size 14 color ("#ffffff" if not is_cleared else "#aaffaa") bold True
                    hbox:
                        spacing 6
                        text f"{n_badge}" size 11 color n_bcolor
                        if is_cleared:
                            text "【✅ 已肅清】" size 11 color "#66ff66" bold True
                        else:
                            text "【⚠️ 可探索】" size 11 color "#ffcc00" bold True

    # 4. 點選某個據點時彈出的【戰術情報簡報浮窗】
    if selected_node_id:
        $ cur_node = next((n for n in ZOMBIE_MAP_NODES if n["id"] == selected_node_id), None)
        if cur_node:
            $ is_n_cleared = zombie_map_nodes_state.get(cur_node["id"], False)
            frame:
                xalign 0.5 yalign 0.5
                xysize (780, 540)
                background "#060e1dfc"
                padding (30, 25)

                vbox:
                    spacing 12
                    xalign 0.5

                    # 標題欄
                    hbox:
                        spacing 15
                        xalign 0.5
                        if is_n_cleared:
                            text f"{cur_node['icon']} {cur_node['name']}" size 22 color "#66ff66" bold True
                            text "【✅ 已肅清】" size 14 color "#66ff66" bold True yalign 0.5
                        else:
                            text f"{cur_node['icon']} {cur_node['name']}" size 22 color "#00ffff" bold True
                            text f"{cur_node['badge']}" size 14 color cur_node['badge_color'] bold True yalign 0.5

                    # 分隔線
                    frame:
                        xysize (720, 2)
                        background "#00ffff55"

                    if is_n_cleared:
                        # 已肅清時：明確標註不可重複解任務，只顯示刷新怪群資訊
                        text "【✅ 該據點支線劇情與密室已探索完結，不可重複解支線任務】" size 14 color "#66ff66" bold True
                        text "【⚠️ 當前僅有區域巡邏刷新怪群可進行戰術刷怪，擊殺可收集基礎素材】" size 13 color "#ffaa00"

                        null height 2

                        # 刷新怪物清單卡片
                        frame:
                            xysize (720, 115)
                            background "#181020ee"
                            padding (15, 10)
                            vbox:
                                spacing 5
                                text "🧟 區域盤踞刷新怪物情報 (可反覆掃蕩)：" size 14 color "#ff9999" bold True
                                $ r_enemies = cur_node.get('repeatable_enemies', cur_node.get('enemies', []))
                                hbox:
                                    spacing 15
                                    for e_info in r_enemies:
                                        $ e_disp_name = e_info.get('name', e_info['id'])
                                        $ e_stat = e_info.get('status', '警戒')
                                        text f"• {e_disp_name} ({e_stat})" size 13 color "#ffcccc"
                                
                                null height 2
                                hbox:
                                    spacing 20
                                    text f"• 擊殺預期點數: +{cur_node.get('repeatable_points', 150)} 點" size 12 color "#ffaa00"
                                    if 'repeatable_items' in cur_node:
                                        $ itm_strs = [f"{it['name']} x{it['count']}" for it in cur_node['repeatable_items']]
                                        text f"• 掉落素材: {', '.join(itm_strs)}" size 12 color "#aaffaa"

                        null height 20

                        # 操作按鈕列 (僅允許刷怪或關閉)
                        hbox:
                            spacing 25
                            xalign 0.5

                            button:
                                xysize (260, 50)
                                background "#245e33"
                                hover_background "#358a4b"
                                action Return(("action_battle", cur_node["id"]))
                                text "⚔️ 掃蕩刷新怪群" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

                            button:
                                xysize (180, 50)
                                background "#333344"
                                hover_background "#555566"
                                action SetScreenVariable("selected_node_id", None)
                                text "❌ 關閉簡報" size 15 color "#ffffff" xalign 0.5 yalign 0.5

                    else:
                        # 未肅清時：顯示首通支線、智者檢定與獨特獎勵
                        text f"{cur_node['desc']}" size 15 color "#dddddd"
                        text f"💡 戰術提示：{cur_node['req_tip']}" size 13 color "#ffcc00"

                        null height 5

                        # 獎勵預覽
                        frame:
                            xysize (720, 85)
                            background "#121d30"
                            padding (12, 8)
                            vbox:
                                spacing 4
                                text "🎁 首通探索與通關預期獎勵：" size 13 color "#00ffcc" bold True
                                hbox:
                                    spacing 20
                                    text f"• 生存點數: +{cur_node['reward_points']} 點" size 13 color "#ffaa00"
                                    if 'reward_shard' in cur_node:
                                        text f"• 命運碎片: {cur_node['reward_shard']} 階 x1" size 13 color "#ddaaff" bold True
                                    if 'reward_items' in cur_node:
                                        $ itm_names = [f"{it['name']} x{it['count']}" for it in cur_node['reward_items']]
                                        text f"• 道具/素材: {', '.join(itm_names)}" size 12 color "#aaffaa"

                        null height 15

                        # 操作按鈕列
                        hbox:
                            spacing 20
                            xalign 0.5

                            if cur_node["type"] == "quest":
                                button:
                                    xysize (240, 50)
                                    background "#8a6d1a"
                                    hover_background "#b38f24"
                                    action Return(("action_quest", cur_node["id"]))
                                    text "🧩 展開支線與智鬥" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5
                            elif cur_node["type"] in ("battle", "farming"):
                                button:
                                    xysize (240, 50)
                                    background "#245e33"
                                    hover_background "#358a4b"
                                    action Return(("action_battle", cur_node["id"]))
                                    text "⚔️ 進入掃蕩戰鬥" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5
                            elif cur_node["type"] == "boss":
                                button:
                                    xysize (240, 50)
                                    background "#7a1b1b"
                                    hover_background "#a82424"
                                    action Return(("action_battle", cur_node["id"]))
                                    text "☠️ 挑戰暴君領主" size 16 color "#ffffff" bold True xalign 0.5 yalign 0.5

                            button:
                                xysize (180, 50)
                                background "#333344"
                                hover_background "#555566"
                                action SetScreenVariable("selected_node_id", None)
                                text "❌ 關閉簡報" size 15 color "#ffffff" xalign 0.5 yalign 0.5


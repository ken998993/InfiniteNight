# ==========================================
# 新人隨機生成與道德抉擇系統 (rookie_system.rpy)
# ==========================================

init python:
    import random

    # 不重複姓名庫
    ROOKIE_NAME_POOL = [
        "陳浩", "林依婷", "張偉", "李欣", "王強", "趙雅", 
        "劉峰", "孫麗", "何志強", "周婷婷", "郭磊", "徐菲", 
        "朱明", "楊雪", "潘勇", "韓梅", "董天明", "馮靜"
    ]

    if 'used_rookie_names' not in globals():
        used_rookie_names = set()

    # 生成 2 名隨機新人
    def generate_campaign_rookies(count=2):
        global used_rookie_names
        available_names = [n for n in ROOKIE_NAME_POOL if n not in used_rookie_names]
        if len(available_names) < count:
            used_rookie_names.clear()
            available_names = list(ROOKIE_NAME_POOL)
            
        selected_names = random.sample(available_names, count)
        for n in selected_names:
            used_rookie_names.add(n)
            
        classes = ["Tank", "Scholar", "Attacker"]
        generated = []
        
        for name in selected_names:
            c_type = random.choice(classes)
            if c_type == "Tank":
                r_dict = {
                    "name": name,
                    "role": "新人·防禦坦克 (Tank)",
                    "combat_role": "前排扛傷 / 嘲諷護衛",
                    "class_type": "Tank",
                    "bloodline": "無",
                    "avatar": "images/core_idle.PNG",
                    "points": 0,
                    "hp": 180, "max_hp": 180,
                    "mp": 30, "max_mp": 30,
                    "atk_bonus": 0,
                    "gene_lock": 0, "survival_pressure": 0,
                    "status": "良好",
                    "is_rookie": True,
                    "skills": [
                        {
                            "id": "tank_guard",
                            "name": "鋼鐵壁壘嘲諷",
                            "energy_type": "mp",
                            "energy_cost": 10,
                            "damage": 0,
                            "heal": 40,
                            "is_heal": True,
                            "desc": "吸引敵方火力並進入高額減傷防禦姿態，回復自身 40 HP。"
                        }
                    ],
                    "desc": "剛被傳送到輪迴世界的新人，體格壯碩，具有天然的肉體防禦潛能。"
                }
            elif c_type == "Scholar":
                r_dict = {
                    "name": name,
                    "role": "新人·智者戰術家 (Scholar)",
                    "combat_role": "戰術推演 / 機關破局",
                    "class_type": "Scholar",
                    "bloodline": "無",
                    "avatar": "images/core_idle.PNG",
                    "points": 0,
                    "hp": 90, "max_hp": 90,
                    "mp": 100, "max_mp": 100,
                    "atk_bonus": 0,
                    "gene_lock": 0, "survival_pressure": 0,
                    "status": "良好",
                    "is_rookie": True,
                    "skills": [
                        {
                            "id": "scholar_analyze",
                            "name": "戰術弱點標記",
                            "energy_type": "mp",
                            "energy_cost": 15,
                            "damage": 75,
                            "heal": 0,
                            "desc": "以超凡直覺洞察敵方要害，造成 75 點真實弱點穿透傷害。"
                        }
                    ],
                    "desc": "思維縝密的名校高材生，能在地圖智鬥與謎題據點提供破局錦囊提示。"
                }
            else: # Attacker
                r_dict = {
                    "name": name,
                    "role": "新人·重裝突擊手 (Attacker)",
                    "combat_role": "高額爆發 / 火力壓制",
                    "class_type": "Attacker",
                    "bloodline": "無",
                    "avatar": "images/core_idle.PNG",
                    "points": 0,
                    "hp": 120, "max_hp": 120,
                    "mp": 40, "max_mp": 40,
                    "atk_bonus": 20,
                    "gene_lock": 0, "survival_pressure": 0,
                    "status": "良好",
                    "is_rookie": True,
                    "skills": [
                        {
                            "id": "attacker_burst",
                            "name": "致命弱點連射",
                            "energy_type": "mp",
                            "energy_cost": 15,
                            "damage": 115,
                            "heal": 0,
                            "desc": "以特種步槍連續傾瀉火力，造成 115 點高額物理傷害。"
                        }
                    ],
                    "desc": "退役特戰隊員，精通槍械射擊與近身肉搏，具備極強的單兵輸出能力。"
                }
            generated.append(r_dict)
            
        return generated

    # 檢查隊伍中是否有存活的智者 (Scholar)
    def has_alive_scholar():
        roster = get_team_roster()
        for m in roster:
            if m.get("hp", 0) > 0 and (m.get("class_type") == "Scholar" or "Scholar" in m.get("role", "")):
                return True
        return False

    # 計算當前動態難度增幅 (每多 1 名存活新人，副本敵方 HP 與 ATK +15%)
    def get_dynamic_difficulty_scale():
        roster = get_team_roster()
        alive_rookies = [m for m in roster if m.get("is_rookie", False) and m.get("hp", 0) > 0]
        count = len(alive_rookies)
        scale = 1.0 + (count * 0.15)
        return scale, count


# ==========================================
# 新人降臨與道德抉擇介面 (rookie_dilemma_screen)
# ==========================================
screen rookie_dilemma_screen(rookies):

    window:
        background "#000000ee"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1600, 880)
        padding (35, 30)
        background "#0f1424fa"

        vbox:
            spacing 15
            xalign 0.5

            # 標題
            text "【 ⚠️ 輪迴空間 · 新人傳送降臨與命運抉擇 】" size 26 color "#ffcc00" bold True xalign 0.5
            text "地面上一陣白光閃爍，兩名滿臉迷茫、驚恐萬狀的新人被強行傳送到了恐怖片副本起點！" size 16 color "#cccccc" xalign 0.5

            null height 5

            # 兩名新人資訊卡片
            hbox:
                spacing 40
                xalign 0.5

                for r in rookies:
                    $ r_name = r.get("name", "新人")
                    $ r_role = r.get("role", "職階")
                    $ r_hp = r.get("max_hp", 100)
                    $ r_mp = r.get("max_mp", 50)
                    $ r_atk = r.get("atk_bonus", 0)
                    $ r_desc = r.get("desc", "")
                    $ r_ctype = r.get("class_type", "Tank")
                    
                    $ type_color = "#ff6666" if r_ctype == "Attacker" else ("#00ffff" if r_ctype == "Scholar" else "#66ff66")
                    $ type_icon = "⚔️" if r_ctype == "Attacker" else ("🧠" if r_ctype == "Scholar" else "🛡️")

                    frame:
                        xysize (720, 360)
                        background "#1a2238ee"
                        padding (15, 12)

                        hbox:
                            spacing 15

                            # 新人頭像 (預設 core_idle.PNG)
                            frame:
                                xysize (130, 330)
                                background "#101626cc"
                                padding (4, 4)
                                vbox:
                                    xalign 0.5 yalign 0.5
                                    spacing 6
                                    $ r_av = r.get('avatar', 'images/core_idle.PNG')
                                    add r_av xysize (120, 270) xalign 0.5 yalign 0.5
                                    text f"{type_icon} {r_name}" size 14 color "#ffffff" bold True xalign 0.5

                            # 右側資訊
                            vbox:
                                spacing 8
                                xysize (540, 330)
                                hbox:
                                    spacing 15
                                    text "[type_icon] [r_name]" size 21 color "#ffffff" bold True
                                    text "[r_role]" size 15 color type_color bold True yalign 0.5

                                text "【 初始戰鬥屬性 】" size 14 color "#ffaa00" bold True
                                hbox:
                                    spacing 20
                                    text f"生命值: {r_hp}" size 13 color "#ff6666"
                                    text f"精神力: {r_mp}" size 13 color "#66ccff"
                                    if r_atk > 0:
                                        text f"攻擊力加成: +{r_atk}" size 13 color "#ffaa00"

                                text "【 職階特性與背景 】" size 14 color "#00ffcc" bold True
                                text "[r_desc]" size 13 color "#dddddd"

                                if r_ctype == "Scholar":
                                    text "💡 核心優勢：在地圖【智鬥謎題據點】中提供專屬破解提示！" size 12 color "#ffff66" bold True
                                elif r_ctype == "Tank":
                                    text "🛡️ 核心優勢：自帶高血量與嘲諷壁壘，有效為資深隊員分擔傷害！" size 12 color "#66ff66" bold True
                                else:
                                    text "⚔️ 核心優勢：火力強勁，開場即具備可觀的單體秒殺爆發！" size 12 color "#ff9999" bold True

            null height 15

            # 道德抉擇說明
            frame:
                xysize (1480, 160)
                background "#141a2c"
                padding (20, 15)
                vbox:
                    spacing 8
                    text "【 輪迴隊長 · 殘酷生存決策 】" size 17 color "#ffaa00" bold True
                    text "• 選擇【🤝 庇護新人入隊】：2 名新人加入團隊參戰與提供智謀，但輪迴世界難度將動態提升（每多 1 名存活新人，敵方 HP/ATK +15%）。" size 14 color "#66ff66"
                    text "• 選擇【💀 無情抹殺掠奪】：當場除掉累贅並掠奪輪迴補給，立即獲得 +1,000 生存點數與急救物資，副本維持 100% 基礎難度。" size 14 color "#ff6666"

            null height 10

            # 決策按鈕列
            hbox:
                spacing 60
                xalign 0.5

                button:
                    xysize (650, 65)
                    background "#1e4d2b"
                    hover_background "#2d7340"
                    padding (20, 12)
                    action Return(("protect", rookies))
                    vbox:
                        xalign 0.5
                        text "🤝 選擇庇護新人 (2人加入隊伍 / 難度+30%)" size 18 color "#66ff66" bold True xalign 0.5
                        text "獲得智者提示與前排戰力支援" size 12 color "#aaaaaa" xalign 0.5

                button:
                    xysize (650, 65)
                    background "#5c1e1e"
                    hover_background "#872b2b"
                    padding (20, 12)
                    action Return(("kill", rookies))
                    vbox:
                        xalign 0.5
                        text "💀 選擇無情抹殺 (獲得 +1,000點與物資)" size 18 color "#ff6666" bold True xalign 0.5
                        text "無新人負擔，副本維持 100% 基礎難度" size 12 color "#aaaaaa" xalign 0.5


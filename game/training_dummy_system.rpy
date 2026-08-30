# ==========================================
# 虛空廣場全息模擬稻草人系統 (training_dummy_system.rpy)
# ==========================================

init python:
    import copy

    if 'is_simulation_mode' not in globals():
        is_simulation_mode = False

    if 'simulation_settings' not in globals():
        simulation_settings = {
            "monsters": ["MOB_ZOMBIE_01"],
            "monster_count": 2,
            "infinite_hp": True,
            "ai_mode": "passive"  # "passive" or "active"
        }

    # 1. 啟動全息模擬戰鬥
    def start_simulation_battle():
        global is_simulation_mode, sim_backup_roster, sim_backup_inv, battle_state
        is_simulation_mode = True
        
        # 備份戰前真實狀態 (血量/精力/背包物資)
        roster = get_team_roster()
        inv = get_inventory()
        sim_backup_roster = copy.deepcopy(roster)
        sim_backup_inv = copy.deepcopy(inv)
        
        # 根據模擬設定生成目標怪獸
        m_id = simulation_settings.get("monsters", ["MOB_ZOMBIE_01"])[0]
        m_cnt = simulation_settings.get("monster_count", 2)
        m_data = get_monster_by_id(m_id) if 'get_monster_by_id' in globals() else None
        
        sim_enemies = []
        base_hp = 99999 if simulation_settings.get("infinite_hp", True) else int(m_data.get("stats",{}).get("hp", 200) if m_data else 200)
        base_name = m_data.get("name", "模擬木樁") if m_data else "全息模擬腐屍"
        base_atk = int(m_data.get("stats",{}).get("atk", 20) if m_data else 20) if simulation_settings.get("ai_mode") == "active" else 0
        
        for idx in range(m_cnt):
            sim_enemies.append({
                "id": m_id,
                "name": f"全息【{base_name}】{chr(65+idx)}號",
                "hp": base_hp,
                "max_hp": base_hp,
                "atk": base_atk,
                "status": "全息木樁 (DPS測試)" if simulation_settings.get("ai_mode") == "passive" else "主動反擊測試",
                "avatar": (m_data.get("avatar") if (m_data and m_data.get("avatar") and m_data.get("avatar") != "images/core_idle.PNG") else ("images/agile_zombie.jpg" if "敏捷" in base_name else "images/zombie.jpg"))
            })
            
        # 構造出戰 6 人團隊 (支援前後排站位與預設繼承)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else roster
        
        # 構造模擬戰鬥 state
        battle_state = {
            "player_team": deployed_team,
            "enemies": sim_enemies,
            "round_number": 1,
            "is_player_turn": True,
            "selected_actor": None,
            "target_mode": None,
            "selected_skill": None,
            "is_simulation": True,
            "infinite_hp": simulation_settings.get("infinite_hp", True),
            "ai_mode": simulation_settings.get("ai_mode", "passive"),
            "total_damage": 0,
            "highest_hit": 0,
            "logs": [
                "🎯 === 全息模擬稻草人戰鬥已啟動 (0 消耗 / 0 掉落 / 數據統計模式) ===",
                f"📊 模擬目標：{m_cnt} 隻【{base_name}】 | 無限血量：{'開啟' if simulation_settings.get('infinite_hp') else '關閉'} | AI模式：{'被動沙包' if simulation_settings.get('ai_mode')=='passive' else '主動攻擊'}"
            ]
        }
        return battle_state

    # 2. 結束模擬並無損還原
    def end_simulation_battle():
        global is_simulation_mode, sim_backup_roster, sim_backup_inv, team_roster, inventory
        is_simulation_mode = False
        if 'sim_backup_roster' in globals() and sim_backup_roster:
            team_roster = copy.deepcopy(sim_backup_roster)
        if 'sim_backup_inv' in globals() and sim_backup_inv:
            inventory = copy.deepcopy(sim_backup_inv)
        return True


# ==========================================
# 稻草人參數自訂設定介面 (training_dummy_screen)
# ==========================================
screen training_dummy_screen():

    $ monsters = get_monsters_db() if 'get_monsters_db' in globals() else []
    $ sel_m_id = simulation_settings.get("monsters", ["MOB_ZOMBIE_01"])[0]
    $ m_cnt = simulation_settings.get("monster_count", 2)
    $ is_inf_hp = simulation_settings.get("infinite_hp", True)
    $ ai_mode = simulation_settings.get("ai_mode", "passive")

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1600, 920)
        padding (30, 25)
        background "#0d121ff5"

        vbox:
            spacing 12
            xalign 0.5

            # 頂部標題
            hbox:
                spacing 35
                xalign 0.5
                text "【 🎯 虛空廣場 · 全息模擬稻草人 (Combat Simulator) 】" size 25 color "#ffcc00" bold True yalign 0.5
                text "（完全無損測試：不消耗任何真實彈藥與藥水，無損還原戰前狀態）" size 15 color "#00ffff" yalign 0.5

            null height 5

            # 主雙欄設定
            hbox:
                spacing 25
                xalign 0.5

                # 左側：選擇模擬怪物種類
                frame:
                    xysize (750, 720)
                    background "#161b2ebb"
                    padding (20, 18)
                    vbox:
                        spacing 10
                        text "【 1. 怪物資料庫調用 (Monster DB Selector) 】" size 19 color "#00ffff" bold True
                        text "自怪物數據庫中選擇要投放至全息模擬戰場的假想敵：" size 13 color "#aaaaaa"

                        null height 5

                        viewport:
                            xysize (710, 600)
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            vbox:
                                spacing 8
                                for m in monsters:
                                    $ m_id = m.get("id")
                                    $ m_name = m.get("name")
                                    $ m_pos = m.get("position_type", "Frontline")
                                    $ m_stats = m.get("stats", {})
                                    $ is_m_sel = (sel_m_id == m_id)

                                    button:
                                        xysize (690, 80)
                                        background ("#3b5288ee" if is_m_sel else "#222a42aa")
                                        hover_background "#4a68aaaa"
                                        padding (12, 8)
                                        action SetDict(simulation_settings, "monsters", [m_id])
                                        hbox:
                                            spacing 15
                                            yalign 0.5
                                            vbox:
                                                spacing 2
                                                xysize (480, None)
                                                text f"★ {m_name} ({m_pos})" size 16 color ("#00ffff" if is_m_sel else "#ffffff") bold True
                                                text f"基礎屬性：HP {m_stats.get('hp')} | ATK {m_stats.get('atk')} | DEF {m_stats.get('def')}" size 12 color "#aaaaaa"
                                            if is_m_sel:
                                                text "【已鎖定】" size 14 color "#66ff66" bold True yalign 0.5

                # 右側：自訂模擬參數
                frame:
                    xysize (750, 720)
                    background "#161b2ebb"
                    padding (25, 20)
                    vbox:
                        spacing 20
                        text "【 2. 模擬參數與模式自訂 】" size 19 color "#00ffff" bold True

                        # 怪物數量設定 (1~5 隻)
                        vbox:
                            spacing 8
                            text f"◈ 假想敵生成數量：{m_cnt} 隻" size 16 color "#ffaa00" bold True
                            hbox:
                                spacing 10
                                for cnt in [1, 2, 3, 4, 5]:
                                    $ is_c_act = (m_cnt == cnt)
                                    button:
                                        xysize (130, 42)
                                        background ("#e6a100" if is_c_act else "#222a42")
                                        action SetDict(simulation_settings, "monster_count", cnt)
                                        text f"{cnt} 隻目標" size 14 color ("#000000" if is_c_act else "#ffffff") bold True xalign 0.5 yalign 0.5

                        # 無限血量設定
                        vbox:
                            spacing 8
                            text "◈ 木樁血量模式 (Infinite HP Toggle)：" size 16 color "#ffaa00" bold True
                            hbox:
                                spacing 15
                                button:
                                    xysize (330, 45)
                                    background ("#245e33" if is_inf_hp else "#222a42")
                                    action SetDict(simulation_settings, "infinite_hp", True)
                                    text "♾️ 無限血量 (純測極限DPS)" size 14 color ("#66ff66" if is_inf_hp else "#ffffff") bold True xalign 0.5 yalign 0.5

                                button:
                                    xysize (330, 45)
                                    background ("#5e2424" if not is_inf_hp else "#222a42")
                                    action SetDict(simulation_settings, "infinite_hp", False)
                                    text "⚔️ 原版正常血量" size 14 color ("#ff6666" if not is_inf_hp else "#ffffff") bold True xalign 0.5 yalign 0.5

                        # AI 攻擊模式 (被動 vs 主動)
                        vbox:
                            spacing 8
                            text "◈ 假想敵 AI 反擊模式 (Enemy AI Active/Passive)：" size 16 color "#ffaa00" bold True
                            hbox:
                                spacing 15
                                button:
                                    xysize (330, 45)
                                    background ("#245e33" if ai_mode == "passive" else "#222a42")
                                    action SetDict(simulation_settings, "ai_mode", "passive")
                                    text "🛡️ 被動沙包 (不還手純吃傷害)" size 14 color ("#66ff66" if ai_mode == "passive" else "#ffffff") bold True xalign 0.5 yalign 0.5

                                button:
                                    xysize (330, 45)
                                    background ("#5e2424" if ai_mode == "active" else "#222a42")
                                    action SetDict(simulation_settings, "ai_mode", "active")
                                    text "🔥 主動反擊 (測試防守坦度)" size 14 color ("#ff6666" if ai_mode == "active" else "#ffffff") bold True xalign 0.5 yalign 0.5

                        null height 15

                        # 啟動模擬戰鬥按鈕
                        button:
                            xysize (700, 65)
                            background "#245e33"
                            hover_background "#358a4b"
                            action Return("launch_simulation")
                            text "⚔️ 啟動全息模擬戰鬥 (進入 battle_screen) ⚔️" size 18 color "#ffffff" bold True xalign 0.5 yalign 0.5

            null height 5

            textbutton "【 🚪 退出模擬器，返回輪迴廣場 】":
                xalign 0.5
                action Return("leave_simulator")
                text_size 19
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


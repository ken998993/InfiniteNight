# ==============================================================================
# 📜 《輪迴世界》戰術陣型與 6 人出戰配置系統 (deployment_system.rpy)
# 依據 developMd/03_Combat_and_Formation.md 規範實現
# ==============================================================================

init python:
    import copy

    # 全域出戰預設陣容紀錄
    if 'last_deployed_party' not in globals():
        last_deployed_party = [
            {"name": "顧臨淵 (你)", "position": "frontline"},
            {"name": "冷月", "position": "frontline"},
            {"name": "項天", "position": "frontline"},
            {"name": "蘇曉", "position": "backline"}
        ]

    if 'current_deployment' not in globals():
        current_deployment = []

    # 1. 取得或初始化當前出戰陣容 (最多 6 人，前排 3 + 後排 3)
    def get_current_deployment():
        global current_deployment, team_roster, last_deployed_party
        roster = get_team_roster()
        if not current_deployment:
            # 優先自上一把預設或名冊初始化
            load_last_preset()
        # 確保資料與 roster 保持同步 (血量、屬性、裝備等)
        for entry in current_deployment:
            if entry and "name" in entry:
                mem = next((m for m in roster if m.get("name") == entry.get("name")), None)
                if mem:
                    entry["member"] = mem
        return current_deployment

    # 2. 一鍵套用上一把預設隊伍 (Load Last Party Preset)
    def load_last_preset():
        global current_deployment, last_deployed_party
        roster = get_team_roster()
        new_dep = []
        
        # 預設槽位：前排 3 個 + 後排 3 個
        front_slots = [None, None, None]
        back_slots = [None, None, None]
        
        preset_list = last_deployed_party if last_deployed_party else []
        for p in preset_list:
            p_name = p.get("name")
            p_pos = p.get("position", "frontline")
            # 尋找存在於名冊且存活的隊員
            mem = next((m for m in roster if m.get("name") == p_name and to_int(m.get("hp", 100)) > 0), None)
            if mem:
                entry = {
                    "name": p_name,
                    "position": p_pos,
                    "member": mem
                }
                if p_pos == "frontline":
                    for i in range(3):
                        if front_slots[i] is None:
                            front_slots[i] = entry
                            break
                else:
                    for i in range(3):
                        if back_slots[i] is None:
                            back_slots[i] = entry
                            break

        # 若預設全空則自動依名冊補位
        if not any(front_slots) and not any(back_slots):
            auto_fill_deployment()
            return

        current_deployment = [s for s in (front_slots + back_slots) if s is not None]
        save_current_preset()

    # 3. 自動快速編隊 (Auto Fill)
    def auto_fill_deployment():
        global current_deployment
        roster = get_team_roster()
        alive_roster = [m for m in roster if to_int(m.get("hp", 100)) > 0]
        
        front_list = []
        back_list = []
        
        # 依角色特性分配前後排 (前排優先坦克/近戰/體質高者)
        for m in alive_roster:
            role = m.get("combat_role", "") + m.get("role", "")
            con = to_int(m.get("con", 20))
            int_val = to_int(m.get("int", 20))
            
            if ("肉搏" in role or "坦克" in role or "經驗" in role or con >= 40) and len(front_list) < 3:
                front_list.append({"name": m.get("name"), "position": "frontline", "member": m})
            elif len(back_list) < 3:
                back_list.append({"name": m.get("name"), "position": "backline", "member": m})
            elif len(front_list) < 3:
                front_list.append({"name": m.get("name"), "position": "frontline", "member": m})

        current_deployment = front_list + back_list
        save_current_preset()

    # 4. 儲存當前陣容為預設
    def save_current_preset():
        global last_deployed_party, current_deployment
        last_deployed_party = [{"name": e.get("name"), "position": e.get("position", "frontline")} for e in current_deployment if e and "name" in e]

    # 5. 上場/下場/切換站位
    def toggle_deploy_member(member_name, target_position=None):
        global current_deployment
        roster = get_team_roster()
        mem = next((m for m in roster if m.get("name") == member_name), None)
        if not mem:
            return
            
        existing = next((e for e in current_deployment if e.get("name") == member_name), None)
        if existing:
            if target_position and existing.get("position") != target_position:
                # 切換前後排
                front_cnt = sum(1 for e in current_deployment if e.get("position") == "frontline")
                back_cnt = sum(1 for e in current_deployment if e.get("position") == "backline")
                if target_position == "frontline" and front_cnt >= 3:
                    return
                if target_position == "backline" and back_cnt >= 3:
                    return
                existing["position"] = target_position
            else:
                # 換下陣容
                current_deployment.remove(existing)
        else:
            # 新增上場
            if len(current_deployment) >= 6:
                return
            front_cnt = sum(1 for e in current_deployment if e.get("position") == "frontline")
            back_cnt = sum(1 for e in current_deployment if e.get("position") == "backline")
            pos = target_position or ("frontline" if front_cnt < 3 else "backline")
            if pos == "frontline" and front_cnt >= 3:
                pos = "backline"
            if pos == "backline" and back_cnt >= 3:
                pos = "frontline"
            current_deployment.append({"name": member_name, "position": pos, "member": mem})
            
        save_current_preset()

    # 6. 生成可供 battle_screen 使用之出戰隊伍列表
    def build_deployed_battle_team():
        get_current_deployment()
        roster = get_team_roster() if 'get_team_roster' in globals() else []
        battle_team = []
        for entry in current_deployment:
            m = entry.get("member")
            if m:
                # 尋找 team_roster 中對應的實時隊員資料 (嚴格保留受創後的即時 HP 與 MP)
                m_live = next((r for r in roster if r.get('name') == m.get('name')), m)
                m_copy = copy.deepcopy(m_live)
                m_copy["position"] = entry.get("position", "frontline")
                battle_team.append(m_copy)
        if not battle_team:
            # 至少派一人出戰
            if roster:
                m_copy = copy.deepcopy(roster[0])
                m_copy["position"] = "frontline"
                battle_team.append(m_copy)
        return battle_team


# ==============================================================================
# 戰前隊伍戰術配置介面 (party_deployment_screen)
# ==============================================================================
screen party_deployment_screen():

    $ roster = get_team_roster()
    $ dep_list = get_current_deployment()
    
    $ front_entries = [e for e in dep_list if e.get("position") == "frontline"]
    $ back_entries = [e for e in dep_list if e.get("position") == "backline"]
    
    $ deployed_names = [e.get("name") for e in dep_list]
    $ total_deployed = len(dep_list)

    window:
        background "#000000ee"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1760, 960)
        padding (30, 20)
        background "#0d121ff8"

        vbox:
            spacing 12
            xalign 0.5

            # 頂部標題與功能按鈕列
            hbox:
                spacing 35
                xalign 0.5
                text "【 ⚔️ 輪迴空間 · 戰前隊伍配置與 6 人陣型 (Party Deployment) 】" size 25 color "#ffcc00" bold True yalign 0.5
                text f"上場人數：{total_deployed} / 6 人 (前排 {len(front_entries)}/3，後排 {len(back_entries)}/3)" size 17 color ("#66ff66" if total_deployed > 0 else "#ff4444") bold True yalign 0.5

            hbox:
                spacing 20
                xalign 0.5
                button:
                    xysize (230, 42)
                    background "#223555"
                    hover_background "#355288"
                    action Function(load_last_preset)
                    text "🔄 套用上次陣容" size 15 color "#00ffff" bold True xalign 0.5 yalign 0.5

                button:
                    xysize (230, 42)
                    background "#224433"
                    hover_background "#336644"
                    action Function(auto_fill_deployment)
                    text "⚡ 自動快速編隊" size 15 color "#66ff66" bold True xalign 0.5 yalign 0.5

                button:
                    xysize (230, 42)
                    background "#442222"
                    hover_background "#663333"
                    action SetVariable("current_deployment", [])
                    text "🧹 清空當前陣容" size 15 color "#ff8888" bold True xalign 0.5 yalign 0.5

            null height 5

            # 主畫面：左側前排與後排陣型槽位 (6 槽)，右側備戰隊員庫
            hbox:
                spacing 25
                xalign 0.5

                # -------------------------------------------------------------
                # 左側：出戰 6 人棋盤槽位 (前排 3 + 後排 3)
                # -------------------------------------------------------------
                frame:
                    xysize (1040, 720)
                    background "#141a2ecc"
                    padding (20, 15)
                    vbox:
                        spacing 15

                        # 🛡️ 前排陣線 (Frontline)
                        vbox:
                            spacing 8
                            hbox:
                                spacing 15
                                text "🛡️ 前排防禦戰線 (Frontline - 最多 3 人)" size 18 color "#ffaa00" bold True
                                text "（保護後排：阻擋敵方地面單體近戰，承受首波衝擊）" size 13 color "#aaaaaa" yalign 0.5

                            hbox:
                                spacing 15
                                for f_idx in range(3):
                                    $ f_entry = front_entries[f_idx] if f_idx < len(front_entries) else None
                                    if f_entry:
                                        $ m_obj = f_entry.get("member", {})
                                        $ m_av = m_obj.get("avatar", "images/core_idle.PNG")
                                        frame:
                                            xysize (315, 270)
                                            background "#1f2942ee"
                                            padding (10, 8)
                                            vbox:
                                                spacing 5
                                                xalign 0.5
                                                add m_av xysize (110, 110) xalign 0.5
                                                text f"{m_obj.get('name')}" size 16 color "#00ffff" bold True xalign 0.5
                                                text f"HP: {m_obj.get('hp')}/{m_obj.get('max_hp')} | 定位: {m_obj.get('combat_role','全能')[:6]}" size 12 color "#ff9999" xalign 0.5
                                                
                                                null height 2
                                                hbox:
                                                    spacing 8
                                                    xalign 0.5
                                                    button:
                                                        xysize (130, 32)
                                                        background "#355288"
                                                        hover_background "#4a6fa8"
                                                        action Function(toggle_deploy_member, m_obj.get('name'), 'backline')
                                                        text "⬇️ 移至後排" size 12 color "#ffffff" xalign 0.5 yalign 0.5

                                                    button:
                                                        xysize (130, 32)
                                                        background "#552222"
                                                        hover_background "#773333"
                                                        action Function(toggle_deploy_member, m_obj.get('name'))
                                                        text "❌ 換下待命" size 12 color "#ff8888" xalign 0.5 yalign 0.5
                                    else:
                                        frame:
                                            xysize (315, 270)
                                            background "#181f3366"
                                            padding (15, 15)
                                            vbox:
                                                xalign 0.5 yalign 0.5
                                                spacing 8
                                                text "【 前排 空置槽位 】" size 15 color "#556688" bold True xalign 0.5
                                                text "請在右側名冊點選隊員加入" size 12 color "#445577" xalign 0.5

                        null height 5

                        # 🏹 後排陣線 (Backline)
                        vbox:
                            spacing 8
                            hbox:
                                spacing 15
                                text "🏹 後排輸出戰線 (Backline - 最多 3 人)" size 18 color "#00ffcc" bold True
                                text "（遠程火力與法術支援，前排全滅時將承擔 20%% 額外暴露受傷）" size 13 color "#aaaaaa" yalign 0.5

                            hbox:
                                spacing 15
                                for b_idx in range(3):
                                    $ b_entry = back_entries[b_idx] if b_idx < len(back_entries) else None
                                    if b_entry:
                                        $ m_obj = b_entry.get("member", {})
                                        $ m_av = m_obj.get("avatar", "images/core_idle.PNG")
                                        frame:
                                            xysize (315, 270)
                                            background "#1f2942ee"
                                            padding (10, 8)
                                            vbox:
                                                spacing 5
                                                xalign 0.5
                                                add m_av xysize (110, 110) xalign 0.5
                                                text f"{m_obj.get('name')}" size 16 color "#00ffff" bold True xalign 0.5
                                                text f"HP: {m_obj.get('hp')}/{m_obj.get('max_hp')} | 定位: {m_obj.get('combat_role','全能')[:6]}" size 12 color "#ff9999" xalign 0.5
                                                
                                                null height 2
                                                hbox:
                                                    spacing 8
                                                    xalign 0.5
                                                    button:
                                                        xysize (130, 32)
                                                        background "#355288"
                                                        hover_background "#4a6fa8"
                                                        action Function(toggle_deploy_member, m_obj.get('name'), 'frontline')
                                                        text "⬆️ 移至前排" size 12 color "#ffffff" xalign 0.5 yalign 0.5

                                                    button:
                                                        xysize (130, 32)
                                                        background "#552222"
                                                        hover_background "#773333"
                                                        action Function(toggle_deploy_member, m_obj.get('name'))
                                                        text "❌ 換下待命" size 12 color "#ff8888" xalign 0.5 yalign 0.5
                                    else:
                                        frame:
                                            xysize (315, 270)
                                            background "#181f3366"
                                            padding (15, 15)
                                            vbox:
                                                xalign 0.5 yalign 0.5
                                                spacing 8
                                                text "【 後排 空置槽位 】" size 15 color "#556688" bold True xalign 0.5
                                                text "請在右側名冊點選隊員加入" size 12 color "#445577" xalign 0.5

                # -------------------------------------------------------------
                # 右側：全體備戰角色名單 (點擊快速上陣)
                # -------------------------------------------------------------
                frame:
                    xysize (640, 720)
                    background "#141a2ecc"
                    padding (20, 15)
                    vbox:
                        spacing 10
                        text "【 👥 隊伍成員備戰庫 (點選加入陣容) 】" size 18 color "#00ffff" bold True
                        text "已招募之後勤副官不佔用 6 人棋盤，被動效果對全隊生效。" size 12 color "#888888"

                        null height 5

                        viewport:
                            xysize (600, 600)
                            scrollbars "vertical"
                            mousewheel True
                            draggable True

                            vbox:
                                spacing 8
                                for mem in roster:
                                    $ m_name = mem.get("name")
                                    $ m_hp = to_int(mem.get("hp", 100))
                                    $ m_max_hp = to_int(mem.get("max_hp", 100))
                                    $ m_role = mem.get("combat_role", "戰鬥員")
                                    $ is_in_dep = (m_name in deployed_names)
                                    $ cur_pos = next((e.get("position") for e in dep_list if e.get("name") == m_name), None)

                                    frame:
                                        xysize (580, 85)
                                        background ("#243859ee" if is_in_dep else "#1a2236aa")
                                        padding (10, 8)
                                        hbox:
                                            spacing 12
                                            yalign 0.5
                                            add mem.get("avatar", "images/core_idle.PNG") xysize (64, 64) yalign 0.5

                                            vbox:
                                                spacing 3
                                                xysize (320, None)
                                                text f"{m_name}" size 16 color ("#66ff66" if is_in_dep else "#ffffff") bold True
                                                text f"HP: {m_hp}/{m_max_hp} | {m_role}" size 12 color "#bbbbbb"
                                                if is_in_dep:
                                                    text f"狀態：已上場 ({'前排 🛡️' if cur_pos=='frontline' else '後排 🏹'})" size 12 color "#ffcc00" bold True
                                                else:
                                                    text "狀態：待命休息中" size 12 color "#888888"

                                            if is_in_dep:
                                                button:
                                                    xysize (130, 42)
                                                    background "#552222"
                                                    hover_background "#773333"
                                                    action Function(toggle_deploy_member, m_name)
                                                    text "❌ 換下" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5
                                            else:
                                                if total_deployed < 6:
                                                    hbox:
                                                        spacing 6
                                                        if len(front_entries) < 3:
                                                            button:
                                                                xysize (70, 42)
                                                                background "#224433"
                                                                hover_background "#336644"
                                                                action Function(toggle_deploy_member, m_name, 'frontline')
                                                                text "+前排" size 12 color "#ffffff" bold True xalign 0.5 yalign 0.5
                                                        if len(back_entries) < 3:
                                                            button:
                                                                xysize (70, 42)
                                                                background "#223555"
                                                                hover_background "#355288"
                                                                action Function(toggle_deploy_member, m_name, 'backline')
                                                                text "+後排" size 12 color "#ffffff" bold True xalign 0.5 yalign 0.5
                                                else:
                                                    text "【陣容已滿】" size 12 color "#777777" yalign 0.5

            null height 5

            # 底部操作按鈕
            hbox:
                spacing 30
                xalign 0.5
                if total_deployed > 0:
                    button:
                        xysize (480, 52)
                        background "#245e33"
                        hover_background "#358a4b"
                        action Return("start_battle_with_deployment")
                        text "🚀 確認配置完畢，立即出戰！" size 18 color "#ffffff" bold True xalign 0.5 yalign 0.5
                else:
                    button:
                        xysize (480, 52)
                        background "#444444"
                        text "⚠️ 請至少配置 1 名隊員上場" size 16 color "#888888" bold True xalign 0.5 yalign 0.5

                button:
                    xysize (320, 52)
                    background "#222a42"
                    hover_background "#3b5288"
                    action Return("cancel_deployment")
                    text "🚪 取消並返回" size 16 color "#dddddd" xalign 0.5 yalign 0.5


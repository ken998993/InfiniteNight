# ==========================================
# 團隊系統與隊員能力列表（強制動態讀取 JSON 版）
# ==========================================

init python:
    import json

    # 取得儲備隊員名冊 (自 jsonData/reserve_members.json 讀取)
    def get_reserve_members():
        global reserve_members_db
        if 'reserve_members_db' in globals() and reserve_members_db:
            return reserve_members_db
        try:
            with renpy.file("jsonData/reserve_members.json") as f:
                reserve_members_db = json.load(f)
                return reserve_members_db
        except Exception as e:
            reserve_members_db = []
            return reserve_members_db

    # 招募儲備隊員加入出戰小隊
    def recruit_reserve_member(member_id):
        global team_roster, points, fate_shards
        pool = get_reserve_members()
        target = None
        for m in pool:
            if m.get("id") == member_id:
                target = m
                break
        if not target:
            return {"success": False, "msg": "查無此儲備隊員資料！"}
            
        roster = get_team_roster()
        if any(mem.get("name") == target.get("name") for mem in roster):
            return {"success": False, "msg": f"隊員【{target.get('name')}】已在隊伍中！"}
            
        cost_pts = target.get("recruit_cost_points", 1000)
        cost_shard = target.get("recruit_fate_shard", "D")
        
        cur_pts = points if 'points' in globals() else 0
        shards = fate_shards if 'fate_shards' in globals() else {}
        
        if cur_pts < cost_pts:
            return {"success": False, "msg": f"輪迴積分不足！需要 {cost_pts} 點，目前僅有 {cur_pts} 點。"}
        if shards.get(cost_shard, 0) < 1:
            return {"success": False, "msg": f"命運碎片不足！需要 {cost_shard} 級命運碎片 x1。"}
            
        points -= cost_pts
        shards[cost_shard] -= 1
        
        new_member = copy.deepcopy(target)
        roster.append(new_member)
        return {"success": True, "msg": f"🎉 成功招募隊員【{target.get('name')}】加入隊伍！", "member": new_member}


# ==========================================
# 團隊狀態面板介面
# ==========================================
screen team_status_screen(page=0):

    # 取得團隊資料（優先讀取遊戲中的 team_roster 全域資料，若無則防呆載入）
    $ roster_data = team_roster if ('team_roster' in globals() and team_roster) else get_team_roster()
    
    $ items_per_page = 2
    $ total_members = len(roster_data)
    $ total_pages = max(1, (total_members + items_per_page - 1) // items_per_page)
    
    $ page = max(0, min(page, total_pages - 1))
    
    $ start_idx = page * items_per_page
    $ end_idx = min(start_idx + items_per_page, total_members)
    $ current_members = roster_data[start_idx:end_idx]

    window:
        background "#000000cc"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1400, 900)
        padding (40, 30)
        background "#111122ee"
        
        vbox:
            spacing 15
            xalign 0.5

            text "【 輪迴空間 · 戰鬥屬性與基因鎖總覽 】" size 26 color "#ffcc00" xalign 0.5
            null height 5

            vbox:
                spacing 15
                xysize (1320, 620)
                
                for member in current_members:
                    $ m_status = member.get('status', '良好')
                    $ m_gene = member.get('gene_lock', 0)
                    $ m_pressure = member.get('survival_pressure', 0)
                    
                    $ status_color = "#ff6666" if "傷" in m_status else "#66ff66"
                    $ lock_text = f"基因鎖 {m_gene} 階" if m_gene > 0 else "未開啟"
                    $ lock_color = "#ff4444" if m_gene > 0 else "#888888"
                    
                    window:
                        xysize (1290, 290)
                        background "#222233aa"
                        padding (15, 12)
                        
                        hbox:
                            spacing 15
                            
                            # 左側隊員頭像框 (預設 core_idle.PNG)
                            frame:
                                xysize (130, 266)
                                background "#121828cc"
                                padding (5, 5)
                                vbox:
                                    xalign 0.5 yalign 0.5
                                    spacing 6
                                    $ m_av = member.get('avatar', 'images/core_idle.PNG')
                                    add m_av xysize (120, 210) xalign 0.5 yalign 0.5
                                    text "[member.get('name', '未知')]" size 13 color "#00ffff" bold True xalign 0.5

                            # 右側隊員詳細資料
                            vbox:
                                spacing 8
                                xysize (1110, 266)
                                
                                hbox:
                                    spacing 20
                                    vbox:
                                        spacing 2
                                        xysize (280, 48)
                                        text "[member.get('name', '未知')]" size 21 color "#00ffff" bold True
                                        text "職稱：[member.get('role', '無')]" size 13 color "#aaaaaa"

                                    vbox:
                                        spacing 2
                                        xysize (380, 48)
                                        text "血統強化：[member.get('bloodline', '無')]" size 14 color "#ffffff"
                                        text "狀態：[lock_text] (壓力值: [m_pressure]/100)" size 14 color lock_color

                                    vbox:
                                        spacing 2
                                        xysize (410, 48)
                                        text f"個人積分：{member.get('points', 0)} 點" size 16 color "#ffcc00"
                                        text f"當前狀態：{m_status}" size 14 color status_color

                                hbox:
                                    spacing 30
                                    vbox:
                                        spacing 2
                                        xysize (320, 38)
                                        text f"生命值 (HP)：{member.get('hp', 100)} / {member.get('max_hp', 100)}" size 13 color "#ff6666"
                                        text f"精神力 (MP)：{member.get('mp', 50)} / {member.get('max_mp', 50)}" size 13 color "#66ccff"

                                    vbox:
                                        spacing 2
                                        xysize (740, 38)
                                        if member.get('neili_max', 0) > 0:
                                            text f"內力 (neili)：{member.get('neili_current', 0)} / {member.get('neili_max', 0)}" size 13 color "#ffaa00"
                                        if member.get('blood_max', 0) > 0:
                                            text f"血族能量 (blood)：{member.get('blood_current', 0)} / {member.get('blood_max', 0)}" size 13 color "#ff4444"
                                        if member.get('mental_max', 0) > 0:
                                            text f"精神力場 (mental)：{member.get('mental_current', 0)} / {member.get('mental_max', 0)}" size 13 color "#00ccff"
                                        if member.get('qi_max', 0) > 0:
                                            text f"氣血之力 (qi)：{member.get('qi_current', 0)} / {member.get('qi_max', 0)}" size 13 color "#ff6666"
                                        if member.get('calc_max', 0) > 0:
                                            text f"計算力 (calc)：{member.get('calc_current', 0)} / {member.get('calc_max', 0)}" size 13 color "#00ffcc"
                                        
                                        if member.get('neili_max', 0) == 0 and member.get('blood_max', 0) == 0 and member.get('mental_max', 0) == 0 and member.get('qi_max', 0) == 0 and member.get('calc_max', 0) == 0:
                                            text "能量體系：無附加" size 13 color "#777777"

                                $ m_skills = member.get('skills', [])
                                if m_skills:
                                    $ sk_names_str = "、".join([s.get('name', '招式') for s in m_skills])
                                    text "🔥 已掌握專屬戰技：[sk_names_str]" size 13 color "#ffcc00"

                                $ eq_strs = []
                                $ slot_icons = {"head": "🪖", "torso": "🥋", "hands": "🧤", "feet": "🥾", "necklace": "📿", "main_hand": "⚔️", "off_hand": "🛡️", "mount": "🚀"}
                                for s_k, s_icon in slot_icons.items():
                                    $ itm_k_id = member.get(f"equipped_{s_k}")
                                    if itm_k_id:
                                        $ eq_obj = get_item_by_id(itm_k_id) if 'get_item_by_id' in globals() else None
                                        if eq_obj:
                                            $ eq_strs.append(f"{s_icon} " + eq_obj.get("name", ""))
                                if eq_strs:
                                    $ eq_text = " | ".join(eq_strs)
                                    text f"🛡️ 已佩戴裝備：{eq_text}" size 12 color "#66ff66"
                                else:
                                    text "角色定位與簡述：[member.get('desc', '無')]" size 12 color "#cccccc"

            null height 10

            hbox:
                spacing 40
                xalign 0.5
                
                $ prev_color = "#00ffff" if page > 0 else "#555555"
                textbutton "◀ 上一頁":
                    action Show("team_status_screen", page=max(0, page - 1))
                    text_size 18
                    text_idle_color prev_color
                    sensitive (page > 0)

                text "第 [page + 1] 頁 / 共 [total_pages] 頁 (團隊總計 [total_members] 人)" size 18 color "#ffffff" yalign 0.5

                $ next_color = "#00ffff" if page < total_pages - 1 else "#555555"
                textbutton "下一頁 ▶":
                    action Show("team_status_screen", page=min(total_pages - 1, page + 1))
                    text_size 18
                    text_idle_color next_color
                    sensitive (page < total_pages - 1)

            null height 5

            textbutton "【 關閉團隊面板 】":
                xalign 0.5
                action Return("close_team")
                text_size 22
                text_idle_color "#ff4444"
                text_hover_color "#ff8888"
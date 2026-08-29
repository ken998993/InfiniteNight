# ==========================================
# 團隊系統與隊員能力列表（強制動態讀取 JSON 版）
# ==========================================

init python:
    import json

    def get_team_roster():
        global team_roster
        if 'team_roster' in globals() and team_roster:
            return team_roster
        try:
            with renpy.file("jsonData/team_data.json") as f:
                team_roster = json.load(f)
                return team_roster
        except Exception as e:
            team_roster = [
                {
                    "name": "預設主角",
                    "role": "資深隊員",
                    "combat_role": "全能平衡",
                    "bloodline": "無",
                    "points": 1000,
                    "hp": 100, "max_hp": 100,
                    "mp": 50, "max_mp": 50,
                    "neili_current": 0, "neili_max": 100,
                    "blood_current": 0, "blood_max": 0,
                    "mental_current": 0, "mental_max": 0,
                    "qi_current": 0, "qi_max": 0,
                    "calc_current": 0, "calc_max": 0,
                    "gene_lock": 0, "survival_pressure": 0,
                    "status": "良好", "desc": "讀取 JSON 失敗的備用預設身分。"
                }
            ]
            return team_roster


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

            text "【 主神空間 · 戰鬥屬性與基因鎖總覽 】" size 26 color "#ffcc00" xalign 0.5
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
                        padding (20, 15)
                        
                        vbox:
                            spacing 10
                            
                            hbox:
                                spacing 30
                                vbox:
                                    spacing 3
                                    xysize (320, 50)
                                    text "[member.get('name', '未知')]" size 22 color "#00ffff" bold True
                                    text "職稱：[member.get('role', '無')]" size 14 color "#aaaaaa"

                                vbox:
                                    spacing 3
                                    xysize (400, 50)
                                    text "血統強化：[member.get('bloodline', '無')]" size 15 color "#ffffff"
                                    text "狀態：[lock_text] (壓力值: [m_pressure]/100)" size 15 color lock_color

                                vbox:
                                    spacing 3
                                    xysize (450, 50)
                                    text "個人積分：[member.get('points', 0)] 點" size 17 color "#ffcc00"
                                    text "當前狀態：[m_status]" size 15 color status_color

                            null height 5

                            hbox:
                                spacing 40
                                vbox:
                                    spacing 3
                                    xysize (360, 40)
                                    text "生命值 (HP)：[member.get('hp', 100)] / [member.get('max_hp', 100)]" size 14 color "#ff6666"
                                    text "精神力 (MP)：[member.get('mp', 50)] / [member.get('max_mp', 50)]" size 14 color "#66ccff"

                                vbox:
                                    spacing 4
                                    xysize (800, 40)
                                    if member.get('neili_max', 0) > 0:
                                        text "內力 (neili)：[member.get('neili_current', 0)] / [member.get('neili_max', 0)]" size 14 color "#ffaa00"
                                    if member.get('blood_max', 0) > 0:
                                        text "血族能量 (blood)：[member.get('blood_current', 0)] / [member.get('blood_max', 0)]" size 14 color "#ff4444"
                                    if member.get('mental_max', 0) > 0:
                                        text "精神力場 (mental)：[member.get('mental_current', 0)] / [member.get('mental_max', 0)]" size 14 color "#00ccff"
                                    if member.get('qi_max', 0) > 0:
                                        text "氣血之力 (qi)：[member.get('qi_current', 0)] / [member.get('qi_max', 0)]" size 14 color "#ff6666"
                                    if member.get('calc_max', 0) > 0:
                                        text "計算力 (calc)：[member.get('calc_current', 0)] / [member.get('calc_max', 0)]" size 14 color "#00ffcc"
                                    
                                    if member.get('neili_max', 0) == 0 and member.get('blood_max', 0) == 0 and member.get('mental_max', 0) == 0 and member.get('qi_max', 0) == 0 and member.get('calc_max', 0) == 0:
                                        text "能量體系：無附加" size 14 color "#777777"

                            null height 3
                            $ m_skills = member.get('skills', [])
                            if m_skills:
                                $ sk_names_str = "、".join([s.get('name', '招式') for s in m_skills])
                                text "🔥 已掌握專屬戰技：[sk_names_str]" size 13 color "#ffcc00"
                            else:
                                text "角色定位與簡述：[member.get('desc', '無')]" size 13 color "#cccccc"

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
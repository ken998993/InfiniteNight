# ==========================================
# 角色六圍屬性加點與成長系統 (stat_system.rpy)
# ==========================================

init python:
    # 1. 六圍屬性定義與中文名稱
    STAT_NAMES_MAP = {
        "CON": {"name": "體質 (CON)", "desc": "影響生命上限 (HP) 與物理防禦 (+5 HP / 點)"},
        "STR": {"name": "力量 (STR)", "desc": "影響物理近戰傷害與負重 (+1 物理傷害 / 點)"},
        "SPD": {"name": "敏捷/速度 (SPD)", "desc": "影響行動順序、閃避率與物理遠程傷害"},
        "INT": {"name": "智力 (INT)", "desc": "影響魔力上限 (MP)、魔法傷害與解鎖智鬥選項 (+5 MP / 點)"},
        "MND": {"name": "精神 (MND)", "desc": "影響能量回復速度、異常抗性與精神力場防護"}
    }

    # 2. 執行屬性加點 (10 點數 = +1 屬性)
    def allocate_stat_points(member_idx, stat_key, count=1):
        global points, team_roster
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "無效目標隊員。"}
            
        cost = count * 10
        if points < cost:
            return {"success": False, "msg": f"【點數不足】提升 {count} 點屬性需要 {cost} 點生存點數，目前僅有 {points} 點！"}
            
        member = roster[member_idx]
        points -= cost
        member["points"] = points
        
        stat_k = stat_key.lower()
        member[stat_k] = int(member.get(stat_k, 20)) + count
        
        # 重新計算衍生屬性 (全面防護型別轉為 int)
        if stat_k == "con":
            cur_max_hp = int(member.get("max_hp", 100)) + (count * 5)
            cur_hp = int(member.get("hp", 100)) + (count * 5)
            member["max_hp"] = cur_max_hp
            member["hp"] = min(cur_max_hp, cur_hp)
            if member_idx == 0:
                hp = member["hp"]
        elif stat_k == "int":
            cur_max_mp = int(member.get("max_mp", 50)) + (count * 5)
            cur_mp = int(member.get("mp", 50)) + (count * 5)
            member["max_mp"] = cur_max_mp
            member["mp"] = min(cur_max_mp, cur_mp)
        elif stat_k == "str":
            member["atk_bonus"] = int(member.get("atk_bonus", 0)) + count
            
        stat_name = STAT_NAMES_MAP.get(stat_key.upper(), {}).get("name", stat_key)
        return {
            "success": True,
            "msg": f"✨【屬性強化成功】消耗 {cost} 點生存點數！\n【{member.get('name')}】的【{stat_name}】提升了 +{count} 點！（當前屬性值: {member[stat_k]}）"
        }


# ==========================================
# 屬性加點介面 (stat_allocation_screen)
# ==========================================
screen stat_allocation_screen(selected_idx=0):

    $ roster = get_team_roster()
    $ total_members = len(roster)
    $ cur_idx = min(selected_idx, max(0, total_members - 1))
    $ member = roster[cur_idx] if roster else {}
    $ p_name = member.get("name", "隊員")
    $ p_role = member.get("role", "無")
    $ p_av = member.get("avatar", "images/core_idle.PNG")

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

            # 頂部狀態列
            hbox:
                spacing 35
                xalign 0.5
                text "【 🧬 輪迴空間 · 核心六圍屬性強化石碑 】" size 25 color "#ffcc00" bold True yalign 0.5
                text f"可用生存點數: {points} 點" size 20 color "#66ff66" bold True yalign 0.5
                text "（兌換匯率：10 點數 = +1 點屬性）" size 15 color "#00ffff" yalign 0.5

            null height 5

            # 隊員選擇頁籤
            hbox:
                spacing 12
                xalign 0.5
                text "選擇強化隊員：" size 16 color "#ffaa00" yalign 0.5
                for idx, mem in enumerate(roster):
                    $ is_mem_active = (cur_idx == idx)
                    button:
                        xysize (180, 42)
                        background ("#e6a100" if is_mem_active else "#222a42")
                        hover_background "#3b5288"
                        action Show("stat_allocation_screen", selected_idx=idx)
                        text f"{mem.get('name')}" size 14 color ("#000000" if is_mem_active else "#ffffff") bold True xalign 0.5 yalign 0.5

            null height 8

            # 主雙欄佈局：左側角色卡與屬性概覽，右側 5 大屬性加點按鈕
            hbox:
                spacing 25
                xalign 0.5

                # 左側角色卡
                frame:
                    xysize (480, 700)
                    background "#161b2ebb"
                    padding (20, 18)
                    vbox:
                        spacing 12
                        xalign 0.5
                        # 頭像框
                        frame:
                            xysize (200, 260)
                            background "#101626cc"
                            padding (5, 5)
                            xalign 0.5
                            vbox:
                                xalign 0.5 yalign 0.5
                                spacing 6
                                add p_av xysize (190, 210) xalign 0.5 yalign 0.5
                                text f"{p_name}" size 15 color "#00ffff" bold True xalign 0.5

                        text f"職階定位：{p_role}" size 15 color "#aaaaaa" xalign 0.5
                        text f"血統：{member.get('bloodline', '無')}" size 14 color "#ddaaff" xalign 0.5

                        null height 5
                        # 衍戰屬性
                        frame:
                            xysize (440, 260)
                            background "#101626aa"
                            padding (15, 12)
                            vbox:
                                spacing 8
                                text "【 戰鬥衍生屬性 】" size 16 color "#ffaa00" bold True
                                $ mem_lvl = int(member.get('level', 1))
                                $ mem_exp = int(member.get('exp', 0))
                                $ mem_next_exp = get_next_level_exp(mem_lvl) if 'get_next_level_exp' in globals() else (mem_lvl * 100)
                                $ mem_cap = calculate_level_cap(member) if 'calculate_level_cap' in globals() else 30
                                text f"當前等級：Lv. {mem_lvl} / {mem_cap} (上限)" size 14 color "#ffff00" bold True
                                text f"經驗值 (EXP)：{mem_exp} / {mem_next_exp}" size 13 color "#00ffcc"
                                text f"生命值上限 (HP): {member.get('max_hp', 100)}" size 14 color "#ff6666"
                                text f"精神力上限 (MP): {member.get('max_mp', 50)}" size 14 color "#66ccff"
                                text f"物理攻擊力加成: +{member.get('atk_bonus', 0)}" size 14 color "#ffaa00"
                                text f"基因鎖階級: 第 {member.get('gene_lock', 0)} 階" size 14 color "#ff4444" bold True

                # 右側：5 大六圍屬性強化面板
                frame:
                    xysize (1040, 700)
                    background "#161b2ebb"
                    padding (25, 20)
                    vbox:
                        spacing 15
                        text "【 六圍基礎屬性分配 】" size 21 color "#00ffff" bold True
                        text "提升基礎屬性可滿足高階血統與暗黑裝備的【穿戴屬性門檻 (req_stats)】！" size 13 color "#aaaaaa"

                        null height 5

                        for s_code, s_info in STAT_NAMES_MAP.items():
                            $ s_k_lower = s_code.lower()
                            $ cur_val = member.get(s_k_lower, 20)
                            $ s_title = s_info["name"]
                            $ s_desc = s_info["desc"]

                            frame:
                                xysize (990, 100)
                                background "#101626aa"
                                padding (15, 10)
                                hbox:
                                    spacing 20
                                    yalign 0.5
                                    vbox:
                                        spacing 3
                                        xysize (420, None)
                                        text f"★ {s_title}：{cur_val} 點" size 17 color "#00ffff" bold True
                                        text f"{s_desc}" size 12 color "#bbbbbb"

                                    # 加點按鈕 (+1, +5, +10)
                                    hbox:
                                        spacing 10
                                        yalign 0.5
                                        button:
                                            xysize (160, 48)
                                            background ("#245e33" if points >= 10 else "#333333")
                                            hover_background "#358a4b"
                                            action Return(("allocate_stat", cur_idx, s_code, 1))
                                            text "+1 點 (10點數)" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5

                                        button:
                                            xysize (160, 48)
                                            background ("#245e33" if points >= 50 else "#333333")
                                            hover_background "#358a4b"
                                            action Return(("allocate_stat", cur_idx, s_code, 5))
                                            text "+5 點 (50點數)" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5

                                        button:
                                            xysize (170, 48)
                                            background ("#245e33" if points >= 100 else "#333333")
                                            hover_background "#358a4b"
                                            action Return(("allocate_stat", cur_idx, s_code, 10))
                                            text "+10 點 (100點數)" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5

            null height 5

            textbutton "【 🚪 完成加點，返回輪迴廣場 】":
                xalign 0.5
                action Return("leave_stat_screen")
                text_size 19
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


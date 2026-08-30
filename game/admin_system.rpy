# ==========================================
# 管理員特權指令系統 (admin_system.rpy)
# ==========================================

init python:
    # 1. 輪迴空間管理員特權指令解析核心
    def process_admin_command(cmd_str):
        global points, hp, team_roster
        if not cmd_str:
            return "【輪迴系統】指令不可為空。"
        cmd = cmd_str.strip().lower()
        roster = get_team_roster()
        player = roster[0] if roster and len(roster) > 0 else None
        
        # 1. 增加 100000 點生存點數指令 (如 addpoints / addpoint)
        if cmd in ("addpoints", "addpoint"):
            added = 100000
            points += added
            if player:
                player["points"] = points
            return f"【輪迴管理員權限生效】檢測到最高管理員密鑰：成功注入 {added} 點生存點數！\n目前可用生存點數：{points} 點。"
            
        # 2. 自訂增加點數 (如 addpoints 50000 或 points 50000)
        elif cmd.startswith("addpoints ") or cmd.startswith("points "):
            try:
                parts = cmd.split()
                val = int(parts[1])
                points += val
                if player:
                    player["points"] = points
                return f"【輪迴管理員權限生效】成功調整生存點數：+{val} 點！\n目前可用生存點數：{points} 點。"
            except Exception:
                return "【指令格式錯誤】範例：addpoints 50000"
                
        # 3. 狀態/全能量/全生命回復指令
        elif cmd in ("fullheal", "heal", "maxstat"):
            if player:
                player["hp"] = player.get("max_hp", 100)
                player["mp"] = player.get("max_mp", 50)
                for k in ["blood", "neili", "qi", "mental", "calc"]:
                    max_k = f"{k}_max"
                    cur_k = f"{k}_current"
                    if max_k in player and player[max_k] > 0:
                        player[cur_k] = player[max_k]
                hp = player["hp"]
            return "【輪迴管理員權限生效】聖光洗禮！全員重創已完全治癒，生命值與所有能量池已全部蓄滿！"
            
        # 4. 基因鎖解鎖指令
        elif cmd in ("genelock", "gene5", "unlockgene", "gene"):
            if player:
                player["gene_lock"] = 5
                player["survival_pressure"] = 0
            return "【輪迴管理員權限生效】強行破除基因鏈桎梏！主角基因鎖已直達【第 5 階·聖人之境】！"
            
        # 5. 至尊 GM 無敵模式
        elif cmd in ("godmode", "admin", "gm", "infinity"):
            points += 999999
            if player:
                player["points"] = points
                player["max_hp"] = 9999
                player["hp"] = 9999
                player["max_mp"] = 9999
                player["mp"] = 9999
                player["gene_lock"] = 5
                for k in ["blood", "neili", "qi", "mental", "calc"]:
                    player[f"{k}_max"] = 1000
                    player[f"{k}_current"] = 1000
                hp = player["hp"]
            # 贈送每種戰術裝備與消耗品各 10 個
            add_item("item_heal_spray", 10)
            add_item("item_mp_potion", 10)
            add_item("item_qi_elixir", 10)
            add_item("item_grenade", 10)
            add_item("weapon_gauss_rifle", 1)
            add_item("armor_nano_suit", 1)
            return "【輪迴至高神明權限已激活】GM模式已開啟：\n• 生存點數 +999,999 點\n• 生命值上限突破至 9999\n• 全部能量池上限擴充至 1000\n• 基因鎖直接登頂第 5 階！\n• 戰術背包已塞滿頂級高斯步槍、奈米裝甲與物資！"
            
        else:
            return f"【輪迴系統提示】未知特權指令「{cmd_str}」。\n\n支援的特權指令清單：\n• addpoints：增加 100,000 點生存點數\n• addpoints 50000：自訂增加指定點數\n• fullheal：生命與能量全部回滿\n• genelock：解鎖五階基因鎖\n• godmode：開啟無敵 GM 模式"


# ==========================================
# 輪迴空間管理員特權指令終端畫面
# ==========================================
screen admin_command_screen():

    default custom_cmd = "addpoints"

    modal True
    window:
        background "#000000bb"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (880, 620)
        padding (35, 30)
        background "#101626f5"

        vbox:
            spacing 15
            xalign 0.5

            text "【 🔑 輪迴空間 · 管理員特權指令終端 】" size 25 color "#ffcc00" bold True xalign 0.5
            text "請在下方輸入指令密碼（支援 addpoints、fullheal、genelock、godmode 等）：" size 15 color "#aaaaaa" xalign 0.5

            null height 5

            # 指令輸入區 (使用 ScreenVariableInputValue 雙向綁定)
            frame:
                xysize (810, 65)
                background "#1a2238ee"
                padding (15, 12)
                hbox:
                    spacing 10
                    yalign 0.5
                    text "COMMAND > " size 18 color "#00ffff" bold True yalign 0.5
                    input value ScreenVariableInputValue("custom_cmd") length 40 color "#ffffaa" size 18

            null height 5

            # 快捷指令按鈕
            text "【 快捷特權密令 (點擊直接生效) 】" size 16 color "#ffaa00" bold True
            grid 2 2:
                spacing 12
                xalign 0.5
                
                button:
                    xysize (395, 62)
                    background "#1f2a44"
                    hover_background "#2f4066"
                    padding (12, 8)
                    action Return("addpoints")
                    vbox:
                        text "⚡ 注入 +100,000 生存點數" size 15 color "#66ff66" bold True
                        text "指令碼：addpoints" size 12 color "#888888"

                button:
                    xysize (395, 62)
                    background "#1f2a44"
                    hover_background "#2f4066"
                    padding (12, 8)
                    action Return("fullheal")
                    vbox:
                        text "💊 全員生命與能量全滿" size 15 color "#66ccff" bold True
                        text "指令碼：fullheal" size 12 color "#888888"

                button:
                    xysize (395, 62)
                    background "#1f2a44"
                    hover_background "#2f4066"
                    padding (12, 8)
                    action Return("genelock")
                    vbox:
                        text "🧬 直接解鎖【五階基因鎖】" size 15 color "#ffaa00" bold True
                        text "指令碼：genelock" size 12 color "#888888"

                button:
                    xysize (395, 62)
                    background "#1f2a44"
                    hover_background "#2f4066"
                    padding (12, 8)
                    action Return("godmode")
                    vbox:
                        text "👑 至尊 GM 無敵模式 (+999k點/滿裝備)" size 15 color "#ff4444" bold True
                        text "指令碼：godmode" size 12 color "#888888"

            null height 10

            # 底部執行與關閉按鈕
            hbox:
                spacing 35
                xalign 0.5
                textbutton "【 ✅ 執行輸入指令 】":
                    action Return(custom_cmd)
                    text_size 19
                    text_idle_color "#00ff00"
                    text_hover_color "#ffffff"

                textbutton "【 ❌ 取消關閉 】":
                    action Return(None)
                    text_size 19
                    text_idle_color "#ff4444"
                    text_hover_color "#ff8888"


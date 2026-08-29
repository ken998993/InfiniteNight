# ==========================================
# 主神空間：自由探索與中央光球系統（共用 team_roster 整合版）
# ==========================================

# 定義一個自動將 1280x720 背景放大並置中填滿 1920x1080 的縮放特效
transform bg_scale_1080p:
    zoom 1.6
    xalign 0.5 yalign 0.5

# 初始化一個半透明黑色遮罩物件
image blackout_overlay = "#00000066"


# ==========================================
# 主神空間主標籤
# ==========================================
label main_room_exploration:
    # 1. 載入背景並套用放大特效
    scene bg_main_room_topdown at bg_scale_1080p

    # 2. 疊加一層半透明黑色遮罩讓背景變暗
    show blackout_overlay:
        xysize (1920, 1080)
    
    # 確保團隊與主角資料已初始化
    if 'team_roster' not in globals() or not team_roster:
        $ team_roster = get_team_roster()
    $ team_roster[0]["points"] = points

    # 呼叫主神空間的互動畫面
    call screen topdown_main_room

    # 接收畫面回傳的動作
    $ action_result = _return

    if action_result == "talk_zhang":
        jump zhang_jie_dialogue
    elif action_result == "exchange_core":
        jump main_exchange_shop    # 前往中央光球兌換介面
    elif action_result == "my_room":
        jump personal_room          # 進入主角房間
    elif action_result == "open_team_menu":
        jump view_team_status       # 開啟團隊狀態面板
    elif action_result == "admin_command":
        jump admin_command_entry    # 開啟特權指令終端
    elif action_result == "next_dungeon":
        jump select_next_dungeon    # 前往下一場副本
        
    return


# ==========================================
# 主神空間介面設計
# ==========================================
screen topdown_main_room():

    # 讓整個互動畫面撐滿 1920x1080 全螢幕
    add "#00000000" xysize (1920, 1080)

    # 1. 中央光球 (文字按鈕，點擊即可進行兌換)
    textbutton "【 💡 中央主神光球 (點擊兌換血統與技能) 】":
        xpos 710 ypos 380
        action Return("exchange_core")
        text_size 28
        text_idle_color "#00ffff"
        text_hover_color "#ffffff"

    # 2. 四周區域按鈕
    textbutton "【 你的房間 】":
        xpos 250 ypos 200
        action Return("my_room")
        text_size 24
        text_idle_color "#ffffff"
        text_hover_color "#00ffff"

    textbutton "【 張傑的位置 】":
        xpos 1400 ypos 250
        action Return("talk_zhang")
        text_size 24
        text_idle_color "#ffffff"
        text_hover_color "#00ffff"

    textbutton "【 團隊狀態與基因鎖 】":
        xpos 1080 ypos 920
        action Return("open_team_menu")
        text_size 26
        text_idle_color "#00ffcc"
        text_hover_color "#ffffff"

    textbutton "【 傳送大門 (下一關) 】":
        xpos 680 ypos 920
        action Return("next_dungeon")
        text_size 26
        text_idle_color "#ff6666"
        text_hover_color "#ff9999"

    # 3. 左上角積分狀態欄
    frame:
        xpos 40 ypos 40
        padding (20, 15)
        background "#000000cc"
        vbox:
            spacing 6
            text "【 主神空間廣場 】" size 20 color "#ffcc00"
            text "生存點數：[points] 點" size 18 color "#ffffff"
            $ cur_b = team_roster[0].get('bloodline', '無') if ('team_roster' in globals() and team_roster) else '無'
            text "當前血統：[cur_b]" size 15 color "#00ffff"

    # 4. 右上角管理員特權指令按鈕
    textbutton "【 🔑 特權密令 (addpoints) 】":
        xpos 1460 ypos 40
        action Return("admin_command")
        text_size 22
        text_idle_color "#ffcc00"
        text_hover_color "#ffffff"


# ==========================================
# 點擊光球後彈出的血統與專屬技能兌換強化系統
# ==========================================
screen item_exchange_screen():

    default current_tab = "vampire_bloodline"
    default current_grade = "C"

    # 取得血統資料庫與玩家資料
    $ catalog = get_bloodlines_data()
    $ player_member = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]
    $ player_bloodline = player_member.get('bloodline', '無')
    $ player_hp = player_member.get('hp', 100)
    $ player_max_hp = player_member.get('max_hp', 100)

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1720, 960)
        padding (30, 25)
        background "#0d111edd"

        vbox:
            spacing 12
            xalign 0.5

            # 頂部狀態資訊列
            hbox:
                spacing 30
                xalign 0.5
                text "【 主神石碑 · 血統強化與專屬技能兌換系統 】" size 25 color "#ffcc00" bold True yalign 0.5
                text "個人生存點數：[points] 點" size 22 color "#00ffcc" bold True yalign 0.5
                text "當前血統：[player_bloodline]" size 17 color "#ffaa88" yalign 0.5
                text "HP：[player_hp]/[player_max_hp]" size 17 color "#ff6666" yalign 0.5
                
                textbutton "【 🔑 特權密令 】":
                    action Return("admin_command")
                    text_size 18
                    text_idle_color "#ffcc00"
                    text_hover_color "#ffffff"
                    yalign 0.5

            null height 2

            # 主體雙欄佈局：左側為血統/道具分類列表，右側為詳細屬性、招式預覽與兌換操作
            hbox:
                spacing 25
                xalign 0.5

                # --------------------------------
                # 左側：血統體系選擇列表
                # --------------------------------
                frame:
                    xysize (480, 780)
                    background "#161b2ebb"
                    padding (20, 15)

                    vbox:
                        spacing 10
                        text "【 選擇強化體系 / 血統列表 】" size 19 color "#ffcc00"
                        null height 5

                        viewport:
                            xysize (440, 700)
                            scrollbars "vertical"
                            mousewheel True
                            draggable True

                            vbox:
                                spacing 10
                                for b in catalog:
                                    $ b_id = b.get('id', '')
                                    $ b_name = b.get('name', '未知血統')
                                    $ b_energy = b.get('energy_name', '特殊能量')
                                    $ is_selected = (current_tab == b_id)
                                    
                                    button:
                                        xysize (420, 90)
                                        if is_selected:
                                            background "#3b5288ee"
                                        else:
                                            background "#222a42aa"
                                        hover_background "#4a68aaaa"
                                        padding (12, 10)
                                        action [SetScreenVariable("current_tab", b_id), SetScreenVariable("current_grade", "C")]

                                        vbox:
                                            spacing 3
                                            text "★ [b_name]" size 17 color ("#00ffff" if is_selected else "#ffffff") bold True
                                            text "核心體系：[b_energy] 專精" size 13 color "#aaaaaa"
                                            $ cur_g_info = b.get("grades", {}).get("C", {})
                                            $ min_pts = cur_g_info.get("points", 2500)
                                            text "階級支援：C / B / A / S 階 (最低 [min_pts] 點起)" size 12 color "#ffcc00"

                                null height 10
                                # 戰術物資分類
                                $ is_item_tab = (current_tab == "tactical_items")
                                button:
                                    xysize (420, 80)
                                    if is_item_tab:
                                        background "#553366ee"
                                    else:
                                        background "#332244aa"
                                    hover_background "#664477aa"
                                    padding (12, 10)
                                    action SetScreenVariable("current_tab", "tactical_items")

                                    vbox:
                                        spacing 3
                                        text "📦 戰術物資與應急補給品" size 17 color ("#ff88ff" if is_item_tab else "#ddaaff") bold True
                                        text "急救噴霧、彈藥包、高爆破片手榴彈" size 13 color "#aaaaaa"

                # --------------------------------
                # 右側：血統階級詳情、技能解鎖預覽與兌換按鈕
                # --------------------------------
                frame:
                    xysize (1150, 780)
                    background "#161b2ebb"
                    padding (25, 20)

                    if current_tab == "tactical_items":
                        # 戰術物資面板
                        vbox:
                            spacing 20
                            text "【 戰術物資 · 應急軍火與生化藥劑兌換 】" size 22 color "#ff88ff" bold True
                            text "主神空間常備作戰物資，可用於戰鬥中應急補給與範圍轟炸。" size 15 color "#cccccc"
                            null height 10

                            hbox:
                                spacing 20
                                # 彈藥
                                frame:
                                    xysize (340, 240)
                                    background "#222a42dd"
                                    padding (15, 15)
                                    vbox:
                                        spacing 10
                                        text "🔫 標準槍械彈藥箱" size 18 color "#00ffff" bold True
                                        text "補充常規 9mm / 5.56mm 彈藥。" size 14 color "#aaaaaa"
                                        text "消耗：100 生存點數" size 15 color "#ffcc00"
                                        null height 20
                                        textbutton "【 立即兌換 (100點) 】":
                                            action Return("buy_ammo")
                                            text_size 15 text_idle_color "#00ff00" text_hover_color "#ffffff"

                                # 急救噴霧
                                frame:
                                    xysize (340, 240)
                                    background "#222a42dd"
                                    padding (15, 15)
                                    vbox:
                                        spacing 10
                                        text "💊 主神止血急救噴霧" size 18 color "#66ff66" bold True
                                        text "迅速止血，戰鬥中立即恢復 60 HP。" size 14 color "#aaaaaa"
                                        text "消耗：150 生存點數" size 15 color "#ffcc00"
                                        null height 20
                                        textbutton "【 立即兌換 (150點) 】":
                                            action Return("buy_spray")
                                            text_size 15 text_idle_color "#00ff00" text_hover_color "#ffffff"

                                # 手榴彈
                                frame:
                                    xysize (340, 240)
                                    background "#222a42dd"
                                    padding (15, 15)
                                    vbox:
                                        spacing 10
                                        text "💣 高爆破片手榴彈" size 18 color "#ff6666" bold True
                                        text "投擲造成 85 點全體範圍爆炸傷害。" size 14 color "#aaaaaa"
                                        text "消耗：200 生存點數" size 15 color "#ffcc00"
                                        null height 20
                                        textbutton "【 立即兌換 (200點) 】":
                                            action Return("buy_grenade")
                                            text_size 15 text_idle_color "#00ff00" text_hover_color "#ffffff"

                    else:
                        # 血統詳情面板
                        $ selected_bloodline = get_bloodline_by_id(current_tab)
                        if selected_bloodline:
                            $ grades_dict = selected_bloodline.get("grades", {})
                            $ cur_grade_data = grades_dict.get(current_grade, {})
                            $ cost_points = cur_grade_data.get("points", 0)
                            $ fate_shard = cur_grade_data.get("fate_shard", cur_grade_data.get("side_story", "C"))
                            $ grade_name = cur_grade_data.get("name", "未命名階級")
                            $ grade_skills = cur_grade_data.get("skills", [])
                            $ grade_attrs = cur_grade_data.get("attributes", {})
                            $ can_afford = (points >= cost_points)

                            vbox:
                                spacing 12
                                
                                # 血統標題與描述
                                vbox:
                                    spacing 4
                                    text "[selected_bloodline.get('name', '')]" size 23 color "#00ffff" bold True
                                    text "[selected_bloodline.get('desc', '')]" size 14 color "#bbbbbb"

                                null height 2

                                # 階級切換標籤列 (C / B / A / S 階)
                                hbox:
                                    spacing 15
                                    text "選擇血統階級：" size 16 color "#ffcc00" yalign 0.5
                                    for g_key in ["C", "B", "A", "S"]:
                                        if g_key in grades_dict:
                                            $ is_g_active = (current_grade == g_key)
                                            $ g_cost = grades_dict[g_key].get("points", 0)
                                            button:
                                                xysize (180, 42)
                                                if is_g_active:
                                                    background "#e6a100"
                                                else:
                                                    background "#2b354f"
                                                hover_background "#53648f"
                                                action SetScreenVariable("current_grade", g_key)
                                                text f"★ {g_key} 階 ({g_cost}點)" size 15 color ("#000000" if is_g_active else "#ffffff") bold True xalign 0.5 yalign 0.5

                                null height 2

                                # 當前選定階級屬性與技能展示框 (支援平滑滾動)
                                frame:
                                    xysize (1100, 470)
                                    background "#0f1424aa"
                                    padding (18, 15)

                                    viewport:
                                        xysize (1064, 440)
                                        scrollbars "vertical"
                                        mousewheel True
                                        draggable True

                                        vbox:
                                            spacing 12

                                            # 第一區塊：兌換條件與屬性加成
                                            hbox:
                                                spacing 30
                                                vbox:
                                                    spacing 4
                                                    xysize (360, None)
                                                    text "【 階級名稱 】[grade_name]" size 16 color "#ffcc00" bold True
                                                    text f"【 需求點數 】{cost_points} 生存點數" size 15 color ("#66ff66" if can_afford else "#ff4444") bold True
                                                    text f"【 命運碎片 】{fate_shard} 階命運碎片 x 1" size 14 color "#ffffff"

                                                vbox:
                                                    spacing 4
                                                    xysize (650, None)
                                                    text "【 屬性與能量池增益 】" size 16 color "#00ffcc" bold True
                                                    hbox:
                                                        spacing 20
                                                        $ hp_gain = grade_attrs.get('hp', grade_attrs.get('max_hp', 0))
                                                        if hp_gain > 0:
                                                            text "生命值上限 +[hp_gain]" size 14 color "#ff6666"
                                                        if grade_attrs.get('blood_max', 0) > 0:
                                                            $ b_max = grade_attrs['blood_max']
                                                            text "血族能量上限 +[b_max]" size 14 color "#ff4444"
                                                        if grade_attrs.get('neili_max', 0) > 0:
                                                            $ n_max = grade_attrs['neili_max']
                                                            text "混元內力上限 +[n_max]" size 14 color "#ffaa00"
                                                        if grade_attrs.get('qi_max', 0) > 0:
                                                            $ q_max = grade_attrs['qi_max']
                                                            text "氣血之力上限 +[q_max]" size 14 color "#ff6666"
                                                        if grade_attrs.get('mental_max', 0) > 0:
                                                            $ m_max = grade_attrs['mental_max']
                                                            text "精神力場上限 +[m_max]" size 14 color "#00ccff"
                                                        if grade_attrs.get('regeneration', 0) > 0:
                                                            $ reg = grade_attrs['regeneration']
                                                            text "自癒恢復速度 +[reg]" size 14 color "#66ff66"

                                            # 分隔線
                                            null height 2
                                            add "#334466" xysize (1050, 1)
                                            null height 2

                                            # 第二區塊：專屬戰鬥技能列表
                                            vbox:
                                                spacing 8
                                                text f"【 該階級可習得/升級之專屬技能 (共 {len(grade_skills)} 招) 】" size 17 color "#ffaa00" bold True

                                                for sk in grade_skills:
                                                    $ sk_name = sk.get('name', '未知招式')
                                                    $ sk_cost = sk.get('energy_cost', sk.get('cost_energy', 0))
                                                    $ sk_type = sk.get('energy_type', 'mp')
                                                    $ sk_dmg = sk.get('damage', 0)
                                                    $ sk_heal = sk.get('heal', 0)
                                                    $ sk_desc = sk.get('desc', '')

                                                    frame:
                                                        xysize (1040, None)
                                                        background "#1c2338aa"
                                                        padding (12, 10)

                                                        vbox:
                                                            spacing 4
                                                            hbox:
                                                                spacing 15
                                                                text "🔥 [sk_name]" size 16 color "#00ffff" bold True
                                                                text f"消耗: {sk_cost} 點 ({sk_type})" size 14 color "#ffcc00"
                                                                if sk_dmg > 0:
                                                                    text f"威力: {sk_dmg} 傷害" size 14 color "#ff6666" bold True
                                                                if sk_heal > 0:
                                                                    text f"自癒: +{sk_heal} HP" size 14 color "#66ff66" bold True

                                                            text "招式效果：[sk_desc]" size 13 color "#cccccc"

                                null height 4

                                # 底部兌換操作按鈕
                                hbox:
                                    spacing 20
                                    xalign 0.5
                                    if can_afford:
                                        textbutton f"【 ⚡ 立即扣除 {cost_points} 點數兌換【{grade_name}】 】":
                                            action Return(("buy_bloodline", current_tab, current_grade))
                                            text_size 19
                                            text_idle_color "#00ff00"
                                            text_hover_color "#ffffff"
                                    else:
                                        $ pts_needed = cost_points - points
                                        textbutton f"【 ❌ 生存點數不足 (尚缺 {pts_needed} 點) 】":
                                            action NullAction()
                                            text_size 18
                                            text_idle_color "#884444"

            null height 5

            # 離開光球返回廣場按鈕
            textbutton "【 🚪 關閉兌換清單，返回主神廣場 】":
                xalign 0.5
                action Return("leave")
                text_size 20
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


# ==========================================
# 主神空間管理員特權指令終端畫面
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

            text "【 🔑 主神空間 · 管理員特權指令終端 】" size 25 color "#ffcc00" bold True xalign 0.5
            text "請在下方輸入指令密碼（支援 addpoints、fullheal、genelock、godmode 等）：" size 15 color "#aaaaaa" xalign 0.5

            null height 5

            # 指令輸入區
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
                        text "👑 至尊 GM 無敵模式 (+999k點/滿血)" size 15 color "#ff4444" bold True
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


# ==========================================
# 各房間與劇情互動邏輯分支
# ==========================================
label zhang_jie_dialogue:
    "你走到張傑身旁。他正叼著菸，靠在柱子上喝酒。"
    "張傑瞥了你一眼，笑道：「怎麼？覺得主神空間殘酷？在這裡，只要有積分，你連神都能兌換出來。活下去，才有未來。」"
    jump main_room_exploration

label personal_room:
    "你推開了屬於你的私人房間大門，在絕對安全的房間內稍微休息、調整裝備，精神恢復了不少。"
    jump main_room_exploration

label view_team_status:
    # 即時將目前主角的點數同步更新到團隊列表第一位
    if 'team_roster' not in globals() or not team_roster:
        $ team_roster = get_team_roster()
    $ team_roster[0]["points"] = points
    
    call screen team_status_screen(page=0)
    jump main_room_exploration

# 主神特權指令執行分支
label admin_command_entry:
    call screen admin_command_screen
    $ cmd_input = _return
    if cmd_input:
        $ res_cmd_msg = process_admin_command(cmd_input)
        python:
            if renpy.loadable("audio/levelup.ogg"):
                renpy.sound.play("audio/levelup.ogg")
        z "[res_cmd_msg]"
    jump main_room_exploration

label admin_command_entry_from_shop:
    call screen admin_command_screen
    $ cmd_input = _return
    if cmd_input:
        $ res_cmd_msg = process_admin_command(cmd_input)
        python:
            if renpy.loadable("audio/levelup.ogg"):
                renpy.sound.play("audio/levelup.ogg")
        z "[res_cmd_msg]"
    jump main_exchange_shop

# 中央光球商店邏輯
label main_exchange_shop:
    call screen item_exchange_screen
    $ shop_choice = _return
    
    if shop_choice == "admin_command":
        jump admin_command_entry_from_shop
        
    elif isinstance(shop_choice, tuple) and len(shop_choice) >= 3 and shop_choice[0] == "buy_bloodline":
        $ b_id = shop_choice[1]
        $ g_key = shop_choice[2]
        $ res = purchase_bloodline(b_id, g_key)
        $ res_msg = res.get("msg", "")
        
        if res.get("success", False):
            # 播放強化光柱音效（若存在）
            python:
                if renpy.loadable("audio/levelup.ogg"):
                    renpy.sound.play("audio/levelup.ogg")
            z "[res_msg]"
        else:
            z "[res_msg]"
            
        jump main_exchange_shop
        
    elif shop_choice == "buy_ammo":
        if points >= 100:
            $ points -= 100
            if 'team_roster' in globals() and team_roster:
                $ team_roster[0]["points"] = points
            z "兌換成功：獲得 9mm 標準彈藥補給包。"
        else:
            z "光球冰冷地機械音響起：「您的生存點數不足。」"
        jump main_exchange_shop

    elif shop_choice == "buy_spray":
        if points >= 150:
            $ points -= 150
            if 'team_roster' in globals() and team_roster:
                $ team_roster[0]["points"] = points
            z "兌換成功：獲得【主神止血急救噴霧】。"
        else:
            z "光球冰冷地機械音響起：「您的生存點數不足。」"
        jump main_exchange_shop

    elif shop_choice == "buy_grenade":
        if points >= 200:
            $ points -= 200
            if 'team_roster' in globals() and team_roster:
                $ team_roster[0]["points"] = points
            z "兌換成功：獲得【高爆破片手榴彈】。"
        else:
            z "光球冰冷地機械音響起：「您的生存點數不足。」"
        jump main_exchange_shop
        
    elif shop_choice == "leave":
        jump main_room_exploration

    jump main_room_exploration

label select_next_dungeon:
    "你站在巨大的傳送光門前，深吸了一口氣，準備迎接下一個殘酷的恐怖片副本……"
    jump zombieCity
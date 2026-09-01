# ==========================================
# 輪迴空間：中央廣場自由探索與導航樞紐 (main_room.rpy)
# ==========================================

init python:
    STAGE_PROGRESSION = [
        {"id": 1, "name": "第一世界 · 喪屍末日 (極光重工)", "label": "stage_1_1_zombie_city"},
        {"id": 2, "name": "第二世界 · 太空真空 (幽靈母艦)", "label": "stage_1_2_alien_ship"},
        {"id": 3, "name": "第三世界 · 日式靈異 (咒怨凶宅)", "label": "stage_1_3_the_grudge"},
        {"id": 4, "name": "第四世界 · 修真神魔 (蜀山血海)", "label": "stage_1_4_cultivation_realm"},
        {"id": 5, "name": "第五世界 · 木乃伊遺跡 (印洲隊團戰)", "label": "stage_1_5_team_battle_india"}
    ]

    def get_next_stage_info():
        cur_idx = current_main_stage_index if 'current_main_stage_index' in globals() else 1
        if 1 <= cur_idx <= len(STAGE_PROGRESSION):
            return STAGE_PROGRESSION[cur_idx - 1]
        return None

transform bg_scale_1080p:
    xsize 1920
    ysize 1080
    xalign 0.5 yalign 0.5

image blackout_overlay = "#00000066"

# 中央主神光球動畫 (只保留純淨去背 ball1.png，呼吸縮放與發光脈動)
image main_god_orb_anim:
    "images/ball1.png"
    xsize 260 ysize 260
    xalign 0.5 yalign 0.5
    alpha 0.95 zoom 1.0
    ease 0.85 alpha 0.65 zoom 0.95
    ease 0.85 alpha 1.0 zoom 1.05
    repeat


# ==========================================
# 輪迴空間主探索標籤
# ==========================================
label main_room_exploration:
    scene bg_main_room_topdown at bg_scale_1080p

    show blackout_overlay:
        xysize (1920, 1080)
    
    if 'team_roster' not in globals() or not team_roster:
        $ team_roster = get_team_roster()
    $ team_roster[0]["points"] = points

    call screen topdown_main_room

    $ action_result = _return

    if action_result == "exchange_core":
        jump main_exchange_hub      # 中央光球總兌換中心
    elif action_result == "open_bloodline":
        jump bloodline_exchange_shop # 血統強化石碑
    elif action_result == "open_stat_alloc":
        jump stat_allocation_hub    # 六圍屬性加點石碑
    elif action_result == "open_training_dummy":
        jump training_dummy_hub     # 全息模擬稻草人
    elif action_result == "open_inventory":
        jump inventory_menu         # 個人戰術背包
    elif action_result == "open_workshop":
        jump fate_shard_workshop_hub # 命運碎片工坊
    elif action_result == "full_heal":
        jump full_heal_action       # 輪迴全身修復
    elif action_result == "open_item_shop":
        jump item_shop_hub          # 軍火與物資商城
    elif action_result == "open_team_menu":
        jump view_team_status       # 團隊狀態面板
    elif action_result == "open_deployment":
        jump party_deployment_hub   # 戰前 6 人陣型與出戰配置
    elif action_result == "admin_command":
        jump admin_command_entry    # 管理員特權指令
    elif action_result == "open_home_base":
        jump home_base_hub          # 專屬神域家園
    elif action_result == "my_room":
        jump personal_room          # 主角私人房間
    elif action_result == "talk_lengyue":
        jump lengyue_dialogue       # 與冷月對話
    elif action_result == "next_dungeon":
        jump campaign_select_entry  # 進入五大副本世界大門
    elif action_result == "enter_next_world_story":
        $ next_stg = get_next_stage_info()
        if next_stg:
            $ n_label = next_stg.get("label")
            $ n_name = next_stg.get("name")
            menu:
                "【 🚀 立即啟程傳送：[n_name] (主線推進，通關後無法重複遊玩) 】":
                    $ renpy.jump(n_label)
                "【 稍作整裝與修煉 (返回廣場) 】":
                    jump main_room_exploration
        jump main_room_exploration
    elif action_result == "all_stages_cleared_msg":
        z "【全主線已通關】恭喜！中洲隊已完美通關全部 5 大主線輪迴世界！所有主線劇情已封存，您可以自由使用傳送門探索大地圖或在神域家園中修煉成長！"
        jump main_room_exploration
        
    return


# ==========================================
# 輪迴空間互動畫面介面 (topdown_main_room)
# ==========================================
screen topdown_main_room():

    default show_main_god_menu = False

    add "#00000000" xysize (1920, 1080)

    # 1. 中央主神大光球動畫 (只保留純淨去背 ball1.png 呼吸脈動，下移至正中間)
    imagebutton:
        xalign 0.5 ypos (210 if show_main_god_menu else 360)
        idle "main_god_orb_anim"
        hover Transform("images/ball1.png", xsize=280, ysize=280, xalign=0.5, yalign=0.5, alpha=1.0)
        action ToggleScreenVariable("show_main_god_menu")

    # 2. 光球下方狀態 / 展開選單
    if not show_main_god_menu:
        textbutton "【 💡 連結主神光球 (點擊展開兌換/商城/強化選單) 】":
            xalign 0.5 ypos 640
            action ToggleScreenVariable("show_main_god_menu")
            text_size 24 text_idle_color "#00ffff" text_hover_color "#ffffff"
    else:
        textbutton "【 ❌ 收起主神兌換選單 】":
            xalign 0.5 ypos 160
            action SetScreenVariable("show_main_god_menu", False)
            text_size 20 text_idle_color "#ff6666" text_hover_color "#ffffff"

        # 主神中央指令選單面板 (購買、兌換、加點、修復、工坊)
        frame:
            xalign 0.5 ypos 480
            xsize 940
            padding (25, 18)
            background "#0b1220f5"

            vbox:
                spacing 10
                xalign 0.5

                hbox:
                    spacing 25
                    xalign 0.5
                    textbutton "【 🛒 軍火與物資商城 】":
                        action Return("open_item_shop")
                        text_size 22 text_idle_color "#00ffff" text_hover_color "#ffffff"

                    textbutton "【 🧬 血統兌換與強化 】":
                        action Return("exchange_core")
                        text_size 22 text_idle_color "#ddaaff" text_hover_color "#ffffff"

                hbox:
                    spacing 25
                    xalign 0.5
                    textbutton "【 ⚡ 六圍屬性加點 (10點=1屬性) 】":
                        action Return("open_stat_alloc")
                        text_size 20 text_idle_color "#00ffcc" text_hover_color "#ffffff"

                    textbutton "【 🎯 全息模擬稻草人 (DPS測試) 】":
                        action Return("open_training_dummy")
                        text_size 20 text_idle_color "#ffcc00" text_hover_color "#ffffff"

                hbox:
                    spacing 25
                    xalign 0.5
                    textbutton "【 🎒 個人戰術背包 (8大部位) 】":
                        action Return("open_inventory")
                        text_size 20 text_idle_color "#66ff66" text_hover_color "#ffffff"

                    textbutton "【 🔮 命運碎片工坊 (合成 / 拆解) 】":
                        action Return("open_workshop")
                        text_size 20 text_idle_color "#ddaaff" text_hover_color "#ffffff"

                hbox:
                    spacing 25
                    xalign 0.5
                    textbutton "【 💖 輪迴全身修復 (消耗 100 點) 】":
                        action Return("full_heal")
                        text_size 20 text_idle_color "#ff88aa" text_hover_color "#ffffff"

                    textbutton "【 🏰 專屬神域家園 (工坊/修煉/羈絆) 】":
                        action Return("open_home_base")
                        text_size 20 text_idle_color "#ffd700" text_hover_color "#ffffff"

    # 4.5. 進入下一個世界主線按鈕 (線性推進，不可重複回溯)
    $ next_stg = get_next_stage_info()
    if next_stg:
        $ n_stg_name = next_stg.get("name")
        textbutton f"【 🌌 進入下一個世界：{n_stg_name} 】":
            xalign 0.5 ypos (800 if show_main_god_menu else 730)
            action Return("enter_next_world_story")
            text_size 23 text_idle_color "#00ffea" text_hover_color "#ffffff"
    else:
        textbutton "【 🏆 全主線輪迴世界已通關 (中洲隊登頂) 】":
            xalign 0.5 ypos (800 if show_main_god_menu else 730)
            action Return("all_stages_cleared_msg")
            text_size 22 text_idle_color "#888888" text_hover_color "#aaaaaa"

    # 5. 四周區域按鈕 (你的房間：平時 door1 關閉，懸停時 door2 打開)
    imagebutton:
        xpos 220 ypos 95
        idle Transform("images/door1.png", xsize=170, ysize=205)
        hover Transform("images/door2.png", xsize=170, ysize=205)
        action Return("my_room")

    textbutton "【 你的房間 】":
        xpos 235 ypos 305
        action Return("my_room")
        text_size 23 text_idle_color "#ffffff" text_hover_color "#00ffff"

    textbutton "【 冷月的位置 】":
        xpos 1400 ypos 250
        action Return("talk_lengyue")
        text_size 24 text_idle_color "#ffffff" text_hover_color "#00ffff"

    textbutton "【 👥 團隊名冊與基因鎖 】":
        xpos 1180 ypos 920
        action Return("open_team_menu")
        text_size 24 text_idle_color "#00ffcc" text_hover_color "#ffffff"

    textbutton "【 ⚔️ 戰前 6 人陣型配置 】":
        xpos 760 ypos 920
        action Return("open_deployment")
        text_size 24 text_idle_color "#ffaa00" text_hover_color "#ffffff"

    textbutton "【 🚪 傳送大門 (五大副本) 】":
        xpos 380 ypos 920
        action Return("next_dungeon")
        text_size 24 text_idle_color "#ff6666" text_hover_color "#ff9999"

    # 5. 左上角積分與碎片狀態欄
    $ shards = get_fate_shards() if 'get_fate_shards' in globals() else {}
    $ next_stg = get_next_stage_info()
    $ stg_progress_txt = next_stg.get('name') if next_stg else '👑 全主線已通關'
    $ save_name = f"顧臨淵 | 主線進度：{stg_progress_txt}"
    frame:
        xpos 40 ypos 40
        padding (20, 15)
        background "#000000cc"
        vbox:
            spacing 5
            text "【 輪迴空間廣場 】" size 20 color "#ffcc00"
            text f"主線進度: {stg_progress_txt}" size 14 color "#00ffea" bold True
            text f"生存點數: {points} 點" size 17 color "#ffffff"
            text f"命運碎片: D({shards.get('D',0)}) C({shards.get('C',0)}) B({shards.get('B',0)}) A({shards.get('A',0)}) S({shards.get('S',0)})" size 14 color "#ddaaff"
            $ cur_b = team_roster[0].get('bloodline', '無') if ('team_roster' in globals() and team_roster) else '無'
            text f"當前血統: {cur_b}" size 13 color "#00ffff"

    # 6. 右上角管理員特權指令按鈕
    textbutton "【 🔑 特權密令 (addpoints) 】":
        xpos 1460 ypos 40
        action Return("admin_command")
        text_size 22 text_idle_color "#ffcc00" text_hover_color "#ffffff"


# ==========================================
# 輪迴全身修復邏輯 (消耗 100 點數)
# ==========================================
label full_heal_action:
    if points >= 100:
        $ points -= 100
        if 'team_roster' in globals() and team_roster:
            $ team_roster[0]["points"] = points
            python:
                for m in team_roster:
                    m["hp"] = m.get("max_hp", 100)
                    m["mp"] = m.get("max_mp", 50)
                    m["status"] = "良好"
                    for k in ["blood", "neili", "qi", "mental", "calc"]:
                        max_k = f"{k}_max"
                        cur_k = f"{k}_current"
                        if max_k in m and m[max_k] > 0:
                            m[cur_k] = m[max_k]
                hp = team_roster[0]["hp"]
        python:
            if renpy.loadable("audio/levelup.ogg"):
                renpy.sound.play("audio/levelup.ogg")
        z "【輪迴聖光洗禮】一陣溫暖純淨的乳白色神聖光柱從大廳穹頂傾瀉而下，籠罩了全體隊員！\n全員所有殘疾、重傷與 Debuff 狀態已徹底淨化，生命值與全部能量池已全部補滿！（消耗 100 生存點數）"
    else:
        z "光球傳來冰冷機械音：「您的生存點數不足 100 點，無法啟動全身修復程序。」"
    jump main_room_exploration


# ==========================================
# 命運碎片工坊分支 (fate_shard_workshop_hub)
# ==========================================
label fate_shard_workshop_hub:
    call screen fate_shard_workshop_screen
    $ ws_res = _return
    
    if isinstance(ws_res, tuple) and len(ws_res) >= 2:
        $ op = ws_res[0]
        $ tier = ws_res[1]
        if op == "synth":
            $ res = synthesize_fate_shard(tier)
            z "[res['msg']]"
            jump fate_shard_workshop_hub
        elif op == "dismantle":
            $ res = dismantle_fate_shard(tier)
            z "[res['msg']]"
            jump fate_shard_workshop_hub
            
    elif ws_res == "close_workshop":
        jump main_room_exploration
        
    jump main_room_exploration


# ==========================================
# 輪迴中央光球兌換總樞紐
# ==========================================
label main_exchange_hub:
    menu:
        "【 🧬 強化基因血統與專屬戰技 (3槽位/同路線升級補差價) 】":
            jump bloodline_exchange_shop

        "【 ⚔️ 戰前 6 人陣型與前後排配置 (Party Deployment) 】":
            jump party_deployment_hub

        "【 📊 核心六圍屬性加點 (10點數 = +1 指定屬性) 】":
            jump stat_allocation_hub

        "【 🎯 虛空廣場 · 全息模擬稻草人 (DPS與配裝木樁測試) 】":
            jump training_dummy_hub

        "【 🛒 進入軍火裝備商城 (8大暗黑部位/科技與魔法) 】":
            jump item_shop_hub

        "【 🔮 開啟命運碎片工坊 (4階碎片合成與拆解) 】":
            jump fate_shard_workshop_hub

        "【 🎒 開啟個人戰術背包 (檢視/穿戴裝備) 】":
            jump inventory_menu

        "【 返回輪迴廣場 】":
            jump main_room_exploration


# ==========================================
# 戰前 6 人陣型與出戰配置分支 (party_deployment_hub)
# ==========================================
label party_deployment_hub:
    call screen party_deployment_screen
    $ dep_res = _return
    if dep_res == "start_battle_with_deployment":
        z "⚔️【陣容配置已儲存】當前 6 人出戰名單與前後排站位已更新！進入戰鬥時將自動採用此陣型！"
        jump main_room_exploration
    elif dep_res == "cancel_deployment":
        jump main_room_exploration
    jump main_room_exploration


# ==========================================
# 屬性加點石碑分支 (stat_allocation_hub)
# ==========================================
label stat_allocation_hub:
    call screen stat_allocation_screen
    $ st_res = _return
    if isinstance(st_res, tuple) and len(st_res) >= 4 and st_res[0] == "allocate_stat":
        $ m_idx = st_res[1]
        $ s_code = st_res[2]
        $ cnt = st_res[3]
        $ res = allocate_stat_points(m_idx, s_code, cnt)
        z "[res['msg']]"
        jump stat_allocation_hub
    elif st_res == "leave_stat_screen":
        jump main_room_exploration
    jump main_room_exploration


# ==========================================
# 全息模擬稻草人分支 (training_dummy_hub)
# ==========================================
label training_dummy_hub:
    call screen training_dummy_screen
    $ td_res = _return
    if td_res == "launch_simulation":
        $ b_state = start_simulation_battle()
        call screen battle_screen(b_state)
        $ end_simulation_battle()
        z "🎯【全息模擬戰鬥結束】全息虛擬系統已關閉！\n戰前所有隊員血量、精神力與戰術背包物資已 100%% 無損還原！"
        jump training_dummy_hub
    elif td_res == "leave_simulator":
        jump main_room_exploration
    jump main_room_exploration


# ==========================================
# 血統強化石碑分支
# ==========================================
label bloodline_exchange_shop:
    call screen bloodline_exchange_screen
    $ b_choice = _return
    
    if b_choice == "admin_command":
        call screen admin_command_screen
        $ cmd_res = _return
        if cmd_res:
            $ msg = process_admin_command(cmd_res)
            z "[msg]"
        jump bloodline_exchange_shop
        
    elif isinstance(b_choice, tuple) and len(b_choice) >= 3 and b_choice[0] == "buy_bloodline":
        $ b_id = b_choice[1]
        $ g_key = b_choice[2]
        $ res = purchase_bloodline(b_id, g_key)
        $ res_msg = res.get("msg", "")
        if res.get("success", False):
            python:
                if renpy.loadable("audio/levelup.ogg"):
                    renpy.sound.play("audio/levelup.ogg")
            z "[res_msg]"
        else:
            z "[res_msg]"
        jump bloodline_exchange_shop
        
    elif b_choice == "leave_bloodline":
        jump main_room_exploration
        
    jump main_room_exploration


# ==========================================
# 道具商城分支
# ==========================================
label item_shop_hub:
    call screen item_shop_screen
    $ s_choice = _return
    
    if isinstance(s_choice, tuple) and len(s_choice) >= 2 and s_choice[0] == "buy_item":
        $ itm_id = s_choice[1]
        $ res = purchase_shop_item(itm_id, 1)
        $ res_msg = res.get("msg", "")
        z "[res_msg]"
        jump item_shop_hub
        
    elif s_choice == "leave_shop":
        jump main_room_exploration
        
    jump main_room_exploration


# ==========================================
# 個人戰術背包分支
# ==========================================
label inventory_menu:
    call screen inventory_screen
    $ inv_action = _return
    
    if isinstance(inv_action, tuple) and len(inv_action) >= 2:
        $ act_type = inv_action[0]
        $ target_id = inv_action[1]
        
        if act_type == "equip":
            $ res = equip_item(target_id, 0)
            z "[res['msg']]"
            jump inventory_menu
            
        elif act_type == "unequip":
            $ res = unequip_item(target_id, 0)
            z "[res['msg']]"
            jump inventory_menu
            
        elif act_type == "use_item":
            $ res = use_inventory_item(target_id, 0)
            z "[res['msg']]"
            jump inventory_menu
            
        elif act_type == "discard":
            $ remove_item(target_id, 1)
            $ itm = get_item_by_id(target_id)
            $ d_name = itm.get('name', '物品') if itm else '物品'
            z "已自背包丟棄【[d_name]】x1。"
            jump inventory_menu
            
    elif inv_action == "close_inventory":
        jump main_room_exploration
        
    jump main_room_exploration


# ==========================================
# 管理員特權指令終端
# ==========================================
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


# ==========================================
# 副本世界傳送與新人道德抉擇入口
# ==========================================
label campaign_select_entry:
    call screen campaign_world_select_screen
    $ w_sel = _return
    
    if w_sel == "cancel":
        jump main_room_exploration
        
    elif isinstance(w_sel, tuple) and len(w_sel) >= 2 and w_sel[0] == "select_world":
        $ current_campaign_world = w_sel[1]
        $ reset_campaign_nodes()
        
        if current_campaign_world == "zombie":
            menu:
                "【 📖 重溫主線第一副本劇情 (喪屍末日 · 極光重工遺址) 】":
                    jump stage_1_1_zombie_city
                "【 🗺️ 開啟大地圖自由探索模式 (支線/隱藏物資/領主挑戰) 】":
                    jump campaign_node_map_hub
        elif current_campaign_world == "space":
            menu:
                "【 📖 重溫主線第二副本劇情 (太空真空 · 幽靈母艦異形危機) 】":
                    jump stage_1_2_alien_ship
                "【 🗺️ 開啟大地圖自由探索模式 (支線/隱藏物資/領主挑戰) 】":
                    jump campaign_node_map_hub
        elif current_campaign_world == "paranormal":
            menu:
                "【 📖 重溫主線第三副本劇情 (日式靈異 · 咒怨凶宅) 】":
                    jump stage_1_3_the_grudge
                "【 🗺️ 開啟大地圖自由探索模式 (支線/隱藏物資/領主挑戰) 】":
                    jump campaign_node_map_hub
        elif current_campaign_world == "magic":
            menu:
                "【 📖 重溫主線第四副本劇情 (修真神魔 · 蜀山血海封印) 】":
                    jump stage_1_4_cultivation_realm
                "【 🗺️ 開啟大地圖自由探索模式 (支線/隱藏物資/領主挑戰) 】":
                    jump campaign_node_map_hub
        elif current_campaign_world == "causality":
            menu:
                "【 📖 重溫主線第五副本劇情 (木乃伊遺跡 · 印洲隊團戰決死鬥) 】":
                    jump stage_1_5_team_battle_india
                "【 🗺️ 開啟大地圖自由探索模式 (支線/隱藏物資/領主挑戰) 】":
                    jump campaign_node_map_hub
        
        jump campaign_node_map_hub
        
    jump main_room_exploration


# ==========================================
# 副本世界節點探索主循環 (campaign_node_map_hub)
# ==========================================
label campaign_node_map_hub:
    if current_campaign_world == "zombie":
        call screen zombie_city_map_screen
        $ node_choice = _return
        
        if node_choice == "return_hub":
            "你選擇退出極光重工遺址，透過輪迴光門返回了輪迴空間廣場。"
            jump main_room_exploration
            
        elif isinstance(node_choice, tuple) and len(node_choice) >= 2:
            $ act_type = node_choice[0]
            $ node_id = node_choice[1]
            $ cur_node = next((n for n in ZOMBIE_MAP_NODES if n["id"] == node_id), None)
            
            if act_type == "action_battle" and cur_node:
                # 判斷是否為已肅清據點 (若已肅清則生成刷新怪群，否則生成首通部隊)
                $ is_node_done = zombie_map_nodes_state.get(node_id, False)
                $ target_enemy_specs = cur_node.get('repeatable_enemies', cur_node.get('enemies', [])) if is_node_done else cur_node.get('enemies', [])
                
                python:
                    deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
                    for m in deployed_team:
                        m['has_acted'] = False
                    
                    e_list = []
                    for e_spec in target_enemy_specs:
                        e_list.append(create_battle_enemy(e_spec['id'], e_spec.get('suffix', ''), status=e_spec.get('status')))
                    
                    log_intro = f"⚠️ 【刷新怪群掃蕩】小隊再次深入【{cur_node['name']}】！" if is_node_done else f"⚠️ 【戰術據點遭遇】小隊突入【{cur_node['name']}】！"
                    b_state = {
                        'round_number': 1,
                        'player_team': deployed_team,
                        'world_id': 'zombie',
                        'enemies': e_list,
                        'logs': [
                            log_intro,
                            "💡 提示：靈活運用近戰、遠程射擊與手雷清除所有敵方目標！"
                        ],
                        'current_turn_name': '第 1 回合 · 我方行動階段',
                        'is_player_turn': True,
                        'selected_actor': None,
                        'target_mode': None,
                        'selected_skill': None
                    }
                    
                call screen battle_screen(b_state)
                $ b_res = _return
                if b_res == "win":
                    if not is_node_done:
                        # 首次攻克獎勵
                        $ zombie_map_nodes_state[node_id] = True
                        $ points += cur_node.get('reward_points', 500)
                        if 'reward_shard' in cur_node:
                            $ add_fate_shard(cur_node['reward_shard'], 1)
                        if 'reward_items' in cur_node:
                            python:
                                for itm_entry in cur_node['reward_items']:
                                    add_item(itm_entry['id'], itm_entry['count'])
                        $ team_roster[0]["points"] = points
                        if renpy.loadable("audio/levelup.ogg"):
                            $ renpy.sound.play("audio/levelup.ogg")
                        $ n_title = cur_node['name']
                        $ n_pts = cur_node.get('reward_points', 500)
                        z "🎉【首通大捷】成功攻克【[n_title]】！獲得首通生存點數 +[n_pts] 點與首通戰術物資獎勵！\n（該據點支線已完結，後續僅可重複刷取巡邏怪物素材）"
                    else:
                        # 已肅清後的重複掃蕩獎勵 (不重複給予任務關鍵道具與首通命運碎片)
                        $ rep_pts = cur_node.get('repeatable_points', 150)
                        $ points += rep_pts
                        if 'repeatable_items' in cur_node:
                            python:
                                for itm_entry in cur_node['repeatable_items']:
                                    add_item(itm_entry['id'], itm_entry['count'])
                        $ team_roster[0]["points"] = points
                        if renpy.loadable("audio/levelup.ogg"):
                            $ renpy.sound.play("audio/levelup.ogg")
                        $ n_title = cur_node['name']
                        z "🎉【掃蕩勝利】成功清剿【[n_title]】刷新怪群！獲得生存點數 +[rep_pts] 點與基礎素材！"
                jump campaign_node_map_hub
                
            elif act_type == "action_quest" and cur_node:
                # 觸發支線劇情與智鬥檢定
                if node_id == "node_infirmary":
                    "你率隊來到了【B1 特種廢棄醫務室】門前，高壓電子防爆鎖發出刺耳的紅光鎖定警告！"
                    $ max_int = get_team_max_int() if 'get_team_max_int' in globals() else 20
                    if max_int >= 100:
                        "【🧠 智者思維感知】隊伍最高智力達到 [max_int] 點（達標 >= 100，蘇曉敏銳破解了防火牆晶片）！"
                        "咔嚓一聲，氣壓消毒門噴出白色煙霧，保險櫃應聲開啟！"
                        $ zombie_map_nodes_state["node_infirmary"] = True
                        $ points += 600
                        $ add_fate_shard("C", 1)
                        $ add_item("item_heal_spray", 2)
                        $ add_item("MAT_ZOMBIE_BLOOD", 10)
                        $ team_roster[0]["points"] = points
                        if renpy.loadable("audio/levelup.ogg"):
                            $ renpy.sound.play("audio/levelup.ogg")
                        z "【智者判定大成功】完美破解醫務室防盜陣列！獲得【輪迴止血急救噴霧 x2】、【高純度喪屍血清 x10】、C 階命運碎片 x1 與 +600 生存點數！"
                    else:
                        "隊伍當前最高智力為 [max_int] 點（未達門檻 100 點），無法無損解鎖，只能暴力破門！"
                        "嗶——！防爆警報驟響，大批狂暴敏捷型喪屍自天花板通風管道飛撲而下！"
                        python:
                            deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
                            for m in deployed_team:
                                m['has_acted'] = False
                            b_state = {
                                'round_number': 1,
                                'player_team': deployed_team,
                                'world_id': 'zombie',
                                'enemies': [
                                    create_battle_enemy("agile_zombie", "A", status="嗜血狂暴"),
                                    create_battle_enemy("agile_zombie", "B", status="狂暴突進"),
                                    create_battle_enemy("MOB_ZOMBIE_01", "A", status="毒液噴濺")
                                ],
                                'logs': ["⚠️ 【警報引發突襲】暴力破門引來了敏捷型喪屍群！"],
                                'current_turn_name': '第 1 回合 · 我方行動階段',
                                'is_player_turn': True,
                                'selected_actor': None,
                                'target_mode': None,
                                'selected_skill': None
                            }
                        call screen battle_screen(b_state)
                        $ b_res = _return
                        if b_res == "win":
                            $ zombie_map_nodes_state["node_infirmary"] = True
                            $ points += 400
                            $ add_item("item_heal_spray", 1)
                            $ team_roster[0]["points"] = points
                            z "【戰鬥勝利】擊潰守衛喪屍，搜刮醫務室獲得【輪迴止血急救噴霧 x1】與 +400 生存點數！"
                    jump campaign_node_map_hub
                    
                elif node_id == "node_server":
                    "你率隊進入【中央主控機房】，巨大藍色全息螢幕上閃爍著 A.D.A.M. 亞當核心原始碼！"
                    $ max_int = get_team_max_int() if 'get_team_max_int' in globals() else 20
                    if max_int >= 100:
                        "【🧠 智者思維入侵】隊伍最高智力達到 [max_int] 點（達標 >= 100），成功強行突破自毀程序！"
                        $ zombie_map_nodes_state["node_server"] = True
                        $ points += 1000
                        $ add_fate_shard("B", 1)
                        $ add_item("ITEM_HIVE_AI_BACKUP", 1)
                        $ add_item("MAT_TECH_PARTS", 8)
                        $ team_roster[0]["points"] = points
                        if renpy.loadable("audio/levelup.ogg"):
                            $ renpy.sound.play("audio/levelup.ogg")
                        show adamcore at item_show_center with dissolve
                        z "【智者駭入大成功】成功下載【亞當神經元矩陣備份 (A.D.A.M. Core)】！獲得 B 階命運碎片 x1、高階超導晶片 x8 與 +1,000 生存點數！"
                        hide adamcore with dissolve
                    else:
                        "智力未達門檻，觸發機房防禦電網，遭遇生化守衛！"
                        python:
                            deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
                            for m in deployed_team:
                                m['has_acted'] = False
                            b_state = {
                                'round_number': 1,
                                'player_team': deployed_team,
                                'world_id': 'zombie',
                                'enemies': [
                                    create_battle_enemy("MOB_ZOMBIE_01", "A", status="重裝防禦"),
                                    create_battle_enemy("MOB_ZOMBIE_01", "B", status="毒素附著"),
                                    create_battle_enemy("agile_zombie", "A", status="致命突進")
                                ],
                                'logs': ["⚠️ 【防禦系統啟動】機房生化守衛發動反擊！"],
                                'current_turn_name': '第 1 回合 · 我方行動階段',
                                'is_player_turn': True,
                                'selected_actor': None,
                                'target_mode': None,
                                'selected_skill': None
                            }
                        call screen battle_screen(b_state)
                        $ b_res = _return
                        if b_res == "win":
                            $ zombie_map_nodes_state["node_server"] = True
                            $ points += 500
                            $ add_item("MAT_TECH_PARTS", 5)
                            $ team_roster[0]["points"] = points
                            z "【戰鬥勝利】擊潰機房守衛，拆解伺服器獲得科技零件 x5 與 +500 生存點數！"
                    jump campaign_node_map_hub
                    
                elif node_id == "node_armory":
                    "你撬開了【地下軍火管制庫】的防爆門，牆面裝備架上擺放著整齊的軍用高爆物資！"
                    $ zombie_map_nodes_state["node_armory"] = True
                    $ points += 500
                    $ add_item("high_explosive", 2)
                    $ add_item("item_grenade", 2)
                    $ team_roster[0]["points"] = points
                    if renpy.loadable("audio/levelup.ogg"):
                        $ renpy.sound.play("audio/levelup.ogg")
                    show high_explosive at item_show_center with dissolve
                    z "【軍火搜刮成功】獲得【high_explosive 高爆破片手雷 x2】、【高爆手榴彈 x2】與 +500 生存點數！"
                    hide high_explosive with dissolve
                    jump campaign_node_map_hub
                    
        jump campaign_node_map_hub

    # 其他副本世界回退標準地圖
    call screen campaign_map_screen
    $ node_choice = _return
    
    if node_choice == "return_hub":
        "你選擇退出當前世界，透過輪迴光門暫時返回了輪迴空間廣場。"
        jump main_room_exploration
        
    elif isinstance(node_choice, tuple) and len(node_choice) >= 2 and node_choice[0] == "enter_node":
        $ node_type = node_choice[1]
        
        # 1. 主線前鋒據點戰鬥
        if node_type == "main":
            "你率領小隊突入主線前哨陣地，遭遇了敵方先鋒防線！"
            call screen battle_screen
            $ b_res = _return
            if b_res == "win":
                $ campaign_nodes_state["main_cleared"] = True
                $ points += 500
                $ team_roster[0]["points"] = points
                z "【節點突擊勝利】敵方先鋒部隊已被肅清！獲得 +500 生存點數，主線已向前推進！"
            jump campaign_node_map_hub
            
        # 2. 命運碎片精英據點戰鬥
        elif node_type == "shard":
            "你踏入了極度危險的精英巢穴，狂暴的精英怪物發出刺耳嘶吼！"
            call screen battle_screen
            $ b_res = _return
            if b_res == "win":
                $ campaign_nodes_state["shard_cleared"] = True
                $ w_info = CAMPAIGN_WORLDS.get(current_campaign_world, CAMPAIGN_WORLDS["zombie"])
                $ s_tier = w_info.get("shard_reward", "C")
                $ add_fate_shard(s_tier, 1)
                $ points += 800
                $ team_roster[0]["points"] = points
                z "【精英試煉大捷】精英鎮守者轟然倒地！成功掠奪【[s_tier] 階命運碎片 x1】與 +800 生存點數！"
            jump campaign_node_map_hub
            
        # 3. NPC 智鬥/謎題推演據點
        elif node_type == "riddle":
            "你來到了一處雕刻著古老符文的機關密室門前，四周散發著致命的毀滅能量。"
            $ max_int = get_team_max_int() if 'get_team_max_int' in globals() else 20
            if max_int >= 100:
                "隊伍中的智者眼中精芒一閃，敏銳推演出機關波長，密室大門應聲開啟！"
                $ campaign_nodes_state["riddle_cleared"] = True
                $ points += 800
                $ add_item("EQ_MAGIC_NECKLACE_01", 1)
                $ team_roster[0]["points"] = points
                z "【智鬥破解成功】完美破解謎題！獲得 +800 生存點數與傳奇飾品【定魂辟邪古玉佩】x1！"
            else:
                "隊伍中智力不足，你只能親自凝神觀察機關符文（進行直覺推演）："
                menu:
                    "【 逆時針轉動純陽生門符印 】":
                        "咔嚓一聲，機關成功解開！"
                        $ campaign_nodes_state["riddle_cleared"] = True
                        $ points += 500
                        $ team_roster[0]["points"] = points
                        z "【直覺破解成功】獲得 +500 生存點數！"
                    "【 順時針強行注入真氣破壞 】":
                        "轟！機關引爆反噬衝擊波，隊長受到了 30 點真實反噬傷害！"
                        $ team_roster[0]["hp"] = max(1, team_roster[0]["hp"] - 30)
                        $ hp = team_roster[0]["hp"]
            jump campaign_node_map_hub
            
        # 4. 野外安全屋補給據點
        elif node_type == "supply":
            "你推開了野外安全屋的防爆鋼門，這裡設有輪迴野外應急補給終端。"
            call screen item_shop_screen
            jump campaign_node_map_hub
            
        # 5. 終極領主決戰
        elif node_type == "boss":
            $ w_info = CAMPAIGN_WORLDS.get(current_campaign_world, CAMPAIGN_WORLDS["zombie"])
            $ b_boss_name = w_info.get("boss_name")
            "你踏入了核心領主領域，【[b_boss_name]】帶著震碎虛空的恐怖氣壓轟然降臨！"
            call screen battle_screen
            $ b_res = _return
            if b_res == "win":
                $ s_tier = w_info.get("shard_reward", "C")
                $ add_fate_shard(s_tier, 1)
                $ points += 2000
                $ team_roster[0]["points"] = points
                z "🎉【世界通關大捷】終極領主【[b_boss_name]】已被徹底擊殺！\n輪迴廣播響起：成功通關本副本世界！獲得 +2,000 點數與【[s_tier] 階命運碎片 x1】！全體隊員傳送回歸輪迴空間！"
                jump main_room_exploration
            jump campaign_node_map_hub
            
    jump main_room_exploration


# ==========================================
# 房間與劇情對話分支
# ==========================================
label lengyue_dialogue:
    "你走到冷月身旁。她正擦拭著手中古樸的銀色雙槍，神情清冷孤傲。"
    "冷月抬起頭看了你一眼，淡淡說道：「怎麼？覺得輪迴世界殘酷？只要有輪迴積分和命運碎片，你連神魔之軀都能兌換出來。想活下去，就收起多餘的同情心，盡快讓自己變強。」"
    jump main_room_exploration

label personal_room:
    call screen personal_room_screen
    $ p_act = _return
    
    if p_act == "craft_elixir":
        $ res = craft_gene_lock_elixir()
        z "[res['msg']]"
        jump personal_room
        
    elif p_act == "use_elixir":
        $ res = use_gene_lock_elixir(0)
        python:
            if res.get("success", False) and renpy.loadable("audio/levelup.ogg"):
                renpy.sound.play("audio/levelup.ogg")
        z "[res['msg']]"
        jump personal_room
        
    elif p_act == "install_ai":
        $ res = install_hive_ai()
        z "[res['msg']]"
        jump personal_room
        
    elif isinstance(p_act, tuple) and len(p_act) >= 2 and p_act[0] == "craft_tech":
        $ recipe_id = p_act[1]
        $ res = craft_tech_equipment(recipe_id)
        z "[res['msg']]"
        jump personal_room
        
    elif p_act == "leave_room":
        jump main_room_exploration
        
    jump main_room_exploration

label view_team_status:
    if 'team_roster' not in globals() or not team_roster:
        $ team_roster = get_team_roster()
    $ team_roster[0]["points"] = points
    call screen team_status_screen(page=0)
    jump main_room_exploration

label home_base_hub:
    call screen home_base_screen
    jump main_room_exploration

label main_room_hub:
    jump main_room_exploration
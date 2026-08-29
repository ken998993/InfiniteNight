# ==========================
# 第一個副本：喪屍都市
# ==========================
label zombieCity:

    scene zombie_street
    
    n "眼前光芒一閃，你們出現在一條殘破的街道上。"
    n "空氣中瀰漫著血腥味與腐臭味。"
    
    z "主線任務：在喪屍都市中生存 24 小時。"
    z "任務獎勵：生存點數 500 點。"

    "遠處傳來低沉的嘶吼聲，幾隻喪屍正朝這裡晃晃悠悠地走來……"

    # ==========================
    # 進入升級後的多重能量與血統戰鬥畫面！
    # ==========================
    python:
        # 初始化戰鬥狀態字典，串接 team_roster 團隊資料
        if 'team_roster' not in globals() or not team_roster:
            team_roster = get_team_roster()

        # 重置我方角色戰鬥狀態與每回合行動標記
        for m in team_roster:
            m['has_acted'] = False
            if m.get('hp', 0) <= 0:
                m['hp'] = m.get('max_hp', 100)

        battle_state = {
            'round_number': 1,
            'player_team': team_roster,
            'enemies': [
                {"name": "狂暴喪屍 A", "hp": 120, "max_hp": 120, "atk": 15, "status": "嗜血"},
                {"name": "狂暴喪屍 B", "hp": 120, "max_hp": 120, "atk": 15, "status": "嗜血"},
                {"name": "迅捷爬行者", "hp": 90, "max_hp": 90, "atk": 20, "status": "敏捷"},
                {"name": "巨型重甲喪屍", "hp": 220, "max_hp": 220, "atk": 30, "status": "堅韌"},
                {"name": "劇毒酸液喪屍", "hp": 110, "max_hp": 110, "atk": 18, "status": "劇毒"},
                {"name": "變異喪屍統領", "hp": 260, "max_hp": 260, "atk": 35, "status": "統領"}
            ],
            'logs': [
                "警報！街道前方湧現了 6 隻具備不同特性的兇暴喪屍！",
                "【第 1 回合開始】每位隊員每回合可行動一次，全體行動完畢後進入敵方反擊回合。"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }

    # 叫出我們全新的 battle_screen 畫面，並用變數接住按鈕回傳的值
    call screen battle_screen(battle_state)
    $ battle_result = _return

    # 根據回傳結果進行分歧跳轉
    if battle_result == "end_battle":
        jump escape_battle
    elif battle_result == "win":
        jump battle_victory
    
    # 預設防呆返回
    return

# 戰鬥勝利標籤（接續完成任務故事進入主神空間）
label battle_victory:
    n "經過一番苦戰，你們總算徹底殲滅了第一波喪屍危機！"
    n "在隨後的殘存時間裡，你們小心翼翼地搜索了附近的街道，躲過了好幾次零星喪屍的遊蕩。"
    
    # 結算時間到，主神光柱降臨
    "當手錶上的倒數歸零時，天空突然亮起了一道熟悉的巨大光柱……"
    
    python:
        if renpy.loadable("teleport.ogg"):
            renpy.sound.play("teleport.ogg")
    
    n "伴隨著溫暖的光芒將你們籠罩，一股不可抗拒的力量將你們向上拉起。"
    
    # 發放任務獎勵
    $ points += 500
    z "主線任務「在喪屍都市中生存 24 小時」已完成。"
    z "獲得獎勵：生存點數 500 點。目前總積分：[points] 點。"

    scene bg__topdown
    
    n "眼前景色一花，你們再次回到了那個無垠的巨大白色廣場——主神空間。"
    n "四周巨大的光球依舊散發著冰冷而神聖的光芒，圓形的兌換石碑在前方靜靜佇立。"
    
    "張傑吐出了一口帶血的唾沫，靠在廣場的柱子上笑著說：「大難不死……我們活下來了！」"
    
    jump main_room_exploration

# 撤退標籤
label escape_battle:
    n "你們狼狽地逃向街道的另一端，暫時脫離了戰場。"
    return
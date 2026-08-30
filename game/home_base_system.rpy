# ==============================================================================
# 📜 《輪迴世界》專屬家園與領地營造系統 (home_base_system.rpy)
# 依據 developMd/11_Home_Base_System.md 規範實現
# ==============================================================================

init python:
    import json
    import copy

    # 1. 取得家園數據庫
    def get_home_base_db():
        global home_base_db_cache
        if 'home_base_db_cache' in globals() and home_base_db_cache:
            return home_base_db_cache
        try:
            with renpy.file("jsonData/home_base_db.json") as f:
                home_base_db_cache = json.load(f)
                return home_base_db_cache
        except Exception as e:
            home_base_db_cache = {"base_tiers": [], "production_facilities": [], "training_programs": [], "trophies": [], "teammate_bonds": []}
            return home_base_db_cache

    # 2. 升級家園階級 (Tier Upgrade)
    def upgrade_home_base():
        global home_base_tier, points, fate_shards
        db = get_home_base_db()
        tiers = db.get("base_tiers", [])
        cur_tier = home_base_tier if 'home_base_tier' in globals() else 1
        
        if cur_tier >= len(tiers):
            return {"success": False, "msg": "家園領域已達最高階級（跨維度永恆神域）！"}
            
        next_tier_info = tiers[cur_tier]
        cost_pts = next_tier_info.get("cost_points", 0)
        cost_shard = next_tier_info.get("cost_shard", None)
        
        cur_pts = points if 'points' in globals() else 0
        shards = fate_shards if 'fate_shards' in globals() else {}
        
        if cur_pts < cost_pts:
            return {"success": False, "msg": f"輪迴點數不足！升級需要 {cost_pts} 點，目前僅有 {cur_pts} 點。"}
        if cost_shard and shards.get(cost_shard, 0) < 1:
            return {"success": False, "msg": f"命運碎片不足！升級需要【{cost_shard} 級命運碎片 x1】。"}
            
        points -= cost_pts
        if cost_shard:
            shards[cost_shard] -= 1
            
        home_base_tier = cur_tier + 1
        
        # 全員屬性增益
        roster = get_team_roster()
        if home_base_tier == 2:
            for m in roster:
                m["max_hp"] = m.get("max_hp", 100) + 50
                m["hp"] = m["max_hp"]
                m["max_mp"] = m.get("max_mp", 50) + 50
                m["mp"] = m["max_mp"]
        elif home_base_tier >= 3:
            for m in roster:
                for k in ["con", "str", "spd", "int", "mnd"]:
                    m[k] = m.get(k, 20) + 10
                    
        return {"success": True, "msg": f"🎉 恭喜！家園成功擴建升級為【{next_tier_info.get('name')} (Tier {home_base_tier})】！\n效果：{next_tier_info.get('passive_desc')}"}

    # 3. 組裝生產設施 (Build Facility)
    def build_home_facility(fac_id):
        global built_facilities, points
        db = get_home_base_db()
        fac_list = db.get("production_facilities", [])
        fac = next((f for f in fac_list if f.get("id") == fac_id), None)
        if not fac:
            return {"success": False, "msg": "查無此生產設施資料！"}
            
        if 'built_facilities' not in globals():
            built_facilities = []
            
        if fac_id in built_facilities:
            return {"success": False, "msg": f"設施【{fac.get('name')}】已經組裝完成，正在待命運作中！"}
            
        cur_tier = home_base_tier if 'home_base_tier' in globals() else 1
        tiers = db.get("base_tiers", [])
        max_slots = tiers[cur_tier - 1].get("max_slots", 2) if cur_tier <= len(tiers) else 2
        
        if len(built_facilities) >= max_slots:
            return {"success": False, "msg": f"家園模組插槽已滿 (當前上限: {max_slots} 個)！請先升級家園以解鎖更多插槽！"}
            
        cost_pts = fac.get("build_cost_points", 1000)
        cur_pts = points if 'points' in globals() else 0
        if cur_pts < cost_pts:
            return {"success": False, "msg": f"輪迴點數不足！組裝需要 {cost_pts} 點，目前僅有 {cur_pts} 點。"}
            
        req_items = fac.get("build_requirements", [])
        for req in req_items:
            itm_id = req.get("id")
            cnt = req.get("count", 1)
            if not has_item(itm_id, cnt):
                return {"success": False, "msg": f"素材不足！缺少【{req.get('name')} x{cnt}】。"}
                
        # 扣除物資
        points -= cost_pts
        for req in req_items:
            remove_item(req.get("id"), req.get("count", 1))
            
        built_facilities.append(fac_id)
        return {"success": True, "msg": f"⚙️ 成功完成【{fac.get('name')}】組裝！已入駐家園工坊模組插槽！"}

    # 4. 批量合成生產物資 (Craft Recipe)
    def craft_home_recipe(fac_id, recipe_id):
        global points
        db = get_home_base_db()
        fac = next((f for f in db.get("production_facilities", []) if f.get("id") == fac_id), None)
        if not fac:
            return {"success": False, "msg": "無效生產設施！"}
            
        rec = next((r for r in fac.get("recipes", []) if r.get("recipe_id") == recipe_id), None)
        if not rec:
            return {"success": False, "msg": "無效合成配方！"}
            
        cost_pts = rec.get("cost_points", 0)
        cur_pts = points if 'points' in globals() else 0
        if cur_pts < cost_pts:
            return {"success": False, "msg": f"點數不足！合成需要 {cost_pts} 點，目前僅有 {cur_pts} 點。"}
            
        mats = rec.get("materials", [])
        for m in mats:
            if not has_item(m.get("id"), m.get("count", 1)):
                return {"success": False, "msg": f"素材不足！缺少【{m.get('name')} x{m.get('count', 1)}】。"}
                
        # 扣除消耗
        points -= cost_pts
        for m in mats:
            remove_item(m.get("id"), m.get("count", 1))
            
        out_id = rec.get("output_id")
        out_cnt = rec.get("output_count", 1)
        add_item(out_id, out_cnt)
        return {"success": True, "msg": f"✨【合成完成】成功產出【{rec.get('name')} x{out_cnt}】！已發放至戰術背包！"}

    # 5. 重力修煉室訓練 (Execute Training)
    def execute_gravity_training(program_id, member_name):
        global points, fate_shards
        db = get_home_base_db()
        prog = next((p for p in db.get("training_programs", []) if p.get("id") == program_id), None)
        if not prog:
            return {"success": False, "msg": "查無此修煉方案！"}
            
        cur_tier = home_base_tier if 'home_base_tier' in globals() else 1
        min_tier = prog.get("min_base_tier", 1)
        if cur_tier < min_tier:
            return {"success": False, "msg": f"家園等級不足！此項目需要家園達 Tier {min_tier} 方可開放！"}
            
        cost_pts = prog.get("cost_points", 0)
        cur_pts = points if 'points' in globals() else 0
        if cur_pts < cost_pts:
            return {"success": False, "msg": f"點數不足！修煉需要 {cost_pts} 點，目前僅有 {cur_pts} 點。"}
            
        # 檢查特殊消耗
        cost_items = prog.get("cost_items", [])
        shards = fate_shards if 'fate_shards' in globals() else {}
        for c in cost_items:
            if "shard" in c:
                sh_tier = c.get("shard")
                if shards.get(sh_tier, 0) < c.get("count", 1):
                    return {"success": False, "msg": f"碎片不足！缺少【{sh_tier} 級命運碎片 x{c.get('count', 1)}】。"}
            elif "id" in c:
                if not has_item(c.get("id"), c.get("count", 1)):
                    return {"success": False, "msg": f"素材不足！缺少【{c.get('name', '材料')} x{c.get('count', 1)}】。"}
                    
        # 尋找目標隊員
        roster = get_team_roster()
        target_member = next((m for m in roster if m.get("name") == member_name), None)
        if not target_member:
            return {"success": False, "msg": "無效目標隊員！"}
            
        # 扣除消耗
        points -= cost_pts
        for c in cost_items:
            if "shard" in c:
                shards[c.get("shard")] -= c.get("count", 1)
            elif "id" in c:
                remove_item(c.get("id"), c.get("count", 1))
                
        # 增加屬性
        bonuses = prog.get("stat_bonuses", {})
        bonus_desc = []
        stat_names = {"con": "體質", "str": "力量", "spd": "敏捷", "int": "智力", "mnd": "精神"}
        for k, v in bonuses.items():
            target_member[k] = target_member.get(k, 20) + v
            bonus_desc.append(f"{stat_names.get(k, k)} +{v}")
            
        return {"success": True, "msg": f"🏋️【極限修煉完成】隊員【{member_name}】在【{prog.get('name')}】中突破極限！\n獲取屬性：{', '.join(bonus_desc)}！"}

    # 6. 隊友休息室互動與贈禮 (Teammate Bonding)
    def reset_teammate_chat_quota():
        global teammate_chat_quota
        teammate_chat_quota = {"冷月": 1, "項天": 1, "蘇曉": 1}

    def interact_teammate(member_name, action_type="chat"):
        global teammate_affection, teammate_chat_quota, points
        if 'teammate_affection' not in globals():
            teammate_affection = {"冷月": 30, "項天": 20, "蘇曉": 20}
        if 'teammate_chat_quota' not in globals():
            teammate_chat_quota = {"冷月": 1, "項天": 1, "蘇曉": 1}
            
        db = get_home_base_db()
        b_info = next((b for b in db.get("teammate_bonds", []) if b.get("name") == member_name), None)
        if not b_info:
            return {"success": False, "msg": "查無此隊友互動檔案！"}
            
        cur_aff = teammate_affection.get(member_name, 0)
        
        if action_type == "chat":
            # 1. 檢測談心剩餘次數限制 (每週期限 1 次)
            cur_quota = teammate_chat_quota.get(member_name, 1)
            if cur_quota <= 0:
                return {
                    "success": False,
                    "msg": f"⚠️【心神飽和】隊員【{member_name}】剛與你相談甚歡，目前心神放鬆正在打坐冥想。\n請在通關下一場副本世界回歸後再次品茗談心！"
                }
                
            # 2. 檢測道具或點數消耗 (優先消耗 1 份「輪迴特級安神靈茶」或 100 點生存點數)
            tea_item_id = "ITEM_TEA_PACK"
            has_tea = has_item(tea_item_id, 1) if 'has_item' in globals() else False
            cur_pts = points if 'points' in globals() else 0
            
            used_desc = ""
            if has_tea:
                remove_item(tea_item_id, 1)
                used_desc = "消耗【輪迴特級安神靈茶 x1】"
            elif cur_pts >= 100:
                points -= 100
                used_desc = "消耗 100 點數向輪迴光球兌換沖泡靈茗"
            else:
                return {
                    "success": False,
                    "msg": "⚠️【缺少茶品】品茗談心需要消耗【輪迴特級安神靈茶 x1】或 100 點生存點數沖泡！請先前往商城購買或累積點數。"
                }
                
            # 扣除次數並增加好感
            teammate_chat_quota[member_name] = max(0, cur_quota - 1)
            teammate_affection[member_name] = cur_aff + 25
            
            # 順便補滿隊友 MP
            roster = get_team_roster()
            target_mem = next((m for m in roster if m.get("name") == member_name), None)
            if target_mem:
                target_mem["mp"] = target_mem.get("max_mp", 50)
                
            dialogues = b_info.get("dialogues", ["很高興能在這裡跟你聊天。"])
            idx = min(len(dialogues) - 1, cur_aff // 100)
            
            return {
                "success": True,
                "msg": f"☕【與 {member_name} 交流品茗】({used_desc})\n『{dialogues[idx]}』\n（💖 好感羈絆 +25，當前好感值: {teammate_affection[member_name]}，該隊員精神力已完全回滿！）"
            }
        elif action_type == "gift":
            fav_gift = b_info.get("fav_gift")
            if not has_item(fav_gift, 1):
                return {"success": False, "msg": f"背包中缺少 {member_name} 喜好的特產禮物！"}
            remove_item(fav_gift, 1)
            teammate_affection[member_name] = cur_aff + 50
            return {
                "success": True,
                "msg": f"🎁【贈送專屬禮物予 {member_name}】\n{member_name} 感到十分驚喜與欣慰，隊員好感度大幅提升 +50！（當前好感值: {teammate_affection[member_name]}）"
            }

# ==========================================
# 家園系統動態變數定義
# ==========================================
default home_base_tier = 1
default built_facilities = []
default active_trophies = []
default teammate_affection = {"冷月": 30, "項天": 20, "蘇曉": 20}
default teammate_chat_quota = {"冷月": 1, "項天": 1, "蘇曉": 1}
default home_base_tab = "overview"
default home_base_feedback = ""

# ==========================================
# 家園系統主面板 UI (screen home_base_screen)
# ==========================================
screen home_base_screen():

    $ db = get_home_base_db()
    $ cur_tier = home_base_tier if 'home_base_tier' in globals() else 1
    $ tiers = db.get("base_tiers", [])
    $ cur_tier_info = tiers[cur_tier - 1] if cur_tier <= len(tiers) else {"name": "自定義神域", "max_slots": 6, "passive_desc": "無"}
    $ cur_facilities = built_facilities if 'built_facilities' in globals() else []
    $ shards = get_fate_shards() if 'get_fate_shards' in globals() else {}
    $ roster = get_team_roster()

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1760, 980)
        padding (30, 22)
        background "#0c111ef8"

        vbox:
            spacing 10
            xalign 0.5

            # 頂部導覽列
            hbox:
                spacing 25
                xalign 0.5
                text "【 🏰 輪迴者專屬神域家園 · 戰術指揮基地 】" size 24 color "#ffcc00" bold True yalign 0.5
                text f"領地等級：Tier {cur_tier} · {cur_tier_info.get('name')}" size 16 color "#00ffff" bold True yalign 0.5
                text f"持有點數: {points} 點" size 16 color "#66ff66" bold True yalign 0.5
                text f"工坊模組插槽: {len(cur_facilities)}/{cur_tier_info.get('max_slots', 2)}" size 15 color "#ddaaff" yalign 0.5

            # 分頁導籤列 (Tabs)
            hbox:
                spacing 12
                xalign 0.5
                
                textbutton "【 🏗️ 領地概況與擴建 】":
                    action [SetVariable("home_base_tab", "overview"), SetVariable("home_base_feedback", "")]
                    text_size 16 text_idle_color ("#ffff00" if home_base_tab == 'overview' else "#cccccc")
                    text_hover_color "#ffffff"

                textbutton "【 ⚙️ 戰術生產工坊 】":
                    action [SetVariable("home_base_tab", "facilities"), SetVariable("home_base_feedback", "")]
                    text_size 16 text_idle_color ("#ffff00" if home_base_tab == 'facilities' else "#cccccc")
                    text_hover_color "#ffffff"

                textbutton "【 🏋️ 重力修煉室 】":
                    action [SetVariable("home_base_tab", "training"), SetVariable("home_base_feedback", "")]
                    text_size 16 text_idle_color ("#ffff00" if home_base_tab == 'training' else "#cccccc")
                    text_hover_color "#ffffff"

                textbutton "【 🏆 戰利品展覽館 】":
                    action [SetVariable("home_base_tab", "trophies"), SetVariable("home_base_feedback", "")]
                    text_size 16 text_idle_color ("#ffff00" if home_base_tab == 'trophies' else "#cccccc")
                    text_hover_color "#ffffff"

                textbutton "【 ☕ 隊員休息室與羈絆 】":
                    action [SetVariable("home_base_tab", "lounge"), SetVariable("home_base_feedback", "")]
                    text_size 16 text_idle_color ("#ffff00" if home_base_tab == 'lounge' else "#cccccc")
                    text_hover_color "#ffffff"

            # 即時操作回饋訊息
            if home_base_feedback:
                frame:
                    xalign 0.5
                    xysize (1700, 36)
                    background "#223344cc"
                    padding (10, 4)
                    text f"💡 {home_base_feedback}" size 14 color "#66ff66" bold True xalign 0.5 yalign 0.5 substitute False

            null height 2

            # ==========================================
            # 1. 領地概況與擴建分頁 (Overview Tab)
            # ==========================================
            if home_base_tab == "overview":
                hbox:
                    spacing 20
                    xalign 0.5

                    # 左側：當前領地狀態
                    frame:
                        xysize (830, 720)
                        background "#141a2ecc"
                        padding (20, 15)
                        vbox:
                            spacing 15
                            text f"【 🏛️ 當前領地境界：Tier {cur_tier} · {cur_tier_info.get('name')} 】" size 20 color "#00ffcc" bold True
                            text f"領域描述：{cur_tier_info.get('desc')}" size 14 color "#cccccc"
                            
                            null height 5
                            text "【 🌟 全隊領域常駐被動加成 】" size 16 color "#ffaa00" bold True
                            text f"• {cur_tier_info.get('passive_desc')}" size 14 color "#66ff66"

                            null height 10
                            text "【 🧩 當前插槽模組部署 】" size 16 color "#ddaaff" bold True
                            if not cur_facilities:
                                text "尚未組裝任何高科技工坊設施。請前往【戰術生產工坊】分頁組裝生產裝置！" size 13 color "#888888"
                            else:
                                for f_id in cur_facilities:
                                    $ fac_obj = next((f for f in db.get("production_facilities", []) if f.get("id") == f_id), None)
                                    if fac_obj:
                                        text f"⚡ 已運作：【{fac_obj.get('name')}】（{fac_obj.get('desc')}）" size 13 color "#00ffea"

                    # 右側：升級與擴建控制台
                    frame:
                        xysize (830, 720)
                        background "#141a2ecc"
                        padding (20, 15)
                        vbox:
                            spacing 15
                            text "【 🚀 領地擴建與昇華控制台 】" size 20 color "#ffaa00" bold True
                            
                            if cur_tier < len(tiers):
                                $ next_t_info = tiers[cur_tier]
                                text f"下一階境界：【{next_t_info.get('name')} (Tier {cur_tier+1})】" size 17 color "#00ffff" bold True
                                text f"升級需求：輪迴點數 {next_t_info.get('cost_points')} 點" + (f" + 【{next_t_info.get('cost_shard')} 級命運碎片 x1】" if next_t_info.get('cost_shard') else "") size 14 color "#ffdd88"
                                text f"解鎖插槽：{next_t_info.get('max_slots')} 個模組插槽" size 14 color "#ddaaff"
                                text f"晉升增益：{next_t_info.get('passive_desc')}" size 14 color "#66ff66"

                                null height 20
                                textbutton "【 ⚡ 立即消耗物資，升級神域領地 】":
                                    action [SetVariable("home_base_feedback", upgrade_home_base().get("msg", "")), renpy.restart_interaction]
                                    text_size 18 text_idle_color "#00ff00" text_hover_color "#ffffff"
                            else:
                                text "🎉 您的專屬神域已登峰造極，達到了至高境界（Tier 4 跨維度永恆神域）！" size 16 color "#ffff00" bold True

            # ==========================================
            # 2. 戰術生產工坊分頁 (Facilities Tab)
            # ==========================================
            elif home_base_tab == "facilities":
                viewport:
                    xysize (1700, 720)
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    
                    vbox:
                        spacing 15
                        for fac in db.get("production_facilities", []):
                            $ f_id = fac.get("id")
                            $ is_built = (f_id in cur_facilities)
                            
                            frame:
                                xysize (1660, 220)
                                background ("#18233ebb" if is_built else "#141824aa")
                                padding (18, 12)
                                hbox:
                                    spacing 20
                                    
                                    # 設施基本資訊
                                    vbox:
                                        xysize (550, 195)
                                        spacing 8
                                        text f"【 裝置：{fac.get('name')} 】" size 18 color ("#00ffcc" if is_built else "#aaaaaa") bold True
                                        text ("狀態：🟢 運作中（已組裝）" if is_built else "狀態：⚪ 未組裝（需解鎖）") size 13 color ("#66ff66" if is_built else "#888888")
                                        text f"功能定位：{fac.get('desc')}" size 12 color "#cccccc"
                                        
                                        if not is_built:
                                            $ req_str = ", ".join([f"{r.get('name')} x{r.get('count')}" for r in fac.get('build_requirements', [])])
                                            text f"組裝需求：{fac.get('build_cost_points')} 點數 + {req_str}" size 12 color "#ffaa88"
                                            textbutton "【 🛠️ 組裝並入駐此設施 】":
                                                action [SetVariable("home_base_feedback", build_home_facility(f_id).get("msg", "")), renpy.restart_interaction]
                                                text_size 14 text_idle_color "#ffcc00" text_hover_color "#ffffff"

                                    # 生產配方列表
                                    vbox:
                                        xysize (1060, 195)
                                        spacing 6
                                        text "【 可生產戰術物資配方 】" size 15 color "#ffdd88" bold True
                                        if not is_built:
                                            text "（請先組裝該設施以解鎖以下配方生產線）" size 13 color "#666666"
                                        
                                        for rec in fac.get("recipes", []):
                                            $ r_id = rec.get("recipe_id")
                                            $ mat_desc = ", ".join([f"{m.get('name')} x{m.get('count')}" for m in rec.get('materials', [])])
                                            hbox:
                                                spacing 15
                                                text f"• {rec.get('name')} x{rec.get('output_count')}" size 14 color ("#ffffff" if is_built else "#666666") bold True yalign 0.5
                                                text f"(消耗: {rec.get('cost_points')} 點 + {mat_desc})" size 12 color ("#00ffff" if is_built else "#555555") yalign 0.5
                                                
                                                if is_built:
                                                    textbutton "【 ⚡ 批量製造 】":
                                                        action [SetVariable("home_base_feedback", craft_home_recipe(f_id, r_id).get("msg", "")), renpy.restart_interaction]
                                                        text_size 13 text_idle_color "#00ff00" text_hover_color "#ffffff" yalign 0.5
                                                text f"- {rec.get('desc')}" size 11 color "#888888" yalign 0.5

            # ==========================================
            # 3. 重力修煉室分頁 (Training Tab)
            # ==========================================
            elif home_base_tab == "training":
                hbox:
                    spacing 20
                    xalign 0.5
                    
                    # 選擇修煉項目
                    frame:
                        xysize (830, 720)
                        background "#141a2ecc"
                        padding (20, 15)
                        vbox:
                            spacing 15
                            text "【 🏋️ 高維重力修煉項目清單 】" size 20 color "#00ffcc" bold True
                            text "空間透過重力力場模擬高維鍛體環境，可直接突破隊員四維屬性！" size 13 color "#aaaaaa"
                            
                            null height 5
                            for prog in db.get("training_programs", []):
                                $ p_id = prog.get("id")
                                $ min_t = prog.get("min_base_tier", 1)
                                $ is_unlocked = (cur_tier >= min_t)
                                
                                frame:
                                    xysize (780, 175)
                                    background ("#1a243ebb" if is_unlocked else "#12151faa")
                                    padding (15, 10)
                                    vbox:
                                        spacing 6
                                        hbox:
                                            spacing 15
                                            text f"【 {prog.get('name')} 】" size 16 color ("#ffaa00" if is_unlocked else "#777777") bold True
                                            text f"(需要家園 Tier {min_t})" size 12 color ("#66ff66" if is_unlocked else "#ff4444")
                                        text f"修煉效果：{prog.get('desc')}" size 13 color "#cccccc"
                                        text f"消耗成本：{prog.get('cost_points')} 點數" size 12 color "#00ffff"
                                        
                                        if is_unlocked:
                                            hbox:
                                                spacing 10
                                                text "指派隊員修煉：" size 13 color "#ffffff" yalign 0.5
                                                for m in roster:
                                                    $ m_n = m.get("name")
                                                    textbutton f"【{m_n}】":
                                                        action [SetVariable("home_base_feedback", execute_gravity_training(p_id, m_n).get("msg", "")), renpy.restart_interaction]
                                                        text_size 13 text_idle_color "#00ffea" text_hover_color "#ffffff" yalign 0.5

                    # 右側隊伍當前屬性預覽
                    frame:
                        xysize (830, 720)
                        background "#141a2ecc"
                        padding (20, 15)
                        vbox:
                            spacing 15
                            text "【 📊 隊伍成員當前六圍屬性總覽 】" size 20 color "#ffdd88" bold True
                            
                            for m in roster:
                                frame:
                                    xysize (780, 110)
                                    background "#101626aa"
                                    padding (12, 8)
                                    vbox:
                                        spacing 5
                                        hbox:
                                            spacing 15
                                            text f"👤 {m.get('name')} ({m.get('role', '隊員')})" size 16 color "#00ffcc" bold True
                                            text f"HP: {m.get('hp')}/{m.get('max_hp')}" size 13 color "#ff6666"
                                            text f"MP: {m.get('mp')}/{m.get('max_mp')}" size 13 color "#66ccff"
                                        hbox:
                                            spacing 18
                                            text f"體質: {m.get('con', 20)}" size 13 color "#ffaa00"
                                            text f"力量: {m.get('str', 20)}" size 13 color "#ff5555"
                                            text f"敏捷: {m.get('spd', 20)}" size 13 color "#55ff55"
                                            text f"智力: {m.get('int', 20)}" size 13 color "#00ffff"
                                            text f"精神: {m.get('mnd', 20)}" size 13 color "#ddaaff"

            # ==========================================
            # 4. 戰利品展覽館分頁 (Trophies Tab)
            # ==========================================
            elif home_base_tab == "trophies":
                viewport:
                    xysize (1700, 720)
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    
                    vbox:
                        spacing 15
                        for tr in db.get("trophies", []):
                            $ req_itm = tr.get("required_item")
                            $ has_tr_item = has_item(req_itm, 1) if 'has_item' in globals() else False
                            
                            frame:
                                xysize (1660, 160)
                                background ("#1a2846cc" if has_tr_item else "#131620aa")
                                padding (18, 12)
                                vbox:
                                    spacing 6
                                    hbox:
                                        spacing 20
                                        text f"🏆 【 標本：{tr.get('name')} 】" size 18 color ("#ffd700" if has_tr_item else "#777777") bold True
                                        text f"來源副本：{tr.get('stage_source')}" size 13 color "#aaaaaa"
                                        text ("陳列狀態：🌟 已解鎖並啟用全域光環" if has_tr_item else "陳列狀態：🔒 尚未獲取此戰利品") size 13 color ("#66ff66" if has_tr_item else "#ff4444")
                                    text f"展品故事：{tr.get('desc')}" size 13 color "#cccccc"
                                    text f"全域被動增益：{tr.get('buff_desc')}" size 14 color ("#00ffcc" if has_tr_item else "#555555") bold True

            # ==========================================
            # 5. 隊員休息室與羈絆分頁 (Lounge Tab)
            # ==========================================
            elif home_base_tab == "lounge":
                hbox:
                    spacing 20
                    xalign 0.5
                    
                    for b_info in db.get("teammate_bonds", []):
                        $ mem_n = b_info.get("name")
                        $ aff_val = teammate_affection.get(mem_n, 0) if 'teammate_affection' in globals() else 0
                        $ aff_lvl = 1 + (aff_val // 100)
                        
                        frame:
                            xysize (540, 720)
                            background "#141a2ecc"
                            padding (18, 15)
                            vbox:
                                spacing 12
                                xalign 0.5
                                
                                frame:
                                    xysize (80, 80)
                                    xalign 0.5
                                    background "#222a44aa"
                                    padding (2, 2)
                                    add b_info.get("avatar", "images/core_idle.PNG") xysize (76, 76) xalign 0.5 yalign 0.5
                                    
                                text f"【 {mem_n} 】" size 20 color "#00ffcc" bold True xalign 0.5
                                text f"身份：{b_info.get('role')}" size 13 color "#aaaaaa" xalign 0.5
                                text f"💖 羈絆好感度：Lv.{aff_lvl} ({aff_val} 點)" size 15 color "#ff66aa" bold True xalign 0.5
                                
                                null height 5
                                text "【 🌟 羈絆解鎖專屬特技 】" size 14 color "#ffdd88" bold True
                                for perk in b_info.get("perks", []):
                                    $ p_lvl = perk.get("level", 1)
                                    $ is_p_act = (aff_lvl >= p_lvl)
                                    text f"• 【Lv.{p_lvl}】 {perk.get('name')}: {perk.get('desc')}" size 12 color ("#66ff66" if is_p_act else "#666666")
                                    
                                null height 10
                                $ cur_q = teammate_chat_quota.get(mem_n, 1) if 'teammate_chat_quota' in globals() else 1
                                $ has_tea_itm = has_item("ITEM_TEA_PACK", 1) if 'has_item' in globals() else False
                                $ tea_cost_label = "靈茶x1" if has_tea_itm else "100點"
                                hbox:
                                    spacing 10
                                    xalign 0.5
                                    if cur_q > 0:
                                        textbutton f"【 ☕ 品茗談心 ({tea_cost_label}) 】":
                                            action [SetVariable("home_base_feedback", interact_teammate(mem_n, 'chat').get("msg", "")), renpy.restart_interaction]
                                            text_size 13 text_idle_color "#00ffea" text_hover_color "#ffffff"
                                    else:
                                        textbutton "【 ☕ 今日已品茗 (冥想中) 】":
                                            action [SetVariable("home_base_feedback", f"⚠️ 隊員【{mem_n}】正在冥想消化剛才的談話，請於通關副本回歸後再次品茗。"), renpy.restart_interaction]
                                            text_size 13 text_idle_color "#666666" text_hover_color "#888888"
                                        
                                    textbutton "【 🎁 贈送心儀禮物 (+50) 】":
                                        action [SetVariable("home_base_feedback", interact_teammate(mem_n, 'gift').get("msg", "")), renpy.restart_interaction]
                                        text_size 13 text_idle_color "#ff88ff" text_hover_color "#ffffff"

            null height 5

            # 底部離開按鈕
            textbutton "【 🚪 返回個人安全屋 / 輪迴廣場 】":
                xalign 0.5
                action Return("exit_home_base")
                text_size 18
                text_idle_color "#ff4444"
                text_hover_color "#ff8888"


# ==========================================
# 3血統槽位、同路線升級補差價與技能系統 (bloodline_system.rpy)
# ==========================================

init python:
    import json
    import copy

    # 1. 取得血統資料庫
    def get_bloodlines_data():
        global bloodlines_catalog
        if 'bloodlines_catalog' in globals() and bloodlines_catalog:
            return bloodlines_catalog
        try:
            with renpy.file("jsonData/bloodlines.json") as f:
                data = json.load(f)
                bloodlines_catalog = data.get("bloodlines", [])
                return bloodlines_catalog
        except Exception as e:
            bloodlines_catalog = []
            return bloodlines_catalog

    def get_bloodline_by_id(bloodline_id):
        catalog = get_bloodlines_data()
        for b in catalog:
            if b.get('id') == bloodline_id:
                return b
        return None

    # 取得隊員擁有的血統槽位列表 (上限 3 個)
    def get_member_bloodlines(member):
        if not member:
            return []
        if "bloodlines" not in member:
            old_b = member.get("bloodline", "無")
            if "吸血鬼" in old_b:
                member["bloodlines"] = [{"family": "vampire", "id": "vampire_bloodline", "grade": "D", "name": old_b, "paid_points": 1000}]
            elif "天使" in old_b:
                member["bloodlines"] = [{"family": "angel", "id": "angel_bloodline", "grade": "D", "name": old_b, "paid_points": 1000}]
            elif "惡魔" in old_b:
                member["bloodlines"] = [{"family": "demon", "id": "demon_bloodline", "grade": "D", "name": old_b, "paid_points": 1000}]
            else:
                member["bloodlines"] = []
        return member["bloodlines"]

    # 3. 根據角色真實血統槽位與基因鎖動態同步招式 (支援讀檔 100% 還原)
    def sync_member_skills_from_bloodlines(member):
        if not member:
            return []
            
        m_bloodlines = get_member_bloodlines(member)
        active_skills = []
        
        # 1. 遍歷當前存檔擁有的血統，裝載對應階級技能
        for b_entry in m_bloodlines:
            b_id = b_entry.get("id")
            g_key = b_entry.get("grade")
            b_data = get_bloodline_by_id(b_id)
            if b_data:
                g_info = b_data.get("grades", {}).get(g_key, {})
                for sk in g_info.get("skills", []):
                    if not any(s.get("id") == sk.get("id") for s in active_skills):
                        active_skills.append(copy.deepcopy(sk))
                        
        # 2. 裝載基因鎖技能 (一階以上)
        if to_int(member.get("gene_lock", 0)) >= 1:
            active_skills.append({
                "id": "gene_lock_burst_strike",
                "name": "基因鎖·極限爆發",
                "desc": "突破人體極限，釋放潛能造成 110 點毀滅性打擊。",
                "damage": 110,
                "ap_cost": 4,
                "cost_energy": 25,
                "energy_cost": 25,
                "energy_type": "mp",
                "heal": 0
            })
            
        # 3. 只有資深者（如資深執行者「冷月」）擁有初始固有招式，新人一律無技能
        m_name = member.get("name", "")
        m_role = member.get("role", "")
        if "冷月" in m_name or "資深" in m_role:
            if not any(s.get("id") == "lengyue_mind_blast" for s in active_skills):
                active_skills.append({
                    "id": "lengyue_mind_blast",
                    "name": "念動力震懾彈",
                    "desc": "以強悍的精神念力引爆空氣，造成 85 點念力衝擊傷害。",
                    "damage": 85,
                    "ap_cost": 4,
                    "energy_cost": 20,
                    "energy_type": "mp",
                    "heal": 0
                })
            if not any(s.get("id") == "lengyue_dual_pistol" for s in active_skills):
                active_skills.append({
                    "id": "lengyue_dual_pistol",
                    "name": "雙槍精準速射",
                    "desc": "資深老兵的雙槍點射，造成 65 點物理穿透傷害。",
                    "damage": 65,
                    "ap_cost": 4,
                    "energy_cost": 10,
                    "energy_type": "mp",
                    "heal": 0
                })
            
        member["skills"] = active_skills
        return active_skills

    # 2. 計算升級補差價與購買判定
    def get_bloodline_purchase_cost(bloodline_id, grade_key, member_idx=0):
        b_data = get_bloodline_by_id(bloodline_id)
        if not b_data:
            return 0, 0, False, "無此血統"
            
        grades = b_data.get("grades", {})
        if grade_key not in grades:
            return 0, 0, False, "無此階級"
            
        full_cost = grades[grade_key].get("points", 0)
        family = b_data.get("family", bloodline_id)
        
        roster = get_team_roster()
        member = roster[member_idx] if roster and member_idx < len(roster) else {}
        m_bloodlines = get_member_bloodlines(member)
        
        # 尋找是否已擁有同家族路線血統
        existing_slot = None
        for b_entry in m_bloodlines:
            if b_entry.get("family") == family or b_entry.get("id") == bloodline_id:
                existing_slot = b_entry
                break
                
        if existing_slot:
            paid_pts = existing_slot.get("paid_points", 0)
            diff_cost = max(0, full_cost - paid_pts)
            return full_cost, diff_cost, True, existing_slot
        else:
            return full_cost, full_cost, False, None

    # 3. 核心：血統購買/升級邏輯 (支援 3 槽位與自動補差價)
    def purchase_bloodline(bloodline_id, grade_key, member_idx=0):
        global points, hp, team_roster
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "找不到目標隊員資料。"}
            
        target_member = roster[member_idx]
        b_data = get_bloodline_by_id(bloodline_id)
        if not b_data:
            return {"success": False, "msg": "輪迴資料庫中無此血統紀錄。"}
            
        grades = b_data.get("grades", {})
        if grade_key not in grades:
            return {"success": False, "msg": f"無此血統階級：{grade_key}。"}
            
        grade_info = grades[grade_key]
        full_cost = grade_info.get("points", 0)
        fate_shard = grade_info.get("fate_shard", "C")
        family = b_data.get("family", bloodline_id)
        
        full_cost, actual_cost, is_upgrade, old_slot = get_bloodline_purchase_cost(bloodline_id, grade_key, member_idx)
        
        # 1. 檢查前置屬性需求門檻 (req_stats)
        req_stats = grade_info.get("req_stats", {})
        for s_k, s_val in req_stats.items():
            cur_s = target_member.get(s_k.lower(), 20)
            if cur_s < s_val:
                return {
                    "success": False,
                    "msg": f"【屬性門檻未達標】融合【{grade_info.get('name')}】需要 {s_k} >= {s_val}！\n【{target_member.get('name')}】當前 {s_k} 僅為 {cur_s}。請前往屬性石碑加點！"
                }

        # 2. 檢查 3 槽位上限
        m_bloodlines = get_member_bloodlines(target_member)
        if not is_upgrade and len(m_bloodlines) >= 3:
            return {
                "success": False,
                "msg": "【輪迴提示】已達到 3 個血統槽位上限！無法再融合新的修煉體系。"
            }
            
        # 檢查生存點數
        current_pts = points if member_idx == 0 else target_member.get("points", 0)
        if current_pts < actual_cost:
            return {
                "success": False,
                "msg": f"【輪迴提示】生存點數不足！\n此強化需補繳 {actual_cost} 點，目前僅有 {current_pts} 點。"
            }
            
        # 檢查命運碎片
        if 'has_fate_shard' in globals() and not has_fate_shard(fate_shard, 1):
            return {
                "success": False,
                "msg": f"【輪迴提示】缺少【{fate_shard} 階命運碎片 x1】！請前往命運碎片工坊合成或在副本中獲取。"
            }
            
        # 扣除生存點數與命運碎片
        if member_idx == 0:
            points -= actual_cost
            target_member["points"] = points
        else:
            target_member["points"] = target_member.get("points", 0) - actual_cost
            
        if 'remove_fate_shard' in globals():
            remove_fate_shard(fate_shard, 1)
            
        # 套用與更新血統槽位
        grade_name = grade_info.get("name", f"{grade_key}級 {b_data.get('name')}")
        
        new_entry = {
            "family": family,
            "id": bloodline_id,
            "grade": grade_key,
            "name": grade_name,
            "paid_points": full_cost
        }
        
        if is_upgrade and old_slot in m_bloodlines:
            idx = m_bloodlines.index(old_slot)
            m_bloodlines[idx] = new_entry
        else:
            m_bloodlines.append(new_entry)
            
        target_member["bloodlines"] = m_bloodlines
        target_member["bloodline"] = " + ".join([b["name"] for b in m_bloodlines])
        
        # 套用屬性提升
        attrs = grade_info.get("attributes", {})
        for attr_key, attr_val in attrs.items():
            if attr_key in ("hp", "max_hp"):
                target_member["max_hp"] = max(int(target_member.get("max_hp", 100)), int(target_member.get("max_hp", 100)) + val_int)
                if member_idx == 0:
                    hp = target_member["hp"]
            elif attr_key in ("mp", "max_mp"):
                target_member["max_mp"] = max(int(target_member.get("max_mp", 50)), int(target_member.get("max_mp", 50)) + val_int)
                target_member["mp"] = target_member["max_mp"]
                target_member[attr_key] = max(int(target_member.get(attr_key, 0)), val_int)
                curr_key = attr_key.replace("_max", "_current")
                target_member[curr_key] = target_member[attr_key]
                target_member[attr_key] = max(int(target_member.get(attr_key, 0)), val_int)
            else:
                target_member[attr_key] = attr_val
                
        existing_skills = target_member.get("skills", [])
        new_skills = grade_info.get("skills", [])
        for nsk in new_skills:
            if not any(esk.get("id") == nsk.get("id") for esk in existing_skills):
                existing_skills.append(nsk)
        target_member["skills"] = existing_skills
        
        upgrade_info = f" (晉升補差價：折抵 {full_cost - actual_cost} 點，實付 {actual_cost} 點)" if is_upgrade else f" (實付 {actual_cost} 點)"
        return {
            "success": True,
            "msg": f"【輪迴強化完成】聖光降臨！成功融合【{grade_name}】{upgrade_info}，消耗 {fate_shard}階命運碎片 x1！\n生命與能量池已全面擴充，目前已融合 {len(m_bloodlines)}/3 個血統槽位！",
            "bloodline_name": grade_name,
            "skills": new_skills
        }


# ==========================================
# 輪迴血統強化石碑介面 (支援3槽位與補差價優惠)
# ==========================================
screen bloodline_exchange_screen():

    default bloodline_filter_tag = "全部"
    default current_tab = "vampire_bloodline"
    default current_grade = "C"

    $ catalog = get_bloodlines_data()
    $ player_member = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]
    $ p_bloodlines = get_member_bloodlines(player_member)
    $ shards = get_fate_shards() if 'get_fate_shards' in globals() else {}

    # 根據標籤過濾血統
    $ filtered_bloodlines = []
    for b in catalog:
        $ b_tags = b.get("tags", [])
        if bloodline_filter_tag == "全部" or bloodline_filter_tag in b_tags:
            $ filtered_bloodlines.append(b)

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1740, 970)
        padding (25, 20)
        background "#0d111edd"

        vbox:
            spacing 10
            xalign 0.5

            # 頂部狀態與 3 槽位展示列
            hbox:
                spacing 30
                xalign 0.5
                text "【 🧬 基因血統與專屬戰技強化石碑 】" size 24 color "#ffcc00" bold True yalign 0.5
                text f"生存點數: {points} 點" size 18 color "#00ffcc" bold True yalign 0.5
                text f"命運碎片: D({shards.get('D',0)}) C({shards.get('C',0)}) B({shards.get('B',0)}) A({shards.get('A',0)}) S({shards.get('S',0)})" size 15 color "#ddaaff" yalign 0.5
                
                textbutton "【 🔑 特權密令 】":
                    action Return("admin_command")
                    text_size 16 text_idle_color "#ffcc00" text_hover_color "#ffffff" yalign 0.5

            # 3 個已融合血統槽位條
            frame:
                xysize (1690, 48)
                background "#161e30ee"
                padding (15, 8)
                hbox:
                    spacing 30
                    yalign 0.5
                    text f"【 當前已融合血統槽位 ({len(p_bloodlines)}/3) 】" size 14 color "#ffaa00" bold True
                    for i in range(3):
                        if i < len(p_bloodlines):
                            $ slot_b = p_bloodlines[i]
                            text f"槽位 {i+1}：★ {slot_b.get('name')}" size 13 color "#66ff66" bold True
                        else:
                            text f"槽位 {i+1}：( 空置空位 )" size 13 color "#666666"

            # 體系標籤列
            hbox:
                spacing 10
                xalign 0.5
                text "修煉體系：" size 15 color "#ffaa00" yalign 0.5
                for t_name in ["全部", "東方修真", "西方神秘", "狂暴變身", "精靈魔法", "宇宙超能", "神聖光明"]:
                    $ is_bt_active = (bloodline_filter_tag == t_name)
                    button:
                        xysize (140, 36)
                        background ("#e6a100" if is_bt_active else "#222a42")
                        action SetScreenVariable("bloodline_filter_tag", t_name)
                        text t_name size 14 color ("#000000" if is_bt_active else "#ffffff") bold True xalign 0.5 yalign 0.5

            # 主雙欄
            hbox:
                spacing 20
                xalign 0.5

                # 左側血統列表
                frame:
                    xysize (480, 750)
                    background "#161b2ebb"
                    padding (15, 12)
                    vbox:
                        spacing 8
                        text f"【 血統清單 · {bloodline_filter_tag} ({len(filtered_bloodlines)} 種) 】" size 17 color "#00ffff" bold True
                        viewport:
                            xysize (450, 690)
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            vbox:
                                spacing 8
                                for b in filtered_bloodlines:
                                    $ b_id = b.get('id', '')
                                    $ b_name = b.get('name', '未知血統')
                                    $ b_energy = b.get('energy_name', '特殊能量')
                                    $ b_tags_str = " · ".join(b.get('tags', []))
                                    $ is_selected = (current_tab == b_id)
                                    $ has_fam = any(b_e.get("family") == b.get("family", b_id) for b_e in p_bloodlines)

                                    button:
                                        xysize (430, 90)
                                        background ("#3b5288ee" if is_selected else ("#24382daa" if has_fam else "#222a42aa"))
                                        hover_background "#4a68aaaa"
                                        action [SetScreenVariable("current_tab", b_id), SetScreenVariable("current_grade", "C")]
                                        vbox:
                                            spacing 2
                                            hbox:
                                                spacing 8
                                                text "★ [b_name]" size 16 color ("#00ffff" if is_selected else "#ffffff") bold True
                                                if has_fam:
                                                    text "【已融合】" size 12 color "#66ff66" bold True
                                            text f"能量體系：{b_energy}" size 12 color "#aaaaaa"
                                            text f"標籤：{b_tags_str}" size 11 color "#ddaaff"

                # 右側血統詳情與階級切換
                frame:
                    xysize (1190, 750)
                    background "#161b2ebb"
                    padding (20, 15)

                    $ selected_bloodline = get_bloodline_by_id(current_tab)
                    if selected_bloodline:
                        $ grades_dict = selected_bloodline.get("grades", {})
                        $ cur_grade_data = grades_dict.get(current_grade, {})
                        $ fate_shard = cur_grade_data.get("fate_shard", "C")
                        $ grade_name = cur_grade_data.get("name", "未命名階級")
                        $ grade_skills = cur_grade_data.get("skills", [])
                        $ grade_attrs = cur_grade_data.get("attributes", {})
                        
                        $ full_cost, actual_cost, is_upg, old_s = get_bloodline_purchase_cost(current_tab, current_grade, 0)
                        $ can_afford_pts = (points >= actual_cost)
                        $ can_afford_shard = has_fate_shard(fate_shard, 1)
                        $ can_afford = can_afford_pts and can_afford_shard

                        vbox:
                            spacing 10
                            vbox:
                                spacing 2
                                text "[selected_bloodline.get('name', '')]" size 22 color "#00ffff" bold True
                                text "[selected_bloodline.get('desc', '')]" size 13 color "#bbbbbb"

                            # 階級按鈕列 (D / C / B / A / S 階)
                            hbox:
                                spacing 10
                                text "選擇階級：" size 15 color "#ffaa00" yalign 0.5
                                for g_key in ["D", "C", "B", "A", "S"]:
                                    if g_key in grades_dict:
                                        $ is_g_active = (current_grade == g_key)
                                        $ g_cost = grades_dict[g_key].get("points", 0)
                                        button:
                                            xysize (155, 38)
                                            background ("#e6a100" if is_g_active else "#2b354f")
                                            hover_background "#53648f"
                                            action SetScreenVariable("current_grade", g_key)

                            # 屬性與技能展示框
                            frame:
                                xysize (1150, 480)
                                background "#0f1424aa"
                                padding (15, 12)
                                viewport:
                                    xysize (1120, 455)
                                    scrollbars "vertical"
                                    mousewheel True
                                    draggable True
                                    vbox:
                                        spacing 10
                                        # 兌換費用與補差價說明
                                        hbox:
                                            spacing 25
                                            vbox:
                                                spacing 3
                                                xysize (480, None)
                                                text f"【 階級名稱 】{grade_name}" size 15 color "#ffcc00" bold True
                                                if is_upg:
                                                    $ discount = full_cost - actual_cost
                                                    text f"【 晉升補差價優惠 】原價 {full_cost} 點 -> 實付 {actual_cost} 點 (折抵 {discount} 點)" size 14 color "#66ff66" bold True
                                                else:
                                                    text f"【 需求點數 】{full_cost} 生存點數" size 14 color ("#66ff66" if can_afford_pts else "#ff4444") bold True
                                                text f"【 命運碎片需求 】{fate_shard} 階命運碎片 x 1" size 14 color ("#ddaaff" if can_afford_shard else "#ff4444") bold True

                                            vbox:
                                                spacing 3
                                                xysize (600, None)
                                                text "【 屬性與能量增益 】" size 15 color "#00ffcc" bold True
                                                hbox:
                                                    spacing 15
                                                    $ hp_gain = grade_attrs.get('hp', grade_attrs.get('max_hp', 0))
                                                    if hp_gain > 0:
                                                        text f"生命上限 +{hp_gain}" size 13 color "#ff6666"
                                                    if grade_attrs.get('blood_max', 0) > 0:
                                                        text f"血能上限 +{grade_attrs['blood_max']}" size 13 color "#ff4444"
                                                    if grade_attrs.get('neili_max', 0) > 0:
                                                        text f"內力上限 +{grade_attrs['neili_max']}" size 13 color "#ffaa00"
                                                    if grade_attrs.get('qi_max', 0) > 0:
                                                        text f"氣血上限 +{grade_attrs['qi_max']}" size 13 color "#ff6666"
                                                    if grade_attrs.get('mental_max', 0) > 0:
                                                        text f"精神上限 +{grade_attrs['mental_max']}" size 13 color "#00ccff"
                                                    if grade_attrs.get('regeneration', 0) > 0:
                                                        text f"自癒 +{grade_attrs['regeneration']}" size 13 color "#66ff66"

                                        null height 2
                                        add "#334466" xysize (1100, 1)

                                        # 專屬技能清單
                                        vbox:
                                            spacing 6
                                            text f"【 該階級專屬戰鬥技能 ({len(grade_skills)} 招) 】" size 16 color "#ffaa00" bold True
                                            for sk in grade_skills:
                                                $ sk_name = sk.get('name', '招式')
                                                $ sk_cost = sk.get('energy_cost', 0)
                                                $ sk_type = sk.get('energy_type', 'mp')
                                                $ sk_dmg = sk.get('damage', 0)
                                                $ sk_heal = sk.get('heal', 0)
                                                $ sk_desc = sk.get('desc', '')
                                                frame:
                                                    xysize (1100, None)
                                                    background "#1c2338aa"
                                                    padding (10, 8)
                                                    vbox:
                                                        spacing 3
                                                        hbox:
                                                            spacing 15
                                                            text f"🔥 {sk_name}" size 15 color "#00ffff" bold True
                                                            text f"消耗: {sk_cost} 點 ({sk_type})" size 13 color "#ffcc00"
                                                            if sk_dmg > 0:
                                                                text f"威力: {sk_dmg} 傷害" size 13 color "#ff6666" bold True
                                                            if sk_heal > 0:
                                                                text f"自癒: +{sk_heal} HP" size 13 color "#66ff66" bold True
                                                        text f"效果說明：{sk_desc}" size 12 color "#cccccc"

                            # 底部兌換操作
                            hbox:
                                spacing 20
                                xalign 0.5
                                if can_afford:
                                    textbutton f"【 ⚡ 立即扣除 {actual_cost} 點數與 {fate_shard} 階碎片融合【{grade_name}】 】":
                                        action Return(("buy_bloodline", current_tab, current_grade))
                                        text_size 18 text_idle_color "#00ff00" text_hover_color "#ffffff"
                                else:
                                    textbutton "【 ❌ 資源不足 (缺少生存點數或命運碎片) 】":
                                        action NullAction()
                                        text_size 17 text_idle_color "#884444"

            null height 2

            textbutton "【 🚪 關閉血統面板，返回輪迴廣場 】":
                xalign 0.5
                action Return("leave_bloodline")
                text_size 19
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"

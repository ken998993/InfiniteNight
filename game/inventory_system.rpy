# ==========================================
# 背包、8大部位裝備與命運碎片工坊系統 (inventory_system.rpy)
# ==========================================

init python:
    import json

    # 1. 取得道具資料庫
    def get_items_data():
        global items_catalog
        if 'items_catalog' in globals() and items_catalog:
            return items_catalog
        try:
            with renpy.file("jsonData/items.json") as f:
                data = json.load(f)
                items_catalog = data.get("items", [])
                return items_catalog
        except Exception as e:
            items_catalog = []
            return items_catalog

    def get_item_by_id(item_id):
        catalog = get_items_data()
        for itm in catalog:
            if itm.get('id') == item_id:
                return itm
        return None

    # 2. 背包基礎操作
    def get_inventory():
        global inventory
        if 'inventory' not in globals() or inventory is None:
            inventory = [
                {"id": "item_heal_spray", "count": 3},
                {"id": "item_mp_potion", "count": 2},
                {"id": "item_grenade", "count": 2},
                {"id": "weapon_gauss_rifle", "count": 1},
                {"id": "EQ_TECH_HELMET_01", "count": 1},
                {"id": "EQ_MOUNT_GLIDER_01", "count": 1}
            ]
        return inventory

    def add_item(item_id, count=1):
        inv = get_inventory()
        for entry in inv:
            if entry["id"] == item_id:
                entry["count"] += count
                return True
        inv.append({"id": item_id, "count": count})
        return True

    def remove_item(item_id, count=1):
        inv = get_inventory()
        for entry in inv:
            if entry["id"] == item_id:
                entry["count"] -= count
                if entry["count"] <= 0:
                    inv.remove(entry)
                return True
        return False

    def has_item(item_id, count=1):
        inv = get_inventory()
        for entry in inv:
            if entry["id"] == item_id and entry["count"] >= count:
                return True
        return False

    # 3. 命運碎片經濟與工坊操作 (4 品質階級 + S 神聖階級)
    def get_fate_shards():
        global fate_shards
        if 'fate_shards' not in globals() or fate_shards is None:
            fate_shards = {"D": 3, "C": 2, "B": 1, "A": 0, "S": 0}
        return fate_shards

    def add_fate_shard(tier, count=1):
        shards = get_fate_shards()
        shards[tier] = shards.get(tier, 0) + count
        return True

    def remove_fate_shard(tier, count=1):
        shards = get_fate_shards()
        if shards.get(tier, 0) >= count:
            shards[tier] -= count
            return True
        return False

    def has_fate_shard(tier, count=1):
        shards = get_fate_shards()
        return shards.get(tier, 0) >= count

    # 3 合 1 碎片合成
    def synthesize_fate_shard(source_tier):
        tier_next = {"D": "C", "C": "B", "B": "A", "A": "S"}
        if source_tier not in tier_next:
            return {"success": False, "msg": "【工坊提示】該階級已達最高神聖品質，無法繼續合成！"}
        target_tier = tier_next[source_tier]
        if not has_fate_shard(source_tier, 3):
            return {"success": False, "msg": f"【工坊提示】合成需要 3 個 {source_tier} 階碎片，目前數量不足！"}
            
        remove_fate_shard(source_tier, 3)
        add_fate_shard(target_tier, 1)
        return {"success": True, "msg": f"✨【合成成功】消耗 3 個 {source_tier} 階命運碎片，成功凝聚出 1 個【{target_tier} 階命運碎片】！"}

    # 1 拆 2 碎片拆解 (含階級損耗)
    def dismantle_fate_shard(source_tier):
        tier_prev = {"S": "A", "A": "B", "B": "C", "C": "D"}
        if source_tier not in tier_prev:
            return {"success": False, "msg": "【工坊提示】該階級已為基礎品質，無法繼續拆解！"}
        target_tier = tier_prev[source_tier]
        if not has_fate_shard(source_tier, 1):
            return {"success": False, "msg": f"【工坊提示】背包中無可拆解的 {source_tier} 階碎片！"}
            
        remove_fate_shard(source_tier, 1)
        add_fate_shard(target_tier, 2)
        return {"success": True, "msg": f"🔨【拆解完成】分解 1 個 {source_tier} 階命運碎片，獲得 2 個【{target_tier} 階命運碎片】（損耗 1 個階級精華）。"}

    # 4. 8 大裝備部位穿戴與卸下邏輯
    EQUIPMENT_SLOTS_MAP = {
        "head": "頭部",
        "torso": "胸甲/身軀",
        "hands": "手套/手腕",
        "feet": "鞋子/靴子",
        "necklace": "項鍊/飾品",
        "main_hand": "主手武器",
        "off_hand": "副手/防盾",
        "mount": "飛行載具/特殊"
    }

    def equip_item(item_id, member_idx=0):
        global hp, team_roster
        itm = get_item_by_id(item_id)
        if not itm:
            return {"success": False, "msg": "找不到該裝備。"}
            
        slot = itm.get("equip_slot")
        if not slot or slot not in EQUIPMENT_SLOTS_MAP:
            return {"success": False, "msg": "該物品非可裝備部位。"}
            
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "無效的目標隊員。"}
            
        member = roster[member_idx]
        slot_key = f"equipped_{slot}"
        
        # 檢驗穿戴屬性門檻 (req_stats)
        req_stats = itm.get("req_stats", {})
        for s_k, s_val in req_stats.items():
            cur_s = member.get(s_k.lower(), 20)
            if cur_s < s_val:
                return {
                    "success": False,
                    "msg": f"【屬性門檻未達標】佩戴【{itm.get('name')}】需要 {s_k} >= {s_val}！\n【{member.get('name')}】當前 {s_k} 僅為 {cur_s}。請前往屬性石碑進行加點！"
                }

        # 若已有舊裝備則先卸下
        if slot_key in member and member[slot_key]:
            unequip_item(slot, member_idx)
            
        # 裝備新物品並套用屬性
        member[slot_key] = item_id
        attrs = itm.get("attributes", {})
        for k, v in attrs.items():
            v_int = int(v) if isinstance(v, (int, str, float)) else 0
            if k == "atk":
                member["atk_bonus"] = int(member.get("atk_bonus", 0)) + v_int
            elif k == "max_hp":
                member["max_hp"] = int(member.get("max_hp", 100)) + v_int
                member["hp"] = min(member["max_hp"], int(member.get("hp", 100)) + v_int)
                if member_idx == 0:
                    hp = member["hp"]
            elif k == "max_mp":
                member["max_mp"] = int(member.get("max_mp", 50)) + v_int
                member["mp"] = min(member["max_mp"], int(member.get("mp", 50)) + v_int)
            elif k in ("blood_max", "neili_max", "qi_max", "mental_max", "calc_max"):
                member[k] = int(member.get(k, 0)) + v_int
                
        slot_name = EQUIPMENT_SLOTS_MAP.get(slot, slot)
        flight_msg = " (賦予【飛行標籤】)" if itm.get("is_flight") else ""
        gas_msg = " (賦予【毒氣免疫】)" if itm.get("is_gas_immune") else ""
        return {"success": True, "msg": f"成功裝備【{itm.get('name')}】至【{slot_name}】部位！{flight_msg}{gas_msg}"}

    def unequip_item(slot, member_idx=0):
        global hp, team_roster
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "無效的目標隊員。"}
            
        member = roster[member_idx]
        slot_key = f"equipped_{slot}"
        old_id = member.get(slot_key)
        if not old_id:
            return {"success": False, "msg": "該欄位未裝備任何物品。"}
            
        old_itm = get_item_by_id(old_id)
        if old_itm:
            attrs = old_itm.get("attributes", {})
            for k, v in attrs.items():
                v_int = int(v) if isinstance(v, (int, str, float)) else 0
                if k == "atk":
                    member["atk_bonus"] = max(0, int(member.get("atk_bonus", 0)) - v_int)
                elif k == "max_hp":
                    member["max_hp"] = max(50, int(member.get("max_hp", 100)) - v_int)
                    member["hp"] = min(member["max_hp"], int(member.get("hp", 100)))
                    if member_idx == 0:
                        hp = member["hp"]
                elif k == "max_mp":
                    member["max_mp"] = max(20, int(member.get("max_mp", 50)) - v_int)
                    member["mp"] = min(member["max_mp"], int(member.get("mp", 50)))
                elif k in ("blood_max", "neili_max", "qi_max", "mental_max", "calc_max"):
                    member[k] = max(0, int(member.get(k, 0)) - v_int)
                    
        member[slot_key] = None
        slot_name = EQUIPMENT_SLOTS_MAP.get(slot, slot)
        old_name = old_itm.get('name', '裝備') if old_itm else '裝備'
        return {"success": True, "msg": f"已成功卸下【{slot_name}】部位的【{old_name}】。"}

    # 5. 特殊標籤判定方法 (飛行 / 防毒 / 魔法打擊)
    def has_flight_capability(member):
        if not member:
            return False
        # 檢查裝備 (飛行滑板 / 噴射背包 / 懸浮飛靴)
        for slot in ["mount", "feet"]:
            eq_id = member.get(f"equipped_{slot}")
            if eq_id:
                itm = get_item_by_id(eq_id)
                if itm and itm.get("is_flight", False):
                    return True
        # 檢查血統 (天使 / 賽亞人)
        b_name = member.get("bloodline", "")
        if "天使" in b_name or "賽亞人" in b_name:
            return True
        return False

    def is_gas_immune(member):
        if not member:
            return False
        for slot in ["head", "torso"]:
            eq_id = member.get(f"equipped_{slot}")
            if eq_id:
                itm = get_item_by_id(eq_id)
                if itm and itm.get("is_gas_immune", False):
                    return True
        return False

    def has_magic_damage(member):
        if not member:
            return False
        for slot in ["main_hand", "off_hand"]:
            eq_id = member.get(f"equipped_{slot}")
            if eq_id:
                itm = get_item_by_id(eq_id)
                if itm and (itm.get("is_magic_weapon", False) or itm.get("category") == "Magic"):
                    return True
        b_name = member.get("bloodline", "")
        if "修真" in b_name or "內力" in b_name or "天使" in b_name or "精靈" in b_name:
            return True
        return False

    # 6. 道具使用與商店購買邏輯
    def use_inventory_item(item_id, member_idx=0):
        global hp, team_roster
        itm = get_item_by_id(item_id)
        if not itm:
            return {"success": False, "msg": "找不到該道具。"}
            
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "無效的目標隊員。"}
            
        member = roster[member_idx]
        if not has_item(item_id, 1):
            return {"success": False, "msg": "背包中無此道具。"}
            
        eff_type = itm.get("effect_type")
        eff_val = itm.get("effect_val", 0)
        m_name = member.get("name", "隊員")
        itm_name = itm.get("name", "道具")
        
        if eff_type == "heal_hp":
            member["hp"] = min(member.get("max_hp", 100), member.get("hp", 100) + eff_val)
            if member_idx == 0:
                hp = member["hp"]
            remove_item(item_id, 1)
            return {"success": True, "msg": f"【使用成功】對 {m_name} 使用了【{itm_name}】，恢復了 {eff_val} 點生命值！"}
            
        elif eff_type == "heal_mp":
            member["mp"] = min(member.get("max_mp", 50), member.get("mp", 50) + eff_val)
            if "mental_current" in member and member.get("mental_max", 0) > 0:
                member["mental_current"] = min(member["mental_max"], member["mental_current"] + 30)
            remove_item(item_id, 1)
            return {"success": True, "msg": f"【使用成功】對 {m_name} 使用了【{itm_name}】，恢復了 {eff_val} 點精神力！"}
            
        elif eff_type == "heal_energy":
            for k in ["blood", "neili", "qi", "mental"]:
                max_k = f"{k}_max"
                cur_k = f"{k}_current"
                if max_k in member and member[max_k] > 0:
                    member[cur_k] = min(member[max_k], member.get(cur_k, 0) + eff_val)
            remove_item(item_id, 1)
            return {"success": True, "msg": f"【使用成功】對 {m_name} 使用了【{itm_name}】，所有能量池補充了 {eff_val} 點！"}
            
        elif itm.get("type") == "tactical":
            return {"success": False, "msg": f"【{itm_name}】屬於戰術爆破武器，請在戰鬥中投擲！"}
            
        else:
            return {"success": False, "msg": f"【{itm_name}】無法直接使用。若是裝備請點擊【穿戴裝備】。"}

    def purchase_shop_item(item_id, count=1):
        global points, team_roster
        itm = get_item_by_id(item_id)
        if not itm:
            return {"success": False, "msg": "商品已下架或不存在。"}
            
        cost_pts = itm.get("cost_points", 0) * count
        cost_shard = itm.get("cost_fate_shard")
        
        if points < cost_pts:
            return {"success": False, "msg": f"【輪迴提示】生存點數不足！需要 {cost_pts} 點，目前僅有 {points} 點。"}
            
        if cost_shard and not has_fate_shard(cost_shard, 1):
            return {"success": False, "msg": f"【輪迴提示】缺少【{cost_shard} 階命運碎片 x1】！可前往命運碎片工坊合成。"}
            
        points -= cost_pts
        if cost_shard:
            remove_fate_shard(cost_shard, 1)
            
        if 'team_roster' in globals() and team_roster and len(team_roster) > 0:
            team_roster[0]["points"] = points
            
        add_item(item_id, count)
        shard_info = f" + {cost_shard}階命運碎片" if cost_shard else ""
        return {"success": True, "msg": f"【兌換成功】扣除 {cost_pts} 點數{shard_info}，獲得【{itm.get('name')}】x{count}！"}


# ==========================================
# 命運碎片工坊介面 (fate_shard_workshop_screen)
# ==========================================
screen fate_shard_workshop_screen():

    $ shards = get_fate_shards()

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1600, 880)
        padding (35, 30)
        background "#0f1424fa"

        vbox:
            spacing 15
            xalign 0.5

            text "【 🔮 輪迴空間 · 命運碎片工坊 (合成 / 拆解) 】" size 26 color "#ffcc00" bold True xalign 0.5
            text "透過法則精煉，可將 3 個同階碎片合成為 1 個高階碎片；或將 1 個高階碎片拆解為 2 個低階碎片。" size 15 color "#bbbbbb" xalign 0.5

            null height 5

            # 當前持有碎片展示列
            frame:
                xysize (1530, 90)
                background "#1a2238ee"
                padding (20, 15)
                hbox:
                    spacing 50
                    xalign 0.5
                    yalign 0.5
                    text f"🟢 D 階 (精良): {shards.get('D',0)} 枚" size 18 color "#66ff66" bold True
                    text f"🔵 C 階 (稀有): {shards.get('C',0)} 枚" size 18 color "#00ffff" bold True
                    text f"🟣 B 階 (史詩): {shards.get('B',0)} 枚" size 18 color "#ddaaff" bold True
                    text f"🟡 A 階 (傳奇): {shards.get('A',0)} 枚" size 18 color "#ffaa00" bold True
                    text f"🔴 S 階 (神聖): {shards.get('S',0)} 枚" size 18 color "#ff4444" bold True

            null height 10

            # 雙欄：左側合成（3合1），右側拆解（1拆2）
            hbox:
                spacing 35
                xalign 0.5

                # 左側：合成配方區
                frame:
                    xysize (740, 520)
                    background "#161b2ebb"
                    padding (20, 15)
                    vbox:
                        spacing 12
                        text "【 ⚡ 命運碎片合成 (3 合 1) 】" size 20 color "#00ffcc" bold True
                        text "消耗 3 枚低階碎片，融合成 1 枚高一階品質碎片：" size 13 color "#aaaaaa"
                        null height 5

                        # D -> C
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 3x D階 (精良) ➜ 1x C階 (稀有)" size 15 color "#ffffff" bold True
                                text f"當前持有 D階: {shards.get('D',0)}/3" size 12 color "#66ff66"
                            button:
                                xysize (200, 42)
                                background ("#1f4433" if shards.get('D',0) >= 3 else "#333333")
                                hover_background "#2e664c"
                                action Return(("synth", "D"))
                                text "⚡ 凝聚合成" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                        # C -> B
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 3x C階 (稀有) ➜ 1x B階 (史詩)" size 15 color "#ffffff" bold True
                                text f"當前持有 C階: {shards.get('C',0)}/3" size 12 color "#00ffff"
                            button:
                                xysize (200, 42)
                                background ("#1f4433" if shards.get('C',0) >= 3 else "#333333")
                                hover_background "#2e664c"
                                action Return(("synth", "C"))
                                text "⚡ 凝聚合成" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                        # B -> A
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 3x B階 (史詩) ➜ 1x A階 (傳奇)" size 15 color "#ffffff" bold True
                                text f"當前持有 B階: {shards.get('B',0)}/3" size 12 color "#ddaaff"
                            button:
                                xysize (200, 42)
                                background ("#1f4433" if shards.get('B',0) >= 3 else "#333333")
                                hover_background "#2e664c"
                                action Return(("synth", "B"))
                                text "⚡ 凝聚合成" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                        # A -> S
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 3x A階 (傳奇) ➜ 1x S階 (神聖)" size 15 color "#ffffff" bold True
                                text f"當前持有 A階: {shards.get('A',0)}/3" size 12 color "#ffaa00"
                            button:
                                xysize (200, 42)
                                background ("#1f4433" if shards.get('A',0) >= 3 else "#333333")
                                hover_background "#2e664c"
                                action Return(("synth", "A"))
                                text "⚡ 凝聚合成" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                # 右側：拆解配方區
                frame:
                    xysize (740, 520)
                    background "#161b2ebb"
                    padding (20, 15)
                    vbox:
                        spacing 12
                        text "【 🔨 命運碎片拆解 (1 拆 2) 】" size 20 color "#ffaa00" bold True
                        text "分解 1 枚高階碎片為 2 枚低一階碎片 (含損耗)：" size 13 color "#aaaaaa"
                        null height 5

                        # S -> A
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 1x S階 (神聖) ➜ 2x A階 (傳奇)" size 15 color "#ffffff" bold True
                                text f"當前持有 S階: {shards.get('S',0)}/1" size 12 color "#ff4444"
                            button:
                                xysize (200, 42)
                                background ("#55331f" if shards.get('S',0) >= 1 else "#333333")
                                hover_background "#77442a"
                                action Return(("dismantle", "S"))
                                text "🔨 碎裂拆解" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                        # A -> B
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 1x A階 (傳奇) ➜ 2x B階 (史詩)" size 15 color "#ffffff" bold True
                                text f"當前持有 A階: {shards.get('A',0)}/1" size 12 color "#ffaa00"
                            button:
                                xysize (200, 42)
                                background ("#55331f" if shards.get('A',0) >= 1 else "#333333")
                                hover_background "#77442a"
                                action Return(("dismantle", "A"))
                                text "🔨 碎裂拆解" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                        # B -> C
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 1x B階 (史詩) ➜ 2x C階 (稀有)" size 15 color "#ffffff" bold True
                                text f"當前持有 B階: {shards.get('B',0)}/1" size 12 color "#ddaaff"
                            button:
                                xysize (200, 42)
                                background ("#55331f" if shards.get('B',0) >= 1 else "#333333")
                                hover_background "#77442a"
                                action Return(("dismantle", "B"))
                                text "🔨 碎裂拆解" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

                        # C -> D
                        hbox:
                            spacing 15
                            vbox:
                                xysize (480, None)
                                text "• 1x C階 (稀有) ➜ 2x D階 (精良)" size 15 color "#ffffff" bold True
                                text f"當前持有 C階: {shards.get('C',0)}/1" size 12 color "#00ffff"
                            button:
                                xysize (200, 42)
                                background ("#55331f" if shards.get('C',0) >= 1 else "#333333")
                                hover_background "#77442a"
                                action Return(("dismantle", "C"))
                                text "🔨 碎裂拆解" size 14 color "#ffffff" bold True xalign 0.5 yalign 0.5

            null height 5

            textbutton "【 🚪 關閉工坊，返回輪迴廣場 】":
                xalign 0.5
                action Return("close_workshop")
                text_size 20
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


# ==========================================
# 8 大裝備部位戰術背包介面 (inventory_screen)
# ==========================================
screen inventory_screen():

    default current_filter_tag = "全部"
    default selected_item_id = None

    $ inv = get_inventory()
    $ player = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]
    $ shards = get_fate_shards()

    # 取得 8 大裝備部位資料
    $ eq_dict = {}
    for slot_k, slot_name in EQUIPMENT_SLOTS_MAP.items():
        $ e_id = player.get(f"equipped_{slot_k}")
        $ eq_dict[slot_k] = get_item_by_id(e_id) if e_id else None

    # 過濾背包物品
    $ filtered_inv = []
    for entry in inv:
        $ itm_data = get_item_by_id(entry["id"])
        if itm_data:
            if current_filter_tag == "全部":
                $ filtered_inv.append((entry, itm_data))
            elif current_filter_tag == "武器" and itm_data.get("equip_slot") in ("main_hand", "weapon"):
                $ filtered_inv.append((entry, itm_data))
            elif current_filter_tag == "防具" and itm_data.get("equip_slot") in ("head", "torso", "hands", "feet", "off_hand"):
                $ filtered_inv.append((entry, itm_data))
            elif current_filter_tag == "飾品/載具" and itm_data.get("equip_slot") in ("necklace", "mount"):
                $ filtered_inv.append((entry, itm_data))
            elif current_filter_tag == "消耗品" and itm_data.get("type") == "consumable":
                $ filtered_inv.append((entry, itm_data))
            elif current_filter_tag == "戰術爆破" and itm_data.get("type") == "tactical":
                $ filtered_inv.append((entry, itm_data))

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

            # 頂部狀態列
            hbox:
                spacing 30
                xalign 0.5
                text "【 🎒 個人戰術背包與 8 大暗黑裝備體系 】" size 24 color "#ffcc00" bold True yalign 0.5
                text f"生存點數: {points} 點" size 18 color "#00ffcc" bold True yalign 0.5
                text f"HP: {player.get('hp',100)}/{player.get('max_hp',100)}" size 17 color "#ff6666" yalign 0.5
                text f"命運碎片: D({shards.get('D',0)}) C({shards.get('C',0)}) B({shards.get('B',0)}) A({shards.get('A',0)}) S({shards.get('S',0)})" size 15 color "#ddaaff" yalign 0.5

            # 標籤切換列
            hbox:
                spacing 10
                xalign 0.5
                text "過濾標籤：" size 15 color "#ffaa00" yalign 0.5
                for t_name in ["全部", "武器", "防具", "飾品/載具", "消耗品", "戰術爆破"]:
                    $ is_t_active = (current_filter_tag == t_name)
                    button:
                        xysize (150, 36)
                        background ("#e6a100" if is_t_active else "#222a42")
                        hover_background "#3b5288"
                        action SetScreenVariable("current_filter_tag", t_name)
                        text t_name size 14 color ("#000000" if is_t_active else "#ffffff") bold True xalign 0.5 yalign 0.5

            # 主雙欄佈局：左側物資清單，右側 8 裝備槽與選定詳情
            hbox:
                spacing 20
                xalign 0.5

                # 左側物資清單
                frame:
                    xysize (680, 780)
                    background "#161b2ebb"
                    padding (15, 12)
                    vbox:
                        spacing 8
                        text f"【 背包物資清單 · {current_filter_tag} ({len(filtered_inv)} 種) 】" size 17 color "#00ffff" bold True
                        viewport:
                            xysize (650, 720)
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            vbox:
                                spacing 6
                                if not filtered_inv:
                                    null height 50
                                    text "此分類下暫無任何物資。" size 15 color "#888888" xalign 0.5
                                else:
                                    for entry, itm in filtered_inv:
                                        $ itm_id = itm.get("id")
                                        $ itm_name = itm.get("name")
                                        $ itm_cnt = entry.get("count", 1)
                                        $ is_selected = (selected_item_id == itm_id)
                                        $ is_eq = any(e_obj and e_obj.get("id") == itm_id for e_obj in eq_dict.values())
                                        $ itm_tags_str = " · ".join(itm.get("tags", []))

                                        button:
                                            xysize (630, 75)
                                            background ("#3b5288ee" if is_selected else ("#2b4238aa" if is_eq else "#222a42aa"))
                                            hover_background "#4a68aaaa"
                                            padding (12, 8)
                                            action SetScreenVariable("selected_item_id", itm_id)
                                            hbox:
                                                spacing 10
                                                yalign 0.5
                                                vbox:
                                                    spacing 2
                                                    xysize (450, None)
                                                    hbox:
                                                        spacing 8
                                                        text "★ [itm_name]" size 15 color ("#00ffff" if is_selected else "#ffffff") bold True
                                                        if is_eq:
                                                            text "【已裝備】" size 12 color "#66ff66" bold True
                                                    text f"標籤：{itm_tags_str}" size 11 color "#aaaaaa"
                                                text f"x{itm_cnt}" size 16 color "#ffcc00" bold True yalign 0.5

                # 右側：8 大裝備部位展示 + 選定詳細面板
                vbox:
                    spacing 12
                    xysize (980, 780)

                    # 8 大裝備部位網格 (4x2 網格)
                    frame:
                        xysize (980, 310)
                        background "#161b2ebb"
                        padding (15, 12)
                        vbox:
                            spacing 6
                            text "【 主角已穿戴之 8 大部位暗黑裝備 】" size 17 color "#ffaa00" bold True
                            grid 4 2:
                                spacing 10
                                for slot_k in ["head", "torso", "hands", "feet", "necklace", "main_hand", "off_hand", "mount"]:
                                    $ slot_disp = EQUIPMENT_SLOTS_MAP[slot_k]
                                    $ cur_eq = eq_dict.get(slot_k)
                                    frame:
                                        xysize (230, 115)
                                        background "#222a42dd"
                                        padding (8, 6)
                                        vbox:
                                            spacing 2
                                            text f"◈ {slot_disp}" size 12 color "#00ffff" bold True
                                            if cur_eq:
                                                text f"{cur_eq.get('name')}" size 12 color "#ffffff" bold True
                                                if cur_eq.get("is_flight"):
                                                    text "【飛行】" size 11 color "#ddaaff"
                                                elif cur_eq.get("is_gas_immune"):
                                                    text "【防毒】" size 11 color "#66ff66"
                                                textbutton "【卸下】":
                                                    action Return(("unequip", slot_k))
                                                    text_size 11 text_idle_color "#ff4444" text_hover_color "#ff8888"
                                            else:
                                                null height 10
                                                text "無裝備" size 12 color "#666666"

                    # 選定物品詳細面板
                    frame:
                        xysize (980, 455)
                        background "#161b2ebb"
                        padding (20, 15)

                        if selected_item_id:
                            $ itm_detail = get_item_by_id(selected_item_id)
                            if itm_detail:
                                $ d_name = itm_detail.get("name", "")
                                $ d_type = itm_detail.get("type", "")
                                $ d_cat = itm_detail.get("category", "Tech")
                                $ d_slot = itm_detail.get("equip_slot")
                                $ d_desc = itm_detail.get("desc", "")
                                $ d_tags = itm_detail.get("tags", [])
                                $ d_attrs = itm_detail.get("attributes", {})
                                $ is_cur_equipped = any(e_obj and e_obj.get("id") == selected_item_id for e_obj in eq_dict.values())
                                $ d_tags_str = " · ".join(d_tags)

                                vbox:
                                    spacing 10
                                    vbox:
                                        spacing 3
                                        text "[d_name]" size 21 color "#00ffff" bold True
                                        hbox:
                                            spacing 12
                                            text f"體系：{d_cat.upper()}" size 13 color ("#00ffcc" if d_cat == "Tech" else "#ddaaff") bold True
                                            if d_slot:
                                                $ s_name_disp = EQUIPMENT_SLOTS_MAP.get(d_slot, d_slot)
                                                text f"部位：{s_name_disp}" size 13 color "#66ff66"
                                            text f"標籤：{d_tags_str}" size 13 color "#aaaaaa"

                                    text "【 性能與效果描述 】" size 15 color "#ffaa00" bold True
                                    text "[d_desc]" size 13 color "#dddddd"

                                    if d_attrs:
                                        hbox:
                                            spacing 15
                                            for ak, av in d_attrs.items():
                                                text f"★ {ak.upper()} +{av}" size 14 color "#66ff66" bold True

                                    $ d_req = itm_detail.get("req_stats", {})
                                    if d_req:
                                        $ req_list = [f"{rk} >= {rv}" for rk, rv in d_req.items()]
                                        $ req_str = " | ".join(req_list)
                                        text f"⚠️ 穿戴屬性需求門檻 (req_stats)：{req_str}" size 13 color "#ffcc00" bold True

                                    null height 10
                                    hbox:
                                        spacing 20
                                        if d_slot in EQUIPMENT_SLOTS_MAP:
                                            if is_cur_equipped:
                                                textbutton "【 ❌ 卸下此裝備 】":
                                                    action Return(("unequip", d_slot))
                                                    text_size 16 text_idle_color "#ff4444" text_hover_color "#ffffff"
                                            else:
                                                textbutton "【 ⚡ 立即穿戴至此部位 】":
                                                    action Return(("equip", selected_item_id))
                                                    text_size 16 text_idle_color "#00ff00" text_hover_color "#ffffff"

                                        if d_type == "consumable":
                                            textbutton "【 💊 立即使用補給品 】":
                                                action Return(("use_item", selected_item_id))
                                                text_size 16 text_idle_color "#66ccff" text_hover_color "#ffffff"

                                        textbutton "【 🗑️ 丟棄 1 個 】":
                                            action Return(("discard", selected_item_id))
                                            text_size 15 text_idle_color "#888888" text_hover_color "#ff4444"
                        else:
                            vbox:
                                spacing 10
                                xalign 0.5 yalign 0.5
                                text "請在左側點選任何背包物品以檢視性能並進行穿戴操作。" size 15 color "#777777"

            null height 2

            textbutton "【 🚪 關閉背包，返回廣場 】":
                xalign 0.5
                action Return("close_inventory")
                text_size 19
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


# ==========================================
# 輪迴空間軍火與裝備商城 (item_shop_screen)
# ==========================================
screen item_shop_screen():

    default shop_filter_tag = "全部"
    default selected_shop_item_id = None

    $ catalog = get_items_data()

    $ filtered_shop = []
    for itm in catalog:
        if shop_filter_tag == "全部":
            $ filtered_shop.append(itm)
        elif shop_filter_tag == "武器" and itm.get("equip_slot") in ("main_hand", "weapon"):
            $ filtered_shop.append(itm)
        elif shop_filter_tag == "防具" and itm.get("equip_slot") in ("head", "torso", "hands", "feet", "off_hand"):
            $ filtered_shop.append(itm)
        elif shop_filter_tag == "飾品/載具" and itm.get("equip_slot") in ("necklace", "mount"):
            $ filtered_shop.append(itm)
        elif shop_filter_tag == "消耗品" and itm.get("type") == "consumable":
            $ filtered_shop.append(itm)
        elif shop_filter_tag == "戰術爆破" and itm.get("type") == "tactical":
            $ filtered_shop.append(itm)

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

            hbox:
                spacing 35
                xalign 0.5
                text "【 🛒 輪迴石碑 · 軍火裝備與戰術物資商城 】" size 25 color "#ffcc00" bold True yalign 0.5
                text f"個人生存點數: {points} 點" size 22 color "#00ffcc" bold True yalign 0.5

            hbox:
                spacing 12
                xalign 0.5
                text "商城分類：" size 16 color "#ffaa00" yalign 0.5
                for t_name in ["全部", "武器", "防具", "飾品/載具", "消耗品", "戰術爆破"]:
                    $ is_st_active = (shop_filter_tag == t_name)
                    button:
                        xysize (160, 40)
                        background ("#e6a100" if is_st_active else "#222a42")
                        hover_background "#3b5288"
                        action SetScreenVariable("shop_filter_tag", t_name)
                        text t_name size 15 color ("#000000" if is_st_active else "#ffffff") bold True xalign 0.5 yalign 0.5

            hbox:
                spacing 25
                xalign 0.5

                # 左側商品清單
                frame:
                    xysize (780, 750)
                    background "#161b2ebb"
                    padding (20, 15)
                    viewport:
                        xysize (740, 715)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            spacing 8
                            for itm in filtered_shop:
                                $ itm_id = itm.get("id")
                                $ itm_name = itm.get("name")
                                $ itm_cost = itm.get("cost_points", 0)
                                $ itm_shard = itm.get("cost_fate_shard")
                                $ is_sel = (selected_shop_item_id == itm_id)
                                $ itm_tags_str = " · ".join(itm.get("tags", []))

                                button:
                                    xysize (720, 85)
                                    background ("#3b5288ee" if is_sel else "#222a42aa")
                                    hover_background "#4a68aaaa"
                                    padding (15, 10)
                                    action SetScreenVariable("selected_shop_item_id", itm_id)
                                    hbox:
                                        spacing 15
                                        yalign 0.5
                                        vbox:
                                            spacing 3
                                            xysize (480, None)
                                            text "★ [itm_name]" size 16 color ("#00ffff" if is_sel else "#ffffff") bold True
                                            text f"標籤：{itm_tags_str}" size 12 color "#aaaaaa"
                                        vbox:
                                            spacing 2
                                            text f"{itm_cost} 點" size 16 color "#ffcc00" bold True
                                            if itm_shard:
                                                text f"+ {itm_shard}階碎片" size 12 color "#ddaaff"

                # 右側商品詳情與兌換
                frame:
                    xysize (850, 750)
                    background "#161b2ebb"
                    padding (25, 20)

                    if selected_shop_item_id:
                        $ shop_detail = get_item_by_id(selected_shop_item_id)
                        if shop_detail:
                            $ s_name = shop_detail.get("name", "")
                            $ s_cost = shop_detail.get("cost_points", 0)
                            $ s_shard = shop_detail.get("cost_fate_shard")
                            $ s_desc = shop_detail.get("desc", "")
                            $ s_tags = shop_detail.get("tags", [])
                            $ s_attrs = shop_detail.get("attributes", {})
                            $ can_buy_pts = (points >= s_cost)
                            $ can_buy_shard = (not s_shard) or has_fate_shard(s_shard, 1)
                            $ can_buy = can_buy_pts and can_buy_shard
                            $ s_tags_str = " · ".join(s_tags)

                            vbox:
                                spacing 15
                                vbox:
                                    spacing 4
                                    text "[s_name]" size 23 color "#00ffff" bold True
                                    text f"標籤：{s_tags_str}" size 14 color "#aaaaaa"

                                vbox:
                                    spacing 6
                                    text f"【 兌換費用 】{s_cost} 生存點數" size 18 color ("#66ff66" if can_buy_pts else "#ff4444") bold True
                                    if s_shard:
                                        text f"【 命運碎片需求 】{s_shard} 階命運碎片 x 1" size 15 color ("#ddaaff" if can_buy_shard else "#ff4444") bold True

                                text "【 物品性能說明 】" size 16 color "#ffaa00" bold True
                                text "[s_desc]" size 14 color "#dddddd"

                                if s_attrs:
                                    text "【 屬性增益 】" size 16 color "#66ff66" bold True
                                    hbox:
                                        spacing 20
                                        for ak, av in s_attrs.items():
                                            text f"★ {ak.upper()} +{av}" size 14 color "#ffffff"

                                $ s_req = shop_detail.get("req_stats", {})
                                if s_req:
                                    $ req_list = [f"{rk} >= {rv}" for rk, rv in s_req.items()]
                                    $ req_str = " | ".join(req_list)
                                    text f"⚠️ 穿戴屬性門檻 (req_stats)：{req_str}" size 14 color "#ffcc00" bold True

                                null height 20
                                if can_buy:
                                    textbutton f"【 ⚡ 立即扣除點數與碎片兌換【{s_name}】 】":
                                        action Return(("buy_item", selected_shop_item_id))
                                        text_size 19 text_idle_color "#00ff00" text_hover_color "#ffffff"
                                else:
                                    textbutton "【 ❌ 資源不足 (點數或命運碎片不足) 】":
                                        action NullAction()
                                        text_size 18 text_idle_color "#884444"
                    else:
                        vbox:
                            spacing 15
                            xalign 0.5 yalign 0.5
                            text "請在左側點選任意商品以檢視性能並兌換。" size 16 color "#777777"

            null height 5

            textbutton "【 🚪 關閉商城，返回輪迴廣場 】":
                xalign 0.5
                action Return("leave_shop")
                text_size 20
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"

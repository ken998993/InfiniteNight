# ==========================================
# 個人房間高科技工坊與收藏室系統 (personal_room_system.rpy)
# ==========================================

init python:
    if 'hive_ai_installed' not in globals():
        hive_ai_installed = False

    # 1. 取得素材庫存數量
    def get_material_count(mat_id):
        inv = get_inventory() if 'get_inventory' in globals() else []
        for entry in inv:
            if entry["id"] == mat_id:
                return entry.get("count", 0)
        return 0

    # 2. 合成基因鎖解鎖藥劑 (需要 100 瓶喪屍血液)
    def craft_gene_lock_elixir():
        blood_cnt = get_material_count("MAT_ZOMBIE_BLOOD")
        if blood_cnt < 100:
            return {"success": False, "msg": f"【工坊提示】喪屍血液不足！目前僅有 {blood_cnt}/100 瓶。"}
            
        remove_item("MAT_ZOMBIE_BLOOD", 100)
        add_item("ITEM_GENE_LOCK_ELIXIR", 1)
        return {"success": True, "msg": "✨【基因鎖藥劑提純成功】消耗 100 瓶喪屍血液，成功提純凝聚出【基因鎖解鎖藥劑 x1】！"}

    # 3. 使用基因鎖解鎖藥劑 (無視條件晉升 1 階基因鎖)
    def use_gene_lock_elixir(member_idx=0):
        global gene_lock, team_roster, hp
        if not has_item("ITEM_GENE_LOCK_ELIXIR", 1):
            return {"success": False, "msg": "背包中無基因鎖解鎖藥劑。"}
            
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "無效目標隊員。"}
            
        member = roster[member_idx]
        cur_lock = member.get("gene_lock", 0)
        if cur_lock >= 5:
            return {"success": False, "msg": "【輪迴提示】基因鎖已達第 5 階（聖人初階），無法繼續以藥劑晉升！"}
            
        remove_item("ITEM_GENE_LOCK_ELIXIR", 1)
        member["gene_lock"] = cur_lock + 1
        new_lock = member["gene_lock"]
        
        # 突破屬性暴漲
        member["max_hp"] = member.get("max_hp", 100) + 150
        member["hp"] = member["max_hp"]
        member["max_mp"] = member.get("max_mp", 50) + 50
        member["mp"] = member["max_mp"]
        member["atk_bonus"] = member.get("atk_bonus", 0) + 25
        
        if member_idx == 0:
            gene_lock = new_lock
            hp = member["hp"]
            
        return {
            "success": True,
            "msg": f"🧬【基因鎖極限突破】狂暴的生化源能衝開遠古基因枷鎖！\n【{member.get('name')}】成功開啟【基因鎖第 {new_lock} 階】！\n生命上限 +150，攻擊力加成 +25，精神力上限 +50，全員全滿狀態！"
        }

    # 4. 安裝蜂巢中央主控 AI 備份
    def install_hive_ai():
        global hive_ai_installed
        if not has_item("ITEM_HIVE_AI_BACKUP", 1):
            return {"success": False, "msg": "背包中未持有【蜂巢基地主控 AI 備份】！請於喪屍副本智鬥中駭入獲取。"}
            
        remove_item("ITEM_HIVE_AI_BACKUP", 1)
        hive_ai_installed = True
        return {"success": True, "msg": "🤖【超級電腦安裝完成】蜂巢基地主控 AI 已與個人房間工作台成功同步！【高科技裝備生成終端】已正式解鎖！"}

    # 5. 高科技裝備打印合成
    def craft_tech_equipment(recipe_id):
        global hive_ai_installed, points, team_roster
        if not hive_ai_installed:
            return {"success": False, "msg": "請先安裝蜂巢主控 AI 備份以解鎖生成終端！"}
            
        # 配方規格
        recipes = {
            "EQ_TECH_PLASMA_RIFLE": {
                "name": "蜂巢電漿脈衝突擊步槍",
                "blood_cost": 50,
                "parts_cost": 10,
                "shard_tier": "B",
                "shard_cost": 1
            },
            "EQ_TECH_PARTICLE_BLADE": {
                "name": "高頻震盪電磁粒子刀",
                "blood_cost": 60,
                "parts_cost": 15,
                "shard_tier": "B",
                "shard_cost": 1
            },
            "EQ_TECH_PULSE_SHIELD": {
                "name": "蜂巢脈衝能量護盾核心",
                "blood_cost": 40,
                "parts_cost": 12,
                "shard_tier": "C",
                "shard_cost": 1
            }
        }
        
        if recipe_id not in recipes:
            return {"success": False, "msg": "無效的科技配方。"}
            
        rec = recipes[recipe_id]
        b_cnt = get_material_count("MAT_ZOMBIE_BLOOD")
        p_cnt = get_material_count("MAT_TECH_PARTS")
        s_tier = rec["shard_tier"]
        
        if b_cnt < rec["blood_cost"]:
            return {"success": False, "msg": f"【素材不足】喪屍血液不足 ({b_cnt}/{rec['blood_cost']})！"}
        if p_cnt < rec["parts_cost"]:
            return {"success": False, "msg": f"【素材不足】科技零件不足 ({p_cnt}/{rec['parts_cost']})！"}
        if 'has_fate_shard' in globals() and not has_fate_shard(s_tier, rec["shard_cost"]):
            return {"success": False, "msg": f"【碎片不足】缺少【{s_tier} 階命運碎片 x{rec['shard_cost']}】！"}
            
        # 扣減素材
        remove_item("MAT_ZOMBIE_BLOOD", rec["blood_cost"])
        remove_item("MAT_TECH_PARTS", rec["parts_cost"])
        if 'remove_fate_shard' in globals():
            remove_fate_shard(s_tier, rec["shard_cost"])
            
        add_item(recipe_id, 1)
        return {"success": True, "msg": f"⚡【高科技打印完成】蜂巢 AI 自動完成微觀分子重構，成功生成【{rec['name']} x1】！"}


# ==========================================
# 個人房間高科技工坊畫面 (personal_room_screen)
# ==========================================
screen personal_room_screen():

    $ player = team_roster[0] if ('team_roster' in globals() and team_roster) else get_team_roster()[0]
    $ blood_cnt = get_material_count("MAT_ZOMBIE_BLOOD")
    $ parts_cnt = get_material_count("MAT_TECH_PARTS")
    $ gene_cnt = get_material_count("MAT_HIGH_MUTANT_GENE")
    $ elixir_cnt = get_material_count("ITEM_GENE_LOCK_ELIXIR")
    $ has_ai_item = has_item("ITEM_HIVE_AI_BACKUP", 1) if 'has_item' in globals() else False
    $ shards = get_fate_shards() if 'get_fate_shards' in globals() else {}
    $ p_lock = player.get("gene_lock", 0)

    window:
        background "#000000dd"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1720, 960)
        padding (30, 25)
        background "#0d121ff5"

        vbox:
            spacing 12
            xalign 0.5

            # 頂部狀態列
            hbox:
                spacing 35
                xalign 0.5
                text "【 🏠 個人安全屋 · 高科技合成工坊與素材收藏室 】" size 25 color "#ffcc00" bold True yalign 0.5
                text f"當前基因鎖：第 {p_lock} 階" size 18 color "#00ffff" bold True yalign 0.5
                text f"生存點數: {points} 點" size 18 color "#66ff66" bold True yalign 0.5
                text f"命運碎片: D({shards.get('D',0)}) C({shards.get('C',0)}) B({shards.get('B',0)}) A({shards.get('A',0)}) S({shards.get('S',0)})" size 15 color "#ddaaff" yalign 0.5

            null height 5

            # 主雙欄：左側素材與基因鎖藥劑，右側蜂巢 AI 高科技裝備打印
            hbox:
                spacing 25
                xalign 0.5

                # -----------------------------------
                # 左側：素材庫存與基因鎖藥劑提純
                # -----------------------------------
                frame:
                    xysize (820, 780)
                    background "#161b2ebb"
                    padding (20, 18)
                    vbox:
                        spacing 15
                        text "【 🧪 怪物素材收藏與基因鎖藥劑工坊 】" size 20 color "#00ffcc" bold True
                        text "在各恐怖片副本中消滅怪物掠奪的珍稀素材將自動保存在此。" size 13 color "#aaaaaa"

                        null height 5

                        # 素材庫存清單
                        frame:
                            xysize (780, 240)
                            background "#101626aa"
                            padding (15, 12)
                            vbox:
                                spacing 10
                                text "【 當前素材庫存 】" size 16 color "#ffaa00" bold True
                                hbox:
                                    spacing 20
                                    text f"🩸 喪屍血液：{blood_cnt} 瓶" size 16 color ("#66ff66" if blood_cnt >= 100 else "#ffffff") bold True
                                    text f"⚙️ 科技零件：{parts_cnt} 個" size 16 color "#00ffff" bold True
                                hbox:
                                    spacing 20
                                    text f"🧬 變異基因片段：{gene_cnt} 份" size 16 color "#ddaaff" bold True
                                    text f"🧪 基因鎖藥劑：{elixir_cnt} 劑" size 16 color ("#ffff00" if elixir_cnt > 0 else "#888888") bold True

                        null height 10

                        # 基因鎖藥劑提純區域
                        frame:
                            xysize (780, 380)
                            background "#101626aa"
                            padding (15, 15)
                            vbox:
                                spacing 12
                                text "【 🧬 基因鎖解鎖藥劑 (Gene Lock Elixir) 提純 】" size 18 color "#ffff00" bold True
                                text "• 提純公式：消耗【喪屍血液 x 100 瓶】➜ 提純 1 劑【基因鎖解鎖藥劑】。" size 14 color "#cccccc"
                                text "• 奇蹟效果：使用後無視任何死亡/瀕死檢定，強制解鎖/晉升 1 階基因鎖！" size 14 color "#66ff66"

                                null height 10
                                hbox:
                                    spacing 15
                                    text f"血液進度：{blood_cnt}/100 瓶" size 16 color ("#66ff66" if blood_cnt >= 100 else "#ff6666") bold True yalign 0.5
                                    button:
                                        xysize (360, 48)
                                        background ("#245e33" if blood_cnt >= 100 else "#333333")
                                        hover_background "#358a4b"
                                        action Return("craft_elixir")
                                        text "🧪 提純合成藥劑 (100血)" size 15 color "#ffffff" bold True xalign 0.5 yalign 0.5

                                null height 10
                                if elixir_cnt > 0:
                                    button:
                                        xysize (740, 55)
                                        background "#5e4b1b"
                                        hover_background "#8a6d27"
                                        action Return("use_elixir")
                                        text "⚡ 立即注射【基因鎖解鎖藥劑】(強制突破+1階) ⚡" size 17 color "#ffff00" bold True xalign 0.5 yalign 0.5
                                else:
                                    frame:
                                        xysize (740, 55)
                                        background "#222222"
                                        text "暫無基因鎖藥劑可用 (請在上方提純合成)" size 14 color "#777777" xalign 0.5 yalign 0.5

                # -----------------------------------
                # 右側：蜂巢中央主控 AI 裝備打印終端
                # -----------------------------------
                frame:
                    xysize (820, 780)
                    background "#161b2ebb"
                    padding (20, 18)
                    vbox:
                        spacing 15
                        text "【 🤖 蜂巢基地主控 AI · 高科技裝備生成終端 】" size 20 color "#00ffcc" bold True

                        if not hive_ai_installed:
                            vbox:
                                spacing 15
                                null height 40
                                text "⚠️ 蜂巢中央超級電腦 AI 終端尚未安裝" size 18 color "#ff6666" bold True xalign 0.5
                                text "在【第一副本·喪屍末日蜂巢基地】中，隊伍派遣智力 >= 100 的智者\n可自機房節點駭入下載【蜂巢基地主控 AI 備份】。" size 15 color "#bbbbbb" xalign 0.5
                                null height 20
                                if has_ai_item:
                                    button:
                                        xysize (650, 60)
                                        background "#1b5e43"
                                        hover_background "#278a63"
                                        action Return("install_ai")
                                        text "🔌 立即安裝【蜂巢基地主控 AI 備份】至房間" size 17 color "#00ffcc" bold True xalign 0.5 yalign 0.5
                                else:
                                    text "（目前背包中尚未持有 AI 備份硬碟）" size 14 color "#777777" xalign 0.5
                        else:
                            vbox:
                                spacing 12
                                text "🟢 蜂巢超級電腦主控 AI 運作中（紅后藍圖資料庫已同步）" size 15 color "#66ff66" bold True

                                # 配方 1：電漿步槍
                                frame:
                                    xysize (780, 155)
                                    background "#101626aa"
                                    padding (12, 10)
                                    vbox:
                                        spacing 4
                                        text "★ 蜂巢電漿脈衝突擊步槍 (主手武器 / 科技類)" size 16 color "#00ffff" bold True
                                        text "屬性：攻擊力 +75，生命上限 +50，無視 30% 防禦" size 12 color "#aaaaaa"
                                        text f"需求素材：喪屍血液 50瓶 ({blood_cnt}/50) | 科技零件 10個 ({parts_cnt}/10) | B階碎片 x1" size 12 color "#ffcc00"
                                        button:
                                            xysize (280, 36)
                                            background ("#245e33" if (blood_cnt>=50 and parts_cnt>=10 and shards.get('B',0)>=1) else "#333333")
                                            hover_background "#358a4b"
                                            action Return(("craft_tech", "EQ_TECH_PLASMA_RIFLE"))
                                            text "⚡ 打印電漿步槍" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5

                                # 配方 2：高頻粒子刀
                                frame:
                                    xysize (780, 155)
                                    background "#101626aa"
                                    padding (12, 10)
                                    vbox:
                                        spacing 4
                                        text "★ 高頻震盪電磁粒子刀 (主手武器 / 科技類)" size 16 color "#00ffff" bold True
                                        text "屬性：攻擊力 +85，生命上限 +40，暴擊率大幅提升" size 12 color "#aaaaaa"
                                        text f"需求素材：喪屍血液 60瓶 ({blood_cnt}/60) | 科技零件 15個 ({parts_cnt}/15) | B階碎片 x1" size 12 color "#ffcc00"
                                        button:
                                            xysize (280, 36)
                                            background ("#245e33" if (blood_cnt>=60 and parts_cnt>=15 and shards.get('B',0)>=1) else "#333333")
                                            hover_background "#358a4b"
                                            action Return(("craft_tech", "EQ_TECH_PARTICLE_BLADE"))
                                            text "⚡ 打印粒子戰刀" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5

                                # 配方 3：脈衝能量護盾
                                frame:
                                    xysize (780, 155)
                                    background "#101626aa"
                                    padding (12, 10)
                                    vbox:
                                        spacing 4
                                        text "★ 蜂巢脈衝能量護盾核心 (副手防具 / 科技類)" size 16 color "#00ffff" bold True
                                        text "屬性：生命上限 +120，防禦力大幅提升，偏折遠程衝擊" size 12 color "#aaaaaa"
                                        text f"需求素材：喪屍血液 40瓶 ({blood_cnt}/40) | 科技零件 12個 ({parts_cnt}/12) | C階碎片 x1" size 12 color "#ffcc00"
                                        button:
                                            xysize (280, 36)
                                            background ("#245e33" if (blood_cnt>=40 and parts_cnt>=12 and shards.get('C',0)>=1) else "#333333")
                                            hover_background "#358a4b"
                                            action Return(("craft_tech", "EQ_TECH_PULSE_SHIELD"))
                                            text "⚡ 打印能量護盾" size 13 color "#ffffff" bold True xalign 0.5 yalign 0.5

            null height 2

            textbutton "【 🚪 離開個人房間，返回輪迴廣場 】":
                xalign 0.5
                action Return("leave_room")
                text_size 20
                text_idle_color "#ff6666"
                text_hover_color "#ff9999"


init python:
    # ==========================================
    # 戰鬥系統核心邏輯與招式/道具/回合制邏輯庫
    # ==========================================
    import random

    def get_actor_skills(actor):
        if not actor:
            return []
            
        # 優先讀取角色已裝備或已習得的血統技能庫
        if actor.get('skills') and len(actor.get('skills')) > 0:
            return actor.get('skills')
            
        name = actor.get('name', '')
        bloodline = actor.get('bloodline', '')
        
        skills = []
        if "吸血鬼" in bloodline or "主角" in name:
            skills.append({
                "name": "血能衝擊",
                "desc": "消耗 15 點血族能量，造成 75 點暗紅衝擊傷害並吸取 25 點 HP。",
                "damage": 75,
                "cost_energy": 15,
                "energy_cost": 15,
                "energy_type": "blood_current",
                "heal": 25
            })
            skills.append({
                "name": "基因鎖·極限爆發",
                "desc": "突破人體極限，釋放潛能造成 110 點毀滅性打擊。",
                "damage": 110,
                "cost_energy": 25,
                "energy_cost": 25,
                "energy_type": "mp",
                "heal": 0
            })
        elif "張傑" in name:
            skills.append({
                "name": "念動力震懾彈",
                "desc": "以強悍的引導者精神念力引爆空氣，造成 85 點念力衝擊傷害。",
                "damage": 85,
                "cost_energy": 20,
                "energy_cost": 20,
                "energy_type": "mp",
                "heal": 0
            })
            skills.append({
                "name": "雙槍精準速射",
                "desc": "資深老兵的雙槍點射，造成 65 點物理穿透傷害。",
                "damage": 65,
                "cost_energy": 10,
                "energy_cost": 10,
                "energy_type": "mp",
                "heal": 0
            })
        elif "鄭吒" in name:
            skills.append({
                "name": "氣血狂暴重拳",
                "desc": "將體內澎湃氣血凝聚於拳鋒，造成 95 點爆發傷害。",
                "damage": 95,
                "cost_energy": 20,
                "energy_cost": 20,
                "energy_type": "qi_current",
                "heal": 0
            })
        elif "詹嵐" in name:
            skills.append({
                "name": "心靈防護屏障",
                "desc": "精神力特化，為自身回復 50 點 HP 並平復精神。",
                "damage": 0,
                "cost_energy": 20,
                "energy_cost": 20,
                "energy_type": "mental_current",
                "heal": 50,
                "is_heal": True
            })
        elif "楚軒" in name:
            skills.append({
                "name": "幾何弱點狙擊",
                "desc": "以絕對邏輯計算敵方致命弱點，造成 120 點高斯穿甲真實傷害。",
                "damage": 120,
                "cost_energy": 20,
                "energy_cost": 20,
                "energy_type": "calc_current",
                "heal": 0
            })
        elif "霸王" in name:
            skills.append({
                "name": "微型火箭彈覆蓋",
                "desc": "傾瀉傭兵重火力，對目標造成 100 點範圍爆炸傷害。",
                "damage": 100,
                "cost_energy": 20,
                "energy_cost": 20,
                "energy_type": "mp",
                "heal": 0
            })
        else:
            skills.append({
                "name": "全力爆發打擊",
                "desc": "凝聚全身力量的強烈攻擊，造成 70 點傷害。",
                "damage": 70,
                "cost_energy": 15,
                "energy_cost": 15,
                "energy_type": "mp",
                "heal": 0
            })
            
        return skills

    def check_battle_victory(battle_state):
        enemies = battle_state.get('enemies', [])
        all_dead = all(e.get('hp', 0) <= 0 for e in enemies)
        if all_dead:
            if 'logs' in battle_state:
                battle_state['logs'].append("🎉【戰鬥勝利】所有 6 隻敵方喪屍已被全數殲滅！")
            renpy.end_interaction("win")
            return True
        return False

    def process_enemy_phase(battle_state):
        enemies = [e for e in battle_state.get('enemies', []) if e.get('hp', 0) > 0]
        players = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0]
        
        round_num = battle_state.get('round_number', 1)
        if 'logs' in battle_state:
            battle_state['logs'].append(f"⚠️ --- 我方全員行動完畢！進入第 {round_num} 回合【敵方反擊階段】---")
        
        if not players:
            if 'logs' in battle_state:
                battle_state['logs'].append("💀 我方小隊全員倒下！戰鬥失敗！")
            return

        for enemy in enemies:
            alive_players = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0]
            if not alive_players:
                break
            target = random.choice(alive_players)
            raw_atk = enemy.get('atk', 18)
            
            # 若處於防禦狀態則減傷 50%
            is_defending = "防禦" in target.get('status', '')
            dmg = max(5, int(raw_atk * 0.5)) if is_defending else raw_atk
            target['hp'] = max(0, target.get('hp', 0) - dmg)
            
            e_name = enemy.get('name', '喪屍')
            t_name = target.get('name', '隊員')
            if is_defending:
                battle_state['logs'].append(f"🧟 {e_name} 猛撲 {t_name}！{t_name} 舉盾防禦，受到 {dmg} 點減免傷害！")
            else:
                battle_state['logs'].append(f"🧟 {e_name} 撕咬了 {t_name}，造成了 {dmg} 點傷害！")
                
            if target.get('hp', 0) <= 0:
                target['status'] = '重傷倒地'
                battle_state['logs'].append(f"⚠️ 隊員【{t_name}】受到致命重創倒下！")
                
        # 檢查是否全滅
        remaining_players = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0]
        if not remaining_players:
            if 'logs' in battle_state:
                battle_state['logs'].append("💀 我方小隊全體陣亡！")
            return
            
        # 結算完畢進入下一回合
        battle_state['round_number'] = round_num + 1
        new_round = battle_state['round_number']
        
        for m in battle_state.get('player_team', []):
            m['has_acted'] = False
            if "防禦" in m.get('status', ''):
                m['status'] = '良好'
                
        battle_state['is_player_turn'] = True
        battle_state['current_turn_name'] = f"第 {new_round} 回合 · 我方行動階段"
        if 'logs' in battle_state:
            battle_state['logs'].append(f"🔔 === 第 {new_round} 回合開始！我方全體已重置行動機會 ===")

    def end_actor_turn(battle_state, actor):
        if actor:
            actor['has_acted'] = True
            
        battle_state['selected_actor'] = None
        battle_state['target_mode'] = None
        battle_state['selected_skill'] = None
        
        # 檢查是否勝利
        if check_battle_victory(battle_state):
            return
            
        # 檢查我方是否所有存活隊員都已行動
        alive_players = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0]
        if alive_players and all(m.get('has_acted', False) for m in alive_players):
            process_enemy_phase(battle_state)
            
        renpy.restart_interaction()

    def process_player_attack(battle_state, actor, target):
        if not actor or not target:
            return
        damage = 35
        target['hp'] = max(0, target['hp'] - damage)
        actor_name = actor.get('name', '隊員')
        target_name = target.get('name', '敵人')
        log_msg = f"⚔️ {actor_name} 發動【普通攻擊】，對 {target_name} 造成了 {damage} 點傷害！"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if target.get('hp', 0) <= 0:
            target['status'] = '已擊殺'
            if 'logs' in battle_state:
                battle_state['logs'].append(f"💥 敵方目標【{target_name}】已被成功擊殺！")
                
        end_actor_turn(battle_state, actor)

    def process_player_skill(battle_state, actor, target, skill):
        if not actor or not skill:
            return
        actor_name = actor.get('name', '隊員')
        skill_name = skill.get('name', '招式')
        damage = skill.get('damage', 0)
        heal = skill.get('heal', 0)
        energy_type = skill.get('energy_type', 'mp')
        cost = skill.get('energy_cost', skill.get('cost_energy', 0))
        
        # 兼容能量屬性別名映射
        energy_map = {
            "blood_energy": "blood_current",
            "blood_current": "blood_current",
            "neili_energy": "neili_current",
            "neili_current": "neili_current",
            "qi_energy": "qi_current",
            "qi_current": "qi_current",
            "mental_energy": "mental_current",
            "mental_current": "mental_current",
            "calc_energy": "calc_current",
            "calc_current": "calc_current",
            "mp": "mp"
        }
        resolved_energy = energy_map.get(energy_type, energy_type)
        
        # 扣減對應能量 (若專屬能量不足或無該池則自 mp 扣除)
        if resolved_energy in actor and actor[resolved_energy] >= cost:
            actor[resolved_energy] = max(0, actor[resolved_energy] - cost)
        elif 'mp' in actor and actor['mp'] >= cost:
            actor['mp'] = max(0, actor['mp'] - cost)
        elif resolved_energy in actor:
            actor[resolved_energy] = max(0, actor[resolved_energy] - cost)
            
        if skill.get('is_heal', False) or (heal > 0 and damage == 0):
            actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + heal)
            log_msg = f"✨ {actor_name} 施展了【{skill_name}】，回復了自身 {heal} 點生命值！"
        else:
            if target:
                target['hp'] = max(0, target['hp'] - damage)
                target_name = target.get('name', '敵人')
                log_msg = f"🔥 {actor_name} 施展了【{skill_name}】，對 {target_name} 造成了 {damage} 點毀滅傷害！"
                if heal > 0:
                    actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + heal)
                    log_msg += f" (同時吸取並恢復了 {heal} 點 HP)"
                if target.get('hp', 0) <= 0:
                    target['status'] = '已擊殺'
                    if 'logs' in battle_state:
                        battle_state['logs'].append(f"💥 敵方目標【{target_name}】已被技能徹底摧毀！")
            else:
                log_msg = f"🔥 {actor_name} 施展了【{skill_name}】！"
                
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        end_actor_turn(battle_state, actor)

    def process_player_defend(battle_state, actor):
        if not actor:
            return
        actor_name = actor.get('name', '隊員')
        heal_hp = 25
        heal_mp = 15
        actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + heal_hp)
        actor['mp'] = min(actor.get('max_mp', 50), actor.get('mp', 50) + heal_mp)
        actor['status'] = '防禦中 (減傷50%)'
        log_msg = f"🛡️ {actor_name} 採取了【防禦姿態】，凝神戒備並回復了 {heal_hp} 點 HP 與 {heal_mp} 點精力！"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        end_actor_turn(battle_state, actor)

    def process_use_item(battle_state, actor, item_type):
        if not actor:
            return
        actor_name = actor.get('name', '隊員')
        if item_type == 'heal_spray':
            actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + 60)
            log_msg = f"💊 {actor_name} 使用了【主神止血急救噴霧】，傷口迅速癒合，恢復了 60 點 HP！"
        elif item_type == 'mp_potion':
            actor['mp'] = min(actor.get('max_mp', 50), actor.get('mp', 50) + 40)
            if 'mental_current' in actor and 'mental_max' in actor:
                actor['mental_current'] = min(actor['mental_max'], actor['mental_current'] + 30)
            log_msg = f"💉 {actor_name} 使用了【強效精神穩定劑】，精神力煥發，恢復了 40 點 MP！"
        elif item_type == 'grenade':
            enemies = battle_state.get('enemies', [])
            damage = 85
            for e in enemies:
                if e.get('hp', 0) > 0:
                    e['hp'] = max(0, e.get('hp', 0) - damage)
                    if e['hp'] <= 0:
                        e['status'] = '已擊殺'
            log_msg = f"💣 {actor_name} 投擲了【高爆破片手榴彈】，轟然巨響！對全體敵方造成了 {damage} 點爆炸傷害！"
        else:
            log_msg = f"🎒 {actor_name} 使用了背包道具。"
            
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        end_actor_turn(battle_state, actor)

    def process_team_all_attack(battle_state):
        if not battle_state.get('is_player_turn', True):
            return
            
        unacted = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0 and not m.get('has_acted', False)]
        if not unacted:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 當前回合所有存活隊員均已行動過！")
            renpy.restart_interaction()
            return
            
        if 'logs' in battle_state:
            battle_state['logs'].append("⚔️ === 我方發動【全體普通攻擊】戰術突擊！ ===")
            
        for member in unacted:
            alive_enemies = [e for e in battle_state.get('enemies', []) if e.get('hp', 0) > 0]
            if not alive_enemies:
                break
                
            target = alive_enemies[0]
            m_name = member.get('name', '隊員')
            e_name = target.get('name', '喪屍')
            damage = 35
            target['hp'] = max(0, target['hp'] - damage)
            member['has_acted'] = True
            
            if 'logs' in battle_state:
                battle_state['logs'].append(f"⚔️ {m_name} 攻擊了 {e_name}，造成了 {damage} 點傷害！")
                
            if target['hp'] <= 0:
                target['status'] = '已擊殺'
                if 'logs' in battle_state:
                    battle_state['logs'].append(f"💥 敵方目標【{e_name}】已被擊斃！")
                    
        battle_state['selected_actor'] = None
        battle_state['target_mode'] = None
        battle_state['selected_skill'] = None
        
        if check_battle_victory(battle_state):
            return
            
        alive_players = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0]
        if alive_players and all(m.get('has_acted', False) for m in alive_players):
            process_enemy_phase(battle_state)
            
        renpy.restart_interaction()

    def process_team_all_defend(battle_state):
        if not battle_state.get('is_player_turn', True):
            return
            
        unacted = [m for m in battle_state.get('player_team', []) if m.get('hp', 0) > 0 and not m.get('has_acted', False)]
        if not unacted:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 當前回合所有存活隊員均已行動過！")
            renpy.restart_interaction()
            return
            
        if 'logs' in battle_state:
            battle_state['logs'].append("🛡️ === 我方全體採取【全體防禦姿態】！全體進入 50% 減傷戒備並恢復精力 ===")
            
        for member in unacted:
            heal_hp = 25
            heal_mp = 15
            member['hp'] = min(member.get('max_hp', 100), member.get('hp', 100) + heal_hp)
            member['mp'] = min(member.get('max_mp', 50), member.get('mp', 50) + heal_mp)
            member['status'] = '防禦中 (減傷50%)'
            member['has_acted'] = True
            
        battle_state['selected_actor'] = None
        battle_state['target_mode'] = None
        battle_state['selected_skill'] = None
        
        # 全員防禦完畢，直接進入敵方反擊階段
        process_enemy_phase(battle_state)
        renpy.restart_interaction()

    def process_manual_end_turn(battle_state):
        if 'logs' in battle_state:
            battle_state['logs'].append("⏩ 手動結束我方階段，直接進入敵方反擊回合！")
        process_enemy_phase(battle_state)
        renpy.restart_interaction()

    def ensure_six_enemies(battle_state):
        if len(battle_state.get('enemies', [])) < 6:
            battle_state['enemies'] = [
                {"name": "狂暴喪屍 A", "hp": 120, "max_hp": 120, "atk": 15, "status": "嗜血"},
                {"name": "狂暴喪屍 B", "hp": 120, "max_hp": 120, "atk": 15, "status": "嗜血"},
                {"name": "迅捷爬行者", "hp": 90, "max_hp": 90, "atk": 20, "status": "敏捷"},
                {"name": "巨型重甲喪屍", "hp": 220, "max_hp": 220, "atk": 30, "status": "堅韌"},
                {"name": "劇毒酸液喪屍", "hp": 110, "max_hp": 110, "atk": 18, "status": "劇毒"},
                {"name": "變異喪屍統領", "hp": 260, "max_hp": 260, "atk": 35, "status": "統領"}
            ]

    def process_instant_win(battle_state):
        enemies = battle_state.get('enemies', [])
        for e in enemies:
            e['hp'] = 0
            e['status'] = '已擊殺'
        if 'logs' in battle_state:
            battle_state['logs'].append("⚡【主神管理員指令】觸發強制抹殺！直接取得戰鬥勝利！")
        renpy.end_interaction("win")


# ==========================================
# 戰鬥畫面介面 (battle_screen) - 回合制 6vs6 升級版
# ==========================================
screen battle_screen(battle_state):

    # 確保敵方擁有 6 隻喪屍（防止熱重載或讀取舊暫存時未更新敵方資料）
    $ ensure_six_enemies(battle_state)

    # 取得當前戰鬥核心資料
    $ round_num = battle_state.get('round_number', 1)
    $ player_team = battle_state.get('player_team', [])
    $ enemies = battle_state.get('enemies', [])
    $ battle_logs = battle_state.get('logs', [])
    $ current_turn_name = battle_state.get('current_turn_name', '我方行動階段')
    $ is_player_turn = battle_state.get('is_player_turn', True)
    $ selected_actor = battle_state.get('selected_actor', None)
    $ target_mode = battle_state.get('target_mode', None)
    $ selected_skill = battle_state.get('selected_skill', None)

    # 計算我方存活與待命人數
    $ alive_members = [m for m in player_team if m.get('hp', 0) > 0]
    $ unacted_members = [m for m in alive_members if not m.get('has_acted', False)]
    $ alive_enemies = [e for e in enemies if e.get('hp', 0) > 0]

    window:
        background "#000000ee"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1840, 1030)
        padding (25, 15)
        background "#111122f5"

        vbox:
            spacing 8
            xalign 0.5

            # 頂部標題與回合資訊列
            hbox:
                xalign 0.5
                spacing 35
                text "【 主神空間 · 6vs6 回合制副本戰鬥系統 】" size 25 color "#ffcc00" yalign 0.5
                text "【 第 [round_num] 回合 】" size 22 color "#00ffff" bold True yalign 0.5
                text "[current_turn_name]" size 20 color ("#66ff66" if is_player_turn else "#ff6666") yalign 0.5
                text "我方待命：[len(unacted_members)]/[len(alive_members)]" size 18 color "#ffffaa" yalign 0.5
                text "敵方存活：[len(alive_enemies)]/6" size 18 color "#ff9999" yalign 0.5

            # 指令提示文字
            if selected_actor:
                $ actor_disp_name = selected_actor.get('name', '')
                if target_mode == 'attack':
                    text "【已選定：[actor_disp_name]】請在右側點擊鎖定敵方目標進行普通攻擊" size 17 color "#00ff00" xalign 0.5
                elif target_mode == 'cast_skill' and selected_skill:
                    $ sk_disp_name = selected_skill.get('name', '')
                    text "【已選定：[actor_disp_name]】請在右側點擊目標釋放招式：[sk_disp_name]" size 17 color "#ffaa00" xalign 0.5
                else:
                    text "【已選定：[actor_disp_name]】請選擇下方行動指令 (攻擊 / 招式 / 防禦 / 背包)" size 17 color "#00ffff" xalign 0.5
            else:
                text "【提示】點擊左側待命隊員發布行動指令，全員行動完成後進入敵方回合" size 16 color "#aaaaaa" xalign 0.5

            null height 2

            # 中部戰場佈局：左側 6 位我方隊員，右側 6 隻喪屍敵人 (均支援平滑滾動)
            hbox:
                spacing 25
                xalign 0.5

                # --------------------------------
                # 左側：我方小隊列表 (每回合每人限行動一次)
                # --------------------------------
                vbox:
                    spacing 5
                    xysize (930, 700)
                    
                    hbox:
                        spacing 15
                        text "【 我方小隊列表 (6人) 】" size 19 color "#00ffff" yalign 0.5
                        if is_player_turn and len(unacted_members) > 0:
                            textbutton "⚔️ 全體普攻":
                                action Function(process_team_all_attack, battle_state)
                                text_size 14 text_idle_color "#00ff00" text_hover_color "#ffffff"
                            textbutton "🛡️ 全體防禦":
                                action Function(process_team_all_defend, battle_state)
                                text_size 14 text_idle_color "#66ccff" text_hover_color "#ffffff"
                    
                    viewport:
                        xysize (930, 665)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vbox:
                            spacing 8
                            for idx, member in enumerate(player_team):
                                $ m_name = member.get('name', '未知')
                                $ m_hp = member.get('hp', 100)
                                $ m_max_hp = member.get('max_hp', 100)
                                $ m_mp = member.get('mp', 50)
                                $ m_max_mp = member.get('max_mp', 50)
                                $ m_status = member.get('status', '良好')
                                $ m_has_acted = member.get('has_acted', False)
                                
                                $ m_gene = member.get('gene_lock', 0)
                                $ m_bloodline = member.get('bloodline', '無')
                                $ lock_text = ("基因鎖 " + str(m_gene) + " 階") if m_gene > 0 else "未開啟"
                                $ lock_color = "#ff4444" if m_gene > 0 else "#888888"
                                
                                $ is_active = (selected_actor == member)
                                $ is_alive = (m_hp > 0)
                                $ can_act = is_alive and (not m_has_acted) and is_player_turn

                                frame:
                                    xysize (905, None)
                                    if not is_alive:
                                        background "#22111166"
                                    elif is_active:
                                        background "#334466ee"
                                    elif m_has_acted:
                                        background "#1b1b2888"
                                    else:
                                        background "#222233aa"
                                    padding (12, 8)
                                    
                                    vbox:
                                        spacing 4
                                        
                                        # 隊員基本資料點擊列 (可行動者才可點擊選定)
                                        button:
                                            xysize (880, 55)
                                            if can_act:
                                                action SetDict(battle_state, 'selected_actor', None if is_active else member)
                                            
                                            vbox:
                                                spacing 2
                                                # 第一行：名稱、行動狀態、基因鎖、血統與狀態
                                                hbox:
                                                    spacing 15
                                                    text m_name size 17 color ("#00ffff" if is_active else ("#ffffff" if is_alive else "#888888")) bold True
                                                    
                                                    if not is_alive:
                                                        text "【💀 已倒下】" size 13 color "#ff4444" bold True yalign 0.5
                                                    elif m_has_acted:
                                                        text "【⏳ 本回合已行動】" size 13 color "#aaaaaa" yalign 0.5
                                                    else:
                                                        text "【⚡ 待命可行動】" size 13 color "#00ff00" bold True yalign 0.5

                                                    text lock_text size 13 color lock_color yalign 0.5
                                                    text ("血統: " + str(m_bloodline)) size 13 color "#ffaa88" yalign 0.5
                                                    text ("狀態: " + str(m_status)) size 13 color "#aaaaaa" yalign 0.5

                                                # 第二行：生命值與各能量
                                                hbox:
                                                    spacing 15
                                                    text ("HP: " + str(m_hp) + "/" + str(m_max_hp)) size 13 color ("#ff6666" if is_alive else "#666666")
                                                    text ("MP: " + str(m_mp) + "/" + str(m_max_mp)) size 13 color "#66ccff"
                                                    
                                                    if member.get('neili_max', 0) > 0:
                                                        text ("內力: " + str(member.get('neili_current', 0)) + "/" + str(member.get('neili_max', 0))) size 13 color "#ffaa00"
                                                    if member.get('blood_max', 0) > 0:
                                                        text ("血族: " + str(member.get('blood_current', 0)) + "/" + str(member.get('blood_max', 0))) size 13 color "#ff4444"
                                                    if member.get('mental_max', 0) > 0:
                                                        text ("精神力場: " + str(member.get('mental_current', 0)) + "/" + str(member.get('mental_max', 0))) size 13 color "#00ccff"
                                                    if member.get('qi_max', 0) > 0:
                                                        text ("氣血: " + str(member.get('qi_current', 0)) + "/" + str(member.get('qi_max', 0))) size 13 color "#ff6666"
                                                    if member.get('calc_max', 0) > 0:
                                                        text ("計算力: " + str(member.get('calc_current', 0)) + "/" + str(member.get('calc_max', 0))) size 13 color "#00ffcc"

                                        # 若為選取角色，展開指令功能按鈕列 (攻擊, 招式, 防禦, 背包, 取消)
                                        if is_active and can_act:
                                            null height 2
                                            hbox:
                                                spacing 12
                                                yalign 0.5
                                                
                                                textbutton "⚔️ 攻擊":
                                                    action SetDict(battle_state, 'target_mode', 'attack')
                                                    text_size 14
                                                    text_idle_color ("#00ff00" if target_mode == 'attack' else "#ffffff")
                                                    text_hover_color "#00ff00"

                                                textbutton "🔥 招式":
                                                    action SetDict(battle_state, 'target_mode', 'skill_menu')
                                                    text_size 14
                                                    text_idle_color ("#ffaa00" if target_mode in ('skill_menu', 'cast_skill') else "#ffffff")
                                                    text_hover_color "#ffaa00"

                                                textbutton "🛡️ 防禦":
                                                    action Function(process_player_defend, battle_state, member)
                                                    text_size 14
                                                    text_idle_color "#66ccff"
                                                    text_hover_color "#99ddff"

                                                textbutton "🎒 背包":
                                                    action SetDict(battle_state, 'target_mode', 'item_menu')
                                                    text_size 14
                                                    text_idle_color ("#ff88ff" if target_mode == 'item_menu' else "#ffffff")
                                                    text_hover_color "#ff88ff"

                                                textbutton "❌ 取消":
                                                    action [SetDict(battle_state, 'selected_actor', None), SetDict(battle_state, 'target_mode', None), SetDict(battle_state, 'selected_skill', None)]
                                                    text_size 14
                                                    text_idle_color "#ff4444"
                                                    text_hover_color "#ff8888"

                                            # 展開招式清單
                                            if target_mode in ('skill_menu', 'cast_skill'):
                                                $ actor_skills = get_actor_skills(member)
                                                frame:
                                                    background "#111122cc"
                                                    padding (10, 8)
                                                    vbox:
                                                        spacing 4
                                                        text "【 選擇施放招式 】" size 13 color "#ffaa00"
                                                        for sk in actor_skills:
                                                            $ sk_name = sk.get('name', '招式')
                                                            $ sk_cost = sk.get('energy_cost', sk.get('cost_energy', 0))
                                                            $ sk_desc = sk.get('desc', '')
                                                            $ is_sk_active = (selected_skill == sk)
                                                            hbox:
                                                                spacing 10
                                                                textbutton "★ [sk_name] (消耗 [sk_cost] 點)":
                                                                    if sk.get('is_heal', False):
                                                                        action Function(process_player_skill, battle_state, member, None, sk)
                                                                    else:
                                                                        action [SetDict(battle_state, 'selected_skill', sk), SetDict(battle_state, 'target_mode', 'cast_skill')]
                                                                    text_size 13
                                                                    text_idle_color ("#ffff00" if is_sk_active else "#00ffff")
                                                                    text_hover_color "#ffffff"
                                                                text "- [sk_desc]" size 12 color "#bbbbbb" yalign 0.5

                                            # 展開背包道具清單
                                            if target_mode == 'item_menu':
                                                frame:
                                                    background "#111122cc"
                                                    padding (10, 8)
                                                    vbox:
                                                        spacing 4
                                                        text "【 戰術背包 · 應急補給品 】" size 13 color "#ff88ff"
                                                        hbox:
                                                            spacing 15
                                                            textbutton "💊 止血急救噴霧 (+60 HP)":
                                                                action Function(process_use_item, battle_state, member, 'heal_spray')
                                                                text_size 13 text_idle_color "#66ff66" text_hover_color "#ffffff"
                                                            textbutton "💉 精神穩定劑 (+40 MP)":
                                                                action Function(process_use_item, battle_state, member, 'mp_potion')
                                                                text_size 13 text_idle_color "#66ccff" text_hover_color "#ffffff"
                                                            textbutton "💣 高爆破片手榴彈 (85 範圍傷害)":
                                                                action Function(process_use_item, battle_state, member, 'grenade')
                                                                text_size 13 text_idle_color "#ff6666" text_hover_color "#ffffff"

                # --------------------------------
                # 右側：敵方 6 隻喪屍怪物列表 (支援滾動)
                # --------------------------------
                vbox:
                    spacing 5
                    xysize (840, 700)
                    text "【 敵方目標列表 (6隻喪屍) 】" size 19 color "#ff4444"
                    
                    viewport:
                        xysize (840, 665)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vbox:
                            spacing 8
                            for e_idx, enemy in enumerate(enemies):
                                $ e_name = enemy.get('name', '喪屍')
                                $ e_hp = enemy.get('hp', 50)
                                $ e_max_hp = enemy.get('max_hp', 50)
                                $ e_atk = enemy.get('atk', 15)
                                $ e_status = enemy.get('status', '正常')
                                $ is_enemy_alive = (e_hp > 0)
                                $ can_target = is_enemy_alive and (target_mode in ('attack', 'cast_skill'))

                                button:
                                    xysize (815, 95)
                                    if not is_enemy_alive:
                                        background "#11111166"
                                    elif can_target:
                                        background "#772222ee"
                                        hover_background "#993333ee"
                                    else:
                                        background "#332222aa"
                                    padding (15, 8)
                                    
                                    # 點擊鎖定目標進行普通攻擊或招式打擊
                                    if can_target:
                                        if target_mode == 'attack':
                                            action Function(process_player_attack, battle_state, selected_actor, enemy)
                                        elif target_mode == 'cast_skill' and selected_skill:
                                            action Function(process_player_skill, battle_state, selected_actor, enemy, selected_skill)

                                    vbox:
                                        spacing 4
                                        hbox:
                                            spacing 20
                                            text e_name size 17 color ("#ff6666" if is_enemy_alive else "#777777") bold True
                                            if not is_enemy_alive:
                                                text "【💀 已被擊殺】" size 14 color "#888888" bold True yalign 0.5
                                            else:
                                                text ("特性/狀態: " + str(e_status)) size 13 color "#aaaaaa" yalign 0.5
                                                text ("攻擊力: " + str(e_atk)) size 13 color "#ffaa88" yalign 0.5

                                        hbox:
                                            spacing 20
                                            text ("生命值 (HP): " + str(e_hp) + " / " + str(e_max_hp)) size 14 color ("#ff4444" if is_enemy_alive else "#555555")
                                            
                                            if not is_enemy_alive:
                                                text "目標已無威脅" size 13 color "#555555" yalign 0.5
                                            elif target_mode == 'attack':
                                                text "【 🎯 點擊鎖定：普通攻擊 】" size 13 color "#00ff00" bold True yalign 0.5
                                            elif target_mode == 'cast_skill' and selected_skill:
                                                $ sk_t_name = selected_skill.get('name', '')
                                                text "【 💥 點擊釋放：[sk_t_name] 】" size 13 color "#ffff00" bold True yalign 0.5
                                            else:
                                                text "敵方威脅目標" size 13 color "#888888" yalign 0.5

            null height 2

            # 底部：戰鬥日誌 (Battle Log) 顯示區
            frame:
                xysize (1790, 115)
                background "#00000077"
                padding (15, 8)
                
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    
                    vbox:
                        spacing 3
                        for log in battle_logs[-5:]:
                            text ("• " + str(log)) size 13 color "#dddddd"

            null height 3

            # 底部功能按鈕列 (含全體普攻、全體防禦、回合切換、直接勝利、撤退)
            hbox:
                spacing 25
                xalign 0.5
                
                if is_player_turn and len(unacted_members) > 0:
                    textbutton "【 ⚔️ 全體普通攻擊 】":
                        action Function(process_team_all_attack, battle_state)
                        text_size 17
                        text_idle_color "#00ff00"
                        text_hover_color "#ffffff"

                    textbutton "【 🛡️ 全體防禦 】":
                        action Function(process_team_all_defend, battle_state)
                        text_size 17
                        text_idle_color "#66ccff"
                        text_hover_color "#ffffff"

                    textbutton "【 ⏩ 結束我方回合 】":
                        action Function(process_manual_end_turn, battle_state)
                        text_size 17
                        text_idle_color "#ffaa00"
                        text_hover_color "#ffffff"

                textbutton "【 ⚡ 直接勝利 (主神管理員權限) 】":
                    action Function(process_instant_win, battle_state)
                    text_size 17
                    text_idle_color "#ffcc00"
                    text_hover_color "#ffffff"

                textbutton "【 🚪 結束戰鬥 / 撤退 】":
                    action Return("end_battle")
                    text_size 17
                    text_idle_color "#ff4444"
                    text_hover_color "#ff8888"
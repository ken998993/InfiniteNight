init python:
    # ==============================================================================
    # 📜 《輪迴世界》戰鬥引擎與介面 (battle_screen.rpy)
    # 依據 developMd/03_Combat_and_Formation.md & developMd/16_uiux.md 規格全面升級
    # 包含：6人陣型、戰力階級壓制與跳彈、動態距離推進與瞄準、速度佇列 (Timeline)、
    #       動態戰場環境面板、3/4 AP 點數體系、全息戰術 HUD
    # ==============================================================================
    import random

    def to_int(val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    def get_actor_skills(actor):
        if not actor:
            return []
        if 'sync_member_skills_from_bloodlines' in globals():
            return sync_member_skills_from_bloodlines(actor)
        return actor.get('skills', [])

    # 1. 戰力階級判定 (Power Tier Scaling)
    def get_actor_power_tier(actor):
        if not actor:
            return 0
        g_lock = to_int(actor.get('gene_lock', 0))
        blood = str(actor.get('bloodline', '無'))
        if g_lock >= 3 or blood in ['四翼熾天使', '修真金丹', '修真元嬰', '神聖巨龍']:
            return 3
        if g_lock >= 2 or (blood != '無' and blood != 'None'):
            return 2
        if g_lock >= 1:
            return 1
        return 0  # Tier 0: 未強化普通人

    def get_enemy_power_tier(enemy):
        if not enemy:
            return 1
        if 'tier' in enemy:
            return to_int(enemy['tier'], 1)
        name = str(enemy.get('name', ''))
        e_id = str(enemy.get('id', ''))
        hp = to_int(enemy.get('max_hp', enemy.get('hp', 100)))
        if "👑" in name or "BOSS" in e_id or hp >= 600 or "母皇" in name or "長老" in name:
            return 3
        if "畸變" in name or "獵手" in name or "暴君" in name or "狼人" in name or hp >= 220:
            return 2
        return 1

    def check_actor_has_gun(actor):
        if not actor:
            return False
        name = str(actor.get('name', ''))
        eq = str(actor.get('equipped_main_hand', '')).lower()
        c_role = str(actor.get('combat_role', ''))
        role = str(actor.get('role', ''))
        
        # 1. 裝備近戰武器時，非槍手
        if any(w in eq for w in ['katana', 'sword', 'blade', 'dagger', 'glove', 'fist', 'spear', 'knife', '刀', '劍', '刃', '拳', '矛']):
            return False
            
        # 2. 明確持槍射手（冷月、言朔）
        if any(n in name for n in ["冷月", "言朔"]):
            return True
            
        # 3. 裝備槍械/弓箭
        if any(w in eq for w in ['gauss_rifle', 'rifle', 'gun', 'sniper', 'bow', 'pistol', 'cannon', '手槍', '步槍', '狙擊', '長弓', '槍']):
            return True
            
        # 4. 定位為槍手/狙擊
        if any(r in c_role for r in ['遠程', '狙擊', '長弓', '雙槍']) or any(r in role for r in ['狙擊手', '槍手']):
            return True
            
        return False

    def check_actor_is_ranged(actor):
        return check_actor_has_gun(actor)

    def log_distance_warning(battle_state, actor, dist):
        m_name = actor.get('name', '隊員') if actor else '隊員'
        dist_val = to_int(dist, 2)
        dist_label = "遠距離 (Far: 2)" if dist_val in (2, 100) else ("中距離 (Mid: 1)" if dist_val in (1, 50, 60) else "近距離 (Close: 0)")
        if 'logs' in battle_state:
            battle_state['logs'].append(f"💡 【怪物尚在遠處】當前戰場處於【{dist_label}】！敵方怪物尚未逼近，徒手/近戰無法隔空攻擊，請點選【🛡️ 防禦】戒備或【⏩ 待命】，等待怪物回合向前逼近進入近距離 (Close: 0)！")
        renpy.restart_interaction()

    def log_aim_required_warning(battle_state, actor):
        m_name = actor.get('name', '隊員') if actor else '隊員'
        if 'logs' in battle_state:
            battle_state['logs'].append(f"⚠️ 【遠距離射擊限制】當前戰場處於【遠距離 (Far: 2)】！【{m_name}】必須先消耗 1 AP 點選【🎯 瞄準】鎖定目標弱點後，方可扣動扳機開火！")
        renpy.restart_interaction()

    # 2. 動態距離判定 (Distance & Accuracy - 03md 三階段極簡距離)
    def get_distance_info(battle_state):
        raw_dist = battle_state.setdefault('distance', 2)
        dist = to_int(raw_dist, 2)
        if dist >= 80 or dist == 2:
            return 2, "遠距離 (Far: 2)", "far", -0.30
        elif dist >= 30 or dist == 1:
            return 1, "中距離 (Mid: 1)", "mid", 0.0
        else:
            return 0, "近距離 (Close: 0)", "close", 0.0

    # 3. 出手順序條佇列 (Speed Gauge / Timeline Ribbon)
    def get_action_order_queue(battle_state):
        queue = []
        for m in battle_state.get('player_team', []):
            if to_int(m.get('hp', 0)) > 0:
                spd = to_int(m.get('spd', 10))
                if m.get('is_gene_burst', False):
                    spd += 20
                queue.append({
                    'is_player': True,
                    'name': m.get('name', '隊員'),
                    'avatar': m.get('avatar', 'images/core_idle.PNG'),
                    'spd': spd,
                    'actor': m,
                    'has_acted': m.get('has_acted', False)
                })
        for e in battle_state.get('enemies', []):
            if to_int(e.get('hp', 0)) > 0:
                spd = to_int(e.get('spd', 12))
                queue.append({
                    'is_player': False,
                    'name': e.get('name', '敵方'),
                    'avatar': e.get('avatar', 'images/core_idle.PNG'),
                    'spd': spd,
                    'actor': e,
                    'has_acted': False
                })
        queue.sort(key=lambda x: x['spd'], reverse=True)
        return queue

    def check_battle_victory(battle_state):
        enemies = battle_state.get('enemies', [])
        all_dead = all(to_int(e.get('hp', 0)) <= 0 for e in enemies)
        if all_dead:
            m_ids = ["MOB_ZOMBIE_01", "MOB_LICKER_01"]
            if 'calculate_monster_drops' in globals():
                drops, int_bonus = calculate_monster_drops(m_ids)
                battle_state['last_loot'] = drops
                if 'logs' in battle_state:
                    bonus_pct = int(int_bonus * 100)
                    bonus_str = f" (隊伍智力加成: +{bonus_pct}% 稀有率)" if bonus_pct > 0 else ""
                    battle_state['logs'].append(f"🎉【戰鬥勝利】全數敵方目標已被殲滅！{bonus_str}")
                    if drops:
                        loot_strs = [f"{d['name']} x{d['count']}" for d in drops.values()]
                        battle_state['logs'].append(f"🎁【掠奪戰利品】已自動存入背包：{', '.join(loot_strs)}")
            # 戰鬥結束時，將戰鬥中隊員的剩餘 HP、MP 完整同步回全域隊伍名單 (禁止自動滿血，受創狀態保留)
            p_team = battle_state.get('player_team', [])
            roster = get_team_roster() if 'get_team_roster' in globals() else []
            for b_mem in p_team:
                m_name = b_mem.get('name')
                for r_mem in roster:
                    if r_mem.get('name') == m_name:
                        r_mem['hp'] = max(1, to_int(b_mem.get('hp', 100)))
                        r_mem['mp'] = max(0, to_int(b_mem.get('mp', 50)))
                        r_mem['status'] = b_mem.get('status', '良好')
            renpy.end_interaction("win")
            return True
        return False

    def check_attack_target_validity(actor, target, enemies, attack_type="melee", distance=2):
        a_name = actor.get('name', '隊員') if actor else '隊員'
        t_is_flight = target.get('is_flight', False) or "飛行" in target.get('status', '') or "翅膀" in target.get('name', '')
        a_is_flight = has_flight_capability(actor) if 'has_flight_capability' in globals() else False
        is_gun = check_actor_has_gun(actor)
        cur_ap = to_int(actor.get('ap', 0)) if actor else 0
        
        if actor and actor.get('has_attacked', False):
            return False, f"⚠️ 【本回合已攻擊】隊員【{a_name}】本回合已發動過攻擊，每回合僅能執行 1 次主要攻擊行動！"
        
        # 距離階段判定 (遠距離=2, 中距離=1, 近距離=0)
        dist_val = to_int(distance, 2)
        dist_label = "遠距離 (Far: 2)" if dist_val in (2, 100) else ("中距離 (Mid: 1)" if dist_val in (1, 50, 60) else "近距離 (Close: 0)")
        
        if attack_type == "melee":
            if dist_val > 0 and not a_is_flight:
                return False, f"💡 【怪物尚在遠處】當前處於【{dist_label}】！敵方怪物尚未逼近，徒手/近戰無法隔空揮擊，請防禦或待命等待怪物逼近！"
            if cur_ap < 3:
                return False, f"⚠️ 【AP不足】徒手/近戰攻擊需要消耗 3 AP！(當前 AP: {cur_ap})"
        elif attack_type == "shoot":
            if not is_gun:
                return False, f"⚠️ 【無槍械】隊員【{a_name}】未裝備槍械或遠程武器，無法進行射擊！"
            req_ap = 4 if dist_val == 2 else 3
            if cur_ap < req_ap:
                if dist_val == 2:
                    return False, f"⚠️ 【AP不足】遠距離【瞄準射擊】需要消耗 4 AP（1 AP 瞄準 + 3 AP 開火）！(當前 AP: {cur_ap})"
                else:
                    return False, f"⚠️ 【AP不足】槍械射擊需要消耗 3 AP！(當前 AP: {cur_ap})"
                
        if t_is_flight and not (a_is_flight or attack_type == "shoot"):
            return False, "⚠️ 【超出距離】目標處於飛行狀態！地面徒手/近戰無法觸及，需使用槍械射擊或飛行技能！"
            
        t_pos = target.get('position', 'frontline')
        if t_pos == 'backline' and not (a_is_flight or attack_type == "shoot"):
            alive_front = [e for e in enemies if to_int(e.get('hp', 0)) > 0 and e.get('position', 'frontline') == 'frontline']
            if alive_front:
                return False, "⚠️ 【前排阻擋】敵方前排防線仍有單位存活！地面近戰無法跨排直接攻擊後排！"
                
        return True, ""

    def process_enemy_phase(battle_state):
        enemies = [e for e in battle_state.get('enemies', []) if to_int(e.get('hp', 0)) > 0]
        players = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0]
        
        round_num = battle_state.get('round_number', 1)
        if 'logs' in battle_state:
            battle_state['logs'].append(f"=== 第 {round_num} 回合 · 敵方反擊與逼近階段 ===")
            
        if battle_state.get('ai_mode') == 'passive':
            if 'logs' in battle_state:
                battle_state['logs'].append("🛡️【全息木樁被動模式】假想敵處於待命狀態，不進行任何反擊！")
            return
        
        if not players:
            if 'logs' in battle_state:
                battle_state['logs'].append("💀 我方小隊全員倒下！戰鬥失敗！")
            return

        # 1. 怪物距離逼近結算 (Monster Movement Resolution)
        cur_dist_tier, cur_dist_name, _, _ = get_distance_info(battle_state)
        max_e_tier = max([get_enemy_power_tier(e) for e in enemies] or [1])
        monsters_can_melee_attack = (cur_dist_tier == 0)
        
        if cur_dist_tier == 2:
            # 遠距離 (Far: 2)
            if max_e_tier >= 2:
                # 高速突變怪物 (Tier 2+) 直接跨越 2 階飛撲至近距離
                battle_state['distance'] = 0
                monsters_can_melee_attack = True
                if 'logs' in battle_state:
                    battle_state['logs'].append("⚡【高速突進】敵方高階突變體發動狂暴飛撲，瞬間跨越距離突進至【近距離 (Close: 0)】！")
            else:
                # 普通慢速喪屍 (Tier 1) 推進 1 階至中距離
                battle_state['distance'] = 1
                monsters_can_melee_attack = False
                if 'logs' in battle_state:
                    battle_state['logs'].append("🧟【怪物前進】慢速喪屍群嘶吼著向我方防線逼近！戰場距離縮短至【中距離 (Mid: 1)】（本回合尚無法近戰肉搏）！")
        elif cur_dist_tier == 1:
            # 中距離 (Mid: 1) -> 推進至近距離
            battle_state['distance'] = 0
            monsters_can_melee_attack = True
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️【近身接觸】敵方怪物群衝破最後距離，進入【近距離 (Close: 0)】白兵戰範圍！")
        else:
            # 近距離 (Close: 0)
            monsters_can_melee_attack = True

        # 2. 怪物攻擊結算
        for enemy in enemies:
            alive_players = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0]
            if not alive_players:
                break
                
            e_has_flight = enemy.get('is_flight', False) or "飛行" in enemy.get('status', '') or "翅膀" in enemy.get('name', '')
            e_is_ranged = enemy.get('is_ranged', False) or "遠程" in enemy.get('status', '') or "酸液" in enemy.get('name', '') or "長舌" in enemy.get('name', '')
            
            # 若怪物不在近距離且無遠程攻擊能力，無法發動肉搏
            if not monsters_can_melee_attack and not (e_is_ranged or e_has_flight):
                continue
                
            alive_frontline = [m for m in alive_players if m.get('position', 'frontline') == 'frontline']
            alive_backline = [m for m in alive_players if m.get('position', 'frontline') == 'backline']
            
            is_backline_exposed = False
            if alive_frontline and not (e_has_flight or e_is_ranged):
                target = random.choice(alive_frontline)
            else:
                target = random.choice(alive_players)
                if not alive_frontline and alive_backline:
                    is_backline_exposed = True
            
            raw_atk = to_int(enemy.get('atk', 18), 18)
            is_defending = "防禦" in target.get('status', '')
            dmg = max(5, int(raw_atk * 0.5)) if is_defending else raw_atk
            
            if is_backline_exposed:
                dmg = int(dmg * 1.2)
                
            target['hp'] = max(0, to_int(target.get('hp', 0)) - dmg)
            
            e_name = enemy.get('name', '敵人')
            t_name = target.get('name', '隊員')
            t_pos_tag = "前排🛡️" if target.get('position', 'frontline') == 'frontline' else "後排🏹"
            exposed_tag = " (⚠️ 前排瓦解，後排暴露受創 +20%)" if is_backline_exposed else ""
            
            if is_defending:
                battle_state['logs'].append(f"【T{round_num}】 💥 {e_name} 猛撲 {t_pos_tag}【{t_name}】！{t_name} 舉盾防禦，受到 {dmg} 點減免傷害！{exposed_tag}")
            else:
                battle_state['logs'].append(f"【T{round_num}】 💥 {e_name} 攻擊了 {t_pos_tag}【{t_name}】，造成了 {dmg} 點傷害！{exposed_tag}")
                
            if to_int(target.get('hp', 0)) <= 0:
                target['status'] = '重傷倒地'
                battle_state['logs'].append(f"【T{round_num}】 ⚠️ 隊員【{t_name}】受到致命重創倒下！")
                
        remaining_players = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0]
        if not remaining_players:
            if 'logs' in battle_state:
                battle_state['logs'].append("💀 我方小隊全體陣亡！")
            return
            
        battle_state['round_number'] = round_num + 1
        new_round = battle_state['round_number']
        
        # 結算環境危害
        current_w = battle_state.get('world_id', 'zombie')
        for m in remaining_players:
            m_name = m.get('name', '隊員')
            g_lock = to_int(m.get('gene_lock', 0))
            is_burst_4 = m.get('is_gene_burst', False) and g_lock >= 4
            env_mult = 0.5 if is_burst_4 else 1.0
            
            if current_w == "zombie":
                is_immune = is_gas_immune(m) if 'is_gas_immune' in globals() else False
                if not is_immune:
                    dmg = max(4, int(to_int(m.get('max_hp', 100)) * 0.03 * env_mult))
                    m['hp'] = max(1, to_int(m.get('hp', 100)) - dmg)
                    if 'logs' in battle_state:
                        battle_state['logs'].append(f"☣️ 生化毒氣侵蝕！【{m_name}】受到 {dmg} 點環境毒氣傷害！")
            elif current_w == "paranormal":
                mp_drain = max(2, int(5 * env_mult))
                m['mp'] = max(0, to_int(m.get('mp', 0)) - mp_drain)
                if 'logs' in battle_state:
                    battle_state['logs'].append(f"👻 陰煞之氣噬魂！【{m_name}】被汲取了 {mp_drain} 點精神力！")
            elif current_w == "causality":
                if random.random() < 0.20:
                    if to_int(m.get('gene_lock', 0)) > 0:
                        if 'logs' in battle_state:
                            battle_state['logs'].append(f"🧬 基因鎖危險感知！【{m_name}】提前預判並閃避了死神意外殺局！")
                    else:
                        trap_dmg = int(35 * env_mult)
                        m['hp'] = max(1, to_int(m.get('hp', 100)) - trap_dmg)
                        if 'logs' in battle_state:
                            battle_state['logs'].append(f"⚠️ 死神因果律意外！【{m_name}】受到 {trap_dmg} 點意外傷害！")

        # 重置回合行動點數 (AP)
        battle_state['show_enemy_intents'] = False
        for m in battle_state.get('player_team', []):
            m['has_acted'] = False
            m['has_attacked'] = False
            m['max_ap'] = 4
            m['ap'] = 4
            m['is_gene_burst'] = False
            m['is_aimed'] = False
            g_lock = to_int(m.get('gene_lock', 0))
            if g_lock >= 3:
                battle_state['show_enemy_intents'] = True
            if "防禦" in m.get('status', ''):
                m['status'] = '良好'
                
        battle_state['is_player_turn'] = True
        battle_state['current_turn_name'] = f"第 {new_round} 回合 · 我方行動階段"
        if 'logs' in battle_state:
            battle_state['logs'].append(f"🔔 === 第 {new_round} 回合開始！我方全體重置行動點數 (4 AP) ===")

    def end_actor_turn(battle_state, actor):
        if actor:
            actor['has_acted'] = True
            actor['ap'] = 0
            
        battle_state['selected_actor'] = None
        battle_state['target_mode'] = None
        battle_state['selected_skill'] = None
        
        if check_battle_victory(battle_state):
            return
            
        alive_players = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0]
        if alive_players and all(m.get('has_acted', False) or to_int(m.get('ap', 0)) <= 0 for m in alive_players):
            process_enemy_phase(battle_state)
            
        renpy.restart_interaction()

    # 4. 戰術推進與精準瞄準指令 (Advance & Aim)
    def process_player_advance(battle_state, actor):
        if not actor:
            return
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < 1:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【AP不足】推進需要消耗 1 AP！")
            renpy.restart_interaction()
            return
            
        cur_tier, cur_name, cur_code, _ = get_distance_info(battle_state)
        if cur_tier <= 0:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【已達近距離】當前已處於【近距離 (Close: 0)】，雙方已進入白兵戰範圍，無需再推進！")
            renpy.restart_interaction()
            return
            
        actor['ap'] = max(0, cur_ap - 1)
        new_tier = max(0, cur_tier - 1)
        battle_state['distance'] = new_tier
        _, new_name, _, _ = get_distance_info(battle_state)
        
        round_num = battle_state.get('round_number', 1)
        actor_name = actor.get('name', '隊員')
        log_msg = f"【T{round_num}】 🏃 【{actor_name}】消耗 1 AP 帶領小隊向前【推進】！戰場距離縮短至 【{new_name}】！(剩餘 AP: {actor['ap']})"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            renpy.restart_interaction()

    def process_player_aim(battle_state, actor):
        if not actor:
            return
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < 1:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【AP不足】精準瞄準需要消耗 1 AP！")
            renpy.restart_interaction()
            return
        actor['ap'] = max(0, cur_ap - 1)
        actor['is_aimed'] = True
        round_num = battle_state.get('round_number', 1)
        actor_name = actor.get('name', '隊員')
        log_msg = f"【T{round_num}】 🎯 【{actor_name}】消耗 1 AP 執行【精準瞄準】！鎖定遠程弱點，下次射擊消除遠距懲罰且暴擊率 +30%！(剩餘 AP: {actor['ap']})"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            renpy.restart_interaction()

    # 5. 普通攻擊 (徒手/近戰) 與 槍械射擊 核心處理
    def process_player_attack(battle_state, actor, target, attack_type=None):
        if not actor or not target:
            return
            
        cur_ap = to_int(actor.get('ap', 4))
        enemies = battle_state.get('enemies', [])
        cur_dist_tier, cur_dist_name, _, _ = get_distance_info(battle_state)
        
        # 決定攻擊類型與 AP 消耗
        if not attack_type:
            target_m = battle_state.get('target_mode', 'melee')
            attack_type = "shoot" if target_m == "shoot" else "melee"
            
        if attack_type == "shoot":
            req_ap = 4 if cur_dist_tier == 2 else 3
        else:
            req_ap = 3
            
        valid, reason = check_attack_target_validity(actor, target, enemies, attack_type=attack_type, distance=cur_dist_tier)
        if not valid:
            if 'logs' in battle_state:
                battle_state['logs'].append(reason)
            renpy.restart_interaction()
            return
            
        actor['ap'] = max(0, cur_ap - req_ap)
        actor['has_attacked'] = True
        round_num = battle_state.get('round_number', 1)
        actor_name = actor.get('name', '隊員')
        target_name = target.get('name', '敵人')
        actor_pos = "前排🛡️" if actor.get('position', 'frontline') == 'frontline' else "後排🏹"

        # 基礎傷害計算
        current_w = battle_state.get('world_id', 'zombie')
        atk_bonus = actor.get("atk_bonus", 0)
        damage = 35 + atk_bonus
        g_lock = to_int(actor.get('gene_lock', 0))
        is_burst = actor.get('is_gene_burst', False)
        
        burst_tag = ""
        # 遠距離單鍵瞄準射擊 (自動包含 1 AP 瞄準必中與暴擊)
        if attack_type == "shoot" and cur_dist_tier == 2:
            burst_tag += " (🎯 遠距瞄準鎖定弱點)"
            crit_rate = 0.75
        elif attack_type == "shoot":
            is_aimed = actor.get('is_aimed', False)
            actor['is_aimed'] = False
            crit_rate = 0.75 if (is_aimed or (is_burst and g_lock >= 3)) else 0.15
        else:
            crit_rate = 0.75 if (is_burst and g_lock >= 3) else 0.15
            
        if is_burst and g_lock >= 2:
            damage = int(damage * 1.5)
            burst_tag += " (⚡ 基因鎖二階力量倍增 +50%)"
            
        if random.random() < crit_rate:
            damage = int(damage * 2.0)
            burst_tag += " (💥 弱點暴擊 x200%!)"
        
        # 階級壓制與跳彈 (Power Tier Scaling)
        a_tier = get_actor_power_tier(actor)
        e_tier = get_enemy_power_tier(target)
        suppression_msg = ""
        
        if a_tier == 0 and not is_burst:
            if attack_type == "melee" and e_tier >= 1:
                damage = max(1, int(damage * 0.10))
                suppression_msg = " 【⚠️ 力量壓制：未強化普通人徒手攻擊無效 -90%！】"
            elif attack_type == "shoot" and e_tier >= 2:
                damage = max(3, int(damage * 0.20))
                suppression_msg = " 【🛡️ 跳彈：普通子彈被硬質甲殼彈開 -80%！】"
        elif a_tier >= 1 or is_burst:
            suppression_msg = " 【⚡ 破甲真實打擊】"

        # 環境懲罰判定
        env_msg = ""
        if current_w == "space":
            has_flight = has_flight_capability(actor) if 'has_flight_capability' in globals() else False
            if not has_flight:
                penalty = 0.25 if (is_burst and g_lock >= 4) else 0.5
                damage = max(10, int(damage * (1.0 - penalty)))
                env_msg = f" (太空失重懲罰 -{int(penalty*100)}% 傷害)"
        elif current_w == "paranormal":
            has_magic = has_magic_damage(actor) if 'has_magic_damage' in globals() else False
            if not has_magic:
                damage = max(8, int(damage * 0.2))
                env_msg = " (靈異幽魂虛化 -80% 物理傷害)"
            else:
                env_msg = " (✨ 魔法破靈全額打擊)"
                
        target['hp'] = max(0, target['hp'] - damage)
        bonus_str = f" (裝備加成 +{atk_bonus})" if atk_bonus > 0 else ""
        if attack_type == "shoot":
            if cur_dist_tier == 2:
                atk_type_label = "瞄準射擊"
                ap_cost_desc = "消耗 4 AP（1 AP 瞄準 + 3 AP 開火）"
                atk_icon = "🎯"
            else:
                atk_type_label = "槍械射擊"
                ap_cost_desc = "消耗 3 AP"
                atk_icon = "🏹"
        else:
            atk_type_label = "徒手/近戰攻擊"
            ap_cost_desc = "消耗 3 AP"
            atk_icon = "⚔️"
            
        log_msg = f"【T{round_num}】 {atk_icon} {actor_pos}【{actor_name}】{ap_cost_desc} 發動【{atk_type_label}】{bonus_str}{burst_tag}{suppression_msg}{env_msg}，對【{target_name}】造成了 {damage} 點傷害！(剩餘 AP: {actor['ap']})"
        
        if battle_state.get('is_simulation'):
            battle_state['total_damage'] = battle_state.get('total_damage', 0) + damage
            battle_state['highest_hit'] = max(battle_state.get('highest_hit', 0), damage)
            if battle_state.get('infinite_hp'):
                target['hp'] = target.get('max_hp', 99999)
                target['status'] = '全息木樁 (DPS測試)'

        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if target.get('hp', 0) <= 0 and not battle_state.get('infinite_hp'):
            target['status'] = '已擊殺'
            if 'logs' in battle_state:
                battle_state['logs'].append(f"【T{round_num}】 💥 敵方目標【{target_name}】已被成功擊殺！")
                
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            battle_state['target_mode'] = None
            if check_battle_victory(battle_state):
                return
            renpy.restart_interaction()
        
        if battle_state.get('is_simulation'):
            battle_state['total_damage'] = battle_state.get('total_damage', 0) + damage
            battle_state['highest_hit'] = max(battle_state.get('highest_hit', 0), damage)
            if battle_state.get('infinite_hp'):
                target['hp'] = target.get('max_hp', 99999)
                target['status'] = '全息木樁 (DPS測試)'

        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if target.get('hp', 0) <= 0 and not battle_state.get('infinite_hp'):
            target['status'] = '已擊殺'
            if 'logs' in battle_state:
                battle_state['logs'].append(f"【T{round_num}】 💥 敵方目標【{target_name}】已被成功擊殺！")
                
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            battle_state['target_mode'] = None
            if check_battle_victory(battle_state):
                return
            renpy.restart_interaction()

    # 6. 專屬技能處理 (4 AP)
    def process_player_skill(battle_state, actor, target, skill):
        if not actor or not skill:
            return
            
        ap_cost = skill.get('ap_cost', 4)
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < ap_cost:
            if 'logs' in battle_state:
                battle_state['logs'].append(f"⚠️ 【AP不足】施展【{skill.get('name')}】需要消耗 {ap_cost} AP！(當前 AP: {cur_ap})")
            renpy.restart_interaction()
            return
            
        actor_name = actor.get('name', '隊員')
        skill_name = skill.get('name', '招式')
        damage = skill.get('damage', 0)
        heal = skill.get('heal', 0)
        energy_type = skill.get('energy_type', 'mp')
        cost = skill.get('energy_cost', skill.get('cost_energy', 0))
        
        energy_map = {
            "blood_energy": "blood_current", "blood_current": "blood_current",
            "neili_energy": "neili_current", "neili_current": "neili_current",
            "qi_energy": "qi_current", "qi_current": "qi_current",
            "mental_energy": "mental_current", "mental_current": "mental_current",
            "calc_energy": "calc_current", "calc_current": "calc_current",
            "mp": "mp"
        }
        resolved_energy = energy_map.get(energy_type, energy_type)
        
        if resolved_energy in actor and actor[resolved_energy] >= cost:
            actor[resolved_energy] = max(0, actor[resolved_energy] - cost)
        elif 'mp' in actor and actor['mp'] >= cost:
            actor['mp'] = max(0, actor['mp'] - cost)
        elif resolved_energy in actor:
            actor[resolved_energy] = max(0, actor[resolved_energy] - cost)
            
        actor['ap'] = max(0, cur_ap - ap_cost)
        actor['has_attacked'] = True
        round_num = battle_state.get('round_number', 1)
        actor_pos = "前排🛡️" if actor.get('position', 'frontline') == 'frontline' else "後排🏹"
        
        if skill.get('is_heal', False) or (heal > 0 and damage == 0):
            actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + heal)
            log_msg = f"【T{round_num}】 ✨ {actor_pos}【{actor_name}】消耗 {ap_cost} AP 施展了【{skill_name}】，回復了自身 {heal} 點生命值！(剩餘 AP: {actor['ap']})"
        else:
            if target:
                target['hp'] = max(0, target['hp'] - damage)
                target_name = target.get('name', '敵人')
                log_msg = f"【T{round_num}】 🔥 {actor_pos}【{actor_name}】消耗 {ap_cost} AP 施展【{skill_name}】(無視防禦)，對【{target_name}】造成了 {damage} 點真實傷害！(剩餘 AP: {actor['ap']})"
                
                if battle_state.get('is_simulation'):
                    battle_state['total_damage'] = battle_state.get('total_damage', 0) + damage
                    battle_state['highest_hit'] = max(battle_state.get('highest_hit', 0), damage)
                    if battle_state.get('infinite_hp'):
                        target['hp'] = target.get('max_hp', 99999)
                        target['status'] = '全息木樁 (DPS測試)'

                if heal > 0:
                    actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + heal)
                    log_msg += f" (同時吸取並恢復了 {heal} 點 HP)"
                if target.get('hp', 0) <= 0 and not battle_state.get('infinite_hp'):
                    target['status'] = '已擊殺'
                    if 'logs' in battle_state:
                        battle_state['logs'].append(f"【T{round_num}】 💥 敵方目標【{target_name}】已被技能徹底摧毀！")
            else:
                log_msg = f"【T{round_num}】 🔥 {actor_pos}【{actor_name}】施展了【{skill_name}】！"
                
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            battle_state['target_mode'] = None
            if check_battle_victory(battle_state):
                return
            renpy.restart_interaction()

    def process_player_defend(battle_state, actor):
        if not actor:
            return
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < 1:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【AP不足】進入防禦姿態需要消耗 1 AP！")
            renpy.restart_interaction()
            return
            
        actor['ap'] = max(0, cur_ap - 1)
        actor_name = actor.get('name', '隊員')
        round_num = battle_state.get('round_number', 1)
        heal_hp = 25
        heal_mp = 15
        actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + heal_hp)
        actor['mp'] = min(actor.get('max_mp', 50), actor.get('mp', 50) + heal_mp)
        actor['status'] = '防禦中 (減傷50%)'
        log_msg = f"【T{round_num}】 🛡️ 【{actor_name}】消耗 1 AP 進入【防禦姿態】，凝神戒備 (受傷 -50%) 並回復了 {heal_hp} 點 HP 與 {heal_mp} 點精力！(剩餘 AP: {actor['ap']})"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            battle_state['target_mode'] = None
            renpy.restart_interaction()

    def process_switch_position(battle_state, actor):
        if not actor:
            return
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < 1:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【AP不足】變更前後排站位需要消耗 1 AP！")
            renpy.restart_interaction()
            return
            
        player_team = battle_state.get('player_team', [])
        cur_pos = actor.get('position', 'frontline')
        new_pos = "backline" if cur_pos == "frontline" else "frontline"
        
        front_cnt = sum(1 for m in player_team if m.get('position', 'frontline') == 'frontline' and to_int(m.get('hp', 0)) > 0)
        back_cnt = sum(1 for m in player_team if m.get('position', 'frontline') == 'backline' and to_int(m.get('hp', 0)) > 0)
        
        if new_pos == 'frontline' and front_cnt >= 3:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 前排槽位已滿 (最多3人)！無法切換至前排！")
            renpy.restart_interaction()
            return
        if new_pos == 'backline' and back_cnt >= 3:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 後排槽位已滿 (最多3人)！無法切換至後排！")
            renpy.restart_interaction()
            return
            
        actor['position'] = new_pos
        actor['ap'] = max(0, cur_ap - 1)
        actor_name = actor.get('name', '隊員')
        round_num = battle_state.get('round_number', 1)
        pos_tag = "前排🛡️" if new_pos == "frontline" else "後排🏹"
        log_msg = f"【T{round_num}】 🔄 【{actor_name}】消耗 1 AP 移動並切換站位至【{pos_tag}】！(剩餘 AP: {actor['ap']})"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            battle_state['target_mode'] = None
            renpy.restart_interaction()

    def process_gene_burst(battle_state, actor):
        if not actor:
            return
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < 1:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【AP不足】開啟基因鎖需要消耗 1 AP！")
            renpy.restart_interaction()
            return
            
        actor['is_gene_burst'] = True
        g_lock = to_int(actor.get('gene_lock', 0))
        actor['ap'] = cur_ap - 1 + 2
        actor['max_ap'] = max(actor.get('max_ap', 4), actor['ap'])
        actor_name = actor.get('name', '隊員')
        round_num = battle_state.get('round_number', 1)
        log_msg = f"【T{round_num}】 🧬 【{actor_name}】消耗 1 AP 開啟【基因鎖 {g_lock} 階】！突破人體極限，獲得額外 +2 AP 突破點數 (當前 AP: {actor['ap']})，暴擊率與速度大幅倍增！"
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
        renpy.restart_interaction()

    def process_use_item(battle_state, actor, item_id):
        if not actor or not item_id:
            return
        cur_ap = to_int(actor.get('ap', 4))
        if cur_ap < 1:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 【AP不足】使用背包物資需要消耗 1 AP！")
            renpy.restart_interaction()
            return
            
        actor['ap'] = max(0, cur_ap - 1)
        actor_name = actor.get('name', '隊員')
        round_num = battle_state.get('round_number', 1)
        itm = get_item_by_id(item_id) if 'get_item_by_id' in globals() else None
        
        if not itm:
            if item_id == 'heal_spray':
                itm = {"name": "輪迴止血急救噴霧", "effect_type": "heal_hp", "effect_val": 80}
            elif item_id == 'mp_potion':
                itm = {"name": "強效精神穩定劑", "effect_type": "heal_mp", "effect_val": 50}
            elif item_id == 'grenade':
                itm = {"name": "高爆破片手榴彈", "effect_type": "aoe_damage", "effect_val": 90}
            else:
                itm = {"name": "戰術物資", "effect_type": "heal_hp", "effect_val": 50}
                
        eff_type = itm.get("effect_type", "heal_hp")
        eff_val = itm.get("effect_val", 50)
        itm_name = itm.get("name", "戰術物資")
        
        if eff_type == "heal_hp":
            actor['hp'] = min(actor.get('max_hp', 100), actor.get('hp', 100) + eff_val)
            log_msg = f"【T{round_num}】 💊 {actor_name} 消耗 1 AP 使用了【{itm_name}】，恢復了 {eff_val} 點 HP！(剩餘 AP: {actor['ap']})"
        elif eff_type == "heal_mp":
            actor['mp'] = min(actor.get('max_mp', 50), actor.get('mp', 50) + eff_val)
            log_msg = f"【T{round_num}】 💉 {actor_name} 消耗 1 AP 使用了【{itm_name}】，恢復了 {eff_val} 點 MP！(剩餘 AP: {actor['ap']})"
        elif eff_type == "aoe_damage":
            enemies = battle_state.get('enemies', [])
            for e in enemies:
                if e.get('hp', 0) > 0:
                    e['hp'] = max(0, e.get('hp', 0) - eff_val)
                    if e['hp'] <= 0:
                        e['status'] = '已擊殺'
            log_msg = f"【T{round_num}】 💣 {actor_name} 消耗 1 AP 投擲了【{itm_name}】，對敵方全體造成了 {eff_val} 點範圍爆炸傷害！(剩餘 AP: {actor['ap']})"
        else:
            log_msg = f"【T{round_num}】 🎒 {actor_name} 消耗 1 AP 使用了【{itm_name}】。(剩餘 AP: {actor['ap']})"
            
        if 'remove_item' in globals():
            remove_item(item_id, 1)
            
        if 'logs' in battle_state:
            battle_state['logs'].append(log_msg)
            
        if actor['ap'] <= 0:
            end_actor_turn(battle_state, actor)
        else:
            battle_state['target_mode'] = None
            if check_battle_victory(battle_state):
                return
            renpy.restart_interaction()

    def process_team_all_attack(battle_state):
        if not battle_state.get('is_player_turn', True):
            return
        cur_dist = to_int(battle_state.setdefault('distance', 100), 100)
        unacted = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0 and not m.get('has_acted', False) and to_int(m.get('ap', m.get('max_ap', 4))) >= 3]
        if not unacted:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 當前回合無剩餘 AP >= 3 的待命隊員可發動攻擊！")
            renpy.restart_interaction()
            return
            
        if 'logs' in battle_state:
            battle_state['logs'].append(f"⚔️ === 我方發動【全體普通攻擊】戰術突擊！(當前距敵 {cur_dist}m) ===")
            
        attacked_any = False
        for member in unacted:
            alive_enemies = [e for e in battle_state.get('enemies', []) if to_int(e.get('hp', 0)) > 0]
            if not alive_enemies:
                break
            m_name = member.get('name', '隊員')
            is_ranged = check_actor_is_ranged(member)
            has_flight = has_flight_capability(member) if 'has_flight_capability' in globals() else False
            
            if not (is_ranged or has_flight) and cur_dist > 20:
                if 'logs' in battle_state:
                    battle_state['logs'].append(f"⚠️ 【{m_name}】為近戰單位，因戰場距離過遠 ({cur_dist}m) 無法攻擊！(請先推進至 <=20m)")
                continue
                
            target = alive_enemies[0]
            e_name = target.get('name', '敵方')
            damage = 35 + member.get("atk_bonus", 0)
            target['hp'] = max(0, to_int(target.get('hp', 0)) - damage)
            member['has_acted'] = True
            member['ap'] = max(0, to_int(member.get('ap', 4)) - 3)
            attacked_any = True
            
            if 'logs' in battle_state:
                battle_state['logs'].append(f"⚔️ 【{m_name}】攻擊了【{e_name}】，造成了 {damage} 點傷害！")
            if to_int(target.get('hp', 0)) <= 0:
                target['status'] = '已擊殺'
                if 'logs' in battle_state:
                    battle_state['logs'].append(f"💥 敵方目標【{e_name}】已被擊斃！")
                    
        if not attacked_any and cur_dist > 20:
            if 'logs' in battle_state:
                battle_state['logs'].append(f"⚠️ 【突擊受阻】待命隊員皆為近戰單位，距敵 {cur_dist}m 過遠！請先點選【🏃 推進】拉近距離至 20m 內！")
                    
        battle_state['selected_actor'] = None
        battle_state['target_mode'] = None
        battle_state['selected_skill'] = None
        if check_battle_victory(battle_state):
            return
        alive_players = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0]
        if alive_players and all(m.get('has_acted', False) or to_int(m.get('ap', 0)) < 1 for m in alive_players):
            process_enemy_phase(battle_state)
        renpy.restart_interaction()

    def process_team_all_defend(battle_state):
        if not battle_state.get('is_player_turn', True):
            return
        unacted = [m for m in battle_state.get('player_team', []) if to_int(m.get('hp', 0)) > 0 and not m.get('has_acted', False)]
        if not unacted:
            if 'logs' in battle_state:
                battle_state['logs'].append("⚠️ 當前回合所有存活隊員均已行動過！")
            renpy.restart_interaction()
            return
        if 'logs' in battle_state:
            battle_state['logs'].append("🛡️ === 我方全體採取【全體防禦姿態】！全體進入 50% 減傷戒備並恢復 15 點精力 ===")
        for member in unacted:
            # 全體防禦：僅提供 50% 減傷狀態與微量精力 (MP) 回復，生命值 (HP) 僅能透過道具或輪迴修復
            heal_mp = 15
            member['mp'] = min(member.get('max_mp', 50), member.get('mp', 50) + heal_mp)
            member['status'] = '防禦中 (減傷50%)'
            member['has_acted'] = True
        battle_state['selected_actor'] = None
        battle_state['target_mode'] = None
        battle_state['selected_skill'] = None
        process_enemy_phase(battle_state)
        renpy.restart_interaction()

    def process_manual_end_turn(battle_state):
        if 'logs' in battle_state:
            battle_state['logs'].append("⏩ 手動結束我方階段，直接進入敵方反擊回合！")
        process_enemy_phase(battle_state)
        renpy.restart_interaction()

    def ensure_six_enemies(battle_state):
        if not battle_state.get('enemies'):
            battle_state['enemies'] = [
                create_battle_enemy("agile_zombie", "A", status="嗜血狂暴"),
                create_battle_enemy("agile_zombie", "B", status="嗜血狂暴"),
                create_battle_enemy("agile_zombie", "C", status="敏捷突進"),
                create_battle_enemy("MOB_ZOMBIE_01", "A", status="毒素附著"),
                create_battle_enemy("MOB_ZOMBIE_01", "B", status="毒素附著"),
                create_battle_enemy("MOB_ZOMBIE_01", "C", status="嗜血")
            ]
        else:
            for e in battle_state.get('enemies', []):
                e_id = e.get('id', '')
                e_name = e.get('name', '')
                e_av = e.get('avatar', '')
                if not e_av or e_av == 'images/core_idle.PNG':
                    if e_id == 'agile_zombie' or '敏捷' in e_name:
                        e['avatar'] = 'images/agile_zombie.jpg'
                    elif e_id == 'MOB_ZOMBIE_01' or '腐屍' in e_name or '喪屍' in e_name:
                        e['avatar'] = 'images/zombie.jpg'

    def process_instant_win(battle_state):
        enemies = battle_state.get('enemies', [])
        for e in enemies:
            e['hp'] = 0
            e['status'] = '已擊殺'
        # 戰鬥結束時，將戰鬥中隊員的剩餘 HP、MP 同步回全域隊伍名單
        p_team = battle_state.get('player_team', [])
        roster = get_team_roster() if 'get_team_roster' in globals() else []
        for b_mem in p_team:
            m_name = b_mem.get('name')
            for r_mem in roster:
                if r_mem.get('name') == m_name:
                    r_mem['hp'] = max(1, to_int(b_mem.get('hp', 100)))
                    r_mem['mp'] = max(0, to_int(b_mem.get('mp', 50)))
                    r_mem['status'] = b_mem.get('status', '良好')
        if 'logs' in battle_state:
            battle_state['logs'].append("⚡【輪迴管理員指令】觸發強制抹殺！直接取得戰鬥勝利！")
        renpy.end_interaction("win")


# ==============================================================================
# 戰鬥畫面介面 (battle_screen) - 賽博全息 HUD 6vs6 旗艦版
# ==============================================================================
screen battle_screen(battle_state):

    $ ensure_six_enemies(battle_state)

    $ round_num = battle_state.get('round_number', 1)
    $ player_team = battle_state.get('player_team', [])
    $ enemies = battle_state.get('enemies', [])
    $ battle_logs = battle_state.get('logs', [])
    $ current_turn_name = battle_state.get('current_turn_name', '我方行動階段')
    $ is_player_turn = battle_state.get('is_player_turn', True)
    $ selected_actor = battle_state.get('selected_actor', None)
    $ target_mode = battle_state.get('target_mode', None)
    $ selected_skill = battle_state.get('selected_skill', None)
    
    # 距離與環境資訊
    $ dist_val, dist_tier_name, dist_code, dist_penalty = get_distance_info(battle_state)
    $ timeline_queue = get_action_order_queue(battle_state)
    $ cur_world = battle_state.get('world_id', 'zombie')
    
    $ world_env_titles = {
        "zombie": "☣️ 生化高溫毒氣: -3% HP/回合",
        "space": "🌌 太空失重真空: 火藥槍械封印",
        "paranormal": "👻 陰煞之氣漫延: 物理免疫 & -5 MP/回合",
        "magic": "🔮 奧術狂暴共鳴: 魔法傷害 +30%",
        "causality": "🔴 死神因果律: 隨機死神追殺陷阱"
    }
    $ env_title_txt = world_env_titles.get(cur_world, "🟢 標準物理常數環境")

    python:
        for _m in player_team:
            for _k in ('hp', 'max_hp', 'mp', 'max_mp', 'gene_lock', 'atk_bonus', 'con', 'str', 'spd', 'int', 'mnd'):
                if _k in _m:
                    _m[_k] = to_int(_m[_k], 100 if 'hp' in _k else 0)
            # 確保主角顧臨淵定位為近戰，冷月頭像載入專屬立繪
            if "顧臨淵" in str(_m.get('name', '')) and _m.get('equipped_main_hand') == 'weapon_gauss_rifle':
                _m['equipped_main_hand'] = 'weapon_plasma_katana'
                _m['combat_role'] = '近戰格鬥 / 異數破局者'
            if "冷月" in str(_m.get('name', '')):
                _m['avatar'] = 'images/coldmoon.PNG'

            # 確保第 1 回合 AP、Max_AP 與行動狀態正確初始化 (基礎固定 4 AP)
            if 'max_ap' not in _m or _m.get('max_ap') is None or to_int(_m.get('max_ap', 0)) <= 0:
                _m['max_ap'] = 4
            if 'ap' not in _m or _m.get('ap') is None or to_int(_m.get('ap', 0)) <= 0 and not _m.get('has_acted', False):
                _m['ap'] = 4
            if 'has_acted' not in _m:
                _m['has_acted'] = False
            if 'has_attacked' not in _m:
                _m['has_attacked'] = False
            if 'is_gene_burst' not in _m:
                _m['is_gene_burst'] = False
            if 'is_aimed' not in _m:
                _m['is_aimed'] = False
                
        for _e in enemies:
            for _k in ('hp', 'max_hp', 'atk', 'spd'):
                if _k in _e:
                    _e[_k] = to_int(_e[_k], 50 if 'hp' in _k else 15)

    $ alive_members = [m for m in player_team if to_int(m.get('hp', 0)) > 0]
    $ unacted_members = [m for m in alive_members if not m.get('has_acted', False) and to_int(m.get('ap', m.get('max_ap', 4))) > 0]
    $ alive_enemies = [e for e in enemies if to_int(e.get('hp', 0)) > 0]

    # 若未手動選取，自動預設選定第一位待命隊員，確保進入戰鬥後面板立即處於就緒狀態
    if (selected_actor is None or selected_actor.get('has_acted', False) or to_int(selected_actor.get('hp', 0)) <= 0 or to_int(selected_actor.get('ap', 0)) <= 0) and len(unacted_members) > 0 and is_player_turn:
        $ battle_state['selected_actor'] = unacted_members[0]
        $ selected_actor = unacted_members[0]

    window:
        background "#0d1117"
        xysize (1920, 1080)

    frame:
        xalign 0.5 yalign 0.5
        xysize (1860, 1040)
        padding (20, 12)
        background "#101624f2"

        vbox:
            spacing 6
            xalign 0.5

            # =========================================================
            # 1. 頂部列：速度行動順序條 (Timeline Ribbon) + 戰場全息膠囊
            # =========================================================
            hbox:
                xalign 0.5
                spacing 15
                
                # 速度出手順序佇列 Ribbon
                frame:
                    background "#080c14dd"
                    padding (10, 4)
                    xysize (950, 52)
                    hbox:
                        spacing 6
                        yalign 0.5
                        text "【 ⚡ 速度行動序 】" size 13 color "#00ffff" bold True yalign 0.5
                        viewport:
                            xysize (800, 44)
                            mousewheel True
                            draggable True
                            hbox:
                                spacing 8
                                yalign 0.5
                                for q_item in timeline_queue:
                                    $ q_is_p = q_item['is_player']
                                    $ q_name = q_item['name']
                                    $ q_spd = q_item['spd']
                                    $ q_active = (selected_actor and selected_actor == q_item.get('actor'))
                                    frame:
                                        xysize (115, 38)
                                        if q_active:
                                            background "#ffcc0044"
                                        elif q_is_p:
                                            background "#00ffff22"
                                        else:
                                            background "#ff336622"
                                        padding (4, 2)
                                        hbox:
                                            spacing 4
                                            yalign 0.5
                                            add q_item['avatar'] xysize (28, 28) yalign 0.5
                                            vbox:
                                                spacing 0
                                                text q_name[:4] size 11 color ("#00ffff" if q_is_p else "#ff6666") bold True
                                                text f"SPD:{q_spd}" size 10 color "#aaaaaa"

                # 戰場距離膠囊
                frame:
                    background ("#ff336633" if dist_code == "far" else ("#ffaa0033" if dist_code == "mid" else "#00ff6633"))
                    padding (12, 6)
                    yalign 0.5
                    text f"📍 距敵: {dist_val}m ({dist_tier_name})" size 14 color ("#ff9999" if dist_code == "far" else ("#ffff66" if dist_code == "mid" else "#66ff66")) bold True

                # 戰場環境膠囊
                frame:
                    background "#9933ff22"
                    padding (12, 6)
                    yalign 0.5
                    text env_title_txt size 14 color "#ddaaff" bold True

                # 回合膠囊
                frame:
                    background "#00ffff22"
                    padding (12, 6)
                    yalign 0.5
                    text f"⏱️ 第 {round_num} 回合 · {current_turn_name}" size 14 color "#00ffff" bold True

            null height 2

            # =========================================================
            # 2. 中部戰場攻防區：左側我方小隊 (6人)，右側敵方怪群 (6隻)
            # =========================================================
            hbox:
                spacing 20
                xalign 0.5

                # --------------------------------
                # 左側：我方小隊列表 (6人)
                # --------------------------------
                vbox:
                    spacing 4
                    xysize (920, 680)
                    
                    hbox:
                        spacing 15
                        text "【 我方作戰編隊 (6人上限) 】" size 18 color "#00ffff" bold True yalign 0.5
                        if is_player_turn and len(unacted_members) > 0:
                            textbutton "⚔️ 全體普攻":
                                action Function(process_team_all_attack, battle_state)
                                text_size 13 text_idle_color "#00ff66" text_hover_color "#ffffff"
                            textbutton "🛡️ 全體防禦":
                                action Function(process_team_all_defend, battle_state)
                                text_size 13 text_idle_color "#66ccff" text_hover_color "#ffffff"
                    
                    viewport:
                        xysize (920, 645)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vbox:
                            spacing 6
                            for idx, member in enumerate(player_team):
                                $ m_name = member.get('name', '未知')
                                $ m_hp = to_int(member.get('hp', 100), 100)
                                $ m_max_hp = to_int(member.get('max_hp', 100), 100)
                                $ m_mp = to_int(member.get('mp', 50), 50)
                                $ m_max_mp = to_int(member.get('max_mp', 50), 50)
                                $ m_status = member.get('status', '良好')
                                $ m_has_acted = member.get('has_acted', False)
                                $ m_gene = to_int(member.get('gene_lock', 0), 0)
                                $ m_pos = member.get('position', 'frontline')
                                $ m_ap = to_int(member.get('ap', 4), 4)
                                $ m_max_ap = to_int(member.get('max_ap', 4), 4)
                                $ m_burst = member.get('is_gene_burst', False)
                                $ m_aimed = member.get('is_aimed', False)
                                $ m_tier = get_actor_power_tier(member)
                                
                                $ is_active = (selected_actor == member)
                                $ is_alive = (m_hp > 0)
                                $ can_act = is_alive and (not m_has_acted) and (m_ap > 0) and is_player_turn

                                frame:
                                    xysize (895, None)
                                    if not is_alive:
                                        background "#1a111166"
                                    elif is_active:
                                        background "#1e2d4add"
                                    elif m_has_acted or m_ap <= 0:
                                        background "#12141ecc"
                                    else:
                                        background "#151c2caa"
                                    padding (10, 6)
                                    
                                    vbox:
                                        spacing 3
                                        
                                        button:
                                            xysize (875, 62)
                                            if can_act:
                                                action SetDict(battle_state, 'selected_actor', None if is_active else member)
                                            
                                            hbox:
                                                spacing 10
                                                yalign 0.5
                                                
                                                frame:
                                                    xysize (52, 52)
                                                    background ("#ffcc00aa" if is_active else ("#00ffff44" if is_alive else "#44444444"))
                                                    padding (2, 2)
                                                    yalign 0.5
                                                    $ m_av = member.get('avatar', 'images/core_idle.PNG')
                                                    add m_av xysize (48, 48) xalign 0.5 yalign 0.5

                                                vbox:
                                                    spacing 2
                                                    hbox:
                                                        spacing 8
                                                        text m_name size 16 color ("#00ffff" if is_active else ("#ffffff" if is_alive else "#777777")) bold True
                                                        text ("【前排🛡️】" if m_pos == "frontline" else "【後排🏹】") size 12 color ("#ffaa00" if m_pos=="frontline" else "#00ffcc") bold True yalign 0.5
                                                        text f"Tier {m_tier}" size 11 color ("#ffcc00" if m_tier >= 2 else "#aaaaaa") bold True yalign 0.5
                                                        
                                                        # AP 水晶粒
                                                        $ ap_beads = "💎" * m_ap + "⚪" * max(0, m_max_ap - m_ap)
                                                        text f"AP: {ap_beads} ({m_ap}/{m_max_ap})" size 12 color "#00ffff" bold True yalign 0.5
                                                        
                                                        if not is_alive:
                                                            text "【💀 已倒下】" size 12 color "#ff4444" bold True yalign 0.5
                                                        elif m_has_acted or m_ap <= 0:
                                                            text "【⏳ 已完成】" size 12 color "#888888" yalign 0.5
                                                        else:
                                                            text "【⚡ 待命】" size 12 color "#00ff66" bold True yalign 0.5

                                                        if m_aimed:
                                                            text "【🎯 已瞄準】" size 11 color "#ffaa00" bold True yalign 0.5
                                                        if m_burst:
                                                            text "【🧬 爆發中】" size 11 color "#ff00ff" bold True yalign 0.5

                                                    hbox:
                                                        spacing 12
                                                        text f"HP: {m_hp}/{m_max_hp}" size 12 color ("#ff6666" if is_alive else "#555555")
                                                        text f"MP: {m_mp}/{m_max_mp}" size 12 color "#66ccff"
                                                        if member.get('neili_max', 0) > 0:
                                                            text f"內力: {member.get('neili_current',0)}/{member.get('neili_max',0)}" size 11 color "#ffaa00"
                                                        if member.get('blood_max', 0) > 0:
                                                            text f"血魄: {member.get('blood_current',0)}/{member.get('blood_max',0)}" size 11 color "#ff4444"
                                                        if member.get('calc_max', 0) > 0:
                                                            text f"算力: {member.get('calc_current',0)}/{member.get('calc_max',0)}" size 11 color "#00ffcc"

                                        # 行動按鈕列 (Active Command Panel)
                                        if is_active and can_act:
                                            $ m_cur_ap = to_int(member.get('ap', member.get('max_ap', 4)))
                                            $ m_has_attacked = member.get('has_attacked', False)
                                            $ can_do_attack = (m_cur_ap >= 3 and not m_has_attacked)
                                            $ can_do_aim_shoot = (m_cur_ap >= 4 and not m_has_attacked)
                                            $ can_do_skill = (m_cur_ap >= 4 and not m_has_attacked)
                                            $ can_do_defend = (m_cur_ap >= 1)
                                            $ can_do_switch = (m_cur_ap >= 1)
                                            $ can_do_burst = (m_cur_ap >= 1 and m_gene > 0 and not m_burst)
                                            $ can_do_item = (m_cur_ap >= 1)
                                            $ actor_skills = get_actor_skills(member)
                                            
                                            null height 2
                                            hbox:
                                                spacing 6
                                                yalign 0.5
                                                
                                                $ is_mem_gun = check_actor_has_gun(member)
                                                
                                                # 1. 徒手/近戰攻擊 (每個人都有)
                                                if dist_val > 0:
                                                    textbutton "⚔️ 徒手/近戰 (待怪物逼近)":
                                                        action Function(log_distance_warning, battle_state, member, dist_val)
                                                        sensitive True
                                                        text_size 12
                                                        text_idle_color "#ff6666"
                                                        text_hover_color "#ffffff"
                                                elif m_has_attacked:
                                                    textbutton "⚔️ 近戰 (本回合已攻擊)":
                                                        action None
                                                        sensitive False
                                                        text_size 12
                                                        text_idle_color "#555555"
                                                else:
                                                    textbutton ("⚔️ 徒手/近戰 (3 AP)" if can_do_attack else "⚔️ 近戰 (AP不足)"):
                                                        action (SetDict(battle_state, 'target_mode', 'melee') if can_do_attack else None)
                                                        sensitive can_do_attack
                                                        text_size 12
                                                        text_idle_color ("#00ff66" if target_mode == 'melee' else ("#ffffff" if can_do_attack else "#555555"))

                                                # 2. 槍械射擊 (只有裝備槍械的單位才有，遠距離自動整合瞄準為4 AP，中/近距離為3 AP)
                                                if is_mem_gun:
                                                    if m_has_attacked:
                                                        textbutton "🏹 射擊 (本回合已射擊)":
                                                            action None
                                                            sensitive False
                                                            text_size 12
                                                            text_idle_color "#555555"
                                                    elif dist_val == 2:
                                                        textbutton ("🎯 瞄準射擊 (4 AP)" if can_do_aim_shoot else "🎯 瞄準射擊 (需4 AP)"):
                                                            action (SetDict(battle_state, 'target_mode', 'shoot') if can_do_aim_shoot else None)
                                                            sensitive can_do_aim_shoot
                                                            text_size 12
                                                            text_idle_color ("#ffff00" if target_mode == 'shoot' else ("#ffff66" if can_do_aim_shoot else "#555555"))
                                                    elif dist_val == 1:
                                                        textbutton ("🏹 槍械射擊 (3 AP)" if can_do_attack else "🏹 射擊 (AP不足)"):
                                                            action (SetDict(battle_state, 'target_mode', 'shoot') if can_do_attack else None)
                                                            sensitive can_do_attack
                                                            text_size 12
                                                            text_idle_color ("#00ffff" if target_mode == 'shoot' else ("#00ffff" if can_do_attack else "#555555"))
                                                    else:
                                                        textbutton ("🏹 貼身射擊 (3 AP)" if can_do_attack else "🏹 射擊 (AP不足)"):
                                                            action (SetDict(battle_state, 'target_mode', 'shoot') if can_do_attack else None)
                                                            sensitive can_do_attack
                                                            text_size 12
                                                            text_idle_color ("#00ffff" if target_mode == 'shoot' else ("#00ffff" if can_do_attack else "#555555"))

                                                if m_has_attacked:
                                                    textbutton "🔥 招式 (本回合已行動)":
                                                        action None
                                                        sensitive False
                                                        text_size 12
                                                        text_idle_color "#555555"
                                                else:
                                                    textbutton ("🔥 招式 (4 AP)" if can_do_skill else "🔥 招式 (AP不足)"):
                                                        action (SetDict(battle_state, 'target_mode', 'skill_menu') if can_do_skill else None)
                                                        sensitive can_do_skill
                                                        text_size 12
                                                        text_idle_color ("#ffaa00" if target_mode in ('skill_menu', 'cast_skill') else ("#ffffff" if can_do_skill else "#555555"))

                                                textbutton ("🛡️ 防禦 (1 AP)" if can_do_defend else "🛡️ 防禦 (AP不足)"):
                                                    action (Function(process_player_defend, battle_state, member) if can_do_defend else None)
                                                    sensitive can_do_defend
                                                    text_size 12
                                                    text_idle_color ("#66ccff" if can_do_defend else "#555555")

                                                textbutton (f"🔄 {'換後排' if m_pos=='frontline' else '換前排'} (1 AP)" if can_do_switch else "🔄 換位 (AP不足)"):
                                                    action (Function(process_switch_position, battle_state, member) if can_do_switch else None)
                                                    sensitive can_do_switch
                                                    text_size 12
                                                    text_idle_color ("#ddaaff" if can_do_switch else "#555555")

                                                if m_gene > 0 and not m_burst:
                                                    textbutton ("🧬 基因鎖 (1 AP->+2)" if can_do_burst else "🧬 基因鎖 (AP不足)"):
                                                        action (Function(process_gene_burst, battle_state, member) if can_do_burst else None)
                                                        sensitive can_do_burst
                                                        text_size 12
                                                        text_idle_color ("#ff44ff" if can_do_burst else "#555555")

                                                textbutton ("🎒 背包 (1 AP)" if can_do_item else "🎒 背包 (AP不足)"):
                                                    action (SetDict(battle_state, 'target_mode', 'item_menu') if can_do_item else None)
                                                    sensitive can_do_item
                                                    text_size 12
                                                    text_idle_color ("#ff88ff" if target_mode == 'item_menu' else ("#ffffff" if can_do_item else "#555555"))

                                                textbutton "⏩ 待命":
                                                    action Function(end_actor_turn, battle_state, member)
                                                    text_size 12 text_idle_color "#ffaa88"

                                            # 招式展開清單
                                            if target_mode in ('skill_menu', 'cast_skill'):
                                                frame:
                                                    background "#0d1424ee"
                                                    padding (8, 6)
                                                    vbox:
                                                        spacing 3
                                                        text "【 選擇施放招式 (4 AP) 】" size 12 color "#ffaa00"
                                                        if not actor_skills:
                                                            text "⚠️ （此新人尚未融合任何輪迴血統或解鎖基因鎖，暫無專屬戰技）" size 12 color "#888888"
                                                        else:
                                                            for sk in actor_skills:
                                                                $ sk_name = sk.get('name', '招式')
                                                                $ sk_cost = sk.get('energy_cost', sk.get('cost_energy', 0))
                                                                $ sk_ap_cost = to_int(sk.get('ap_cost', 4), 4)
                                                                $ is_sk_active = (selected_skill == sk)
                                                                $ can_cast_this_sk = (m_cur_ap >= sk_ap_cost)
                                                                hbox:
                                                                    spacing 8
                                                                    if can_cast_this_sk:
                                                                        textbutton f"★ {sk_name} ({sk_ap_cost} AP / 消耗 {sk_cost})":
                                                                            if sk.get('is_heal', False):
                                                                                action Function(process_player_skill, battle_state, member, None, sk)
                                                                            else:
                                                                                action [SetDict(battle_state, 'selected_skill', sk), SetDict(battle_state, 'target_mode', 'cast_skill')]
                                                                            text_size 12 text_idle_color ("#ffff00" if is_sk_active else "#00ffff")
                                                                    else:
                                                                        textbutton f"★ {sk_name} (AP不足)":
                                                                            action None
                                                                            sensitive False
                                                                            text_size 12 text_idle_color "#555555"

                                            # 背包物資展開清單
                                            if target_mode == 'item_menu':
                                                $ cur_inv = get_inventory() if 'get_inventory' in globals() else []
                                                $ usable_inv_items = []
                                                for ent in cur_inv:
                                                    $ itm_obj = get_item_by_id(ent["id"]) if 'get_item_by_id' in globals() else None
                                                    if itm_obj and (itm_obj.get("usable_in_battle", False) or itm_obj.get("type") in ("consumable", "tactical")):
                                                        $ usable_inv_items.append((ent, itm_obj))
                                                frame:
                                                    background "#0d1424ee"
                                                    padding (8, 6)
                                                    vbox:
                                                        spacing 3
                                                        text "【 戰術背包 · 戰場物資 (1 AP) 】" size 12 color "#ff88ff"
                                                        if not usable_inv_items:
                                                            text "背包內目前無可於戰鬥中使用的消耗品或爆破道具。" size 12 color "#888888"
                                                        else:
                                                            hbox:
                                                                spacing 10
                                                                for ent, itm_obj in usable_inv_items:
                                                                    $ itm_id = itm_obj.get("id")
                                                                    $ itm_name = itm_obj.get("name")
                                                                    $ itm_cnt = ent.get("count", 1)
                                                                    if can_do_item:
                                                                        textbutton f"★ {itm_name} x{itm_cnt}":
                                                                            action Function(process_use_item, battle_state, member, itm_id)
                                                                            text_size 12 text_idle_color "#66ff66" text_hover_color "#ffffff"
                                                                    else:
                                                                        textbutton f"★ {itm_name} (AP不足)":
                                                                            action None
                                                                            sensitive False
                                                                            text_size 12 text_idle_color "#555555"

                # --------------------------------
                # 右側：敵方 6 隻目標列表
                # --------------------------------
                vbox:
                    spacing 4
                    xysize (880, 680)
                    text "【 敵方威脅目標 (6體) 】" size 18 color "#ff4444" bold True
                    
                    viewport:
                        xysize (880, 645)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        
                        vbox:
                            spacing 6
                            for e_idx, enemy in enumerate(enemies):
                                $ e_name = enemy.get('name', '喪屍')
                                $ e_hp = to_int(enemy.get('hp', 50), 50)
                                $ e_max_hp = to_int(enemy.get('max_hp', 50), 50)
                                $ e_atk = to_int(enemy.get('atk', 15), 15)
                                $ e_status = enemy.get('status', '正常')
                                $ e_tier = get_enemy_power_tier(enemy)
                                $ is_enemy_alive = (e_hp > 0)
                                $ is_sel_gun = check_actor_has_gun(selected_actor) if selected_actor else False
                                $ sel_actor_ap = to_int(selected_actor.get('ap', 0)) if selected_actor else 0
                                $ shoot_req_ap = (4 if dist_val == 2 else 3)
                                $ has_enough_ap_to_hit = (sel_actor_ap >= 3) if target_mode in ('melee', 'attack') else ((sel_actor_ap >= shoot_req_ap) if target_mode == 'shoot' else (sel_actor_ap >= to_int(selected_skill.get('ap_cost', 4), 4) if selected_skill else False))
                                
                                $ is_melee_blocked = (target_mode in ('melee', 'attack') and dist_val > 0)
                                $ is_shoot_blocked = (target_mode == 'shoot' and (not is_sel_gun or sel_actor_ap < shoot_req_ap))
                                
                                $ can_target = is_enemy_alive and (target_mode in ('melee', 'shoot', 'attack', 'cast_skill')) and has_enough_ap_to_hit and not is_melee_blocked and not is_shoot_blocked

                                button:
                                    xysize (855, 88)
                                    if not is_enemy_alive:
                                        background "#11111166"
                                    elif can_target:
                                        background "#661828dd"
                                        hover_background "#882035ee"
                                    else:
                                        background "#22141a99"
                                    padding (10, 6)
                                    
                                    if can_target:
                                        if target_mode in ('melee', 'attack'):
                                            action Function(process_player_attack, battle_state, selected_actor, enemy, "melee")
                                        elif target_mode == 'shoot':
                                            action Function(process_player_attack, battle_state, selected_actor, enemy, "shoot")
                                        elif target_mode == 'cast_skill' and selected_skill:
                                            action Function(process_player_skill, battle_state, selected_actor, enemy, selected_skill)
                                    elif is_enemy_alive and target_mode in ('melee', 'attack') and is_melee_blocked:
                                        action Function(log_distance_warning, battle_state, selected_actor, dist_val)

                                    hbox:
                                        spacing 10
                                        yalign 0.5

                                        frame:
                                            xysize (56, 56)
                                            background ("#ff336644" if is_enemy_alive else "#33333344")
                                            padding (2, 2)
                                            yalign 0.5
                                            $ e_av = enemy.get('avatar', 'images/core_idle.PNG')
                                            if not e_av or e_av == 'images/core_idle.PNG':
                                                if '敏捷' in e_name or enemy.get('id') == 'agile_zombie':
                                                    $ e_av = 'images/agile_zombie.jpg'
                                                elif '腐屍' in e_name or enemy.get('id') == 'MOB_ZOMBIE_01' or '喪屍' in e_name:
                                                    $ e_av = 'images/zombie.jpg'
                                            add e_av xysize (52, 52) xalign 0.5 yalign 0.5

                                        vbox:
                                            spacing 2
                                            hbox:
                                                spacing 8
                                                text e_name size 16 color ("#ff6666" if is_enemy_alive else "#666666") bold True
                                                if not is_enemy_alive:
                                                    text "【💀 已被擊殺】" size 12 color "#777777" bold True yalign 0.5
                                                else:
                                                    $ e_pos = enemy.get('position', 'frontline')
                                                    $ e_flight = enemy.get('is_flight', False) or "飛行" in enemy.get('status', '') or "翅膀" in enemy.get('name', '')
                                                    text ("【前排🛡️】" if e_pos == "frontline" else "【後排🏹】") size 11 color ("#ffaa00" if e_pos=="frontline" else "#00ffcc") yalign 0.5
                                                    text f"Tier {e_tier}" size 11 color ("#ff4444" if e_tier >= 2 else "#aaaaaa") bold True yalign 0.5
                                                    if e_flight:
                                                        text "【🕊️ 飛行】" size 11 color "#ddaaff" bold True yalign 0.5
                                                    text f"ATK: {e_atk}" size 12 color "#ffaa88" yalign 0.5

                                            hbox:
                                                spacing 12
                                                text f"HP: {e_hp}/{e_max_hp}" size 12 color ("#ff4444" if is_enemy_alive else "#555555")
                                                text f"特性: {e_status}" size 12 color "#aaaaaa"
                                                if is_enemy_alive:
                                                    if target_mode in ('melee', 'attack'):
                                                        if dist_val > 0:
                                                            text f"【 ⏳ 怪物處於{dist_tier_name} (請防禦/待命等待怪物逼近) 】" size 12 color "#ff9999" bold True yalign 0.5
                                                        else:
                                                            text "【 ⚔️ 點擊鎖定：徒手/近戰攻擊 (3 AP) 】" size 12 color "#00ff66" bold True yalign 0.5
                                                    elif target_mode == 'shoot':
                                                        if not is_sel_gun:
                                                            text "【 ⚠️ 該隊員未裝備槍械武器 】" size 12 color "#888888" bold True yalign 0.5
                                                        elif dist_val == 2:
                                                            text "【 🎯 點擊鎖定：瞄準射擊 (4 AP / 必中暴擊) 】" size 12 color "#ffff00" bold True yalign 0.5
                                                        elif dist_val == 1:
                                                            text "【 🏹 點擊鎖定：槍械射擊 (3 AP / 最佳射程) 】" size 12 color "#00ffff" bold True yalign 0.5
                                                        else:
                                                            text "【 🏹 點擊鎖定：貼身射擊 (3 AP) 】" size 12 color "#00ffff" bold True yalign 0.5
                                                    elif target_mode == 'cast_skill' and selected_skill:
                                                        text f"【 💥 點擊釋放：{selected_skill.get('name','')} 】" size 12 color "#ffff00" bold True yalign 0.5

                                            if battle_state.get('show_enemy_intents', False) and is_enemy_alive:
                                                text f"👁️ 【基因鎖預判】意圖撲擊我方前排單位 (預計造成 {e_atk} 點物理傷害)" size 11 color "#ffdd44" bold True

            null height 2

            # =========================================================
            # 3. 底部列：黑客終端風格戰鬥日誌 (Combat Terminal Log)
            # =========================================================
            frame:
                xysize (1820, 140)
                background "#080c14ee"
                padding (12, 6)
                
                vbox:
                    spacing 2
                    hbox:
                        spacing 15
                        text "【 📜 戰場戰術日誌 (Terminal Log) 】" size 13 color "#00ffff" bold True yalign 0.5
                        text f"共 {len(battle_logs)} 筆紀錄" size 12 color "#888888" yalign 0.5
                        textbutton "【 🔍 展開完整日誌視窗 】":
                            action SetDict(battle_state, "show_full_logs", True)
                            text_size 12 text_idle_color "#ffcc00" text_hover_color "#ffffff" yalign 0.5

                    viewport id "battle_log_vp":
                        xysize (1790, 98)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 1.0
                        
                        vbox:
                            spacing 2
                            for log in battle_logs:
                                $ log_str = str(log)
                                if "===" in log_str or "回合" in log_str:
                                    text f"• {log_str}" size 12 color "#ffdd88" bold True substitute False
                                elif "重創" in log_str or "倒下" in log_str or "陣亡" in log_str or "MISS" in log_str or "跳彈" in log_str or "壓制" in log_str:
                                    text f"• {log_str}" size 12 color "#ff6666" bold True substitute False
                                elif "回復" in log_str or "防禦" in log_str or "勝利" in log_str or "推進" in log_str or "瞄準" in log_str:
                                    text f"• {log_str}" size 12 color "#00ff66" substitute False
                                elif "攻擊" in log_str or "傷害" in log_str or "施展" in log_str:
                                    text f"• {log_str}" size 12 color "#ffffff" substitute False
                                else:
                                    text f"• {log_str}" size 12 color "#aaaaaa" substitute False

            null height 2

            # =========================================================
            # 4. 底部全域功能按鈕
            # =========================================================
            hbox:
                spacing 20
                xalign 0.5
                
                if is_player_turn and len(unacted_members) > 0:
                    textbutton "【 ⚔️ 全體普通攻擊 】":
                        action Function(process_team_all_attack, battle_state)
                        text_size 15 text_idle_color "#00ff66" text_hover_color "#ffffff"

                    textbutton "【 🛡️ 全體防禦 】":
                        action Function(process_team_all_defend, battle_state)
                        text_size 15 text_idle_color "#66ccff" text_hover_color "#ffffff"

                    textbutton "【 ⏩ 結束我方回合 】":
                        action Function(process_manual_end_turn, battle_state)
                        text_size 15 text_idle_color "#ffaa00" text_hover_color "#ffffff"

                textbutton "【 ⚡ 直接勝利 (管理員) 】":
                    action Function(process_instant_win, battle_state)
                    text_size 15 text_idle_color "#ffcc00" text_hover_color "#ffffff"

                if battle_state.get('is_simulation'):
                    textbutton "【 🛑 結束全息模擬 】":
                        action Return("end_simulation")
                        text_size 15 text_idle_color "#ff4444" text_hover_color "#ff8888"
                else:
                    textbutton "【 🚪 結束戰鬥 / 撤退 】":
                        action Return("end_battle")
                        text_size 15 text_idle_color "#ff4444" text_hover_color "#ff8888"

    # =========================================================
    # 5. 完整戰鬥歷史紀錄彈窗
    # =========================================================
    if battle_state.get('show_full_logs', False):
        window:
            background "#000000dd"
            xysize (1920, 1080)

        frame:
            xalign 0.5 yalign 0.5
            xysize (1400, 860)
            background "#0d121ff8"
            padding (30, 25)

            vbox:
                spacing 12
                xalign 0.5

                hbox:
                    spacing 30
                    xalign 0.5
                    text "【 📜 完整戰鬥歷史紀錄與回合成效分析 】" size 23 color "#ffcc00" bold True yalign 0.5
                    text f"累積總紀錄：{len(battle_logs)} 筆" size 15 color "#00ffff" yalign 0.5

                viewport id "full_battle_logs_vp":
                    xysize (1340, 680)
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yinitial 1.0

                    vbox:
                        spacing 4
                        for log_idx, log in enumerate(battle_logs):
                            $ log_str = str(log)
                            if "===" in log_str or "回合" in log_str:
                                frame:
                                    xysize (1310, 32)
                                    background "#1e2842aa"
                                    padding (8, 3)
                                    text f"★ {log_str}" size 13 color "#ffdd88" bold True substitute False
                            elif "重創" in log_str or "倒下" in log_str or "陣亡" in log_str or "MISS" in log_str or "跳彈" in log_str or "壓制" in log_str:
                                text f"• ({log_idx+1}) {log_str}" size 13 color "#ff6666" bold True substitute False
                            elif "回復" in log_str or "防禦" in log_str or "勝利" in log_str or "推進" in log_str or "瞄準" in log_str:
                                text f"• ({log_idx+1}) {log_str}" size 13 color "#00ff66" substitute False
                            elif "攻擊" in log_str or "傷害" in log_str or "施展" in log_str:
                                text f"• ({log_idx+1}) {log_str}" size 13 color "#ffffff" substitute False
                            else:
                                text f"• ({log_idx+1}) {log_str}" size 13 color "#aaaaaa" substitute False

                textbutton "【 ❌ 關閉紀錄視窗，返回戰鬥 】":
                    xalign 0.5
                    action SetDict(battle_state, "show_full_logs", False)
                    text_size 18 text_idle_color "#ff4444" text_hover_color "#ff8888"
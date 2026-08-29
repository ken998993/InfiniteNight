# ==========================================
# 遊戲全域資料與初始化方法集中管理
# ==========================================
init python:
    import json

    # 1. 封裝取得團隊名單的方法 (自 jsonData/team_data.json 讀取)
    def get_team_roster():
        global team_roster
        if 'team_roster' in globals() and team_roster:
            return team_roster
        try:
            with renpy.file("jsonData/team_data.json") as f:
                team_roster = json.load(f)
        except Exception as e:
            team_roster = [
                {
                    "name": "主角 (你)",
                    "role": "資深隊員",
                    "combat_role": "全能平衡 / 成長型",
                    "bloodline": "無 (可兼修多重體系)",
                    "points": 1000,
                    "hp": 100, "max_hp": 100,
                    "mp": 50, "max_mp": 50,
                    "neili_current": 0, "neili_max": 100,
                    "blood_current": 0, "blood_max": 100,
                    "mental_current": 0, "mental_max": 0,
                    "qi_current": 0, "qi_max": 0,
                    "calc_current": 0, "calc_max": 0,
                    "gene_lock": 0, "survival_pressure": 0,
                    "status": "良好",
                    "skills": [],
                    "desc": "經歷了初步的試煉，正逐漸掌握主神空間的生存法則。"
                }
            ]
        return team_roster

    # 2. 封裝取得血統列表的方法 (自 jsonData/bloodlines.json 讀取)
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

    # 3. 核心：血統兌換與升級邏輯
    def purchase_bloodline(bloodline_id, grade_key, member_idx=0):
        global points, hp, team_roster
        roster = get_team_roster()
        if not roster or member_idx >= len(roster):
            return {"success": False, "msg": "找不到目標隊員資料。"}
            
        target_member = roster[member_idx]
        b_data = get_bloodline_by_id(bloodline_id)
        if not b_data:
            return {"success": False, "msg": "主神資料庫中無此血統紀錄。"}
            
        grades = b_data.get("grades", {})
        if grade_key not in grades:
            return {"success": False, "msg": f"無此血統階級：{grade_key}。"}
            
        grade_info = grades[grade_key]
        cost_points = grade_info.get("points", 0)
        
        current_pts = points if member_idx == 0 else target_member.get("points", 0)
        if current_pts < cost_points:
            return {
                "success": False,
                "msg": f"【主神提示】生存點數不足！\n需要生存點數 {cost_points} 點，目前僅擁有 {current_pts} 點。"
            }
            
        # 扣除生存點數
        if member_idx == 0:
            points -= cost_points
            target_member["points"] = points
        else:
            target_member["points"] = target_member.get("points", 0) - cost_points
            
        # 套用血統名稱
        grade_name = grade_info.get("name", f"{grade_key}級 {b_data.get('name')}")
        target_member["bloodline"] = grade_name
        
        # 套用屬性提升
        attrs = grade_info.get("attributes", {})
        for attr_key, attr_val in attrs.items():
            if attr_key == "hp":
                target_member["max_hp"] = max(target_member.get("max_hp", 100), target_member.get("max_hp", 100) + attr_val)
                target_member["hp"] = target_member["max_hp"]
                if member_idx == 0:
                    hp = target_member["hp"]
            elif attr_key == "max_hp":
                target_member["max_hp"] = max(target_member.get("max_hp", 100), attr_val)
                target_member["hp"] = target_member["max_hp"]
                if member_idx == 0:
                    hp = target_member["hp"]
            elif attr_key == "mp":
                target_member["max_mp"] = target_member.get("max_mp", 50) + attr_val
                target_member["mp"] = target_member["max_mp"]
            elif attr_key == "max_mp":
                target_member["max_mp"] = max(target_member.get("max_mp", 50), attr_val)
                target_member["mp"] = target_member["max_mp"]
            elif attr_key in ("blood_max", "neili_max", "mental_max", "qi_max", "calc_max"):
                target_member[attr_key] = max(target_member.get(attr_key, 0), attr_val)
                curr_key = attr_key.replace("_max", "_current")
                target_member[curr_key] = target_member[attr_key]
            elif attr_key in ("blood_current", "neili_current", "mental_current", "qi_current", "calc_current"):
                target_member[attr_key] = max(target_member.get(attr_key, 0), attr_val)
            else:
                target_member[attr_key] = attr_val
                
        # 賦予專屬技能
        new_skills = grade_info.get("skills", [])
        target_member["skills"] = new_skills
        
        return {
            "success": True,
            "msg": f"【主神強化完成】一道乳白色神聖光柱降臨，你已成功融合【{grade_name}】！\n生命上限提升，能量池完全啟動，並已自動掌握 {len(new_skills)} 項全新血統專屬招式！",
            "bloodline_name": grade_name,
            "skills": new_skills
        }

    # 4. 初始化全域變數 (讀取 JSON 填入 team_roster)
    if 'team_roster' not in store.__dict__:
        team_roster = get_team_roster()

    if 'points' not in store.__dict__:
        points = 1000

    if 'bloodlines_catalog' not in store.__dict__:
        bloodlines_catalog = get_bloodlines_data()

    # 5. 主神空間管理員特權指令解析核心
    def process_admin_command(cmd_str):
        global points, hp, team_roster
        if not cmd_str:
            return "【主神系統】指令不可為空。"
        cmd = cmd_str.strip().lower()
        roster = get_team_roster()
        player = roster[0] if roster and len(roster) > 0 else None
        
        # 1. 增加 100000 點生存點數指令 (如 addpoints / addpoint)
        if cmd in ("addpoints", "addpoint"):
            added = 100000
            points += added
            if player:
                player["points"] = points
            return f"【主神管理員權限生效】檢測到最高管理員權限：成功注入 {added} 點生存點數！\n目前可用生存點數：{points} 點。"
            
        # 2. 自訂增加點數 (如 addpoints 50000 或 points 50000)
        elif cmd.startswith("addpoints ") or cmd.startswith("points "):
            try:
                parts = cmd.split()
                val = int(parts[1])
                points += val
                if player:
                    player["points"] = points
                return f"【主神管理員權限生效】成功調整生存點數：+{val} 點！\n目前可用生存點數：{points} 點。"
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
            return "【主神管理員權限生效】聖光洗禮！全員重創已完全治癒，生命值與所有能量池已全部蓄滿！"
            
        # 4. 基因鎖解鎖指令
        elif cmd in ("genelock", "gene5", "unlockgene", "gene"):
            if player:
                player["gene_lock"] = 5
                player["survival_pressure"] = 0
            return "【主神管理員權限生效】強行破除基因鏈桎梏！主角基因鎖已直達【第 5 階·聖人之境】！"
            
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
            return "【主神至高神明權限已激活】GM模式已開啟：\n• 生存點數 +999,999 點\n• 生命值上限突破至 9999\n• 全部能量池上限擴充至 1000\n• 基因鎖直接登頂第 5 階！"
            
        else:
            return f"【主神系統提示】未知特權指令「{cmd_str}」。\n\n支援的特權指令清單：\n• addpoints：增加 100,000 點生存點數\n• addpoints 50000：自訂增加指定點數\n• fullheal：生命與能量全部回滿\n• genelock：解鎖五階基因鎖\n• godmode：開啟無敵 GM 模式"

    # 6. 安全更新隊員點數的方法
    def update_member_points(new_points):
        global points, team_roster
        points = new_points
        roster = get_team_roster()
        if roster and len(roster) > 0:
            roster[0]["points"] = points
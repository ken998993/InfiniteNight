# ==============================================================================
# 📜 《輪迴世界》第三副本：日式靈異世界 · 咒怨凶宅 (the_grudge.rpy)
# 依據 developMd/13_Story_Stage_1_3_The_Grudge.md 規範實現
# ==============================================================================

# 定義關卡專屬角色對話物件
define lengyue = Character("冷月", color="#00ffcc", image="lengyue")
define xiangtian = Character("項天", color="#ff8844", image="xiangtian")
define suxiao = Character("蘇曉", color="#66ccff", image="suxiao")
define gulin = Character("顧臨淵", color="#00ffea")
define yanshuo = Character("言朔", color="#ddaaff")
define yeling = Character("葉靈 (道家天師)", color="#ffff00")
define moli_rookie = Character("莫離 (恐慌新人)", color="#ff9999")
define kayako = Character("咒怨伽椰子", color="#ff2222")

# 定義關卡背景圖元別名 (全圖縮放拉滿 1920x1080，消除黑邊與馬賽克邊)
image bg_japanese_haunted_house = Transform("images/trial_room.png", xsize=1920, ysize=1080)
image bg_tatami_room_dark = Transform("images/zombie_street.PNG", xsize=1920, ysize=1080)
image bg_staircase_curse = Transform("images/trial_room.png", xsize=1920, ysize=1080)

# ==========================================
# 關卡進入點 (相容 theGrudge 與 stage_1_3)
# ==========================================
label theGrudge:
    jump stage_1_3_the_grudge

label stage_1_3_the_grudge:
    scene bg_japanese_haunted_house with fade
    
    # -------------------------------------------------------------
    # 1. 傳送降臨與靈異氛圍 (資深小隊 + 新人葉靈 & 莫離)
    # -------------------------------------------------------------
    "【主神傳送光束消退，空氣中瀰漫著令人作嘔的陳舊霉味與刺骨怨氣……】"
    "【耳邊傳來一陣令人毛骨悚然的骨骼扭曲折疊聲 —— 咯咯咯咯……】"
    
    yanshuo "（冷靜地環顧破舊的日式和室與牆上的昭和日曆）……這裡是 1990 年代初期的日本東京都郊區。環境溫度比常規體感低 8.5 度，周圍空間存在高密度未知負能量場。"
    
    yeling "（手握硃砂桃木劍，秀眉微蹙，神情極度凝重）諸位道友小心！此宅陰煞之氣直衝雲霄，有修為極深的百年冤魂厲鬼盤踞不散！"
    
    moli_rookie "鬼……鬼啊！我不待在這種鬼屋裡！你們這群神經病，放我出去啊啊啊！"
    
    gulin "莫離！站在原地別動！這個副本的敵人是無實體靈體，單獨離隊必死無疑！"
    
    xiangtian "新人！給老子冷靜點！顧哥跟言朔說的話你聽不見嗎？！"
    
    # -------------------------------------------------------------
    # 💀 2. 事故發生：新人莫離獨自逃往閣樓，遭伽椰子吞噬
    # -------------------------------------------------------------
    "新人莫離完全陷入崩潰失控，尖叫著甩開眾人，瘋狂衝上二樓，把自己反鎖在黑暗的閣樓衣櫃中！"
    "黑暗中，衣櫃縫隙裡緩緩垂下無數冰冷的黑色長髮……"
    
    moli_rookie "不要過來……不要抓我！救命啊啊啊啊————！！"
    
    "【閣樓上方傳來極度淒厲的慘叫聲與骨肉撕裂聲，隨後濃稠的黑血從天花板縫隙滴滴答答滲了下來……】"
    
    suxiao "（按住太陽穴，臉色煞白）莫離的生命信號……瞬間歸零了！凶宅的無差別詛咒已經鎖定我們所有人！"
    
    lengyue "不聽指揮的蠢貨。全員拔出靈力武器，準備迎戰！"
    
    # -------------------------------------------------------------
    # ⚔️ 3. 【第一波戰鬥】：怨念爬行體群 (靈體物理免疫測試)
    # -------------------------------------------------------------
    scene bg_tatami_room_dark with flash
    
    "榻榻米地板寸寸碎裂，數隻由黑色長髮與怨念凝聚而成的『怨念爬行體』從地底扭曲爬出！"
    "【警告：敵方具備『靈體免疫』標籤！常規實體物理砍擊與無附魔槍械傷害無效！】"
    
    xiangtian "可惡！我的拳頭打在牠們身上就像打在霧氣上一樣，完全吃不到力道！"
    
    yeling "諸位莫慌！天地玄宗，萬炁本根！廣修浩劫，證吾神通 —— 破魔靈符，敕！"
    
    python:
        # 發放茅山開光符文支援物資
        add_item("MAT_TAOIST_RUNES", 2)
        
        # 初始化第一波靈異戰鬥
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave1 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'paranormal',
            'enemies': [
                {"id": "MOB_SPIRIT_01", "name": "黑髮怨念爬行體 A (靈體)", "hp": 150, "max_hp": 150, "atk": 22, "status": "物理免疫", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_SPIRIT_01", "name": "黑髮怨念爬行體 B (靈體)", "hp": 150, "max_hp": 150, "atk": 22, "status": "物理免疫", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_SPIRIT_02", "name": "溺死冤魂凶煞 (靈體)", "hp": 220, "max_hp": 220, "atk": 30, "status": "精神噬魂", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "👻 【第一波遭遇戰】靈異環境降臨！敵方具備靈體免疫，請使用葉靈符法與能量技能！",
                "⚠️ 精神威壓：詛咒正在侵蝕心神，全隊每回合損失 3%% MP！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave1)
    
    "【第一波戰鬥結束！在葉靈的破魔朱砂神符壓制下，怨念爬行體化為青煙消散！】"
    
    # -------------------------------------------------------------
    # 💣 4. 【第二波決戰】：咒怨伽椰子本體襲擊 (詛咒蔓延 + 驅魔絕殺)
    # -------------------------------------------------------------
    scene bg_staircase_curse with flash
    
    "陰風大作，整座凶宅的牆壁開始流淌鮮血。"
    "在吱呀作響的木樓梯上方，一個全身慘白、關節扭曲骨折的女鬼（伽椰子）帶著滿身怨氣，伴隨著慘厲貓叫聲緩緩爬下！"
    
    kayako "咯……咯……咯……（怨念衝擊直擊靈魂）"
    
    yanshuo "（推了推眼鏡，計算力全開）伽椰子的怨念場具備空間扭曲與精神穿透特性。若不能在短時間內施展大範圍神聖靈術將其本體震散，空間封閉將在 3 分鐘內引發全隊精神崩潰！"
    
    gulin "項天、冷月，掩護葉靈施法！葉靈，發動最強的『九天玄女驅魔陣』！"
    
    yeling "領命！九天玄女降真靈，蕩盡幽冥斬妖形 —— 神兵火急如律令！"
    
    python:
        # 初始化第二波 Boss 戰鬥 (伽椰子本體 + 俊雄)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave2 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'paranormal',
            'enemies': [
                {"id": "MOB_TOSHIO", "name": "怨念化身·俊雄 (靈體)", "hp": 240, "max_hp": 240, "atk": 28, "status": "恐懼凝視", "avatar": "images/core_idle.PNG"},
                {"id": "BOSS_KAYAKO", "name": "👑 咒怨真身·伽椰子 (本體)", "hp": 800, "max_hp": 800, "atk": 55, "status": "詛咒源頭", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "👑 【第二波終極決戰】咒怨本體降臨！全隊每回合扣除 5%% MP 詛咒傷害！",
                "🔥 戰術指南：消耗 4 AP 發動【九天玄女驅魔陣】或全隊能量大招，強力破滅怨念源頭！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave2)
    
    "【在浩瀚純陽金光的照耀下，伽椰子發出淒厲哀嚎，巨大的怨念軀體被鎮魂符徹底淨化撕碎！】"
    "凶宅的幻象隨之寸寸崩塌，清晨的第一縷陽光透過破碎的窗戶灑落進來。"
    
    # -------------------------------------------------------------
    # 🧠 5. 底層智者檢定：提煉『陰陽怨念核心晶片』
    # -------------------------------------------------------------
    python:
        team_roster = get_team_roster()
        team_max_int = max([int(m.get('int', 20)) for m in team_roster])
        has_scholar_int = (team_max_int >= 100)
        
    if has_scholar_int:
        n "【智者思維感知】隊伍最高智力達到 [team_max_int] 點（達標 >= 100，言朔與道士葉靈成功聯手推導出怨靈能量矩陣）！"
        menu:
            "【🧠 智者檢定】由言朔與葉靈合力提煉『陰陽怨念核心晶片』":
                python:
                    add_item("MAT_SPIRIT_CORE", 1)
                    points += 2500
                    add_fate_shard("C", 1)
                
                "【智者判定大成功！】成功提煉獲取【陰陽怨念核心晶片 (MAT_SPIRIT_CORE)】！"
                "（此珍貴素材可帶回神域家園工坊，解鎖『辟邪清心血清』研發，戰鬥中瞬間回滿 50%% MP 並免疫詛咒！）"
                "獲得額外獎勵：生存點數 +2,500 點、C 階命運碎片 x1！"
                
            "直接踏入傳送光柱回歸":
                python:
                    points += 1200
                "獲得基礎任務獎勵：生存點數 +1,200 點。"
    else:
        n "隊伍當前最高智力為 [team_max_int] 點（未達門檻 100 點），無法在怨氣消散前完成封存，只能立刻撤離凶宅。"
        python:
            points += 1200
        "獲得基礎任務獎勵：生存點數 +1,200 點。"

    # -------------------------------------------------------------
    # 🏆 6. 副本結算、葉靈正式入隊與回歸輪迴空間
    # -------------------------------------------------------------
    scene bg_japanese_haunted_house with flash
    
    "凶宅詛咒破除，手錶上的任務倒數歸零，神聖純潔的光柱自天穹轟然降臨！"
    
    python:
        # 第三副本通關結算獎勵
        stage_clear_bonus = 3000
        points += stage_clear_bonus
        add_fate_shard("B", 1)
        add_fate_shard("C", 1)
        
        # 新人道士葉靈 (REC_017) 正式登錄加入隊伍名冊！
        roster = get_team_roster()
        if not any(m.get("name") == "葉靈" for m in roster):
            new_member_yeling = {
                "name": "葉靈",
                "gender": "女",
                "role": "道家靈修天師 / 破魔者",
                "combat_role": "破邪符籙 / 靈魂淨化 / 靈異剋制",
                "bloodline": "無 (天生靈瞳潛能)",
                "avatar": "images/core_idle.PNG",
                "points": 1800,
                "con": 28, "str": 22, "spd": 35, "int": 95, "mnd": 65,
                "hp": 220, "max_hp": 220,
                "mp": 280, "max_mp": 280,
                "neili_current": 20, "neili_max": 80,
                "blood_current": 0, "blood_max": 0,
                "mental_current": 0, "mental_max": 0,
                "qi_current": 0, "qi_max": 0,
                "calc_current": 0, "calc_max": 0,
                "gene_lock": 0,
                "survival_pressure": 20,
                "status": "靈符護體",
                "skills": [],
                "equipped_head": "EQ_MAGIC_HOOD_01",
                "equipped_torso": None,
                "equipped_hands": "EQ_MAGIC_BRACER_01",
                "equipped_feet": None,
                "equipped_necklace": "EQ_MAGIC_NECKLACE_01",
                "equipped_main_hand": "weapon_plasma_katana",
                "equipped_off_hand": None,
                "equipped_mount": None,
                "desc": "傳承古老道術的天師少女，天生開啟靈瞳，對靈異鬼怪與不死生物擁有極強的神聖克制效果。"
            }
            team_roster.append(new_member_yeling)
            
        # 重置全隊休息室談心與修煉配額
        global current_main_stage_index
        current_main_stage_index = max(current_main_stage_index if 'current_main_stage_index' in globals() else 1, 4)
        if 'reset_teammate_chat_quota' in globals():
            reset_teammate_chat_quota()
            
        if renpy.loadable("audio/levelup.ogg"):
            renpy.sound.play("audio/levelup.ogg")
            
    z "【主線任務 · 日式靈異世界（咒怨凶宅）已完美通關！】"
    z "結算統計：成功擊殺咒怨本體！道家天師【葉靈】生還加入團隊！\n獲得獎勵：生存點數 +3,000 點、B 階命運碎片 x1、C 階命運碎片 x1！"
    z "目前持有總點數：[points] 點。"
    
    yeling "多謝顧隊長與諸位道友相助！若無諸位齊心協力，小女子今日恐難破除此凶煞大劫。今後願隨隊長斬妖除魔！"
    gulin "歡迎加入，葉靈。你的破魔道術是我們應對靈異世界最關鍵的底牌。"
    
    scene bg_main_room_topdown with fade
    "白光籠罩全身，眾人帶著珍貴的靈異戰利品，安然返回輪迴空間中央廣場！"
    
    jump main_room_exploration


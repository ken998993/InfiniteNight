# ==============================================================================
# 📜 《輪迴世界》第五副本：木乃伊遺跡 · 印洲隊團戰遭遇戰 (team_battle.rpy)
# 依據 developMd/15_Story_Stage_1_5_Team_Battle_India.md 規範實現
# ==============================================================================

# 定義關卡專屬角色對話物件
define lengyue = Character("冷月", color="#00ffcc", image="lengyue")
define xiangtian = Character("項天", color="#ff8844", image="xiangtian")
define suxiao = Character("蘇曉", color="#66ccff", image="suxiao")
define gulin = Character("顧臨淵", color="#00ffea")
define yanshuo = Character("言朔", color="#ddaaff")
define linwei = Character("林微 (暗影刺客)", color="#cc66ff")
define barut = Character("巴魯特 (印洲隊狼人隊長)", color="#ff3333")
define shala = Character("莎拉 (印洲隊精神感應者)", color="#ff88cc")
define god_announcer = Character("輪迴核心廣播", color="#ffff00")

# 定義關卡背景圖元別名 (全圖縮放拉滿 1920x1080，消除黑邊與馬賽克邊)
image bg_egypt_pyramid_desert = Transform("images/trial_room.png", xsize=1920, ysize=1080)
image bg_desert_temple_entrance = Transform("images/zombie_street.PNG", xsize=1920, ysize=1080)
image bg_pyramid_interior_core = Transform("images/trial_room.png", xsize=1920, ysize=1080)

# ==========================================
# 關卡進入點 (相容 teamBattle 與 stage_1_5)
# ==========================================
label teamBattle:
    jump stage_1_5_team_battle_india

label stage_1_5_team_battle_india:
    scene bg_egypt_pyramid_desert with fade
    
    # -------------------------------------------------------------
    # 1. 傳送降臨與團戰廣播劇情
    # -------------------------------------------------------------
    "【主神冰冷威嚴的通告聲在全體隊員腦海中炸響 —— 團戰模式啟動！】"
    god_announcer "【警告！進入副本『木乃伊 / 死者之城』！】"
    god_announcer "【檢測到敵對輪迴小隊『印洲隊』已於 20 分鐘前提前降臨本世界！】"
    god_announcer "【團戰死鬥規則：擊殺敵對小隊成員獲得高額點數與獎勵碎片；團戰結束時若團隊總積分為負，全員直接抹殺！】"
    
    yanshuo "（推了推無框眼鏡，指尖在戰術終端上飛速點擊）敵方比我們早降臨 20 分鐘。在心理學與戰術博弈上，他們必定已佔據了卡納克神廟的主控高地，並透過當地死者之書控制了阿努比斯沙土軍團。"
    
    linwei "（雙手反握暗影雙刃，眼神冰冷如幽夜寒霜）剛才對方的精神感應者試圖對我們發動『心靈狂暴衝擊』……但被言朔的心靈防護壁障無聲阻隔了。"
    
    gulin "印洲隊把我們當成主動送上門的獎勵點數了。項天、冷月，在前排頂住正面沙暴衝擊！林微，利用暗影遁形潛伏，尋找機會一擊秒殺他們的精神感應者！"
    
    xiangtian "哈哈！早就想跟別的輪迴小隊掰掰手腕了！看老子砸爛這群傢伙的狗頭！"
    
    # -------------------------------------------------------------
    # ⚔️ 2. 【第一波戰鬥】：阿努比斯沙土軍團 (不死沙體測試)
    # -------------------------------------------------------------
    scene bg_desert_temple_entrance with flash
    
    "狂暴的黃沙漫天蔽日，印洲隊召喚的數百隻手持彎刀的『阿努比斯死士』如黑色潮水般湧出，組成了密不透風的鋼鐵防線！"
    "【警告：阿努比斯軍團具備『不死沙體』特性！常規物理斬擊傷害減半，請使用大範圍聖光或奧術魔法進行神聖淨化！】"
    
    gulin "艾莉絲、蘇曉！發動太陽神聖光術，淨化這片沙暴！"
    
    python:
        # 發放團戰狼人基因素材支援
        add_item("MAT_WOLF_GENE", 2)
        
        # 初始化第一波戰鬥
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave1 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'causality',
            'enemies': [
                {"id": "MOB_ANUBIS_01", "name": "阿努比斯死士 A (不死沙體)", "hp": 180, "max_hp": 180, "atk": 25, "status": "不死沙身", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_ANUBIS_01", "name": "阿努比斯死士 B (不死沙體)", "hp": 180, "max_hp": 180, "atk": 25, "status": "不死沙身", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_SAND_BEAST", "name": "沙暴狂化法老巨衛", "hp": 260, "max_hp": 260, "atk": 35, "status": "重裝霸體", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "⚔️ 【第一波遭遇戰】阿努比斯沙土大軍衝鋒！神聖魔法與能量戰技可破除不死沙體！",
                "💡 戰術指示：前排項天與顧臨淵發動 3 AP 普攻防守反擊，後排準備 4 AP 大招清場！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave1)
    
    "【第一波戰鬥結束！神聖聖光撕裂沙暴，阿努比斯死士全數化為普通塵埃！】"
    
    # -------------------------------------------------------------
    # 💣 3. 【第二波決戰】：印洲隊主力對決 (林微暗影秒殺 + 斬首狼人隊長)
    # -------------------------------------------------------------
    scene bg_pyramid_interior_core with flash
    
    "眾人踏入金字塔核心祭壇。"
    "祭壇中央，印洲隊隊長巴魯特仰天長嘯，周身肌肉瘋狂暴漲撕裂鎧甲，化為高達 4 公尺的恐怖嗜血巨狼！"
    
    barut "哈哈哈哈！中洲隊的軟弱菜鳥們，乖乖化為我們印洲隊晉升的積分吧 —— 狂暴撕裂！"
    
    yanshuo "（透過心靈防護網向林微精準下達微操坐標）言朔：『林微，敵方精神感應者莎拉隱匿在祭壇左上方第三根巨柱陰影下，物理防禦僅有 15 點。』"
    
    gulin "林微，暗影絕殺！"
    
    linwei "（身形如墨水般融入陰影）……已鎖定目標。暗夜影襲 —— 瞬殺！"
    
    "嗤————！！"
    "一道漆黑如魅影的紫黑色刀光自虛空中憑空暴射而出，精準無比地自背後貫穿了莎拉的咽喉！"
    
    shala "呃……你……怎麼可能繞過隊長……（瞳孔渙散，頹然倒地）"
    
    python:
        # 擊殺精神感應者獎勵
        points += 2000
        add_fate_shard("B", 1)
        
    god_announcer "【擊殺印洲隊精神感應者·莎拉！中洲隊獲得團隊積分 +1 分！獲得生存點數 +2,000 點、B 階命運碎片 x1！】"
    
    barut "不！！莎拉！！混蛋我要把你們全部嚼成肉泥————！！"
    
    gulin "項天、冷月！他陷入狂暴了！開啟基因鎖三階，隨我將他徹底斬殺！"
    
    python:
        # 初始化第二波 Boss 戰鬥 (印洲隊狼人隊長巴魯特)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave2 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'causality',
            'enemies': [
                {"id": "MOB_WOLF_GUARD", "name": "狂化生化血狼護衛", "hp": 300, "max_hp": 300, "atk": 40, "status": "狂暴突進", "avatar": "images/core_idle.PNG"},
                {"id": "BOSS_BARUT_WOLF", "name": "👑 印洲隊隊長·狼人巴魯特", "hp": 1100, "max_hp": 1100, "atk": 70, "status": "嗜血狂暴", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "👑 【第二波終極決戰】印洲隊狼人隊長巴魯特狂暴出擊！攻擊力高達 70 點！",
                "🧬 基因鎖三階引導：顧臨淵預知狼人撲咬目標，及時防禦或發動 4 AP 大招絕殺！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave2)
    
    "【顧臨淵在預知視野中提前側身避過狼爪，手中古武粒子刀與項天的混元拳罡同時轟入巴魯特的心臟！】"
    "印洲隊隊長巴魯特轟然倒地，巨大的狼人軀體化為塵埃潰散！"
    
    python:
        # 擊殺隊長獎勵
        points += 5000
        add_fate_shard("A", 1)
        
    god_announcer "【擊殺印洲隊隊長·巴魯特！中洲隊獲得團隊積分 +1 分！獲得生存點數 +5,000 點、A 階命運碎片 x1！】"
    
    # -------------------------------------------------------------
    # 🧠 4. 底層智者檢定：掠奪『太陽金字塔核心晶片』
    # -------------------------------------------------------------
    python:
        team_roster = get_team_roster()
        team_max_int = max([int(m.get('int', 20)) for m in team_roster])
        has_scholar_int = (team_max_int >= 100)
        
    if has_scholar_int:
        n "【智者思維感知】隊伍最高智力達到 [team_max_int] 點（達標 >= 100，言朔成功破譯印洲隊戰術終端核心）！"
        menu:
            "【🧠 智者檢定】由言朔破解並奪取印洲隊遺留的『太陽金字塔核心晶片』":
                python:
                    add_item("MAT_SOLAR_PYRAMID_CORE", 1)
                    points += 3000
                    add_fate_shard("A", 1)
                
                "【智者判定大成功！】成功奪取獲取【太陽金字塔核心晶片 (MAT_SOLAR_PYRAMID_CORE)】！"
                "（此神器晶片可帶回神域家園工坊，解鎖『太陽神聖槍』打印，對靈體與黑暗生物造成 200%% 破甲毀滅傷害！）"
                "獲得額外獎勵：生存點數 +3,000 點、A 階命運碎片 x1！"
                
            "直接踏入傳送光柱回歸":
                python:
                    points += 2000
                "獲得基礎任務獎勵：生存點數 +2,000 點。"
    else:
        n "隊伍當前最高智力為 [team_max_int] 點（未達門檻 100 點），無法在金字塔崩塌前完成破解，只能迅速撤離祭壇。"
        python:
            points += 2000
        "獲得基礎任務獎勵：生存點數 +2,000 點。"

    # -------------------------------------------------------------
    # 🏆 5. 副本結算、林微正式入隊與全員凱旋回歸
    # -------------------------------------------------------------
    scene bg_egypt_pyramid_desert with flash
    
    "團戰大獲全勝，手錶上的積分結算為正分，通天徹地的純金神聖光柱從天穹籠罩了中洲隊全體成員！"
    
    python:
        # 第五副本團戰通關結算獎勵
        stage_clear_bonus = 5000
        points += stage_clear_bonus
        add_fate_shard("S", 1)
        add_fate_shard("A", 1)
        add_fate_shard("B", 1)
        
        # 新人暗影刺客林微 (REC_006) 歷經生死團戰，正式登錄加入隊伍名冊！
        roster = get_team_roster()
        if not any(m.get("name") == "林微" for m in roster):
            new_member_linwei = {
                "name": "林微",
                "gender": "女",
                "role": "暗夜刺客世家 / 影襲者",
                "combat_role": "極速影襲 / 致命背刺 / 後排刺殺",
                "bloodline": "無 (刺客世家潛能)",
                "avatar": "images/core_idle.PNG",
                "points": 2400,
                "con": 30, "str": 35, "spd": 60, "int": 50, "mnd": 45,
                "hp": 240, "max_hp": 240,
                "mp": 180, "max_mp": 180,
                "neili_current": 0, "neili_max": 0,
                "blood_current": 0, "blood_max": 0,
                "mental_current": 0, "mental_max": 0,
                "qi_current": 0, "qi_max": 0,
                "calc_current": 0, "calc_max": 0,
                "gene_lock": 0,
                "survival_pressure": 40,
                "status": "潛伏陰影",
                "skills": [],
                "equipped_head": "EQ_MAGIC_HOOD_01",
                "equipped_torso": "EQ_TECH_ARMOR_01",
                "equipped_hands": "EQ_TECH_GLOVES_01",
                "equipped_feet": "EQ_TECH_BOOTS_01",
                "equipped_necklace": None,
                "equipped_main_hand": "weapon_plasma_katana",
                "equipped_off_hand": None,
                "equipped_mount": None,
                "desc": "自幼接受殘酷暗殺訓練的少女刺客，身法飄忽如魅影，擅長短刃近身割喉與致命背刺。"
            }
            team_roster.append(new_member_linwei)
            
        # 重置全隊休息室談心與修煉配額
        global current_main_stage_index
        current_main_stage_index = max(current_main_stage_index if 'current_main_stage_index' in globals() else 1, 6)
        if 'reset_teammate_chat_quota' in globals():
            reset_teammate_chat_quota()
            
        if renpy.loadable("audio/levelup.ogg"):
            renpy.sound.play("audio/levelup.ogg")
            
    z "🎉【團戰大捷 · 擊滅印洲隊】木乃伊死者之城副本完美通關！\n中洲隊以壓倒性戰術全面殲滅印洲隊！暗夜刺客【林微】正式加入團隊！\n獲得史詩級大獎：生存點數 +5,000 點、S 階命運碎片 x1、A 階命運碎片 x1、B 階命運碎片 x1！"
    z "目前持有總點數：[points] 點。"
    
    linwei "（收回雙匕，向顧臨淵微微欠身）顧隊長的指揮很精準。我願意留在中洲隊，成為你手中的暗影之刃。"
    xiangtian "哈哈哈哈！痛快！印洲隊這幫傢伙還想伏擊我們，直接被我們連鍋端了！"
    yanshuo "（冷靜總結）本次團戰戰術執行率 98.4%%，戰利品收益達到了預期峰值。我們已具備正面迎戰高難度輪迴小隊的絕對實力。"
    lengyue "做得很漂亮。但更廣闊的多元宇宙與惡魔隊還在前方等著我們。回廣場整裝出發吧！"
    
    scene bg_main_room_topdown with fade
    "在絢爛耀眼的 S 級傳送金光照耀下，全員攜帶著豐碩戰果，昂首闊步凱旋返回輪迴空間中央廣場！"
    
    jump main_room_exploration


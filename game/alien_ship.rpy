# ==============================================================================
# 📜 《輪迴世界》第二副本：太空真空世界 · 幽靈探索母艦 (alien_ship.rpy)
# 依據 developMd/12_Story_Stage_1_2_Alien_Ship.md 規範實現
# ==============================================================================

# 定義關卡專屬角色對話物件
define lengyue = Character("冷月", color="#00ffcc", image="lengyue")
define xiangtian = Character("項天", color="#ff8844", image="xiangtian")
define suxiao = Character("蘇曉", color="#66ccff", image="suxiao")
define gulin = Character("顧臨淵", color="#00ffea")
define yanshuo = Character("言朔", color="#ddaaff")
define hanyu = Character("韓羽 (驚恐新人)", color="#ff9999")
define duanheng = Character("段恆 (投機新人)", color="#aaaaaa")
define ship_ai = Character("母艦主控廣播", color="#ffff00")
define alien_queen = Character("異形母皇", color="#ff2222")

# 定義關卡背景圖元別名 (全圖縮放拉滿 1920x1080，消除黑邊與馬賽克邊)
image spaceShip = Transform("images/spaceShip.jpg", xsize=1920, ysize=1080)
image bg_alien_ship_hub = Transform("images/spaceShip.jpg", xsize=1920, ysize=1080)
image bg_alien_corridor_vacuum = Transform("images/spaceShip.jpg", xsize=1920, ysize=1080)
image bg_alien_core_reactor = Transform("images/spaceShip.jpg", xsize=1920, ysize=1080)

# ==========================================
# 關卡進入點 (相容 alienShip 與 stage_1_2)
# ==========================================
label alienShip:
    jump stage_1_2_alien_ship

label stage_1_2_alien_ship:
    scene spaceShip with fade
    
    # -------------------------------------------------------------
    # 1. 輪迴光束降臨，新人醒來與規則說明劇情
    "【深邃冰冷的失重感與刺鼻的機油鐵鏽味瞬間充斥了神經……】"
    "【輪迴傳送光束消退，眼前的景象變成了一艘幽暗死寂的巨型深空戰艦內部。】"
    
    
    duanheng "操！少跟我裝神弄鬼！老子在外面有的是錢，開個價放我走，否則我叫人剁了你們！"
    
    yanshuo "（冷靜地蹲下撫摸著冰冷的鈦合金地板，推了推無框眼鏡）……大氣壓為 0.8 標準氣壓、金屬蜂巢結構超越當前人類科技 50 年以上。手腕上的黑科技手環連接著微觀神經電信號……這不是任何已知的影視基地或綁架惡作劇。"
    
    lengyue "吵死了。再敢發出一聲廢話，我就在輪迴光球抹殺你們之前先扣動扳機。"
    
    suxiao "新人們，請冷靜聽好。你們已經被選入《輪迴世界》了。請看你們手腕上的腕錶終端 —— 本次主線任務：在這艘母艦上『消滅異形巢穴並生存 24 小時』。"
    
    gulin "我是顧臨淵。想活命就牢記三條鐵律：第一，嚴格跟緊戰鬥小隊；第二，絕對不要觸碰任何外星生物膠囊或隔離閥門；第三，在輪迴世界裡死了就是真正的死亡。"
    
    xiangtian "沒錯！聽顧哥與冷月的準沒錯！上一場副本在極光重工不聽指揮的刺青流氓，開場不到三分鐘就被融得連骨頭都不剩！"
    
    # -------------------------------------------------------------
    # 💀 2. 事故發生：恐慌新人韓羽觸發抱臉體 (Facehugger) 寄生
    # -------------------------------------------------------------
    "眾人開始沿著漆黑的母艦主走廊向前排查，兩側艙壁黏附著大量令人作嘔的黑色生物樹脂黏液。"
    "新人韓羽因為極度恐慌精神崩潰，突然失控尖叫著衝向旁邊一扇半掩著的廢棄生化冷藏艙！"
    
    hanyu "我不相信！放我出去！這裡一定有逃生艙——！"
    
    gulin "韓羽！別碰那個密封艙——！"
    
    "嗤————！！"
    "破裂的外星生物卵中猛然爆射出一道帶著長尾的肉色黑影，以雷霆萬鈞之勢死死吸附並扣住了韓羽的面罩！"
    
    hanyu "唔……唔唔唔——！！（劇烈掙扎並痛苦倒地）"
    
    suxiao "抱臉體（Facehugger）！牠正在透過氣孔強行往宿主體內注入寄生胚胎……！"
    
    yanshuo "（眼神冷酷如手術刀）生物熱感掃描顯示其胚胎已穿透食道進入寄主胸腔縱隔。為防止二度寄生擴散，理性上建議立刻執行高溫焚化淨化。"
    
    # 💀 段恆投機取巧死於酸液陷阱
    "一旁的段恆見狀嚇得魂飛魄散，趁眾人不備偷偷轉動了旁邊標記著『高壓廢料排放閥』的紅色轉輪，企圖獨自鑽進管道逃命……"
    
    duanheng "這群瘋子……老子才不陪你們送死！逃生管道是我的——"
    
    "滋滋滋————！！"
    "閘門開啟的瞬間，積壓數百年的超濃縮強酸液態廢料如瀑布般噴湧而出！段恆連慘叫都來不及發出，整個人在幾秒內被腐蝕成了白骨與黑煙！"
    
    lengyue "韓羽被寄生、段恆貪婪送命……新人們，這就是擅自行動的代價。"
    
    # -------------------------------------------------------------
    # ⚔️ 3. 【第一波戰鬥】：真空無重力走廊 + 幼體怪群 (槍械封印機制)
    # -------------------------------------------------------------
    scene bg_alien_corridor_vacuum with flash
    
    "走廊前方的外層裝甲突然破裂，刺耳的失壓警報瞬間響徹全艦！"
    ship_ai "【警告：進入真空無重力破損區域！常規火藥槍械彈道已被限制！】"
    "【數十隻『異形幼體群』踩著天花板在無重力環境下急速攀爬襲來！】"
    
    gulin "全員拔出近戰光刃與近距能量武器！前排頂住，後排準備火力支援！"
    
    python:
        # 初始化第一波戰鬥 (真空無重力環境，幼體怪群)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave1 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'space',
            'enemies': [
                {"id": "MOB_ALIEN_LARVA_01", "name": "異形幼體群 A", "hp": 140, "max_hp": 140, "atk": 20, "status": "無重力跳躍", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_ALIEN_LARVA_02", "name": "異形幼體群 B", "hp": 140, "max_hp": 140, "atk": 20, "status": "無重力跳躍", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_ACID_RUNNER_01", "name": "酸蝕突變迅猛獵犬", "hp": 180, "max_hp": 180, "atk": 28, "status": "強酸血液", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "🌌 【第一波遭遇戰】太空真空環境！常規槍械受阻，近戰與能量戰技享有加成！",
                "⚔️ 戰術指示：由前排顧臨淵與項天發動【普通攻擊 (3 AP)】阻截撲躍幼體！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave1)
    
    "【第一波戰鬥大捷！撲躍而來的異形幼體群被全數斬殺於氣閥前！】"
    
    # -------------------------------------------------------------
    # 💀 4. 破胸體爆發與異形進化
    # -------------------------------------------------------------
    "戰鬥剛剛平息，躺在地上陷入深度昏迷的韓羽突然發出滲人的骨骼爆裂聲！"
    "啪嚓——！"
    "胸腔皮肉瞬間炸開，一隻渾身覆蓋著漆黑甲殼的幼年異形破胸而出，發出一聲刺耳尖嘯，以超越肉眼捕捉的極速遁入了深邃的通風管道之中！"
    
    lengyue "該死！那隻破胸體正沿著能源管道衝向母艦核心反應爐！"
    
    yanshuo "（迅速在控制台調出母艦管線藍圖）反應爐區域擁有龐大的高純度核聚變等離子燃料。若讓其吸收能源完成變態發育進化為『異形母皇』，我方小隊的生還率將降至 0.2%%。"
    
    gulin "沒時間猶豫了，全員全速前進，在牠完成完全體進化前引爆反應爐！"
    
    # -------------------------------------------------------------
    # 💣 5. 【第二波 Boss 戰】：異形母皇 + 異形獵手 (飛行標籤機制)
    # -------------------------------------------------------------
    scene bg_alien_core_reactor with flash
    
    "眾人殺入母艦最底層的巨型核反應爐大廳。"
    "高達數十公尺的等離子反應堆上方，一隻體長超過八公尺、長著巨大扇形王冠頭骨的猙獰巨獸 —— 【異形母皇 (Alien Queen)】 正倒掛在鋼樑上冷冷俯瞰著眾人！"
    "在牠身側，兩隻體型修長、具備空中懸浮滑翔能力的【異形獵手 (Alien Hunters)】正發出嘶嘶低鳴！"
    
    alien_queen "吼——————！！（震耳欲聾的蟲族精神咆哮撕裂耳膜）"
    
    ship_ai "【警告：偵測到超高能生物力場！異形獵手獲得『無重力飛行標籤』，可無視前排阻擋直接突襲後排！】"
    
    gulin "項天！開啟混元血魄在前排築起防線！蘇曉、言朔，注意保持安全距離！"
    
    xiangtian "哈哈！來得正好！老子倒要看看這隻大蜥蜴能不能咬碎我的拳頭！"
    
    python:
        # 發放懸浮戰術支援
        add_item("MAT_ZERO_G_ALLOY", 2)
        
        # 初始化第二波 Boss 戰鬥 (異形母皇 + 2 異形獵手)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave2 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'space',
            'enemies': [
                {"id": "MOB_ALIEN_HUNTER_01", "name": "異形獵手 Alpha (飛行)", "hp": 200, "max_hp": 200, "atk": 30, "status": "飛行突進", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_ALIEN_HUNTER_02", "name": "異形獵手 Beta (飛行)", "hp": 200, "max_hp": 200, "atk": 30, "status": "飛行突進", "avatar": "images/core_idle.PNG"},
                {"id": "BOSS_ALIEN_QUEEN", "name": "👑 異形母皇·終極完全體", "hp": 650, "max_hp": 650, "atk": 48, "status": "強酸狂暴", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "👑 【第二波終極決戰】異形母皇降臨！敵方獵手具備飛行標籤，可直接突襲後排！",
                "🔥 戰術指南：消耗 4 AP 釋放專屬戰技，集中火力先消滅兩側獵手再圍攻母皇！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave2)
    
    "【在全隊默契配合下，異形母皇發出絕望慘嚎，巨大的身軀被等離子爆彈重重轟斷了支撐鋼樑！】"
    "顧臨淵果斷扣動扳機引爆了外側閥門，數百萬噸的高壓氣流瞬間將異形母皇的殘軀吸入了無垠死寂的宇宙深空中！"
    
    # -------------------------------------------------------------
    # 🧠 6. 底層智者檢定：言朔採集異形皇后 DNA 突變株
    # -------------------------------------------------------------
    python:
        team_roster = get_team_roster()
        team_max_int = max([int(m.get('int', 20)) for m in team_roster])
        has_scholar_int = (team_max_int >= 100)
        
    if has_scholar_int:
        n "【智者思維感知】隊伍最高智力達到 [team_max_int] 點（達標 >= 100，新人言朔的頂級軍工科研才能發揮了關鍵作用）！"
        menu:
            "【🧠 智者檢定】由言朔執行無菌採樣，提取『異形皇后酸性 DNA 突變株』":
                python:
                    add_item("MAT_ALIEN_QUEEN_DNA", 1)
                    points += 2500
                    add_fate_shard("C", 1)
                
                "【智者判定大成功！】言朔以冷靜精準的手法採集到了活性最純淨的【異形皇后酸性 DNA 突變株 (MAT_ALIEN_QUEEN_DNA)】！"
                "（此珍貴素材可帶回神域家園工坊，解鎖『腐蝕強酸塗料』研發，為全隊武器附加削弱 50%% 防禦的強酸特效！）"
                
            "直接開啟逃生艙通訊，不進行採集":
                python:
                    points += 1200
                "眾人迅速撤出機房，獲得基礎任務獎勵：生存點數 +1,200 點。"
    else:
        n "隊伍當前最高智力為 [team_max_int] 點（未達門檻 100 點），無法在高溫強酸環境中完成精細採樣，只能立刻撤離機房。"
        python:
            points += 1200
        "獲得基礎任務獎勵：生存點數 +1,200 點。"

    # -------------------------------------------------------------
    # 🏆 7. 副本結算、言朔正式入隊與回歸輪迴空間
    # -------------------------------------------------------------
    scene bg_alien_ship_hub with flash
    
    "手錶上的 24 小時倒數歸零，神聖浩瀚的純白光柱自深空穹頂貫穿而下，溫暖地包裹住殘存的眾人！"
    
    python:
        # 第二副本通關結算獎勵
        stage_clear_bonus = 3000
        points += stage_clear_bonus
        add_fate_shard("C", 2)
        add_fate_shard("B", 1)
        
        # 新人言朔 (REC_003) 歷經生死考驗，正式登錄加入隊伍名冊！
        roster = get_team_roster()
        if not any(m.get("name") == "言朔" for m in roster):
            new_member_yanshuo = {
                "name": "言朔",
                "gender": "男",
                "role": "軍工首席科學家 / 第一智者",
                "combat_role": "絕對理性 / 幾何狙擊",
                "bloodline": "無 (基因改造無痛覺)",
                "avatar": "images/core_idle.PNG",
                "points": 5000,
                "con": 35,
                "str": 30,
                "spd": 35,
                "int": 150,
                "mnd": 80,
                "hp": 300,
                "max_hp": 300,
                "mp": 400,
                "max_mp": 400,
                "neili_current": 0,
                "neili_max": 0,
                "blood_current": 0,
                "blood_max": 0,
                "mental_current": 0,
                "mental_max": 0,
                "qi_current": 0,
                "qi_max": 0,
                "calc_current": 200,
                "calc_max": 200,
                "gene_lock": 0,
                "survival_pressure": 0,
                "status": "絕對冷靜",
                "skills": [],
                "equipped_head": None,
                "equipped_torso": "EQ_TECH_ARMOR_01",
                "equipped_hands": None,
                "equipped_feet": None,
                "equipped_necklace": None,
                "equipped_main_hand": "weapon_gauss_rifle",
                "equipped_off_hand": None,
                "equipped_mount": None,
                "desc": "國家第一科學家，不具備凡人情感與痛覺神經，能以純粹的幾何邏輯計算出敵方弱點與勝率。"
            }
            team_roster.append(new_member_yanshuo)
            
        # 重置全隊休息室談心與修煉配額
        global current_main_stage_index
        current_main_stage_index = max(current_main_stage_index if 'current_main_stage_index' in globals() else 1, 3)
        if 'reset_teammate_chat_quota' in globals():
            reset_teammate_chat_quota()
            
        if renpy.loadable("audio/levelup.ogg"):
            renpy.sound.play("audio/levelup.ogg")
            
    z "【主線任務 · 太空真空世界（幽靈探索母艦）已完美通關！】"
    z "結算統計：成功擊殺異形母皇！軍工首席智者【言朔】生還加入團隊！\n獲得獎勵：生存點數 +3,000 點、B 階命運碎片 x1、C 階命運碎片 x2！"
    z "目前持有總點數：[points] 點。"
    
    yanshuo "（推了推眼鏡，神情自若）經過這場實戰數據採樣，我已初步解析出這個輪迴空間的底層邏輯。顧臨淵，我認可你的戰術決策。從現在起，我的算力將全力輔助團隊。"
    xiangtian "哈哈！有言朔大科學家加入，我們小隊的智商直接翻倍了！"
    lengyue "別放鬆得太早。後面的副本只會比異形更恐怖。先回廣場強化自身吧。"
    
    scene bg_main_room_topdown with fade
    "光芒散去，眾人帶著豐厚的戰利品與全新智者隊友，昂首踏回了輪迴空間中央廣場！"
    
    jump main_room_exploration


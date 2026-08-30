# ==============================================================================
# 📜 《輪迴世界》第四副本：修真神魔世界 · 蜀山血海封印 (cultivation_realm.rpy)
# 依據 developMd/14_Story_Stage_1_4_Cultivation_Realm.md 規範實現
# ==============================================================================

# 定義關卡專屬角色對話物件
define lengyue = Character("冷月", color="#00ffcc", image="lengyue")
define xiangtian = Character("項天", color="#ff8844", image="xiangtian")
define suxiao = Character("蘇曉", color="#66ccff", image="suxiao")
define gulin = Character("顧臨淵", color="#00ffea")
define yanshuo = Character("言朔", color="#ddaaff")
define ailisi = Character("艾莉絲 (魔法學者)", color="#66ffff")
define fengwuhen = Character("風無痕 (雙刀遊俠)", color="#ffaa00")
define duanheng_rookie = Character("段恆 (貪婪新人)", color="#aaaaaa")
define demon_elder = Character("血魔長老", color="#ff2222")

# 定義關卡背景圖元別名 (全圖縮放拉滿 1920x1080，消除黑邊與馬賽克邊)
image bg_shushan_floating_mountain = Transform("images/trial_room.png", xsize=1920, ysize=1080)
image bg_shushan_cave_entrance = Transform("images/zombie_street.PNG", xsize=1920, ysize=1080)
image bg_shushan_blood_pool = Transform("images/trial_room.png", xsize=1920, ysize=1080)

# ==========================================
# 關卡進入點 (相容 cultivationRealm 與 stage_1_4)
# ==========================================
label cultivationRealm:
    jump stage_1_4_cultivation_realm

label stage_1_4_cultivation_realm:
    scene bg_shushan_floating_mountain with fade
    
    # -------------------------------------------------------------
    # 1. 傳送降臨與修真仙境 (顧臨淵 + 冷月 + 言朔 + 新人艾莉絲 & 風無痕 & 段恆)
    # -------------------------------------------------------------
    "【主神傳送光柱消退，眼前的景象變為浮空千丈的蜀山懸崖，遠方血雲翻滾，劍氣縱橫！】"
    
    ailisi "（閉上雙眸，纖手輕拂空氣中跳躍的魔力粒子）……好濃郁的游離元素濃度！這不是科技或末日世界，而是高階神魔修真位面！"
    
    fengwuhen "（壓低黑色草帽，拇指微頂雙刀刀柄）山風裡夾雜著極其濃烈的血腥味與狂暴殺氣。諸位，獵殺時刻到了。"
    
    duanheng_rookie "（看見崖壁邊散落的幾塊發光血紅色晶石，雙眼放光）哈哈！這石頭竟然自帶光芒，絕對是修仙寶物！老子發財了！"
    
    gulin "段恆！住手！不要碰這座山上的任何不明發光體！"
    
    # -------------------------------------------------------------
    # 💀 2. 事故發生：貪婪新人段恆私拿血靈石，被血魔吸乾爆體
    # -------------------------------------------------------------
    "段恆貪婪成性，完全不顧顧臨淵的警告，一把撲上前將血紅色靈石抓入懷中！"
    "嗤嗤嗤————！"
    "血靈石瞬間融化為無數條長著尖刺的血色觸手，瘋狂刺入段恆的四肢百骸與咽喉！"
    
    duanheng_rookie "呃……救……救我……我的血……都在被抽走……！"
    
    "短短三秒鐘，段恆整個人被抽成了乾癟的人皮乾屍，隨後轟然爆碎為漫天血霧！"
    
    yanshuo "（冷靜地記錄光學頻譜）確認該物質具備『精血吸附與主動肉體寄生』特性。危險等級：S 級。任何物理接觸都會引發連鎖吞噬。"
    
    xiangtian "呸！自作自受的貪心鬼！顧哥，前方洞窟有大量魔氣湧出來了！"
    
    # -------------------------------------------------------------
    # ⚔️ 3. 【第一波戰鬥】：血傀儡怪群 (護體靈光機制測試)
    # -------------------------------------------------------------
    scene bg_shushan_cave_entrance with flash
    
    "無數由濃稠精血凝聚而成的『蜀山血傀儡』從血海洞窟中蜂擁而出，周身籠罩著厚達數尺的血色護體靈光！"
    "【警告：敵方擁有 500 點『護體靈光 (Barrier)』！常規物理攻擊將被大幅折減，需使用元素法術破甲！】"
    
    ailisi "交給我！奧術激流，元素解離術 —— 破！"
    
    python:
        # 發放蜀山靈石素材支援
        add_item("MAT_DEMON_ESSENCE", 2)
        
        # 初始化第一波戰鬥
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave1 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'magic',
            'enemies': [
                {"id": "MOB_BLOOD_PUPPET_01", "name": "蜀山血傀儡 A (護體靈光)", "hp": 180, "max_hp": 180, "atk": 25, "status": "靈光護體", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_BLOOD_PUPPET_01", "name": "蜀山血傀儡 B (護體靈光)", "hp": 180, "max_hp": 180, "atk": 25, "status": "靈光護體", "avatar": "images/core_idle.PNG"},
                {"id": "MOB_BLOOD_BAT_01", "name": "嗜血魔道飛蝠 (飛行)", "hp": 220, "max_hp": 220, "atk": 32, "status": "精血汲取", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "🛡️ 【第一波遭遇戰】魔道血傀儡現身！艾莉絲使用元素破靈箭可無視護體靈光造成真實傷害！",
                "🌪️ 戰術提示：風無痕消耗 4 AP 釋放【雙刃血風暴】可快速橫掃前排血傀儡！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave1)
    
    "【第一波戰鬥結束！艾莉絲的元素奧術成功撕裂護體靈光，風無痕雙刀如疾風狂瀾將血傀儡全數斬碎！】"
    
    # -------------------------------------------------------------
    # 💣 4. 【第二波決戰】：血魔長老本體與顧臨淵基因鎖三階突破
    # -------------------------------------------------------------
    scene bg_shushan_blood_pool with flash
    
    "眾人踏入蜀山封魔洞最底層。"
    "方圓千丈的巨型血池中萬千血劍沖天而起，魔教巨擘 —— 【血魔長老】 顯化出高達百丈的猙獰血煞法相！"
    
    demon_elder "桀桀桀……哪裡來的螻蟻凡人，竟敢妄圖修復本座的封魔大陣！給本座化為血海養料吧 —— 『血海滔天』！"
    
    "轟隆隆————！！"
    "整座封魔洞被萬鈞血煞真氣封鎖，全體隊員被沉重的靈氣威壓死死壓制在原地！"
    
    gulin "（在極致的死亡窒息壓迫下，腦海深處的基因鏈如星辰爆發般瘋狂重組破裂……）"
    "【極限突破！生死邊界頓悟！顧臨淵成功開啟『基因鎖階級三 (Gene Lock Tier 3)』！】"
    "【思維運算速度暴增百倍！獲得『敵方招式預知』與『動態弱點洞察』神技！】"
    
    gulin "言朔！我看到了！血魔長老下一回合的真氣核心在左上方第三根封魔柱！"
    gulin "冷月、項天、風無痕，集中全隊最強火力，隨我一擊貫穿陣眼！"
    
    python:
        # 初始化第二波 Boss 戰鬥 (血魔長老)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave2 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'magic',
            'enemies': [
                {"id": "MOB_BLOOD_GUARDIAN", "name": "陣眼血魄護法 (護體靈光)", "hp": 260, "max_hp": 260, "atk": 35, "status": "陣眼守衛", "avatar": "images/core_idle.PNG"},
                {"id": "BOSS_DEMON_ELDER", "name": "👑 蜀山魔祖·血魔長老 (法相)", "hp": 950, "max_hp": 950, "atk": 60, "status": "血海法相", "avatar": "images/core_idle.PNG"}
            ],
            'logs': [
                "👑 【第二波終極決戰】血魔長老降臨！顧臨淵已洞察血魔破綻陣眼！",
                "🧬 基因鎖 Tier 3 特性：全體暴擊率 +40%%，全力轟擊陣眼弱點！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave2)
    
    "【顧臨淵精準預知血魔的所有反撲軌跡，合全隊之力一劍貫穿了封魔血核！】"
    "血魔長老發出絕望咆哮，百丈法相轟然瓦解，狂暴的血海被蜀山天雷大陣徹底鎮壓回地底！"
    
    # -------------------------------------------------------------
    # 🧠 5. 底層智者檢定：採集『蜀山天雷靈石核心』
    # -------------------------------------------------------------
    python:
        team_roster = get_team_roster()
        team_max_int = max([int(m.get('int', 20)) for m in team_roster])
        has_scholar_int = (team_max_int >= 100)
        
    if has_scholar_int:
        n "【智者思維感知】隊伍最高智力達到 [team_max_int] 點（達標 >= 100，言朔與艾莉絲成功解析出蜀山大陣的陣眼靈石結構）！"
        menu:
            "【🧠 智者檢定】由言朔抽取並封存『蜀山天雷靈石核心』":
                python:
                    add_item("MAT_THUNDER_SPIRIT_STONE", 1)
                    points += 3000
                    add_fate_shard("B", 1)
                
                "【智者判定大成功！】成功安全採集獲取【蜀山天雷靈石核心 (MAT_THUNDER_SPIRIT_STONE)】！"
                "（此稀世珍寶可帶回神域家園工坊，解鎖『天雷電磁飛劍』打印，使全隊攻擊附加天雷麻痺與真實破甲傷害！）"
                "獲得額外獎勵：生存點數 +3,000 點、B 階命運碎片 x1！"
                
            "直接踏入傳送光柱回歸":
                python:
                    points += 1500
                "獲得基礎任務獎勵：生存點數 +1,500 點。"
    else:
        n "隊伍當前最高智力為 [team_max_int] 點（未達門檻 100 點），無法在天雷大陣閉合前完成採樣，只能迅速撤離封魔洞。"
        python:
            points += 1500
        "獲得基礎任務獎勵：生存點數 +1,500 點。"

    # -------------------------------------------------------------
    # 🏆 6. 副本結算、艾莉絲與風無痕入隊與回歸輪迴空間
    # -------------------------------------------------------------
    scene bg_shushan_floating_mountain with flash
    
    "蜀山血海封印修復完畢，主神宏大的金色傳送光柱穿透九天雲霄降臨！"
    
    python:
        # 第四副本通關結算獎勵
        stage_clear_bonus = 3500
        points += stage_clear_bonus
        add_fate_shard("A", 1)
        add_fate_shard("B", 1)
        
        # 顧臨淵解鎖基因鎖階級三
        if team_roster and len(team_roster) > 0:
            team_roster[0]["gene_lock"] = max(3, team_roster[0].get("gene_lock", 0))
            
        # 新人魔法學者艾莉絲 (REC_015) 與雙刀浪人風無痕 (REC_019) 正式登錄加入隊伍名冊！
        roster = get_team_roster()
        if not any(m.get("name") == "艾莉絲" for m in roster):
            new_member_ailisi = {
                "name": "艾莉絲",
                "gender": "女",
                "role": "密教魔導學者 / 元素使",
                "combat_role": "元素衝擊 / 奧術護盾 / 魔力撕裂",
                "bloodline": "無 (元素親和潛能)",
                "avatar": "images/core_idle.PNG",
                "points": 1700,
                "con": 25, "str": 18, "spd": 30, "int": 110, "mnd": 70,
                "hp": 210, "max_hp": 210,
                "mp": 320, "max_mp": 320,
                "neili_current": 0, "neili_max": 0,
                "blood_current": 0, "blood_max": 0,
                "mental_current": 0, "mental_max": 0,
                "qi_current": 0, "qi_max": 0,
                "calc_current": 0, "calc_max": 0,
                "gene_lock": 0,
                "survival_pressure": 20,
                "status": "魔力充盈",
                "skills": [],
                "equipped_head": "EQ_MAGIC_HOOD_01",
                "equipped_torso": None,
                "equipped_hands": "EQ_MAGIC_BRACER_01",
                "equipped_feet": None,
                "equipped_necklace": "EQ_MAGIC_NECKLACE_01",
                "equipped_main_hand": None,
                "equipped_off_hand": None,
                "equipped_mount": None,
                "desc": "對古老以太魔力有極高親和度的學者，能凝聚純粹的魔力激流撕裂敵方護甲。"
            }
            team_roster.append(new_member_ailisi)
            
        if not any(m.get("name") == "風無痕" for m in roster):
            new_member_fengwuhen = {
                "name": "風無痕",
                "gender": "男",
                "role": "雙刀浪人遊俠 / 刺客",
                "combat_role": "疾風連斬 / 旋風突刺 / 高速連擊",
                "bloodline": "無",
                "avatar": "images/core_idle.PNG",
                "points": 1700,
                "con": 36, "str": 38, "spd": 52, "int": 40, "mnd": 40,
                "hp": 250, "max_hp": 250,
                "mp": 160, "max_mp": 160,
                "neili_current": 0, "neili_max": 0,
                "blood_current": 0, "blood_max": 0,
                "mental_current": 0, "mental_max": 0,
                "qi_current": 0, "qi_max": 0,
                "calc_current": 0, "calc_max": 0,
                "gene_lock": 0,
                "survival_pressure": 35,
                "status": "雙刀戒備",
                "skills": [],
                "equipped_head": None,
                "equipped_torso": "EQ_TECH_ARMOR_01",
                "equipped_hands": "EQ_TECH_GLOVES_01",
                "equipped_feet": "EQ_TECH_BOOTS_01",
                "equipped_necklace": None,
                "equipped_main_hand": "weapon_plasma_katana",
                "equipped_off_hand": None,
                "equipped_mount": None,
                "desc": "手持雙刀的流浪劍士，刀法迅捷凌厲如同疾風，擅長在短時間內施展多次高速斬擊。"
            }
            team_roster.append(new_member_fengwuhen)
            
        # 重置全隊休息室談心與修煉配額
        global current_main_stage_index
        current_main_stage_index = max(current_main_stage_index if 'current_main_stage_index' in globals() else 1, 5)
        if 'reset_teammate_chat_quota' in globals():
            reset_teammate_chat_quota()
            
        if renpy.loadable("audio/levelup.ogg"):
            renpy.sound.play("audio/levelup.ogg")
            
    z "【主線任務 · 修真神魔世界（蜀山血海封印）已完美通關！】"
    z "結算統計：成功斬殺血魔長老！隊長顧臨淵突破『基因鎖階級三』！\n魔法學者【艾莉絲】與雙刀浪人【風無痕】生還加入團隊！\n獲得獎勵：生存點數 +3,500 點、A 階命運碎片 x1、B 階命運碎片 x1！"
    z "目前持有總點數：[points] 點。"
    
    ailisi "顧隊長，在生死一瞬展現的預知洞察力令人震撼！我很樂意加入你的團隊，探索更多宇宙的終極真理。"
    fengwuhen "這把雙刀，從今往後只為中洲隊而拔。"
    
    scene bg_main_room_topdown with fade
    "金光消散，全員沐浴在輪迴聖光中，昂首凱旋返回輪迴空間中央廣場！"
    
    jump main_room_exploration


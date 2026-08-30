# 📜 《輪迴世界》開發規格書 - 15: 團戰機制與第五關劇情 (1_5_Team_Battle_India)

本文件定義《輪迴世界》的「純劇情化團戰系統（Plot-Driven Team Battle）」運作機制，以及第五副本「木乃伊遺跡 · 印洲隊團戰遭遇戰」的完整主線劇情腳本 (`team_battle_india.rpy`)、角色登場名單、戰力對決、材料採集與專屬 AI 視覺提示詞。

---

## 1. 團戰系統劇情化運作機制 (Team Battle Rules)

為了保持遊戲戰鬥程式簡潔並凸顯故事張力，團戰機制採取 **「純劇情與文字演出驅動（Plot-Driven）」**，不引入複雜的程式動態計分演算與扣分計數器：

1. **降臨時間差（劇情設定）：** 劇本固定設定敵對小隊（印洲隊）評價較低，**已提前 20 分鐘降臨**並控制了當地的「阿努比斯沙土軍團」與卡納克神廟地形，我方一降臨即處於「突圍與破局」的被動優勢陣型。
2. **正負分與擊殺廣播（對話框與系統提示）：** 
   * 當我方角色（如林微或顧臨淵）在劇情/戰鬥中擊殺敵方成員時，畫面彈出主神經典提示（如：`【擊殺印洲隊精神感應者，獲得點數 2,000 點、B 級碎片 x1】`）。
   * 劇情中透過資深者或智者的對話強調「每陣亡一人扣 2,000 點，負分抹殺」的殘酷規則，營造緊迫感，但結算時固定以我方順利大勝、獲取高額點數通關。
3. **心靈與精神戰力對決：** 透過智者「言朔」發動心靈防禦屏障，在劇情中化解印洲隊精神感應者「莎拉」的精神迷霧干擾，為隊友創造精準切入敵方後排的戰機。

---

## 2. 副本核心背景與登場角色對照

### 2.1 人員對照表
* **中洲隊 (我方陣營):**
  * **破局隊長 (MAIN):** **顧臨淵**（已解鎖基因鎖階級三，預知敵方動向並正面硬剛敵方隊長）。
  * **資深引導者 (GUIDE):** **冷月**（爆發四翼天使血統，壓制敵方空戰與近戰）。
  * **智者智囊 (REC_003):** **言朔**（精神壁障防禦，微操指導刺客林微切後排）。
  * **重裝主力 (REC_001):** **陸沉**（前排正面抵擋變身狼人）。
  * **遠程支援 (REC_015):** **艾莉絲**（魔法學者，大範圍聖光淨化阿努比斯軍團）。
  * **新登場刺客 (REC_006):** **林微**（趙櫻空原型，本關全新登場！暗影刺客，發動影襲秒殺敵方精神感應者）。
* **印洲隊 (Team India - 敵對陣營):**
  * **巴魯特 (狼人隊長 - 原型: 伊瑪尼):** B級狼人變身血統，高 HP、高物防重裝前排。
  * **莎拉 (精神感應者 - 原型: 雪莉):** 精神心理控制者，發動心靈衝擊與迷霧干擾。
  * **阿努比斯死士:** 印洲隊召喚的無限不死沙土軍團前排。

---

## 3. Ren'Py 主線劇情腳本範例 (`team_battle_india.rpy`)

```renpy
label stage_1_5_team_battle_india:
    scene bg_egypt_pyramid_desert with fade
    
    # -------------------------------------------------------------
    # 1. 傳送降臨與團戰廣播劇情
    # -------------------------------------------------------------
    play sound "god_broadcast.wav"
    "【主神嚴肅無情的廣播聲響起：進入副本『木乃伊 / 死者之城』！】"
    "【警告！檢測到『印洲隊』已於 20 分鐘前降臨本世界！】"
    "【團戰規則啟動：擊殺敵對小隊成員獲得點數與獎勵碎片；團戰結束時若團隊總積分為負，全員抹殺！】"
    
    show portrait_yanshuo_m at center
    yanshuo "（推了推眼鏡，冷靜地關閉手環面板）敵方比我們早到 20 分鐘。這意味著他們已經佔據了卡納克神廟的有利地形，並且控制了當地的阿努比斯軍團。"
    
    show portrait_linwei_f at right
    linwei "（雙手反握暗影雙刃，冷冷開口）對方的精神感應者剛才嘗試掃描我們……但被言朔的精神壁障隔絕了。"
    
    show portrait_gulin_m at left
    gulin "印洲隊把我們當成送上門的獎勵點數了。陸沉、冷月，準備正面迎敵！林微，尋找機會繞去後排切掉他們的精神感應者！"
    
    # -------------------------------------------------------------
    # ⚔️ 【第一波戰鬥】：阿努比斯沙土軍團 (阻擋機制測試)
    # -------------------------------------------------------------
    scene bg_desert_temple_entrance with flash
    "【印洲隊召喚的數百隻『阿努比斯死士』從狂暴的沙暴中湧出，組成鋼鐵前排！】"
    "【提示：阿努比斯軍團具備『不死沙體』，請使用艾莉絲的大範圍聖光魔法進行淨化！】"
    
    show portrait_ailisi_f at right
    ailisi "太陽神之光 —— 淨化此地的邪靈！"
    
    # 呼叫第一波戰鬥（清掃敵方召喚前排）
    call battle_start(stage_id="1-5_WAVE_1_SUMMONS")
    
    "【第一波戰鬥結束，艾莉絲成功淨化沙土軍團！】"
    
    # -------------------------------------------------------------
    # 💣 【第二波戰鬥】：印洲隊主力對決 (雙智者博弈 + 林微切後排)
    # -------------------------------------------------------------
    scene bg_pyramid_interior_core with flash
    play sound "wolf_howl.wav"
    
    "金字塔核心祭壇前，印洲隊隊長巴魯特體型暴漲，化為高達 3 米的巨狼！"
    "巴魯特 『哈哈哈哈！中洲隊的菜鳥們，成為我們的獎勵點數吧！』"
    
    yanshuo "（透過心靈壁障向全隊發送微操指令）言朔：『顧臨淵，敵方精神感應者莎拉的位置在祭壇左上方石柱陰影處，防禦極低。』"
    
    gulin "林微，就是現在！發動暗影襲殺！"
    
    show portrait_linwei_f at right
    "【林微化為一道黑色殘影，瞬間越過狼人隊長，暗影雙刃精準刺穿莎拉的咽喉！】"
    
    # 播放主神擊殺廣播
    $ renpy.notify("【擊殺印洲隊精神感應者·莎拉！獲得獎勵點數 2,000 點、B 級命運碎片 x1！】")
    play sound "reward_point.wav"
    
    # 呼叫 Boss 戰 (印洲隊狼人隊長巴魯特)
    call battle_start(stage_id="1-5_WAVE_2_PVP_BOSS")
    
    "【第二波戰鬥結束，顧臨淵開啟基因鎖三階預知狼人動作，與陸沉合力將巴魯特斬首！】"
    $ renpy.notify("【擊殺印洲隊隊長·巴魯特！獲得獎勵點數 5,000 點、A 級命運碎片 x1！】")
    play sound "reward_point.wav"
    
    # -------------------------------------------------------------
    # 🧠 底層智者檢定：採集『太陽金字塔核心晶片』
    # -------------------------------------------------------------
    if player_party.max_int >= 100:
        menu:
            "【智者檢定】隊伍智力 >= 100，由言朔破解並奪取印洲隊遺留的『太陽金字塔核心晶片』":
                $ player_inventory.add("MAT_SOLAR_PYRAMID_CORE")
                "【成功採集太陽金字塔核心！可帶回個人房間『亞當 AI 3D 列印機』解鎖高階神聖武器列印！】"
            "直接搭乘傳送光柱回歸":
                pass
                
    "【主線任務『木乃伊遺跡擊滅印洲隊』完成！中洲隊最終獲勝，獲得高額獎勵點數！】"
    "【傳送光柱降臨，全員成功返回虛空大廳！】"
    $ player_progress.completed_main_stages["STAGE_1_5"] = True
    jump void_hall_main
4. 本關卡產出資材與家園生產連動 (10_Production_System.md)
通關第五副本或在關卡中進行智者檢定，可獲得以下專屬材料，帶回個人房間的「戰術指揮面板」：

太陽金字塔核心晶片 (MAT_SOLAR_PYRAMID_CORE):

解鎖生產： 解鎖「亞當 AI 3D 裝備列印機」高階配方 —— 「太陽神聖槍 (EQ_HOLY_SUN_GUN)」（高階能量武器，對靈體、惡魔與異形造成 200% 破甲傷害）。

印洲隊狼人基因精粹 (MAT_WOLF_GENE):

解鎖生產： 解鎖「生化基因合成儀」配方 —— 「獸化爆發血清 (ITEM_WOLF_SERUM)」（使用後 3 回合內近戰傷害 +40%，防禦力 +20，並每回合自動恢復 5% HP）。

5. 本關卡專屬 AI 視覺提示詞 (AI Prompts)
🖼️ 關卡背景圖 (Backgrounds - 16:9)
埃及金字塔沙漠 (bg_egypt_pyramid_desert.png)

Prompt: Epic ancient Egyptian desert landscape, massive stone pyramids, glowing golden sun in dusty sky, dark sci-fi anime concept art --ar 16:9

神廟遺跡入口 (bg_desert_temple_entrance.png)

Prompt: Ancient Egyptian temple ruins surrounded by giant sandstorm, glowing red jackal statues, eerie dark adventure concept art --ar 16:9

金字塔核心祭壇 (bg_pyramid_interior_core.png)

Prompt: Dark interior of ancient pyramid core, golden sarcophagus surrounded by floating blue laser runes, epic sci-fi high fantasy fusion, 2d game art --ar 16:9

👤 登場角色頭像 (Portraits - 1:1)
林微 (新登場暗影刺客) (portrait_linwei_f.png)

Prompt: Game avatar portrait, beautiful deadly female assassin, short black hair, wearing black stealth tactical suit with glowing purple trim, cold lethal eyes, anime art style --ar 1:1

巴魯特 (印洲隊狼人隊長) (portrait_team_india_leader.png)

Prompt: Game avatar portrait, monstrous werewolf warrior leader, savage glowing red eyes, sharp fangs, wearing tattered golden Egyptian armor, intimidating presence, anime art style --ar 1:1
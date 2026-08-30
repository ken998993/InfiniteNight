# 📜 《輪迴世界》開發規格書 - 13: 第三關劇情與機制 (1_3_The_Grudge)

本文件定義第三副本「日式靈異世界（咒怨凶宅 / 怨靈危機）」的主線劇情腳本 (`the_grudge.rpy`)、靈體物理免疫機制、精神力與詛咒蔓延、人員退場歷程、靈異資材採集與專屬 AI 提示詞。

---

## 1. 副本核心背景與陣容對照

### 1.1 人員對照表
* **破局主角 (MAIN):** **顧臨淵**（冷靜決斷，帶領團隊破解規律）。
* **資深引導者 (GUIDE):** **冷月**（資深執行者，對靈體攻擊手段有限）。
* **核心隊員 (REC_002):** **蘇曉**（精神感知型，預警怨靈靠近與詛咒強度）。
* **智者智囊 (REC_003):** **言朔**（理智分析伽椰子殺人的『接觸與空間詛咒邏輯』）。
* **新登場靈異主角 (REC_017):** **葉靈**（茅山道士原型，本關全新登場！提供靈氣符咒破除物理免疫）。
* **恐慌新人 (REC_013):** **莫離**（極度恐慌新人，違規獨自躲進閣樓遭怨靈吞噬）。

---

## 2. 副本特色環境與戰術機制

1. **靈體物理免疫 (Spirit Immunity):**
   * **物理無效：** 普通槍械、物理近戰（大劍、刀砍）對怨靈敵人造成 **0% 傷害（提示：【靈體免疫】無實體無效）**。
   * **破靈手段：** 必須使用葉靈的『朱砂驅魔符』、高階血統（如四翼天使/血族）、裝備附魔（強酸/靈光塗料）或消耗 MP 的能量技能。
2. **精神力與詛咒蔓延 (Curses & SAN Value):**
   * **詛咒氣場：** 副本中所有人每回合扣除 3% MP（精神力）。MP 降至 0 時進入【混亂瘋狂】狀態，無法選取目標。
3. **戰鬥 AP 規則實踐 (3 AP Normal / 4 AP AOE):**
   * 葉靈『破魔符』消耗 **3 AP**（單體靈術打擊）。
   * 葉靈『九天玄女驅魔陣』消耗 **4 AP**（全體靈體 AOE 清場）。
   * 開啟基因鎖可突破上限，達成「1 AP 喝精神藥水 + 3 AP 符咒攻擊」。

---

## 3. Ren'Py 主線劇情腳本範例 (`the_grudge.rpy`)

```renpy
label stage_1_3_the_grudge:
    scene bg_japanese_haunted_house with fade
    
    # -------------------------------------------------------------
    # 1. 傳送降臨與靈異氛圍 (1 資深者 + 顧臨淵 + 蘇曉 + 言朔 + 新人葉靈 & 莫離)
    # -------------------------------------------------------------
    "【主神光束消退，空氣中瀰漫著濃重的霉味與冰冷的怨氣……】"
    "【耳邊傳來一陣令人毛骨悚然的咯咯咯咯折骨聲……】"
    
    show portrait_yeming_m at right
    yanshuo "（觀察日式和室與牆上的日曆）……這裡是 1990 年代初期的日本東京都郊區。空氣溫度比體感低 8 度，屬於異常能量場。"
    
    show portrait_yeling_m at center
    yeling "（手握黃紙木劍，面色凝重）諸位小心！此地陰氣衝天，有極強的冤魂盤踞不散！"
    
    show portrait_moli_m at right
    moli "鬼……鬼啊！我不待在這裡！這地方太邪門了！"
    
    show portrait_gulin_m at left
    gulin "莫離！別亂跑！這個副本的怪物是靈體，單獨行動必死無疑！"
    
    # -------------------------------------------------------------
    # 💀 事故發生：新人莫離獨自逃往閣樓，遭伽椰子吞噬
    # -------------------------------------------------------------
    "新人莫離完全不聽勸告，尖叫著衝上二樓，把自己關進了黑暗的閣樓衣櫃中！"
    play sound "kayako_throat.wav"
    "【閣樓上方傳來極度恐怖的慘叫聲與骨骼撕裂聲，隨後一灘鮮血從天花板縫隙滲了下來……】"
    
    suxiao "莫離的生命訊號……消失了！詛咒已經鎖定我們所有人！"
    
    # -------------------------------------------------------------
    # ⚔️ 【第一波戰鬥】：怨念爬行體 (物理免疫測試)
    # -------------------------------------------------------------
    scene bg_tatami_room_dark with flash
    "【數隻黑髮纏繞的『怨念集結體』從地板縫隙中爬出！】"
    "【警告：敵方具備『靈體標籤』，普通槍械與物理砍擊無效！】"
    
    show portrait_luchen_m at left
    luchen "可惡！我的大劍砍上去像砍在空氣上一樣！"
    
    yeling "讓我來！天地玄宗，萬炁本根！破魔符 —— 敕！"
    
    # 呼叫第一波戰鬥（葉靈加入隊伍，使用符咒開路）
    call battle_start(stage_id="1-3_WAVE_1_SPIRIT")
    
    "【第一波戰鬥結束，葉靈的朱砂符咒成功淨化怨念體！】"
    
    # -------------------------------------------------------------
    # 💣 【第二波戰鬥】：伽椰子本體襲擊 (詛咒蔓延 + 全體驅魔陣)
    # -------------------------------------------------------------
    scene bg_staircase_curse with flash
    play sound "ghost_screaming.wav"
    
    "樓梯上方，一個全身慘白、關節扭曲的恐怖女鬼（伽椰子）爬了下來，伴隨著俊雄的貓叫聲！"
    "【環境懲罰：詛咒強度暴增！全隊每回合扣除 5% MP，若 MP 歸零將直接發狂！】"
    
    yanshuo "顧臨淵，伽椰子的攻擊帶有空間扭曲特性。必須在 3 回合內用高階靈力將其鎮壓，否則我們會在空間封閉中被抹殺！"
    
    gulin "葉靈！配合我的基因鎖爆發，用最大威力的『九天玄女驅魔陣』！"
    
    # 發放靈力支援，呼叫 Boss 戰
    call battle_start(stage_id="1-3_WAVE_2_BOSS")
    
    "【第二波戰鬥結束，葉靈發動絕招將伽椰子暫時封印入鎮魂鏡中，凶宅幻境破滅！】"
    
    # -------------------------------------------------------------
    # 🧠 底層智者檢定：採集『純陽靈木與怨念結晶』
    # -------------------------------------------------------------
    if player_party.max_int >= 100:
        menu:
            "【智者檢定】隊伍智力 >= 100，由言朔與葉靈提煉『陰陽怨念核心晶片』":
                $ player_inventory.add("MAT_SPIRIT_CORE")
                "【成功提煉怨念核心！可帶回個人房間『生化基因合成儀』解鎖靈力附魔武器與辟邪血清！】"
            "直接踏入傳送光柱離去":
                pass
                
    "【主線任務『咒怨凶宅生存』完成！傳送光束降臨，成功帶著新人道士葉靈返回虛空大廳！】"
    $ player_progress.completed_main_stages["STAGE_1_3"] = True
    jump void_hall_main


    4. 本關卡產出資材與家園生產連動 (10_Production_System.md)
通關第三副本或在關卡中進行智者檢定，可獲得以下專屬材料，帶回個人房間的「戰術指揮面板」：

陰陽怨念核心晶片 (MAT_SPIRIT_CORE):

解鎖生產： 解鎖「生化基因合成儀」高階配方 —— 「辟邪清心血清 (ITEM_SAN_SERUM)」（戰鬥中瞬間恢復 50% MP，並免疫詛咒 3 回合）。

茅山朱砂與靈木碎片 (MAT_TAOIST_RUNES):

解鎖生產： 解鎖「脈衝壓電整備台」配方 —— 「破魔靈光子彈/附魔塗料 (ITEM_SPIRIT_AMMO)」（賦予普通槍械與近戰武器打擊靈體的能力）。

5. 本關卡專屬 AI 視覺提示詞 (AI Prompts)
🖼️ 關卡背景圖 (Backgrounds - 16:9)
日式咒怨凶宅 (bg_japanese_haunted_house.png)

Prompt: Eerie traditional Japanese wooden house at night, foggy creepy atmosphere, glowing pale moonlight, Japanese suburban horror style, high resolution anime concept art --ar 16:9

榻榻米暗室 (bg_tatami_room_dark.png)

Prompt: Dark dimly lit traditional tatami room, bloody handprints on paper sliding doors, ominous shadows creeping from ceiling corners, psychological horror atmosphere --ar 16:9

詛咒樓梯與陰森走廊 (bg_staircase_curse.png)

Prompt: Creepy dark wooden staircase inside Japanese house, long black hair strands hanging from ceiling, pale blue ghostly fog, chilling horror atmosphere --ar 16:9

👤 登場角色頭像 (Portraits - 1:1)
葉靈 (茅山道士新人) (portrait_yeling_m.png)

Prompt: Game avatar portrait, young heroic Taoist exorcist, wearing modern black tactical coat over traditional yellow Taoist robe, holding a glowing magical paper rune, sharp eyes, anime art style --ar 1:1

莫離 (恐慌新人) (portrait_moli_m.png)

Prompt: Game avatar portrait, terrified young man with pale face and sweating forehead, trembling eyes, Japanese horror anime art style --ar 1:1
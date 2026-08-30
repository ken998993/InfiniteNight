Markdown
# 📜 《輪迴世界》開發規格書 - 14: 第四關劇情與機制 (1_4_Cultivation_Realm)

本文件定義第四副本「修真神魔世界（蜀山血海封印 / 血魔危機）」的主線劇情腳本 (`cultivation_realm.rpy`)、護體靈光與真實傷害機制、基因鎖三階突破、人員退場歷程、高階修真資材採集與專屬 AI 提示詞。

---

## 1. 副本核心背景與陣容對照

### 1.1 人員對照表
* **破局主角 (MAIN):** **顧臨淵**（在本關戰鬥中感應生死危機，正式**突破『基因鎖階級三』**，獲得敵方招式預測與動態洞察）。
* **資深引導者 (GUIDE):** **冷月**（發動四翼天使血統，正面對抗魔教長老）。
* **智者智囊 (REC_003):** **言朔**（以極致理智破解『蜀山封魔大陣』的陣眼符文）。
* **新登場魔法學者 (REC_015):** **艾莉絲**（魔法/法術型原型，本關全新傳送登場！提供護盾破解與元素支援）。
* **新登場雙刀浪人 (REC_019):** **風無痕**（遊俠刺客原型，近戰暴擊輸出）。
* **貪婪新人 (REC_012):** **段恆**（因貪圖血海中的靈石私自離隊，被血魔吸乾精血爆體死亡）。

---

## 2. 副本特色環境與戰術機制

1. **護體靈光與真氣值 (Barrier & QI System):**
   * **護體靈光 (Barrier):** 魔教修士與血魔具備高額護體靈光（相當於額外護盾）。一般物理攻擊需優先扣除靈光，只有使用**元素法術（艾莉絲）**或**基因鎖暴擊**才能造成「貫穿真實傷害」。
   * **靈氣威壓 (QI Suppression):** 副本中靈氣狂暴，角色使用技能消耗 MP 增加 50%。
2. **基因鎖階級三突破 (Gene Lock Tier 3):**
   * 顧臨淵在本關生死戰中解鎖 Tier 3，開啟後消耗 1 AP，當回合 AP 突破至 5 AP，且 **預知敵方下一回合所有攻擊目標與招式**，暴擊率提升 40%。
3. **戰鬥 AP 規則實踐 (3 AP Normal / 4 AP AOE):**
   * 艾莉絲『元素破靈箭』消耗 **3 AP**（單體真實法術打擊）。
   * 風無痕『雙刃血風暴』/ 艾莉絲『天火焚世』消耗 **4 AP**（全體範圍 AOE 轟炸）。

---

## 3. Ren'Py 主線劇情腳本範例 (`cultivation_realm.rpy`)

```renpy
label stage_1_4_cultivation_realm:
    scene bg_shushan_floating_mountain with fade
    
    # -------------------------------------------------------------
    # 1. 傳送降臨與修真仙境 (顧臨淵 + 冷月 + 言朔 + 新人艾莉絲 & 風無痕 & 段恆)
    # -------------------------------------------------------------
    "【主神光束消退，眼前的景色變為浮空千丈的仙山懸崖，遠方血雲翻滾，劍氣縱橫！】"
    
    show portrait_ailisi_f at right
    ailisi "（撫摸空氣中的游離能量）……好濃郁的元素濃度！這不是科技世界，而是高階魔法或修真位面！"
    
    show portrait_fengwuhen_m at center
    fengwuhen "（壓低草帽，手按雙刀刀柄）空氣中有很濃的血腥味與殺氣，大家小心。"
    
    show portrait_duanheng_m at right
    duanheng "（看見地上散落的發光靈石）哈哈！這石頭發光，一定是寶物！發財了！"
    
    show portrait_gulin_m at left
    gulin "段恆！住手！不要碰此地的任何物品！"
    
    # -------------------------------------------------------------
    # 💀 事故發生：貪婪新人段恆私拿血靈石，被血魔吸乾爆體
    # -------------------------------------------------------------
    "段恆完全不聽勸告，一把撿起地上的血紅色靈石。"
    play sound "blood_suck.wav"
    "【靈石瞬間化為無數血色藤蔓刺入段恆體內，短短三秒內將他吸成乾屍爆開！】"
    
    yanshuo "（推了推眼鏡）確認標的物具備『生物寄生與精血吸附』特性，屬於極高危險物質。"
    
    # -------------------------------------------------------------
    # ⚔️ 【第一波戰鬥】：血傀儡怪群 (護體靈光機制測試)
    # -------------------------------------------------------------
    scene bg_shushan_cave_entrance with flash
    "【無數由精血凝聚的『血傀儡』從血海中湧出，地表張開高濃度的血色護體靈光！】"
    "【提示：敵方擁有 500 點『護體靈光』，請使用艾莉絲的元素法術破甲！】"
    
    ailisi "交給我！元素解離術 —— 破！"
    
    # 呼叫第一波戰鬥（艾莉絲加入隊伍破盾）
    call battle_start(stage_id="1-4_WAVE_1_BARRIER")
    
    "【第一波戰鬥結束，艾莉絲成功破除護體靈光，風無痕雙刀清場！】"
    
    # -------------------------------------------------------------
    # 💣 【第二波戰鬥】：血魔長老本體與顧臨淵基因鎖三階突破
    # -------------------------------------------------------------
    scene bg_shushan_blood_pool with flash
    play sound "demon_roar.wav"
    
    "眾人踏入蜀山封魔洞底層，巨大血池中伸出萬千血刃，血魔長老顯化巨大法相！"
    "【血魔長老發動全體禁錮『血海滔天』，恐怖的威壓讓眾人無法移動！】"
    
    gulin "（在極致的死亡壓力下，腦海中基因鏈瘋狂解鎖崩裂……）"
    "【警告！顧臨淵成功突破『基因鎖階級三』！獲得意識超算與敵方招式預知能力！】"
    
    gulin "言朔！我看到了！血魔長老下一回合的攻勢在左側陣眼！冷月、風無痕，跟我集中一點轟擊！"
    
    # 呼叫 Boss 戰 (開啟基因鎖三階)
    call battle_start(stage_id="1-4_WAVE_2_BOSS")
    
    "【第二波戰鬥結束，顧臨淵憑藉預知能力精準斬斷血核，蜀山封印成功修復！】"
    
    # -------------------------------------------------------------
    # 🧠 底層智者檢定：採集『天雷靈石與封魔陣法核心』
    # -------------------------------------------------------------
    if player_party.max_int >= 100:
        menu:
            "【智者檢定】隊伍智力 >= 100，由言朔解析並抽取『蜀山天雷靈石核心』":
                $ player_inventory.add("MAT_THUNDER_SPIRIT_STONE")
                "【成功採集天雷靈石！可帶回個人房間『脈衝壓電整備台』解鎖天雷附魔與飛劍武器列印！】"
            "直接踏入傳送光柱離去":
                pass
                
    "【主線任務『蜀山血海封印』完成！傳送光束降臨，成功帶領艾莉絲與風無痕返回虛空大廳！】"
    $ player_progress.completed_main_stages["STAGE_1_4"] = True
    jump void_hall_main
4. 本關卡產出資材與家園生產連動 (10_Production_System.md)
通關第四副本或在關卡中進行智者檢定，可獲得以下專屬材料，帶回個人房間的「戰術指揮面板」：

蜀山天雷靈石核心 (MAT_THUNDER_SPIRIT_STONE):

解鎖生產： 解鎖「脈衝壓電整備台」高階配方 —— 「天雷電磁飛劍 / 天雷槍械彈藥 (ITEM_THUNDER_AMMO)」（戰鬥中使攻擊附加雷電真實傷害，並有 30% 機率麻痺敵方 1 回合）。

千年血魔精粹 (MAT_DEMON_ESSENCE):

解鎖生產： 解鎖「生化基因合成儀」配方 —— 「狂暴精血狂熱血清 (ITEM_BERSERK_SERUM)」（戰鬥中消耗 20% HP，換取當回合 ATK +50% 與額外 +1 AP）。

5. 本關卡專屬 AI 視覺提示詞 (AI Prompts)
🖼️ 關卡背景圖 (Backgrounds - 16:9)
蜀山浮空仙山 (bg_shushan_floating_mountain.png)

Prompt: Epic sci-fi fantasy scene, floating mountain islands in clouds, ancient Chinese Taoist temples with glowing magic runes, blood-red clouds on the horizon, cinematic anime art style --ar 16:9

封魔洞入口 (bg_shushan_cave_entrance.png)

Prompt: Dark mystical mountain cave entrance, glowing blue lightning runes carved into stone walls, sinister red mist creeping from dark depths, xianxia horror concept art --ar 16:9

血海封印池 (bg_shushan_blood_pool.png)

Prompt: Dark underground cavern with massive pool of glowing red demonic blood, glowing magical array swords floating above, dark high fantasy atmosphere, epic 2d game concept art --ar 16:9

👤 登場角色頭像 (Portraits - 1:1)
艾莉絲 (魔法學者新人) (portrait_ailisi_f.png)

Prompt: Game avatar portrait, beautiful young female mage scholar, long silver hair, holding a glowing crystal staff, wearing elegant blue tactical robes, intelligent eyes, anime art style --ar 1:1

風無痕 (雙刀浪人新人) (portrait_fengwuhen_m.png)

Prompt: Game avatar portrait, handsome wandering ronin samurai, sharp dark eyes, wearing dark straw hat and black tactical martial arts coat, holding dual katana handles, anime art style --ar 1:1
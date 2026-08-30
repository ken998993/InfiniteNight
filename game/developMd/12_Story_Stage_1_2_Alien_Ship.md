# 📜 《輪迴世界》開發規格書 - 12: 第二關劇情與機制 (1_2_Alien_Ship)

本文件定義第二副本「太空真空世界（幽靈探索母艦 / 異形危機）」的主線劇情腳本 (`alien_ship.rpy`)、新人傳送與規則說明劇情、無重力與槍械封印機制、人員退場歷程、材料搜集與專屬 AI 提示詞。

---

## 1. 副本核心背景與陣容替換對照

### 1.1 人員對照表
* **破局主角 (MAIN):** **顧臨淵**（原創破局者，擁有銳利的戰術洞察力）。
* **資深引導者 (GUIDE):** **冷月**（資深執行者，冷酷現實）。
* **核心隊員 (REC_002):** **蘇曉**（精神/情報型，分析母艦結構與異形生態）。
* **主力戰力 (REC_001):** **陸沉**（重裝輸出手，承擔隊伍正面硬剛重任）。
* **智者智囊 (REC_003):** **言朔**（軍方智囊，本關全新傳送登場的新人！）。
* **遠程狙擊 (REC_005):** **凌澈**（冷酷槍手/刺客）。
* **恐慌新人 (REC_013):** **韓羽**（極度恐慌的新人，觸發寄生死亡）。
* **自私新人 (REC_012):** **段恆**（投機取巧的新人，違規觸發陷阱死亡）。

---

## 2. 新人傳送與規則說明機制

每進入一個全新副本，主神光束強制傳送 **2~3 名新玩家** 加入隊伍：

1. **新人傳送醒來：** 新人（言朔、韓羽、段恆）在異形母艦冰冷的鐵地板上醒來，產生混亂與質疑。
2. **資深者與資深隊員講解（世界觀與生存規則）：**
   * **冷月（冷酷威壓）：** 展示點數手環，警告「完成任務活著回去，否則直接抹殺」。
   * **蘇曉（情報解析）：** 為新人解答「這裡不是遊戲，是真實的死亡拷問」。
   * **顧臨淵（戰術領導）：** 提醒新人「聽從指揮，不要隨便碰觸任何外星膠囊與密封閥門」。

---

## 3. Ren'Py 主線劇情腳本範例 (`alien_ship.rpy`)

```renpy
label stage_1_2_alien_ship:
    scene bg_alien_ship_hub with fade
    
    # -------------------------------------------------------------
    # 1. 主神光束降臨，新人醒來與規則說明劇情
    # -------------------------------------------------------------
    "【主神傳送光速消退，強烈的失重感與血腥味襲來……】"
    
    show portrait_hanyu_m at right
    hanyu "這……這是哪裡？！我不是剛在網咖上網嗎？你們是誰？綁架嗎？！"
    
    show portrait_duanheng_m at right
    duanheng "操！少跟我裝神弄鬼！老子有的是錢，開個價放我走！"
    
    show portrait_yanshuo_m at center
    yanshuo "（冷靜地觀察四周金屬結構與手腕上的黑科技手環）……大氣壓異常、金屬結構超越現有科技。這不是任何已知的影視基地。"
    
    show portrait_lengyue_f at left
    lengyue "吵死了。再叫一聲，我就在主神抹殺你們之前先扣動扳機。"
    
    show portrait_suxiao_f at left
    suxiao "新人們，聽好了。你們已經不在原本的世界了。這裡叫《輪迴世界》，手環上是你們這場副本的任務 —— 在這艘母艦上『生存 24 小時』。"
    
    show portrait_gulin_m at center
    gulin "我是顧臨淵。想活命就記住三件事：第一，跟緊隊伍；第二，別碰任何發光的卵或閥門；第三，這裡死了就是真的死了。"
    
    show portrait_luchen_m at left
    luchen "嘿，聽顧哥的準沒錯！上次在極光重工不聽話的人，連骨頭灰都沒剩下來！"
    
    # -------------------------------------------------------------
    # 💀 事故發生：恐慌新人韓羽觸發面幼體 (Facehugger) 寄生
    # -------------------------------------------------------------
    "眾人開始探索走廊，新人韓羽因為極度恐慌，擅自開啟了廢棄的生物儲藏艙門！"
    play sound "facehugger_attack.wav"
    "【一道黑影從破裂的外星異形卵中爆射而出，死死扣住了韓羽的面罩！】"
    
    suxiao "韓羽！別動！牠正在透過氣孔往你體內注入胚胎……"
    yanshuo "（冷酷地推了推眼鏡）生物訊號顯示其胚胎已進入寄主胸腔。為防止二次擴散，建議立刻執行淨化。"
    
    # -------------------------------------------------------------
    # ⚔️ 【第一波戰鬥】：真空環境 + 幼體怪群戰鬥 (槍械封印測試)
    # -------------------------------------------------------------
    scene bg_alien_corridor_vacuum with flash
    "【警告：進入真空無重力區域！普通火藥槍械已被封印限制！】"
    "【敵方『異形幼體群』從天花板無重力爬行襲來！】"
    
    # 呼叫第一波戰鬥
    call battle_start(stage_id="1-2_WAVE_1_VACUUM")
    
    "【第一波戰鬥結束，顧臨淵與陸沉憑藉近戰武器成功清空幼體！】"
    
    # -------------------------------------------------------------
    # 💀 破胸體爆發與異形進化
    # -------------------------------------------------------------
    "躺在地上昏迷的韓羽突然劇烈抽搐，胸腔伴隨骨骼碎裂聲轟然炸開！"
    "一隻血淋淋的異形幼體破胸而出，以極快的速度遁入暗壓壓的通風管道中。"
    
    lengyue "該死，牠去母艦核心汲取核燃料進化了！"
    yanshuo "顧臨淵，如果任由牠進化成『異形皇后』，我們所有人死亡率為 99.8%。必須立刻去中央機房。"
    
    # -------------------------------------------------------------
    # 💣 【第二波戰鬥】：成熟期異形獵手 (無重力 + 飛行標籤機制)
    # -------------------------------------------------------------
    scene bg_alien_core_reactor with flash
    
    "眾人踏入機房，巨大高聳的異形皇后懸掛在中央反應爐上方，兩側伏擊著數隻『異形獵手』！"
    "【異形獵手獲得『無重力飛行標籤』，直接越過前排陸沉，撲向後排的蘇曉與言朔！】"
    
    gulin "陸沉、言朔！穿上『懸浮飛靴』，獲取無重力標籤攔截牠們！"
    
    # 發放飛靴戰術支援，呼叫 Boss 戰
    call battle_start(stage_id="1-2_WAVE_2_BOSS")
    
    "【第二波戰鬥結束，顧臨淵利用爆破點精準炸毀反應爐，異形皇后被推進太空真空死寂中！】"
    
    # -------------------------------------------------------------
    # 🧠 底層智者檢定：言朔採集異形 DNA 晶片
    # -------------------------------------------------------------
    if player_party.max_int >= 100:
        menu:
            "【智者檢定】隊伍智力 >= 100，由言朔採集『異形皇后酸性 DNA 突變株』":
                $ player_inventory.add("MAT_ALIEN_QUEEN_DNA")
                "【成功採集異形皇后 DNA！可帶回個人房間『生化基因合成儀』解鎖腐蝕強酸武器生產！】"
            "直接搭乘逃生艙離開":
                pass
                
    "【主線任務『幽靈母艦生存』完成！傳送光束降臨，成功帶著新人言朔返回虛空大廳！】"
    $ player_progress.completed_main_stages["STAGE_1_2"] = True
    jump void_hall_main
4. 本關卡產出資材與家園生產連動 (10_Production_System.md)
通關第二副本或在關卡中進行智者檢定，可獲得以下專屬材料，帶回個人房間的「戰術指揮面板」：

異形皇后酸性 DNA 突變株 (MAT_ALIEN_QUEEN_DNA):

解鎖生產： 解鎖「生化基因合成儀」高階配方 —— 「腐蝕強酸塗料 (ITEM_ACID_COATING)」（賦予武器 3 回合無視 50% 防禦的中毒酸蝕效果）。

太空零重力合金 (MAT_ZERO_G_ALLOY):

解鎖生產： 解鎖「脈衝壓電整備台」配方 —— 「懸浮組件 (EQ_TECH_BOOTS_01)」（批量列印懸浮飛靴）。

5. 本關卡專屬 AI 視覺提示詞 (AI Prompts)
🖼️ 關卡背景圖 (Backgrounds - 16:9)
幽靈母艦大廳 (bg_alien_ship_hub.png)

Prompt: Dark futuristic spaceship interior, eerie abandoned sci-fi hallway, biological resin webbing on metal bulkheads, blue emergency lighting, realistic detail, 2d game concept art --ar 16:9

真空走廊 (bg_alien_corridor_vacuum.png)

Prompt: Damaged spaceship corridor opening into outer space, floating zero-gravity debris, dark cosmic background with distant stars outside the hull breach, sci-fi atmosphere --ar 16:9

異形皇后機房反應爐 (bg_alien_core_reactor.png)

Prompt: Epic sci-fi reactor core chamber, massive alien queen structure suspended over glowing plasma core, sinister dark atmospheric lighting, high resolution game concept art --ar 16:9

👤 登場角色頭像 (Portraits - 1:1)
顧臨淵 (主角) (portrait_gulin_m.png)

Prompt: Game avatar portrait, determined young male sci-fi tactician, sharp intelligent eyes, short messy dark hair, wearing sleek black carbon fiber suit, anime art style --ar 1:1

蘇曉 (portrait_suxiao_f.png)

Prompt: Game avatar portrait, smart female intel officer with short brown hair, wearing tactical glasses, calm expression, blue holographic HUD reflecting on face, anime art style --ar 1:1

言朔 (新加入智者) (portrait_yanshuo_m.png)

Prompt: Game avatar portrait, cold intellectual male strategist, silver hair, rimless glasses, wearing neat high-tech suit, calculating look, anime art style --ar 1:1

韓羽 (恐慌新人) (portrait_hanyu_m.png)

Prompt: Game avatar portrait, panicked young male rookie, terrified face, sweaty forehead, casual clothing in dark sci-fi hallway, anime art style --ar 1:1
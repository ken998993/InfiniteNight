# 📜 《輪迴世界》開發規格書 - 09: 第一關劇情與教學流程 (1_1_Zombie_City)

本文件定義第一副本「喪屍末日世界 · 諾克斯市（極光重工地下研究所）」的主線劇情腳本 (`zombie_city.rpy`)、團隊人員死亡退場機制、點擊式戰術推進地圖、兩波戰鬥教學與專屬 AI 視覺提示詞。

---

## 1. 團隊開局陣容與人員存活歷程 (Party Status Flow)

* **開局人員（共 7 人）：** 
  * 1 個資深者：資深執行者「冷月」。
  * 6 個新人：主角 (顧臨淵)、白領青年「項天」、心靈感應少女「蘇曉」、刺青流氓「趙虎」、驚慌青年「周揚」、發福大叔「錢富貴」。

* **死亡與退場淘汰鏈：**
  1. **趙虎 (刺青流氓) — 擅自離隊死：** 10 分鐘保護光幕碎裂後，不信邪撞開密封閥門，觸發「超音波奈米防禦」被瞬間分解成透明黏液（警告玩家不可違規）。
  2. **周揚 (驚慌青年) — 第一波戰鬥死：** 突入生化隔離防爆大門時，因恐慌擅離前排陣型，被第 1 波敏捷型喪屍 (agile_zombie) 撲倒咬喉致死（展示前後排保護陣型的重要性）。
  3. **錢富貴 (慢吞吞大叔) — 毒氣關門死：** 第 2 波毒氣走廊戰鬥清場後，安全防爆門發出 5 秒閉合倒數，錢富貴體能不足被困在門外，遭高壓毒氣焚化與重裝閘門重重阻隔。
  4. **最終存活人數 (4 人)：** **資深者 (冷月) + 主角 (顧臨淵) + 2 個生還新人 (項天 & 蘇曉)**，四人一同回歸輪迴空間廣場。

---

## 2. 深度世界觀交代與開局四大階段 (Opening & Worldbuilding)

1. **【第一階段：10分鐘保護光幕降臨與新人甦醒】**
   * 伴隨時空扭曲眩暈感，6 名互不相識的新人（顧臨淵、項天、蘇曉、趙虎、周揚、錢富貴）跌落在 B1 外部聯絡站，四周籠罩淡金色半透明保護光幕（倒數 09分59秒）。
   * 輪迴系統身份覆蓋：`極光重工安保部 · 第 7 應急支援組`。
   * 新人們各自產生普通人應有的真實反應（錢富貴發抖要回家、周揚恐慌求饒、趙虎暴躁罵街、項天觀察腕錶、蘇曉憑作家直覺觀察生化警告標籤與濃煙中的人影）。
   * 資深者**冷月**冷酷喝止新人，詳細解說 10 分鐘保護光幕與「不可暴露輪迴空間否則抹殺」的鐵律。
2. **【第二階段：極光安保隊長（雷恩）登場與斥責】**
   * 雷恩隊長（`aurora_captain`）身著深藍外骨骼裝甲登場，斥責總部派來連站都站不穩的外包臨時工。
3. **【第三階段：資深者冷月上前交涉與三大世界觀深度交代】**
   * 只有資深者**冷月**了解輪迴任務情境，主動亮出外包應急電子授權碼，向雷恩隊長報告並要求簡報地下設施現況。
   * **諾克斯市與生化浩劫：** 3 天前水源污染，全市 9 成市民變異，城市被外圍防爆門封鎖為死城。
   * **地下研究所與失控主機 ADAM：** B4 超級電腦 A.D.A.M. 判定 7 級洩漏啟動自毀封鎖協議，釋放毒氣並鎖死各層。
   * **極光畸變體與狂暴屍潮：** 死亡研究員變異為敏捷型喪屍（`agile_zombie`），骨刺外露、天花板攀爬、保留開門肌肉記憶。
4. **【第四階段：發放 tactical_hazmat_armor 戰術服與破幕】**
   * 雷恩隊長發放戰術服（中央展示），冷月喝令新人全員穿戴。
   * 保護光幕倒數歸零如玻璃碎裂，趙虎違抗命令踢門被超音波分解。
   * 雷恩隊長開啟戰術俯瞰全息藍圖（`stage_1_1_tactical_map_screen`）啟動推進。

---

## 3. 劇情推進與戰鬥流程腳本範例 (`zombie_city.rpy`)

```renpy
label stage_1_1_zombie_city:
    scene bg_aurora_lab_entrance with fade
    
    # 1. 10分鐘保護光幕降臨與開局
    "【輪迴終端播報】：當前世界：【末日廢墟 · 諾克斯市】，新手保護光幕已啟動（09分59秒）！"
    
    # 2. 安保隊長雷恩登場與世界觀交代
    show aurora_captain at center with dissolve
    aurora_captain "總部怎麼派來你們這群外包臨時工？！"
    
    # 3. 發放戰術服與著裝
    python:
        add_item("tactical_hazmat_armor", 1)
    show tactical_hazmat_armor at item_show_center with dissolve
    "【獲得戰術裝備：【tactical_hazmat_armor 戰術服】已放入背包！】"
    hide tactical_hazmat_armor with dissolve
    
    # 4. 光幕碎裂與趙虎違規死亡
    "倒數歸零，金色光幕寸寸碎裂！趙虎強行踹門被超音波分解成黏液！"
    
    # 5. 點擊式戰術地圖推進（階段 1：防爆大門）
    call screen stage_1_1_tactical_map_screen(current_step=1)
    
    # 6. 【第一波戰鬥】：3 隻敏捷型喪屍 (周揚脫隊死亡)
    call screen party_deployment_screen
    call screen battle_screen(b_wave1)
    
    # 7. 點擊式戰術地圖推進（階段 2：電梯井與毒氣走廊）
    call screen stage_1_1_tactical_map_screen(current_step=2)
    
    # 8. 【第二波戰鬥】：毒氣走廊 + high_explosive 高爆手雷 (錢富貴被防爆門隔絕死亡)
    $ add_item("high_explosive", 2)
    call screen battle_screen(b_wave2)
    
    # 9. 點擊式戰術地圖推進（階段 3：神經核心機房）
    call screen stage_1_1_tactical_map_screen(current_step=3)
    
    # 10. A.D.A.M. 核心與智者檢定 (隊伍最高 INT >= 100)
    if player_party.max_int >= 100:
        "【智者判定成功！】下載【亞當神經元矩陣備份 (adamcore.jpg)】！"
    
    # 11. 回歸輪迴空間廣場與冷月新手導引
    $ player_progress.completed_main_stages["STAGE_1_1"] = True
    jump main_room_exploration
```

---

## 4. 本關卡美術資源與命名綁定 (Asset Mappings)

### 🖼️ 關卡背景圖
* **極光重工實驗室入口：** `images/zombie_street.PNG` (`bg_aurora_lab_entrance`)
* **極光重工生化走廊：** `images/zombie_street.PNG` (`bg_aurora_corridor`)
* **生物神經網絡核心機房：** `images/adamcore.jpg` (`bg_aurora_core`)
* **戰術俯瞰全息藍圖：** `images/zombieCityMap.jpg` (`stage_1_1_tactical_map_screen`)

### 👤 登場角色與頭像
* **資深者：冷月：** `images/coldmoon.PNG` / `images/portrait_lengyue_f.jpg`
* **女作家·蘇曉：** `images/femalewriter.PNG`
* **極光安保隊長·雷恩：** `images/securegurde.jpg`

### 🧟 怪物陣容 (主線劇情嚴格限制 2 種)
* **敏捷型喪屍 (Tier 1 高速突變體)：** `images/agile_zombie.jpg` (`agile_zombie`)
* **變異腐屍 (Tier 1 劇毒近戰體)：** `images/zombie.jpg` (`MOB_ZOMBIE_01`)

### 💣 專屬道具與展示
* **tactical_hazmat_armor 戰術服：** `images/tactical_hazmat_armor.jpg`
* **high_explosive 高爆破片手雷：** `images/high_explosive_fragmentation_grenade.jpg`
* **亞當神經元矩陣備份 (A.D.A.M. Core)：** `images/adamcore.jpg`
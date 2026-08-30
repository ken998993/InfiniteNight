# 📜 《輪迴世界》開發規格書 - 17: 喪屍末日世界 (Zombie City) 完整遊戲內容與戰術地圖規格書

本文件定義第一副本「喪屍末日世界 · 極光重工遺址」的完整遊戲內容，包含主線劇情 (`zombie_city.rpy`)、全息戰術大地圖自由探索 (`zombieCityMap.jpg` / `zombie_city_map_screen`)、7 大戰術據點、已肅清狀態鎖定與怪物刷新機制、生命持久化規則及美術素材綁定。

---

## 1. 副本概覽與環境機制 (World Overview & Hazard)

* **副本名稱：** 喪屍末日世界 · 極光重工遺址 (Zombie City - Aurora Heavy Industry)
* **世界背景：** 極光重工地下生化研發中心發生 4 級生化病毒洩漏事故，底層生物超級電腦 A.D.A.M. 啟動自毀與安全防禦程序。企業武裝清理隊封鎖現場，將輪迴者視為開路工具。
* **環境懲罰：** 【☣️ 高溫生化毒氣】——走廊與部分密閉區域每回合扣除 5% 最大生命值。
  * **抗性解法：** 裝備 `tactical_hazmat_armor 戰術服` 或融合環境適應型血統即可 100% 免疫毒氣扣血。

---

## 2. 主線劇情模式：點擊式戰術地圖推進機制 (方案 2 · DOOM/暗黑地牢模式)

為了兼顧劇情代入感、戰術沉浸感與 0 卡頓流暢度，主線劇情（`zombie_city.rpy`）採用 **「點擊式戰術地圖（方案 2）」** 串接兩波戰鬥與事件推進 (`stage_1_1_tactical_map_screen`)：

```text
               ┌────────────────────── 主線戰術推進地圖 (方案 2) ──────────────────────┐
               │                                                                      │
               │   [ 🚪 區域一：防爆大門 ] ──► [ 🛗 區域二：電梯井毒氣 ] ──► [ 🧠 區域三：神經核心 ]  │
               │   (突破第一波 3 隻敏捷喪屍)   (投擲手雷突破 5 隻密集怪)   (智力 >= 100 駭入下載) │
               │                                                                      │
               └──────────────────────────────────────────────────────────────────────┘
```

### 2.1 劇情三階段推進節點與戰鬥卡片規範

| 推進階段 | 區域名稱 | 關聯劇情與死亡事件 | 戰鬥/行動內容與獎勵 |
| :---: | :--- | :--- | :--- |
| **階段 1** | **🚪 區域一：生化隔離防爆大門** | 趙虎踹門被分解 ➔ 安保隊長發放戰術服 ➔ **查看戰術地圖點選區域一** ➔ 周揚恐慌逃跑被敏捷喪屍咬喉致死 | **【第一波遭遇戰】**：3 隻敏捷型喪屍 (`agile_zombie.jpg`)。<br>• 教學：6 人陣型前後排配置與基礎攻擊。<br>• 勝利後地圖更新階段 1 為 `【✅ 已突破】`。 |
| **階段 2** | **🛗 區域二：廢棄電梯井與毒氣走廊** | 升降電梯纜繩斷裂，被迫穿越主通風走廊 ➔ **查看戰術地圖點選區域二** ➔ 安保隊長發放高爆破片手雷 | **【第二波決戰】**：3 隻變異腐屍 + 2 隻敏捷喪屍 (毒氣每回合 -5% HP)。<br>• 教學：戰鬥中使用 `high_explosive` 範圍清場。<br>• 勝利後防爆門 5 秒關閉，錢富貴大叔落後被隔絕焚化。 |
| **階段 3** | **🧠 區域三：深層神經中樞 A.D.A.M. 機房** | 後路封死，深入 B3 最底層 ➔ **查看戰術地圖點選區域三** ➔ 抵達神經主機 | **【智者入侵檢定】**：<br>• **隊伍最高 INT $\ge 100$**：下載【亞當神經元矩陣備份 (`adamcore.jpg`)】，獲得 C 階碎片 + 1500 點數。<br>• **INT 不足**：炸毀主機，獲得基礎 800 點數。<br>• 全員回歸輪迴廣場，冷月新手引導。 |

---

## 3. 本章節專屬 AI 圖片生成提示詞庫 (AI Visual Prompts)

### 🗺️ Prompt 1：地下設施戰術俯瞰地圖 (16:9 點擊地圖背景)
* **適用位置：** `stage_1_1_tactical_map_screen` 戰術全息藍圖底圖
* **英文 Prompt：**
  ```text
  Full screen game map background, top-down clean tactical map layout of a multi-level underground facility, showing multiple basement floors connected by elevator shafts and heavy blast doors, dark metallic steel corridors, subtle blue glowing power lines on floor, clean blueprint style, highly detailed environment art, zero text, no words, no fake UI icons, plain background --ar 16:9
  ```

### 🚪 Prompt 2：鎖死喪屍的重型防爆大門 (16:9 劇情/地圖背景)
* **適用位置：** 區域一防爆大門戰前背景與卡片展示
* **英文 Prompt：**
  ```text
  Full screen environment concept art, giant reinforced steel sci-fi blast door completely sealed, heavy lockdown lock bars engaged, glowing red warning status light above door, dark industrial concrete hallway, dynamic cinematic lighting, dark atmospheric sci-fi game art style, no text, zero words, high quality --ar 16:9
  ```

### 🛗 Prompt 3：向下延伸的廢棄電梯井與控制台 (16:9 核心事件背景)
* **適用位置：** 區域二廢棄電梯井與毒氣走廊戰前背景與卡片展示
* **英文 Prompt：**
  ```text
  Full screen environment concept art, wide angle view of a dark industrial underground elevator shaft, massive steel elevator cage suspended by heavy cables going deep down, glowing cyan status screen on wall, flickering red emergency hazard light, dark metallic sci-fi corridor, atmospheric horror game background, no text, no words --ar 16:9
  ```

---

## 4. 全息戰術大地圖自由探索 (`images/zombieCityMap.jpg`)

通關主線後，點擊輪迴傳送大門進入大地圖自由探索模式，開啟 1920x1080 戰術全息地圖 (`zombie_city_map_screen`)：

```text
       ┌─────────────────────────────── 極光重工戰術全息地圖 ───────────────────────────────┐
       │                                                                                  │
       │  [🛡️ 蜂巢生化隔離閘門]         [💉 B1 特種廢棄醫務室]            [🔥 生化培育溫室] │
       │     (X:260, Y:240)                  (X:680, Y:180)                 (X:1420, Y:240) │
       │                                                                                  │
       │                               [🧠 中央主控機房 (A.D.A.M.)]                        │
       │                                     (X:960, Y:360)                               │
       │                                                                                  │
       │  [💨 毒氣冷卻管道區]            [🎒 地下軍火管制庫]              [☠️ 暴君培養槽]   │
       │     (X:280, Y:660)                  (X:680, Y:720)                 (X:1500, Y:720) │
       │                                                                                  │
       │   [ 🚪 返回輪迴空間 (右上角常駐按鈕 X:1530, Y:20 & 底部中央常駐按鈕 Y:1015) ]        │
       └──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 7 大戰術據點首通與重複刷怪規格表

| 據點代號 | 據點名稱 | 類型 | 座標 | 首次通關機制 (首通獎勵) | 已肅清重複刷怪機制 (不可重複解支線) |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `node_gate` | **🛡️ 蜂巢生化隔離閘門** | 遭遇戰 | `(260, 240)` | 擊潰前哨防線。<br>首通：點數 +400、血液 x6、零件 x3。 | 巡邏腐屍 + 敏捷喪屍。<br>掉落：血液 x3、零件 x1、點數 +150。 |
| `node_infirmary` | **💉 B1 特種廢棄醫務室** | 支線智鬥 | `(680, 180)` | 密閉電子門鎖死。<br>• **INT $\ge 100$**：無損破解。<br>• **INT 不足**：引發警報戰鬥。<br>首通：**C 階碎片 x1**、急救噴霧 x2、高純血清 x10、點數 +600。 | **支線不可重複解**。<br>殘存遊蕩敏捷喪屍 x2。<br>掉落：血液 x4、點數 +200。 |
| `node_cooling` | **💨 地下毒氣冷卻管道區** | 管道伏擊 | `(280, 660)` | 生化毒氣走廊，3 隻敏捷型喪屍倒吊撲殺（需戰術防護服）。<br>首通：**D 階碎片 x1**、零件 x5、點數 +500。 | 管道敏捷喪屍 + 變異腐屍。<br>掉落：零件 x2、點數 +200。 |
| `node_server` | **🧠 中央主控機房 (A.D.A.M.)** | 核心支線 | `(960, 360)` | A.D.A.M. 亞當核心主機。<br>• **INT $\ge 100$**：下載完整 AI 原始碼。<br>• **INT 不足**：觸發防禦電網與守衛戰鬥。<br>首通：**B 階碎片 x1**、【亞當神經元矩陣備份】、超導晶片 x8、點數 +1000。 | **核心不可重複下載**。<br>巡邏機房守衛 + 敏捷守衛。<br>掉落：零件 x3、點數 +250。 |
| `node_incubation` | **🔥 生化培育溫室** | 狂暴刷怪 | `(1420, 240)` | 破碎培養槽大量怪群湧出（建議手雷清場）。<br>首通：大量血液 x12、零件 x6、點數 +600。 | 培養槽腐屍群 + 敏捷喪屍。<br>掉落：血液 x8、零件 x3、點數 +300。 |
| `node_armory` | **🎒 地下軍火管制庫** | 戰術搜刮 | `(680, 720)` | 撬開極光重工安保軍火庫。<br>首通：**high_explosive 高爆破片手雷 x2**、手榴彈 x2、點數 +500。 | **手雷不可重複搜刮**。<br>軍火庫遊蕩腐屍 x2。<br>掉落：零件 x2、點數 +150。 |
| `node_boss` | **☠️ 深層生物重裝試驗場** | 領主決戰 | `(1500, 720)` | 迎戰終極生物兵器——**暴君 T-002 原型機** + 敏捷親衛。<br>首殺：**C 階碎片 x1**、【極光暴君生化心臟標本】、重裝作戰服、點數 +2000。 | 暴君 T-002 突變殘影 + 敏捷親衛。<br>掉落：高濃度血液 x8、合金零件 x4、點數 +500。 |

### 3.2 已肅清任務狀態鎖定機制 (Cleared State & Repeatable Farm Logic)
1. **已肅清標記 (`is_cleared == True`)：**
   * 據點標籤切換為綠色 `【✅ 已肅清】`。
   * 點開簡報彈窗時，頂部明確顯示：`【✅ 該據點支線劇情與密室已探索完結，不可重複解支線任務】`。
2. **資訊純粹化：**
   * 隱藏原有的支線劇情故事、選擇肢與唯一性首通道具（如亞當核心、首通命運碎片等）。
   * **僅展示該區域盤踞刷新的怪物情報（名稱、狀態）與掉落素材清單**。
3. **操作按鈕自適應：**
   * 支線按鈕徹底移除，僅保留 **`【 ⚔️ 掃蕩刷新怪群 】`** 與 `【 ❌ 關閉簡報 】`。
4. **常駐返回按鈕：**
   * **右上角常駐按鈕 (`xpos 1530, ypos 20`)：** 紅色高亮 `【 🚪 返回輪迴空間廣場 】`。
   * **底部中央常駐按鈕 (`ypos 1015`)：** `【 🌌 🚪 退出當前地圖 · 安全返回輪迴空間廣場 】`。

---

## 4. 戰鬥系統與生命持久化規則 (Combat & Persistent Health)

1. **生命不自動回復 (Strict HP Persistence):**
   * 戰鬥結束後實時血量寫回 `team_roster`。
   * 進入新戰鬥、大地圖切換或連續探索時，**角色不自動補滿生命值**。
   * 僅能透過消耗「輪迴止血急救噴霧」等道具，或返回輪迴空間進行「全身修復 (Full Heal - 100 點數)」回復。
2. **防禦機制修正：**
   * 消耗 1 AP 進入防禦姿態，獲得 -50% 受傷減免與 +15 MP，**不回復 HP**。
3. **主線怪物限制：**
   * 喪屍主線劇情僅出現 2 種怪物：**敏捷型喪屍 (`agile_zombie`)** 與 **變異腐屍 (`MOB_ZOMBIE_01`)**。
   * 舔食者、暴君等強力變異體僅出現在大地圖探索與 Boss 試驗場中。

---

## 5. 美術素材與命名精確對照清單 (Asset Registry)

| 類別 | 識別碼 / 變數名 | 檔案路徑 | 尺寸 / 顯示規範 |
| :--- | :--- | :--- | :--- |
| **地圖背景** | `zombieCityMap` / `bg_zombie_city_map` | `images/zombieCityMap.jpg` | 1920x1080 全圖 |
| **場景背景** | `bg_aurora_lab_entrance` | `images/zombie_street.PNG` | 1920x1080 全圖 |
| **場景背景** | `bg_aurora_corridor` | `images/zombie_street.PNG` | 1920x1080 全圖 (踏入基地即切換) |
| **核心背景** | `bg_aurora_core` / `adamcore` | `images/adamcore.jpg` | 1920x1080 全圖 / 中央展示 `yalign 0.32` |
| **怪物頭像** | `agile_zombie` (敏捷型喪屍) | `images/agile_zombie.jpg` | 1:1 頭像 / 中央立繪 |
| **怪物頭像** | `MOB_ZOMBIE_01` (變異腐屍) | `images/zombie.jpg` | 1:1 頭像 / 中央立繪 |
| **防具裝備** | `tactical_hazmat_armor` (戰術服) | `images/tactical_hazmat_armor.jpg` | 中央展示 `yalign 0.32` |
| **武器手雷** | `high_explosive` / `item_grenade` | `images/high_explosive_fragmentation_grenade.jpg` | 中央展示 `yalign 0.32` |
| **角色立繪** | `lengyue` (冷月) | `images/portrait_lengyue_f.jpg` | 對話頭像 / 立繪 |
| **角色立繪** | `suxiao` (女作家·蘇曉) | `images/femalewriter.jpg` | 對話頭像 / 立繪 |
| **角色立繪** | `aurora_captain` (安保隊長) | `images/securegurde.jpg` | 對話頭像 / 立繪 |
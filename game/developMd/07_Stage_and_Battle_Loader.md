# 📜 《輪迴世界》開發規格書 - 07: 關卡地圖 JSON 與戰鬥載入器 (整合版)

本文件定義遊戲關卡之「首次主線劇情模式」與「二次地圖探索刷怪模式」的切換邏輯，以及四層資料架構（Ren'Py 腳本 + 3 個 JSON 資料庫）的對接與戰鬥載入規格。

---

## 1. 關卡雙模式進入機制 (Stage Progression Mechanics)

每個關卡節點（如 `1-1`, `1-2`）均具備兩種模式狀態：

```text
                  [ 玩家點擊關卡 (例如 1-1) ]
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       【首次進入 (is_cleared == False)】   【二次進入 (is_cleared == True)】
                │                             │
                ▼                             ▼
      1. 強制播放主線劇情 (.rpy)             1. 開啟地圖選擇點模式
                │                             │
                ▼                             ├─► [首次點擊] ➔ 觸發支線劇情 (.json)
      2. 進入主線強制戰鬥                     │
                │                             └─► [二次點擊] ➔ 直接進入怪物刷怪戰鬥 (.json)
                ▼
      3. 標記該關卡已通關 (is_cleared = True)




## 2. 四層檔案資料架構 (Data Architecture)
系統將關卡解構為 4 個獨立檔案：

| 檔案類型 | 建議檔案名稱 / 格式 | 負責功能與內容 |
| :--- | :--- | :--- |
| **1. 主線劇情** | `zombie_city.rpy` 等 | 首次進入時的對話、CG、演出與主線強制戰鬥流程（Ren'Py 原生腳本）。 |
| **2. 支線劇情庫** | `side_quests.json` | 首次點擊地圖點觸發的支線對話、選擇肢、智鬥檢定與專屬獎勵。 |
| **3. 地圖關卡點庫** | `map_nodes.json` | 地圖上的圖示座標、可刷出的怪物組合、波次與刷怪難度。 |
| **4. 怪物屬性與掉落庫** | `monsters_db.json` | 怪物的基礎六圍屬性、技能、普通/稀有掉落物及掉落機率。 |

---

## 3. 三大 JSON 資料庫標準範例與說明

### 3.1 支線劇情資料庫 (`side_quests.json`)
二次進入地圖時，首次點擊地圖點觸發的文本、選擇肢與智鬥檢定：

```json
{
  "side_quests": [
    {
      "quest_id": "SQ_1_1_A",
      "node_id": "NODE_1_1_EXPLORE",
      "quest_title": "被遺棄的醫務室",
      "dialogue_lines": [
        { "speaker": "隊友", "text": "這裡看起來像個特種醫務室，但高壓電子鎖鎖死了。" },
        { "speaker": "系統", "text": "請選擇隊伍行動方案：" }
      ],
      "choices": [
        {
          "option_text": "[智者檢定] 嘗試破解電子鎖 (需要隊伍最高 INT >= 100)",
          "req_int": 100,
          "success": {
            "text": "破解成功！找到了高純度喪屍血清與輪迴止血急救噴霧。",
            "reward_items": [
              { "item_id": "MAT_ZOMBIE_BLOOD", "count": 10 },
              { "item_id": "item_heal_spray", "count": 2 }
            ],
            "reward_fate_shard": "C",
            "reward_points": 600
          },
          "fail": {
            "text": "警報響起，吸引了周圍大批狂暴敏捷型喪屍！",
            "trigger_battle_monsters": [
              { "monster_id": "agile_zombie", "count": 2 }
            ]
          }
        },
        {
          "option_text": "暴力破門 (直接觸發戰鬥)",
          "trigger_battle_monsters": [
            { "monster_id": "agile_zombie", "count": 2 },
            { "monster_id": "MOB_ZOMBIE_01", "count": 1 }
          ]
        }
      ]
    }
  ]
}
```

### 3.2 地圖關卡點與刷怪庫 (`map_nodes.json`)
定義地圖節點座標，以及支線完成後純刷怪的波次（Waves）與怪物配置：

```json
{
  "map_nodes": [
    {
      "node_id": "NODE_1_1_EXPLORE",
      "node_name": "B1 醫務室廢墟",
      "map_position": { "x": 680, "y": 180 },
      "side_quest_id": "SQ_1_1_A",
      "is_side_quest_cleared": false,
      "repeatable_battle": {
        "battle_waves": [
          {
            "wave_number": 1,
            "monsters": [
              { "monster_id": "agile_zombie", "count": 2, "position": "Frontline" }
            ]
          }
        ]
      }
    }
  ]
}
```

### 3.3 怪物屬性與掉落率資料庫 (`monsters_db.json`)
儲存怪物的面板數值、技能模式（前後排/單體/群體）及普通/稀有物品掉落機率：

```json
{
  "monsters": [
    {
      "id": "MOB_ZOMBIE_01",
      "name": "變異腐屍",
      "avatar": "images/zombie.jpg",
      "stats": { "hp": 250, "atk": 35, "def": 10, "speed": 8 },
      "skills": [
        {
          "skill_name": "腐蝕抓咬",
          "cost_ap": 2,
          "damage": 40,
          "target": "Single_Frontline",
          "effect": "Apply_Poison"
        }
      ],
      "drop_table": {
        "common_drops": [
          { "item_id": "MAT_ZOMBIE_BLOOD", "item_name": "喪屍血液", "drop_chance": 0.85, "min": 1, "max": 3 }
        ],
        "rare_drops": [
          { "item_id": "CURRENCY_FATE_SHARD_RARE", "item_name": "精良命運碎片", "drop_chance": 0.05, "min": 1, "max": 1 }
        ]
      }
    }
  ]
}
```

---

## 4. 戰鬥資料載入與邏輯鏈 (Data Loading Flow)
當玩家在地圖畫面上點擊關卡圖示時，程式執行以下判斷與動態載入流程：

```text
       [玩家點擊地圖據點 (如 node_infirmary)]
                         │
                         ▼
             【檢查該據點是否已通關】
                ├── False (未肅清) ➔ 顯示完整支線劇情/智者檢定/首通獎勵預覽
                │                       ├── 點選智鬥 ➔ 進行 INT 檢定 ➔ 判定成功/觸發警報
                │                       └── 點選戰鬥 ➔ 載入首通怪群 ➔ 勝利發放首通大獎並標記已肅清
                │
                └── True  (已肅清) ➔ 隱藏支線與首通大獎，僅展示刷新怪群情報
                                        │
                                        ▼
                                   點選【⚔️ 掃蕩刷新怪群】
                                        │
                                        ▼
                   自 monsters_db.json 讀取刷新怪物數值與頭像
                                        │
                                        ▼
                   調用 battle_screen 進行回合制戰鬥，獲勝後僅發放基礎素材
```
這是一份已將 「歷程紀錄與戰鬥統計數據庫 (Player Progress & Stats Tracking System)」 整合進去後的 07_Stage_and_Battle_Loader.md（完整包含：劇情模式通關標記、支線通關標記、總殺敵數、累積輸出傷害與戰鬥載入邏輯）：Markdown# 📜 《輪迴世界》開發規格書 - 07: 關卡地圖 JSON 與戰鬥載入器 (整合版)

本文件定義遊戲關卡之「首次主線劇情模式」與「二次地圖探索刷怪模式」的切換邏輯、全局歷程與戰鬥數據追蹤系統，以及四層資料架構（Ren'Py 腳本 + 3 個 JSON 資料庫）的對接與戰鬥載入規格。

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
2. 玩家歷程紀錄與戰鬥統計數據庫 (Player Progress & Stats Tracking)為了讓後續劇情判斷、稱號解鎖、成就系統與個人房間合成台能讀取玩家行為，系統將建立全域歷程紀錄字典（player_progress_db）。2.1 歷程紀錄數據結構範例JSON{
  "player_progress": {
    "completed_main_stages": {
      "STAGE_1_1": true,
      "STAGE_1_2": false
    },
    "completed_side_quests": {
      "SQ_1_1_A": true,
      "SQ_1_1_B": false
    },
    "battle_statistics": {
      "total_kills": 142,
      "kills_by_type": {
        "MOB_ZOMBIE_01": 120,
        "MOB_LICKER_01": 22
      },
      "total_damage_dealt": 85400,
      "total_damage_taken": 12300,
      "highest_single_hit": 3450
    }
  }
}
2.2 歷程數據判斷與應用（開發範例）判斷是否可進入地圖模式： if player_progress["completed_main_stages"].get("STAGE_1_1"):判斷是否觸發支線或直接刷怪： if player_progress["completed_side_quests"].get("SQ_1_1_A"):解鎖成就/專屬裝備： 當 kills_by_type["MOB_ZOMBIE_01"] >= 100 時，個人房間解鎖基因藥劑兌換。3. 四層檔案資料架構 (Data Architecture)系統將關卡解構為 4 個獨立檔案。後續 AI 擴充內容時，請依據下表名稱建立對應檔案：檔案類型建議檔案名稱 / 格式負責功能與內容1. 主線劇情stage_main_story.rpy首次進入時的對話、CG、演出與主線強制戰鬥流程（Ren'Py 原生腳本）。2. 支線劇情庫side_quests.json首次點擊地圖點觸發的支線對話、選擇肢、智鬥檢定與專屬獎勵。3. 地圖關卡點庫map_nodes.json地圖上的圖示座標、可刷出的怪物組合、波次與刷怪難度。4. 怪物屬性與掉落庫monsters_db.json怪物的基礎六圍屬性、前後排技能、普通/稀有掉落物及掉落機率（%）。4. 三大 JSON 資料庫標準範例與說明以下為 3 個 JSON 資料庫的對接欄位說明與單筆完整範例，AI 後續開檔時請嚴格遵循此格式規範：4.1 支線劇情資料庫 (side_quests.json)說明： 二次進入地圖時，首次點擊地圖點觸發的文本、選擇肢與智鬥檢定。JSON{
  "side_quests": [
    {
      "quest_id": "SQ_1_1_A",
      "node_id": "NODE_1_1_EXPLORE",
      "quest_title": "被遺棄的醫務室",
      "dialogue_lines": [
        { "speaker": "隊友", "text": "這裡看起來像個醫務室，但鎖住了。" },
        { "speaker": "系統", "text": "請選擇行動：" }
      ],
      "choices": [
        {
          "option_text": "[智者檢定] 嘗試破解電子鎖 (需要 INT >= 100)",
          "req_int": 100,
          "success": {
            "text": "破解成功！找到了隱藏的備份醫療日誌與基因藥劑碎片。",
            "reward_item": "ITEM_GENE_ELIXIR_FRAGMENT",
            "reward_fate_shard": "CURRENCY_FATE_SHARD_RARE"
          },
          "fail": {
            "text": "警報響起，吸引了周圍的怪物！",
            "trigger_battle_wave": "WAVE_ALERT_ZOMBIES"
          }
        },
        {
          "option_text": "暴力破門 (直接觸發戰鬥)",
          "trigger_battle_wave": "WAVE_DOOR_ZOMBIES"
        }
      ]
    }
  ]
}
4.2 地圖關卡點與刷怪庫 (map_nodes.json)說明： 定義地圖節點座標，以及支線完成後純刷怪的波次（Waves）與怪物配置。JSON{
  "map_nodes": [
    {
      "node_id": "NODE_1_1_EXPLORE",
      "node_name": "B1 醫務室廢墟",
      "map_position": { "x": 350, "y": 600 },
      "side_quest_id": "SQ_1_1_A",
      "repeatable_battle": {
        "battle_waves": [
          {
            "wave_number": 1,
            "monsters": [
              { "monster_id": "MOB_ZOMBIE_01", "count": 3, "position": "Frontline" }
            ]
          }
        ]
      }
    }
  ]
}
4.3 怪物屬性與掉落率資料庫 (monsters_db.json)說明： 儲存怪物的面板數值、技能模式（前後排/單體/群體）及普通/稀有物品掉落機率。JSON{
  "monsters": [
    {
      "id": "MOB_ZOMBIE_01",
      "name": "變異腐屍",
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
5. 戰鬥資料載入與歷程更新邏輯鏈 (Data Loading & Stats Update Flow)當玩家在地圖畫面上點擊關卡圖示時，程式執行以下判斷、動態載入與數據更新流程：Plaintext[玩家點擊地圖關卡點 (NODE_1_1_EXPLORE)]
                   │
                   ▼
       【檢查 player_progress.completed_main_stages】
          ├── False (首次進入) ➔ 跳轉至 stage_main_story.rpy 播放主線並戰鬥
          │                       └── 勝利後更新 completed_main_stages["STAGE_1_1"] = true
          │
          └── True  (二次進入) ➔ 進入地圖選擇點邏輯
                                       │
                                       ▼
                     【檢查 player_progress.completed_side_quests】
                        ├── False ➔ 讀取 side_quests.json 觸發支線對話/智鬥
                        │           └── 完成後註記 completed_side_quests["SQ_1_1_A"] = true
                        │
                        └── True  ➔ 讀取 map_nodes.json 的 repeatable_battle 進入純刷怪
                                       │
                                       ▼
                     跨檔至 monsters_db.json 撈取怪物數據 (HP, ATK, 技能, 掉落物)
                                       │
                                       ▼
                     套用隊伍人數動態難度加成 (動態 HP/ATK = 基礎 × [1 + (N-1)×15%])
                                       │
                                       ▼
                     初始化戰鬥介面，生成敵方單位並進入回合制戰鬥
                                       │
                                       ▼
                     【戰鬥結束結算階段】
                     1. 累加 player_progress.battle_statistics.total_damage_dealt
                     2. 累加 player_progress.battle_statistics.total_kills 與 kills_by_type
                     3. 計算掉落物並發放至背包/個人房間


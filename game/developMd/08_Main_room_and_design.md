# 📜 《輪迴世界》開發規格書 - 07: 房間收藏系統與怪物數據庫

本文件定義主角個人房間（`main_room.rpy` 延伸）的**收藏與高科技合成系統**，以及副本怪物的 **JSON 數據結構與掉落率機制**。

---

## 1. 個人房間收藏與高科技合成系統 (Room Collection & Crafting)

個人房間升級為**「高科技工坊 / 收藏室」**，玩家可以將副本中獲取的特殊數據與怪特掉落物帶回房間進行兌換與武器生成。

### 1.1 基因鎖藥劑兌換機制 (Gene Lock Elixir)
* **兌換需求：** 集齊 `喪屍血液 (Zombie Blood)` × 100 瓶。
* **兌換成果：** 獲得 **「基因鎖解鎖藥劑 (Gene Lock Injection)」** × 1。
* **使用效果：** 使用後可直接無視前置條件，強制開啟/升級 1 階基因鎖。

---

### 1.2 蜂巢 AI 備份 (Hive AI Backup) 與高科技武器生成
1. **觸發與獲取條件：**
   * 進入第一副本「喪屍末日世界（蜂巢基地）」時，若玩家隊伍中包含 **`智力 (INT) >= 100`** 的角色（如智者職階或開啟思維模擬者）。
   * 將在地圖中解鎖專屬智鬥/駭客選項：`[下載蜂巢基地主控 AI 備份]`。
2. **房間解鎖高科技合成台 (Tech-Crafting Terminal):**
   * 將 AI 備份帶回個人房間安裝後，房間解鎖「高科技生成終端」。
   * **生成機制：** 消耗打怪掉落的普通與稀有素材，由 AI 自動打印高科技武器與防具（如：電漿步槍、高振動粒子刀、脈衝防護盾）。

---

## 2. 怪物掉落率與掉落邏輯 (Monster Drop Mechanics)

戰鬥勝利結算時，系統自動讀取當前怪物的掉落表並執行隨機判定：

1. **普通掉落物 (Common Drop):** 
   * 掉落機率：**70% ~ 100%**。主要為基礎素材（如：喪屍血液、科技零件）。
2. **稀有掉落物 (Rare Drop):** 
   * 掉落機率：**5% ~ 15%**。主要為高階裝備、稀有材料或命運碎片。
3. **隊伍智力加成 (INT Drop Rate Bonus):** 
   * 隊伍最高智力每高出 50 點，稀有掉落率提升 **+2%**。

---

## 3. 怪物 JSON 數據庫規格 (Monster JSON Database)

怪物數據儲存於 `monsters_db.json`，包含基本屬性、前後排技能、普通掉落與稀有掉落。

### 3.1 JSON 資料結構範例 (`monsters_db.json`)

```json
{
  "monsters": [
    {
      "id": "MOB_ZOMBIE_01",
      "name": "變異腐屍",
      "world_id": "WORLD_ZOMBIE",
      "position_type": "Frontline",
      "stats": {
        "hp": 250,
        "max_hp": 250,
        "atk": 35,
        "def": 10,
        "speed": 8
      },
      "skills": [
        {
          "skill_name": "腐蝕抓咬",
          "cost_ap": 2,
          "damage": 40,
          "target": "Single_Frontline",
          "effect": "Apply_Poison_3_Turns"
        },
        {
          "skill_name": "屍毒咆哮",
          "cost_ap": 3,
          "damage": 20,
          "target": "All_Party",
          "effect": "Reduce_Party_AP_1"
        }
      ],
      "drop_table": {
        "common_drops": [
          {
            "item_id": "MAT_ZOMBIE_BLOOD",
            "item_name": "喪屍血液",
            "drop_chance": 0.85,
            "min_quantity": 1,
            "max_quantity": 3
          }
        ],
        "rare_drops": [
          {
            "item_id": "EQ_TECH_GAS_MASK",
            "item_name": "舊型防毒面具",
            "drop_chance": 0.10,
            "min_quantity": 1,
            "max_quantity": 1
          },
          {
            "item_id": "CURRENCY_FATE_SHARD_RARE",
            "item_name": "精良命運碎片",
            "drop_chance": 0.05,
            "min_quantity": 1,
            "max_quantity": 1
          }
        ]
      }
    },
    {
      "id": "MOB_LICKER_01",
      "name": "舔食者",
      "world_id": "WORLD_ZOMBIE",
      "position_type": "Backline_Hunter",
      "stats": {
        "hp": 600,
        "max_hp": 600,
        "atk": 85,
        "def": 25,
        "speed": 18
      },
      "skills": [
        {
          "skill_name": "長舌刺穿",
          "cost_ap": 2,
          "damage": 90,
          "target": "Bypass_Frontline_Single_Backline",
          "effect": "Bleeding"
        }
      ],
      "drop_table": {
        "common_drops": [
          {
            "item_id": "MAT_ZOMBIE_BLOOD",
            "item_name": "喪屍血液",
            "drop_chance": 1.0,
            "min_quantity": 3,
            "max_quantity": 5
          }
        ],
        "rare_drops": [
          {
            "item_id": "MAT_HIGH_MUTANT_GENE",
            "item_name": "高階變異基因片段",
            "drop_chance": 0.15,
            "min_quantity": 1,
            "max_quantity": 1
          }
        ]
      }
    }
  ]
}
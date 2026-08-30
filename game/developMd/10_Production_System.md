# 📜 《輪迴世界》開發規格書 - 10: 戰術家園資源生產裝置與合成系統 (Production System)

本文件定義玩家在「個人房間戰術指揮面板 (Tactical Dashboard)」內部的資源生產裝置組裝與自動合成機制。透過連結副本獲取的素材與核心組件，玩家可組裝高科技生產裝置，批量製造疫苗、補血藥劑、高爆手雷與高階戰術裝備。

---

## 1. 資源生產與副本循環 (Core Loop)

```text
  [ 副本刷怪 / 地圖探索 / 智者檢定 ]
                 │
                 ▼
     取得【素材與特殊零件】 (如：喪屍血液、壓電晶體、亞當 AI 備份)
                 │
                 ▼
     [ 返回個人房間 ➔ 開啟戰術指揮面板 (Tactical Dashboard) ]
                 │
                 ▼
     【解鎖與組裝生產裝置】 (消耗指定零件與基礎點數)
                 │
                 ├─► 1. 生化基因合成儀 ──► 研發【喪屍疫苗】&【高濃縮補血血清】
                 ├─► 2. 脈衝壓電整備台 ──► 批量製造【高脈衝手雷】&【穿甲電磁彈藥】
                 └─► 3. 亞當 AI 3D 列印機 ──► 研發【全封閉作戰服】&【懸浮飛靴】




2. 三大自動生產裝置規格 (Production Facilities)
玩家可在戰術面板的模組插槽（Slots）中，利用副本搜集來的材料組裝以下 3 種生產裝置：

💉 裝置一：生化基因合成儀 (FAC_GENE_SYNTHESIZER)
組裝需求零件： MAT_ZOMBIE_BLOOD (喪屍血液 x10) + ITEM_HIVE_AI_BACKUP (亞當 AI 備份 x1) + 1,000 基礎點數。

可生產物資：

喪屍病毒抗體疫苗 (ITEM_ZOMBIE_VACCINE): 戰術道具，使用後下場戰鬥全隊免疫「屍毒/腐蝕」狀態，且受傷減少 15%。

高濃縮複合補血血清 (ITEM_HEAL_SERUM_MAX): 戰鬥消耗品，瞬間恢復單體 50% HP 與 30% MP。

💣 裝置二：脈衝壓電整備台 (FAC_PULSE_WORKSHOP)
組裝需求零件： MAT_PIEZO_CRYSTAL (壓電晶體碎片 x5) + MAT_SCRAP_METAL (廢棄合金 x15) + 1,500 基礎點數。

可生產物資：

高脈衝震波彈 (ITEM_GRENADE): 投擲武器，戰鬥中對全體敵人造成大量震波傷害（AOE 清場必備）。

穿甲電磁彈藥包 (ITEM_AMMO_AP): 戰力 Buff 道具，賦予隊伍槍手/輸出手下一場戰鬥「無視敵方 30% 防禦」效果。

🖥️ 裝置三：亞當 AI 3D 裝備列印機 (FAC_ADAM_PRINTER)
組裝需求零件： ITEM_HIVE_AI_BACKUP (亞當 AI 備份 x1) + MAT_HIGH_TECH_CHIP (高階晶片 x3) + 3,000 基礎點數。

可生產物資：

全封閉作戰服 (EQ_TECH_ARMOR_02): 胸甲裝備，提供防禦 +30、HP +100 與 【毒氣免疫】 標籤。

懸浮飛靴 (EQ_TECH_BOOTS_01): 腳部裝備，賦予角色 【飛行標籤】，可無視前排直接攻擊敵方空中或後排單位。

3. 生產裝置 JSON 數據庫結構 (production_db.json)
此 JSON 數據庫定義了裝置組裝配方、消耗材料與自動生產倒數計時，供程式直接讀取與維護：

JSON
{
  "production_facilities": [
    {
      "facility_id": "FAC_GENE_SYNTHESIZER",
      "name": "生化基因合成儀",
      "build_recipe": {
        "required_items": [
          { "item_id": "MAT_ZOMBIE_BLOOD", "count": 10 },
          { "item_id": "ITEM_HIVE_AI_BACKUP", "count": 1 }
        ],
        "cost_points": 1000
      },
      "production_recipes": [
        {
          "recipe_id": "RECIPE_VACCINE",
          "recipe_name": "喪屍病毒抗體疫苗",
          "output_item": "ITEM_ZOMBIE_VACCINE",
          "output_count": 1,
          "production_time_seconds": 600,
          "cost_materials": [
            { "item_id": "MAT_ZOMBIE_BLOOD", "count": 2 }
          ]
        },
        {
          "recipe_id": "RECIPE_HEAL_SERUM",
          "recipe_name": "高濃縮複合補血血清",
          "output_item": "ITEM_HEAL_SERUM_MAX",
          "output_count": 2,
          "production_time_seconds": 300,
          "cost_materials": [
            { "item_id": "MAT_ZOMBIE_BLOOD", "count": 1 }
          ]
        }
      ]
    },
    {
      "facility_id": "FAC_PULSE_WORKSHOP",
      "name": "脈衝壓電整備台",
      "build_recipe": {
        "required_items": [
          { "item_id": "MAT_PIEZO_CRYSTAL", "count": 5 },
          { "item_id": "MAT_SCRAP_METAL", "count": 15 }
        ],
        "cost_points": 1500
      },
      "production_recipes": [
        {
          "recipe_id": "RECIPE_GRENADE",
          "recipe_name": "高脈衝震波彈",
          "output_item": "ITEM_GRENADE",
          "output_count": 2,
          "production_time_seconds": 400,
          "cost_materials": [
            { "item_id": "MAT_PIEZO_CRYSTAL", "count": 1 },
            { "item_id": "MAT_SCRAP_METAL", "count": 2 }
          ]
        }
      ]
    }
  ]
}
4. 裝置 UI 狀態與交互邏輯 (Facility UI Logic)
在戰術面板的 UI 中，每個裝置模組具備以下 3 種狀態切換：

未組裝狀態 (Unbuilt): 顯示【組裝裝置】按鈕，點擊跳出配方需求視窗。若玩家背包持有足量零件與點數，扣除後解鎖該裝置。

待機/生產選擇狀態 (Idle): 顯示【選擇生產配方】按鈕，玩家選擇欲生產的物品（如疫苗或手雷）並投入對應素材後開始倒數。

生產倒數與收穫狀態 (Working / Harvest):

計時中： 顯示動態進度條與倒數時間（如：05:42）。

完成時： 進度條轉為金黃色，顯示【領取物資】按鈕。點擊後物品直接發放至玩家背包 (player_inventory)。

5. 本系統專屬 AI 視覺提示詞 (AI Prompts)
📦 裝置 icon 與產出物資圖示 (Icons - 1:1)
生化基因合成儀圖示 (icon_facility_synthesizer.png)

Prompt: Game UI icon, high-tech chemical synthesizer device, glowing blue and green glass tubes, futuristic medical equipment, dark background, 2d vector asset --ar 1:1

喪屍病毒抗體疫苗 (ITEM_ZOMBIE_VACCINE.png)

Prompt: Game item icon, glowing green glowing syringe filled with vaccine liquid, high-tech medical injector, dark background, 2d game asset --ar 1:1

高濃縮複合補血血清 (ITEM_HEAL_SERUM_MAX.png)

Prompt: Game item icon, futuristic red health potion flask, glowing crimson energy liquid inside, dark background, 2d game asset --ar 1:1
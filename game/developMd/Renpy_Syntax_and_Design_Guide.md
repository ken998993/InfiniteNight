# 📜 《輪迴世界》開發規格書 - 09: Ren'Py 設計語法與避坑開發指南

本文件匯總了在《輪迴世界》與 Ren'Py 8.x 引擎開發過程中**必須遵循的語法規範、解析器行為機制與常見致命 Bug 避坑指南**。所有後續模組開發與 AI 擴充均需嚴格遵守此規範。

---

## 📌 目錄
1. [Screen 語法核心規則 (避免 Parser 崩潰)](#1-screen-語法核心規則)
2. [對話與文本字串轉義機制 (避免 String Format 崩潰)](#2-對話與文本字串轉義機制)
3. [文字方括號與變數插值規則 (避免 NameError 崩潰)](#3-文字方括號與變數插值規則)
4. [全域狀態管理與 Screen 互動更新](#4-全域狀態管理與-screen-互動更新)
5. [圖像資源讀取與預設缺省綁定](#5-圖像資源讀取與預設缺省綁定)
6. [模組化與四層資料庫架構設計](#6-模組化與四層資料庫架構設計)

---

## 1. Screen 語法核心規則

### ⚠️ 致命地雷 1：Screen 屬性中的三元運算子必須加「圓括號 `()`」
* **錯誤示範 (引發編譯解析崩潰):**
  ```renpy
  # ❌ 錯誤：Ren'Py 解析器會將 "if" 誤判為 button 的子語句，拋出 "The if statement is not a valid child of the button statement"
  button:
      background "#e6a100" if is_active else "#222a42"
      action Return("click")
  ```
* **正確寫法 (加括號封裝為 Python 表達式):**
  ```renpy
  # ✅ 正確：將三元運算式以圓括號包覆
  button:
      background ("#e6a100" if is_active else "#222a42")
      action Return("click")
  ```
* **適用屬性：** `background`、`hover_background`、`text_idle_color`、`text_hover_color`、`padding`、`xysize` 等所有 Screen 屬性。

---

## 2. 對話與文本字串轉義機制

### ⚠️ 致命地雷 2：對話（Say Statement）中的百分比符號必須轉義為 `%%`
* **錯誤示範 (引發 ValueError: unsupported format character 崩潰):**
  ```renpy
  # ❌ 錯誤：Ren'Py 角色對話會執行內部 % 格式化，若遇到單個 % 會將後續中文字視為佔位符而崩潰
  z "副本難度動態提升 +30%，可在智鬥據點提供支援！"
  z "無新人負擔，副本維持 100% 基礎難度。"
  ```
* **正確寫法 (使用雙百分比 `%%` 進行轉義):**
  ```renpy
  # ✅ 正確：對話文本中的百分比符號一律寫為 %%
  z "兩名新人加入團隊！副本難度動態提升 +30%%，可在智鬥據點提供支援！"
  z "你抹殺了新人，獲得物資！（副本維持 100%% 基礎難度）"
  ```
* **注意：** Screen 中的 `text "難度：[scale*100]%"` 是 Screen 專用標籤，不受此限制；但 Character 說話的 Say 語句（如 `z "..."`、`"..."`）必須轉義為 `%%`。

### ⚠️ 致命地雷 3：對話（Say Statement）嚴禁直接接 Python `f"..."`
* **錯誤示範 (引發 Say has image attributes ('f',) 崩潰):**
  ```renpy
  # ❌ 錯誤：Ren'Py 解析器會將角色名稱後的 'f' 誤解析為 Character 立繪的屬性標籤 (Image Attributes)
  z f"🎉【掃蕩勝利】成功清剿【{cur_node['name']}】刷新怪群！獲得生存點數 +{rep_pts} 點！"
  z f"【精英試煉大捷】成功掠奪【{s_tier} 階命運碎片 x1】！"
  ```
* **正確寫法 (三種標準解決方案):**
  ```renpy
  # ✅ 方案 A（推薦）：使用 Ren'Py 原生方括號變數插值
  $ n_title = cur_node['name']
  z "🎉【掃蕩勝利】成功清剿【[n_title]】刷新怪群！獲得生存點數 +[rep_pts] 點！"
  
  # ✅ 方案 B：先用 Python 變數組裝完整字串再輸出
  $ win_msg = f"🎉【掃蕩勝利】成功清剿【{cur_node['name']}】刷新怪群！獲得生存點數 +{rep_pts} 點！"
  z "[win_msg]"
  
  # ✅ 方案 C：使用 Python 函數式呼叫
  $ z(f"🎉【掃蕩勝利】成功清剿【{cur_node['name']}】刷新怪群！")
  ```

---

## 3. 文字方括號與變數插值規則

### ⚠️ 致命地雷 4：Screen `text` 中的英文方括號會自動觸發變數求值
* **錯誤示範 (引發 NameError: name 'xxx' is not defined 崩潰):**
  ```renpy
  # ❌ 錯誤：Ren'Py 會將 [ 空置空位 ] 視為 [variable_name] 進行 Python 求值，因變數不存在而崩潰
  text f"槽位 {i+1}：[ 空置空位 ]" size 13 color "#666666"
  text "[ 智者檢定 ] 嘗試破解電子密碼鎖" size 16
  ```
* **正確寫法 (三種解決方案):**
  ```renpy
  # ✅ 方案 A（推薦）：使用全形符號或圓括號
  text f"槽位 {i+1}：( 空置空位 )" size 13 color "#666666"
  text f"槽位 {i+1}：【 空置空位 】" size 13 color "#666666"
  
  # ✅ 方案 B：使用雙方括號 [[ ]] 進行原生轉義
  text f"槽位 {i+1}：[[ 空置空位 ]]" size 13 color "#666666"
  
  # ✅ 方案 C：真正的變數插值才使用單方括號
  text "[member.get('name', '未知')]" size 21 color "#00ffff"
  ```

---

## 4. 全域狀態管理與 Screen 互動更新

### 4.1 變數初始化與跨存檔持久化
1. **遊戲運行變數**：在 `game_init.rpy` 中統一使用 `store.__dict__` 或 `default` 初始化，防止熱重載或讀檔時變數遺失。
   ```renpy
   init python:
       if 'team_roster' not in store.__dict__:
           team_roster = get_team_roster()
       if 'points' not in store.__dict__:
           points = 1000
   ```

### 4.2 Screen 按鈕動作規範
* **觸發 Python 方法**：使用 `Function(func_name, arg1, arg2)`
* **修改字典/列表**：使用 `SetDict(dict_obj, 'key', value)`
* **修改畫面局部變數**：使用 `SetScreenVariable('var_name', value)`
* **返回互動控制權**：使用 `Return(return_val)`（推薦使用 Tuple 攜帶參數，如 `Return(("buy_item", item_id))`）

---

## 5. 圖像資源讀取與預設缺省綁定

### 5.1 角色頭像與怪物圖片動態載入
1. **預設立繪綁定**：未指定頭像或資源丟失時，統一 fallback 至 `images/core_idle.PNG`。
2. **渲染語法範例**：
   ```renpy
   frame:
       xysize (130, 260)
       background "#121828cc"
       padding (4, 4)
       $ m_av = member.get('avatar', 'images/core_idle.PNG')
       add m_av xysize (120, 210) xalign 0.5 yalign 0.5
   ```
3. **圖片支援格式**：支援 `.png`、`.PNG`、`.jpg`、`.webp`。Ren'Py 對大寫副檔名敏感，需確保路徑大小寫一致。

---

## 6. 模組化與四層資料庫架構設計

為維持程式碼的高可讀性與避免單一 `.rpy` 檔案過於龐大，專案採**功能模組化拆分**：

```text
game/
├── jsonData/
│   ├── monsters_db.json         # Layer 4: 怪物屬性、前後排技能、普通/稀有掉落表
│   ├── map_nodes.json           # Layer 3: 關卡地圖座標點、波次怪物刷怪配置
│   ├── side_quests.json         # Layer 2: 支線對話樹、智者 INT 檢定與專屬獎勵
│   ├── items.json               # 道具、8 大部位裝備、材料素材
│   ├── bloodlines.json          # 6 大血統家族、D/C/B/A/S 階晉升樹
│   └── team_data.json           # 初始團隊成員數值與頭像
├── stage_system.rpy             # 關卡雙模式 (首次主線演出 vs 二次節點自由探索)
├── personal_room_system.rpy     # 個人房間高科技工坊、基因鎖藥劑提純、蜂巢 AI 終端打印
├── battle_screen.rpy            # 6vs6 回合制戰鬥、前後排打擊、環境危害結算、掉落物結算
├── bloodline_system.rpy         # 3 槽位血統強化石碑、同系升級補差價
├── inventory_system.rpy         # 8 大裝備部位穿脫、4 階命運碎片 3合1/1拆2 工坊
├── rookie_system.rpy            # 2 名新人隨機生成 (Tank/Scholar/Attacker) 與道德抉擇
├── campaign_system.rpy          # 五大輪迴世界、環境懲罰與剋制裝備
└── main_room.rpy                # 主神廣場探索中樞、全身修復、傳送大門
```

---

### 💡 開發自檢清單 (Checklist)
- [ ] 所有 Screen 內的 `background` 三元運算是否均加上了 `()`？
- [ ] 角色 Say 對話中所有的 `%` 是否均已寫成 `%%`？
- [ ] Screen 文字中的 `[xxx]` 是否確實為 Python 變數而非文字方括號？
- [ ] 新增的角色/怪物是否皆具備 `avatar`（預設 `images/core_idle.PNG`）？
- [ ] 戰鬥與商城中是否使用 `Function` / `Return` 而非直接在 Screen 內做複雜賦值？


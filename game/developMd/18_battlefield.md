# 🗺️ 《輪迴世界》開放式地圖（四向出口）實作規格書

## 1. 資源與地圖圖檔說明
* **圖檔名稱：** `zombieroom.png`（請放置於專案的 `game/images/` 資料夾內）。
* **地圖解析度：** `1920 x 1080` (16:9 全螢幕)。
* **地圖佈局：** 中央為空曠的地下研究所大廳，四周（東、西、南、北）各有一處合金氣壓門出口。

---

## 2. 座標設定與觸發邊界 (Trigger Zones)

預設玩家小人起始座標為畫面中央：`px = 960`, `py = 540`。

| 出口方向 | 觸發檢定區域 (座標條件) | 碰撞邊界設定 | 連接區域 / 事件名稱 |
| :---: | :---: | :---: | :--- |
| **北方 (Top)** | `py < 150` | 限制 `py` 最小為 `100` | 通往 B2 電梯井 / 下一層 |
| **南方 (Bottom)** | `py > 930` | 限制 `py` 最大為 `980` | 通往 B1 防爆大門通道 |
| **西方 (Left)** | `px < 200` | 限制 `px` 最小為 `150` | 通往 醫療整備站 / 藥品庫 |
| **東方 (Right)** | `px > 1720` | 限制 `px` 最大為 `1770` | 通往 武器庫 / 警衛室 |

---

## 3. Ren'Py 實作腳本 (`open_zombieroom.rpy`)

這段程式碼實現了：
1. 載入 `zombieroom.png` 作為開放式背景。
2. 使用 `WASD` 或 **方向鍵** 控制玩家小人在場地內自由移動。
3. 當小人靠近四周出口邊界時，自動跳出「切換地圖」按鈕。

```renpy
# -----------------------------------------------------------------------------
# 1. 變數初始化
# -----------------------------------------------------------------------------
# 玩家座標 (起始點為中央)
default px = 960
default py = 540
default move_step = 20 # 每次按鍵移動的像素距離

# -----------------------------------------------------------------------------
# 2. 開放式四向地圖 Screen
# -----------------------------------------------------------------------------
screen zombieroom_map():

    # 載入研究所背景圖
    add "images/zombieroom.png"

    # 繪製玩家小人 Icon (圖像尺寸建議 64x64 或 128x128)
    add "images/player_icon.png":
        xpos px
        ypos py
        anchor (0.5, 0.5)

    # -------------------------------------------------------------------------
    # 鍵盤監聽 (WASD & 方向鍵)
    # -------------------------------------------------------------------------
    # 往左 (Left / A)
    key "repeat_K_LEFT" action [SetVariable("px", max(100, px - move_step)), Function(renpy.restart_interaction)]
    key "repeat_K_a"    action [SetVariable("px", max(100, px - move_step)), Function(renpy.restart_interaction)]

    # 往右 (Right / D)
    key "repeat_K_RIGHT" action [SetVariable("px", min(1820, px + move_step)), Function(renpy.restart_interaction)]
    key "repeat_K_d"     action [SetVariable("px", min(1820, px + move_step)), Function(renpy.restart_interaction)]

    # 往上 (Up / W)
    key "repeat_K_UP"   action [SetVariable("py", max(100, py - move_step)), Function(renpy.restart_interaction)]
    key "repeat_K_w"    action [SetVariable("py", max(100, py - move_step)), Function(renpy.restart_interaction)]

    # 往下 (Down / S)
    key "repeat_K_DOWN" action [SetVariable("py", min(980, py + move_step)), Function(renpy.restart_interaction)]
    key "repeat_K_s"    action [SetVariable("py", min(980, py + move_step)), Function(renpy.restart_interaction)]

    # -------------------------------------------------------------------------
    # 四向出口觸發檢定與互動按鈕
    # -------------------------------------------------------------------------
    # 北方出口 (py < 150)
    if py < 150:
        frame:
            align (0.5, 0.1)
            padding (15, 10)
            textbutton "【進入 北方·B2 電梯井】" action Jump("goto_north_elevator")

    # 南方出口 (py > 930)
    elif py > 930:
        frame:
            align (0.5, 0.9)
            padding (15, 10)
            textbutton "【進入 南方·防爆大門通道】" action Jump("goto_south_gate")

    # 西方出口 (px < 200)
    elif px < 200:
        frame:
            align (0.1, 0.5)
            padding (15, 10)
            textbutton "【進入 西方·醫療整備站】" action Jump("goto_west_medical")

    # 東方出口 (px > 1720)
    elif px > 1720:
        frame:
            align (0.9, 0.5)
            padding (15, 10)
            textbutton "【進入 東方·重型軍火庫】" action Jump("goto_east_armory")

# -----------------------------------------------------------------------------
# 3. 劇情事件與切換 Label
# -----------------------------------------------------------------------------
label start_zombieroom_exploration:
    # 呼叫地圖介面
    call screen zombieroom_map

label goto_north_elevator:
    scene bg_black with fade
    "你推開了北方的重型閘門，前方的通道直通 B2 深層電梯井……"
    # 重置座標並切換至下一張地圖
    $px = 960$ py = 850
    jump start_next_level

label goto_south_gate:
    scene bg_black with fade
    "你退回了南方的防爆大門前，後方依然傳來喪屍拍打鐵門的巨響。"
    $px = 960$ py = 200
    call screen zombieroom_map

label goto_west_medical:
    scene bg_black with fade
    "你進入了西側的醫療整備站，空氣中散發著濃烈的消毒水與藥品氣味。"
    jump medical_room_event

label goto_east_armory:
    scene bg_black with fade
    "你進入了東側的軍火庫，幾排鎖著的金屬槍櫃映入眼簾。"
    jump armory_room_event

---

## 4. 🎮 即時動作突圍戰鬥規格 (`action_battlefield.rpy`)

有別於傳統 6v6 回合制 RPG 戰鬥，在進入第一關末日喪屍大廳突入時，觸發第一人稱/俯瞰即時微操戰鬥：

### 4.1 核心機制與資產配置
* **戰場背景：** `images/zombieroom.jpg` (1920x1080)。
* **玩家單位：** `images/c1.png`，支援上下左右（WASD / 方向鍵）平滑 340px/s 移動與朝向翻轉。
* **敵人單位：** `images/agile_zombie.jpg`，自四向大門以 140~185px/s 速度全向追蹤逼近主角。
* **射擊系統：** 支援滑鼠游標 360 度定向瞄準或空白鍵定向射擊，發射高能電漿光彈 (850px/s)。

### 4.2 受創反饋與碰撞特效 (Visual & Audio Feedbacks)
1. **射擊受傷回饋 (Shooting Hits):**
   * 子彈擊中敏捷型喪屍時：怪物觸發硬直減速與 22px 擊退效果。
   * 浮動傷害數字：跳出黃色暴擊 `-35 (CRIT!)` 或紅色 `-20` 數字。
   * 命中效果：產生 6 顆血花噴濺粒子。
   * 動態血條：喪屍頭頂顯示綠/紅即時血條。
   * 擊殺回饋：怪物血量歸零時噴發 16 顆大型血花粒子，彈出 `💥 殲滅！+40 EXP`。
2. **肉體碰撞受創 (Collision Hurts):**
   * 敏捷型喪屍撲咬命中主角（距離 < 55px）時：主角扣除 15 點 HP。
   * **碰撞震屏 (Screen Shake):** 畫面產生劇烈隨機震盪 0.35 秒。
   * **血光遮罩 (Red Vignette):** 全螢幕泛起猩紅危險血霧 0.45 秒。
   * **無敵時間 (i-frames):** 玩家獲得 0.8 秒閃爍無敵幀，防止連續受創暴斃。
   * **受創擊退 (Knockback):** 玩家被強力彈開 40px，頭頂彈出 `⚠️ 咬傷 -15 HP!`。

### 4.3 結算獎勵
* **突圍成功：** 擊斃 8 隻敏捷型喪屍，獎勵 +300 生存點數與 +150 角色經驗值 (EXP)。
* **火力掩護跳過：** 若生命值耗盡，可選擇由資深者冷月發動念動雙槍火力支援脫險，不卡關。
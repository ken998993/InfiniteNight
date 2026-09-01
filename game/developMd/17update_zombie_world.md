 《輪迴世界》第一關：諾克斯市地下設施（點擊式層級地圖）1. 遊戲玩法與地圖核心機制 (Core Gameplay)核心目標： 隊伍必須從 B1 廢棄整備區開始，不斷尋找「電梯鑰匙卡」或修復電源，一層層往下探索（B1 ➔ B2 ➔ B3 ➔ ADAM 核心房）。防爆大門抵御機制（Blast Door Security）： 每一層的電梯口或關鍵通道都配有「防爆鐵閘門」。玩家可以選擇：【關閉防爆門】： 消耗 1 次電氣能量，徹底擋住身後追擊的喪屍群，獲得安全的休整與搜刮時間。【強行破門】： 吸引迅捷畸變體，觸發高難度戰鬥。點擊式移動 (Point-and-Click System)： 玩家點擊畫面上已探索/鄰近的地點按鈕，角色 Icon 冰滑移動至該地點並觸發區域事件。2. 地下區域層級規劃 (Level Layout)層級 (Depth)區塊名稱主要探索點關鍵物資 / 離場條件B1 階梯廢棄安保通道安保室、醫療站、B1 電梯井獲得【B2 權限卡】、第一道防爆門控B2 階梯生化實驗室毒氣洩漏區、武器庫、B2 電梯井獲得【全封閉戰術服】、手榴彈、修復電梯發電機B3 階梯機密資料庫警衛長室、ADAM 前哨對話站取得【ADAM 解密硬碟】、關閉最後一道隔離閘門B4 核心ADAM 主機房ADAM 核心塔、最終防禦終端進入 BOSS 戰，鎖死外圍大門將喪屍擋在門外3. Ren'Py 點擊式地圖系統程式碼 (sub_level_map.rpy)程式碼片段# -----------------------------------------------------------------------------
# 變數定義 (Variables)
# -----------------------------------------------------------------------------
default current_floor = "B1"          # 當前層級
default player_node = "b1_entrance"    # 當前節點
default has_b2_keycard = False         # B2 鑰匙卡
default blast_door_closed = False     # 防爆門狀態

# -----------------------------------------------------------------------------
# 點擊式地圖介面 (Tactical Map Screen)
# -----------------------------------------------------------------------------
screen sub_level_map():
    # 1. 地圖背景圖 (16:9 全螢幕)
    add "images/bg_sublevel_tactical_map.png"

    # 2. 當前狀態 UI (左上角)
    frame:
        xpos 40 ypos 40
        padding (20, 15)
        vbox:
            spacing 5
            text "【極光重工地下設施 - 戰術地圖】" color "#00FFFF" size 24 bold True
            text "當前位置：[current_floor] 層 - [player_node]" color "#FFFFFF" size 18
            if blast_door_closed:
                text "後方防爆大門：【已鎖死】(喪屍群暫時被阻擋)" color "#00FF00" size 16
            else:
                text "後方防爆大門：【開啟中】(警告：屍潮距離逼近中！)" color "#FF3333" size 16

    # -------------------------------------------------------------------------
    # B1 節點地圖按鈕 (Nodes)
    # -------------------------------------------------------------------------
    if current_floor == "B1":
        # 安保室節點
        imagebutton:
            idle "images/icon_node_security.png"
            hover "images/icon_node_security_hover.png"
            xpos 500 ypos 600
            action Jump("event_b1_security")

        # B1 電梯井/大門節點
        imagebutton:
            idle "images/icon_node_elevator.png"
            hover "images/icon_node_elevator_hover.png"
            xpos 1100 ypos 400
            action Jump("event_b1_elevator")

# -----------------------------------------------------------------------------
# 劇情邏輯區 (Labels)
# -----------------------------------------------------------------------------
label event_b1_security:
    scene bg_lab_room
    "隊伍進入了廢棄安保室，桌上有一張散發著微光的權限卡。"
    $ has_b2_keycard = True
    "獲得了【B2 電梯權限卡】！"
    call screen sub_level_map

label event_b1_elevator:
    scene bg_elevator_hall
    if not has_b2_keycard:
        "【電梯控制台】：『警告，前往 B2 生化實驗室需要最高權限卡。』"
        "蘇曉：「大家小心，背後走廊傳來無數喪屍的腳步聲了！」"
        call screen sub_level_map
    else:
        "【電梯控制台】：『權限確認，電梯準備下降。』"
        menu:
            "【拉下緊急閘門，鎖死身後防爆大門】：":
                $ blast_door_closed = True
                "厚重的鈦合金防爆大門轟然落下！將無數瘋狂拍打的喪屍阻擋在大門外！"
                "隊伍搭乘電梯前往 B2 層..."
                $ current_floor = "B2"
                jump start_b2_level
            "【直接搭乘電梯下降】：":
                "你們跳入電梯，幾隻迅捷畸變體在電梯門關上前的最後一秒撲了進來！"
                call battle_quick_zombie
                $ current_floor = "B2"
                jump start_b2_level
🎨 4. AI 生圖提示詞 (Prompts)所有 Prompt 已優化為 16:9 全螢幕 (--ar 16:9)、無假文字 (no text, no UI)，並加入防爆大門、地下層級與電梯井的強烈視覺要素：🗺️ Prompt 1：地下設施戰術俯瞰地圖 (16:9 點擊地圖背景)Prompt:Full screen game map background, top-down clean tactical map layout of a multi-level underground facility, showing multiple basement floors connected by elevator shafts and heavy blast doors, dark metallic steel corridors, subtle blue glowing power lines on floor, clean blueprint style, highly detailed environment art, zero text, no words, no fake UI icons, plain background --ar 16:9🚪 Prompt 2：鎖死喪屍的重型防爆大門 (劇情/地圖背景)Prompt:Full screen environment concept art, giant reinforced steel sci-fi blast door completely sealed, heavy lockdown lock bars engaged, glowing red warning status light above door, dark industrial concrete hallway, dynamic cinematic lighting, dark atmospheric sci-fi game art style, no text, zero words, high quality --ar 16:9🛗 Prompt 3：向下延伸的廢棄電梯井與控制台 (16:9 核心事件背景)Prompt:Full screen environment concept art, wide angle view of a dark industrial underground elevator shaft, massive steel elevator cage suspended by heavy cables going deep down, glowing cyan status screen on wall, flickering red emergency hazard light, dark metallic sci-fi corridor, atmospheric horror game background, no text, no words --ar 16:9